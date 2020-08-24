from pyserini.search import pysearch
import pandas as pd
import json
from transformers import BertTokenizer, BartTokenizer, BartForConditionalGeneration, BertForQuestionAnswering
import torch
import numpy as np


torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'

QA_MODEL = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
QA_TOKENIZER = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
QA_MODEL.to(torch_device)
QA_MODEL.eval()

def _construct_doi_to_search_hit_dict(search_hits):
    if search_hits == None:
        return {}
    doi_to_search_hit = dict()
    if len(search_hits) > 0:
        for each_result in search_hits:
        	doi_to_search_hit[each_result.doi] = each_result
    return doi_to_search_hit

def makeBERTSQuADPrediction(document, question):
    nWords = len(document.split())
    input_ids_all = QA_TOKENIZER.encode(question, document, max_length=250)
    tokens_all = QA_TOKENIZER.convert_ids_to_tokens(input_ids_all)
    overlapFac = 1.1
    if len(input_ids_all)*overlapFac > 2048:
        nSearchWords = int(np.ceil(nWords/5))
        quarter = int(np.ceil(nWords/4))
        docSplit = document.split()
        docPieces = [' '.join(docSplit[:int(nSearchWords*overlapFac)]),
                     ' '.join(docSplit[quarter-int(nSearchWords*overlapFac/2):quarter+int(quarter*overlapFac/2)]),
                     ' '.join(docSplit[quarter*2-int(nSearchWords*overlapFac/2):quarter*2+int(quarter*overlapFac/2)]),
                     ' '.join(docSplit[quarter*3-int(nSearchWords*overlapFac/2):quarter*3+int(quarter*overlapFac/2)]),
                     ' '.join(docSplit[-int(nSearchWords*overlapFac):])]
        input_ids = [QA_TOKENIZER.encode(question, dp) for dp in docPieces]

    elif len(input_ids_all)*overlapFac > 1536:
        nSearchWords = int(np.ceil(nWords/4))
        third = int(np.ceil(nWords/3))
        docSplit = document.split()
        docPieces = [' '.join(docSplit[:int(nSearchWords*overlapFac)]),
                     ' '.join(docSplit[third-int(nSearchWords*overlapFac/2):third+int(nSearchWords*overlapFac/2)]),
                     ' '.join(docSplit[third*2-int(nSearchWords*overlapFac/2):third*2+int(nSearchWords*overlapFac/2)]),
                     ' '.join(docSplit[-int(nSearchWords*overlapFac):])]
        input_ids = [QA_TOKENIZER.encode(question, dp) for dp in docPieces]

    elif len(input_ids_all)*overlapFac > 1024:
        nSearchWords = int(np.ceil(nWords/3))
        middle = int(np.ceil(nWords/2))
        docSplit = document.split()
        docPieces = [' '.join(docSplit[:int(nSearchWords*overlapFac)]),
                     ' '.join(docSplit[middle-int(nSearchWords*overlapFac/2):middle+int(nSearchWords*overlapFac/2)]),
                     ' '.join(docSplit[-int(nSearchWords*overlapFac):])]
        input_ids = [QA_TOKENIZER.encode(question, dp) for dp in docPieces]
    elif len(input_ids_all)*overlapFac > 512:
        nSearchWords = int(np.ceil(nWords/2))
        docSplit = document.split()
        docPieces = [' '.join(docSplit[:int(nSearchWords*overlapFac)]), ' '.join(docSplit[-int(nSearchWords*overlapFac):])]
        input_ids = [QA_TOKENIZER.encode(question, dp) for dp in docPieces]
    else:
        input_ids = [input_ids_all]
    absTooLong = False

    answers = []
    cons = []
    for iptIds in input_ids:
        tokens = QA_TOKENIZER.convert_ids_to_tokens(iptIds)
        sep_index = iptIds.index(QA_TOKENIZER.sep_token_id)
        num_seg_a = sep_index + 1
        num_seg_b = len(iptIds) - num_seg_a
        segment_ids = [0]*num_seg_a + [1]*num_seg_b
        assert len(segment_ids) == len(iptIds)
        n_ids = len(segment_ids)

        if n_ids < 512:
            start_scores, end_scores = QA_MODEL(torch.tensor([iptIds]).to(torch_device),
                                     token_type_ids=torch.tensor([segment_ids]).to(torch_device))
        else:
            absTooLong = True
            start_scores, end_scores = QA_MODEL(torch.tensor([iptIds[:512]]).to(torch_device),
                                     token_type_ids=torch.tensor([segment_ids[:512]]).to(torch_device))
        start_scores = start_scores[:,1:-1]
        end_scores = end_scores[:,1:-1]
        answer_start = torch.argmax(start_scores)
        answer_end = torch.argmax(end_scores)
        answer = reconstructText(tokens, answer_start, answer_end+2)

        if answer.startswith('. ') or answer.startswith(', '):
            answer = answer[2:]

        c = start_scores[0,answer_start].item()+end_scores[0,answer_end].item()
        answers.append(answer)
        cons.append(c)

    maxC = max(cons)
    iMaxC = [i for i, j in enumerate(cons) if j == maxC][0]
    confidence = cons[iMaxC]
    answer = answers[iMaxC]

    sep_index = tokens_all.index('[SEP]')
    full_txt_tokens = tokens_all[sep_index+1:]

    abs_returned = reconstructText(full_txt_tokens)

    ans={}
    ans['answer'] = answer
    if answer.startswith('[CLS]') or answer_end.item() < sep_index or answer.endswith('[SEP]'):
        ans['confidence'] = -1000000
    else:
        ans['confidence'] = confidence
    ans['abstract_bert'] = abs_returned
    ans['abs_too_long'] = absTooLong
    return ans

def reconstructText(tokens, start=0, stop=-1):
    tokens = tokens[start: stop]
    if '[SEP]' in tokens:
        sepind = tokens.index('[SEP]')
        tokens = tokens[sepind+1:]
    txt = ' '.join(tokens)
    txt = txt.replace(' ##', '')
    txt = txt.replace('##', '')
    txt = txt.strip()
    txt = " ".join(txt.split())
    txt = txt.replace(' .', '.')
    txt = txt.replace('( ', '(')
    txt = txt.replace(' )', ')')
    txt = txt.replace(' - ', '-')
    txt_list = txt.split(' , ')
    txt = ''
    nTxtL = len(txt_list)
    if nTxtL == 1:
        return txt_list[0]
    newList =[]
    for i,t in enumerate(txt_list):
        if i < nTxtL -1:
            if t[-1].isdigit() and txt_list[i+1][0].isdigit():
                newList += [t,',']
            else:
                newList += [t, ', ']
        else:
            newList += [t]
    return ''.join(newList)

def searchPapers(relevent_papers, query, run_on_abstract=True):
    doi_to_search_hit_map = _construct_doi_to_search_hit_dict(relevent_papers)
    theResults = {}
    for each_paper in relevent_papers:
        if not each_paper.has_abstract(): #skip if has no abstract
            continue
        if run_on_abstract:
            ans = makeBERTSQuADPrediction(each_paper.abstract, query)
            if ans['answer']:
                confidence = ans['confidence']
                theResults[confidence]={}
                theResults[confidence]['answer'] = ans['answer']
                theResults[confidence]['abstract_bert'] = ans['abstract_bert']
                theResults[confidence]['idx'] = each_paper.doi
                theResults[confidence]['abs_too_long'] = ans['abs_too_long']
        else:
            ans = makeBERTSQuADPrediction(each_paper.raw_text, query)
            if ans['answer']:
                confidence = ans['confidence']
                theResults[confidence]={}
                theResults[confidence]['answer'] = ans['answer']
                theResults[confidence]['body_bert'] = ans['abstract_bert']
                theResults[confidence]['idx'] = each_paper.doi
                theResults[confidence]['body_too_long'] = ans['abs_too_long']

    cList = list(theResults.keys())

    if cList:
        maxScore = max(cList)
        total = 0.0
        exp_scores = []
        for c in cList:
            s = np.exp(c-maxScore)
            exp_scores.append(s)
        total = sum(exp_scores)
        for i,c in enumerate(cList):
            theResults[exp_scores[i]/total] = theResults.pop(c)

        #map result to paper:
        papers_to_return = []
        for each_result in theResults:
            the_doi = theResults[each_result]['idx']

            if the_doi in doi_to_search_hit_map:
                if run_on_abstract:
                    doi_to_search_hit_map[the_doi].bert_abstract_answer = theResults[each_result]
                else:
                    doi_to_search_hit_map[the_doi].bert_body_answer = theResults[each_result]
                papers_to_return.append(doi_to_search_hit_map[the_doi])
        return papers_to_return
