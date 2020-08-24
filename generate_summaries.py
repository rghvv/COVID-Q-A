import argparse
from pathlib import Path

import torch
from tqdm import tqdm

from transformers import BartForConditionalGeneration, BartTokenizer

torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'

DEFAULT_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

SUMMARY_TOKENIZER = BartTokenizer.from_pretrained('bart-large-cnn')
SUMMARY_MODEL = BartForConditionalGeneration.from_pretrained('bart-large-cnn')
SUMMARY_MODEL.to(torch_device)
SUMMARY_MODEL.eval()

def clean_text(text):
    tokens = text.split(" ")
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
    return txt

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def generate_summaries(examples: list,batch_size: int = 8,min_percent=0.5,max_percent=0.75):
    model = SUMMARY_MODEL
    tokenizer = SUMMARY_TOKENIZER
    device = torch_device

    actual_length = len(examples[0].strip().split(" "))
    max_length = int(actual_length * max_percent)
    min_length = int(actual_length * min_percent)

    for batch in tqdm(list(chunks(examples, batch_size))):
        dct = tokenizer.batch_encode_plus(batch, max_length=1024, return_tensors="pt", pad_to_max_length=True)
        summaries = model.generate(
            input_ids=dct["input_ids"].to(device),
            attention_mask=dct["attention_mask"].to(device),
            num_beams=4,
            length_penalty=2.0,
            max_length=max_length + 2,  # +2 from original because we start at step=1 and stop before max_length
            min_length=min_length + 1,  # +1 from original because we start at step=1
            no_repeat_ngram_size=3,
            early_stopping=True,
            decoder_start_token_id=model.config.eos_token_id,
        )
        dec = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summaries]
        to_return = []
        for hypothesis in dec:
            to_return.append(clean_text(hypothesis))
        return "\n".join(to_return)
    return ""


def run_bart_summary(to_summarize,min_percent=0.5,max_percent=0.75):
    try:
        to_summarize = clean_text(to_summarize)
        examples = [" " + x.rstrip() for x in to_summarize.split("\n")]
        return generate_summaries(examples,min_percent=0.5,max_percent=0.75)
    except Exception as e:
        print("error in bart summary:")
        print(e)
        return None


if __name__ == "__main__":
    #text = """the novel coronavirus (sars-cov-2 / 2019-ncov) identified in wuhan, china, in december 2019 has caused great damage to public health and economy worldwide with over 140,000 infected cases up to date. previous research has suggested an involvement of meteorological conditions in the spread of droplet-mediated viral diseases, such as influenza. however, as for the recent novel coronavirus, few studies have discussed systematically about the role of daily weather in the epidemic transmission of the virus. here, we examine the relationships of meteorological variables with the severity of the outbreak on a worldwide scale. the confirmed case counts, which indicates the severity of covid-19 spread, and four meteorological variables, i. e., air temperature, relative humidity, wind speed, and visibility, were collected daily between january 20 and march 11 (52 days) for 430 cities and districts. cc-by-nc-nd 4. 0 international license it is made available under a is the author / funder, who has granted medrxiv a license to display the preprint in perpetuity."""
    text = 'transmission was first thought to not be a mode of transmission, there are several documented cases that support that 2019-ncov is capable of human-to-human transmission [ 1 ]. atypical pneumonia of unexplained cause was first reported on 30 december 2019 in wuhan city, the capital of hubei province in central china. initially, four cases were noted which presented with fever (greater than 38°c), malaise, dry cough, and shortness of breath. imaging was consistent with pneumonia or acute respiratory distress syndrome (ards) and patients had either reduced or normal white blood cell counts. an early link to the wuhan south china seafood city (also known as the south china seafood wholesale market or the huanan seafood market) was identified as a common factor in four of the patients. treatment with antibiotics did not improve their condition over the next 3-5 days and a viral etiology was suspected. the patients were placed in isolation conditions. on 31 december 2020, it was announced that 27 cases of pneumonia, with 7 severe cases, had been identified [ 2 ]. most of the patients were stall workers at wuhan south china seafood city. the market'
    run_bart_summary(to_summarize)
    
