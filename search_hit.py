import json
#from generate_qa_pairs import run_question_generation

def _get_raw_text_from_body(body):
    if isinstance(body,dict) and 'text' in body:
        return body['text']
    return ""


class search_hit:
    def __init__(self,hit,article):
        self.title = ""
        self.doi = ""
        self.authors = []
        self.body = []
        self.score = -1.0
        self.abstract = ""
        self.raw_text = ""
        self.qa_pairs = []

        self._populate_hit(hit,article)
        self._extract_raw_text()

        self.bert_abstract_answer = None
        self.bert_body_answer = None

        self.bart_abstract_summary = None
        self.bart_body_summary = None

    def _populate_hit(self,hit,article):
            self.title = article['metadata']['title']
            self.authors = article['metadata']['authors']
            self.doi = hit.lucene_document.get('doi')
            self.score = hit.score
            self.body = article['body_text']

            if 'abstract' in article.keys() and len(article['abstract']) > 0:
                self.abstract = article['abstract'][0]['text']

    def _extract_raw_text(self):
        raw_text_list = []
        for each_section in self.body:
            raw_text_list.append(_get_raw_text_from_body(each_section))
        self.raw_text = "\n".join(raw_text_list)

    def has_abstract(self):
        return self.abstract != ""

    def _get_qa_pairs(self):
        self.qa_pairs = run_question_generation(self.raw_text)

    def has_bert_abstract(self):
        return self.bert_abstract_answer != None and 'answer' in self.bert_abstract_answer

    def has_bert_body(self):
        return self.bert_body_answer != None and 'answer' in self.bert_body_answer

    def has_bart_abstract(self):
        return self.bart_abstract_summary != None

    def has_bart_body(self):
        return self.bart_body_summary != None


    def __repr__(self):
        to_return = ["Paper doi: {}".format(self.doi)]

        if self.has_bert_abstract:
            to_return.append("Abstract Answer: {}".format(self.bert_abstract_answer['answer']))

        if self.has_bert_body and self.bert_body_answer:
            to_return.append("Body Answer: {}".format(self.bert_body_answer['answer']))

        if self.has_bart_abstract:
            to_return.append("Abstract Summary (bart): {}".format(self.bart_abstract_summary))

        if self.has_bart_body:
            to_return.append("Body Summary (bart): {}".format(self.bart_body_summary))

        return "\n".join(to_return)
