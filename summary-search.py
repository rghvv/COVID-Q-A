import os
import json
import pandas as pd
from pyserini.search import pysearch
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-1.11.0-openjdk-amd64" #comment this out if you have JAVA_HOME setup

from search_hit import search_hit
from bert_and_summary import searchPapers,_construct_doi_to_search_hit_dict
from answer import answer
from generate_summaries import run_bart_summary

SORT_CRITERTIA = ['start_conf','end_conf','avg_conf']

def _normalize_query(text):
    return text.lower().strip()

def cut_list(the_list,max_number_of_vals=1):
    if len(the_list) <= max_number_of_vals:
        return the_list
    else:
        return the_list[:max_number_of_vals]


def search_for_papers_relevent_to_query(query,number_of_papers_to_retrieve=10):
    results = []

    query = _normalize_query(query)

    searcher = pysearch.SimpleSearcher('lucene-index/') #path to index
    hits = searcher.search(query, number_of_papers_to_retrieve)

    for hit in hits:
        key = hit.docid[:8]
        json_result = searcher.doc(key).raw()

        if len(json_result):
            article = json.loads(searcher.doc(key).raw())

            results.append(search_hit(hit,article))

    return results

def search_for_answers(query,number_of_papers_to_retrieve=10):
    '''search index for (number_of_papers_to_retrieve) papers, feed into bert, and retrieve the top (max_number_of_answers) answers [sorted by sort criteria]'''
    print("query =",query)
    relevent_papers = search_for_papers_relevent_to_query(query,number_of_papers_to_retrieve)

    #run on abstracts:
    abstract_answers = searchPapers(relevent_papers, query, run_on_abstract=True)

    #run on body of text:
    body_answers = searchPapers(relevent_papers, query, run_on_abstract=False)

    #construct id to hit map:
    abstract_map = _construct_doi_to_search_hit_dict(abstract_answers)
    body_map = _construct_doi_to_search_hit_dict(body_answers)

    all_results = []
    for each_id in abstract_map:
        if each_id in body_map:
            abstract_map[each_id].bert_body_answer = body_map[each_id].bert_body_answer
        all_results.append(abstract_map[each_id])

    for each_id in body_map:
        if each_id not in abstract_map:
            all_results.append(body_map[each_id])

    #summarize abstract and bosy:
    for each_result in all_results:
        each_result.bart_abstract_summary = run_bart_summary(each_result.abstract,0.5,0.75)
        each_result.bart_body_summary = run_bart_summary(each_result.raw_text,0.1,0.25)

    return all_results

def print_results(all_results):
    for each_paper in all_results:
        print(each_paper)



if __name__ == "__main__":
    query = 'What do we know about virus genetics, origin, and evolution?'
    #query = 'Are people with high blood pressure (hypertension) at higher risk from COVID-19?'
    #query  = "How can I help protect myself from coronavirus?"
    top_answers = search_for_answers(query,10)
    print_results(top_answers)
