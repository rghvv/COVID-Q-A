# COVID19NLP
Generate answer summaries from user queries about COVID-19.

## Setup:
Download the indexed Lucene file (5 GB), unzip, rename to 'lucene_index/' and place it in same directory as scripts

https://www.dropbox.com/s/xg2b4aapjvmx3ve/lucene-index-cord19-paragraph-2020-04-24.tar.gz

## Library Requirements:
Please ensure you have all the following libraries installed:
1) [transformers](https://github.com/huggingface/transformers)
`pip install transformers`

2) pytorch

3) pyserini

## Notes:
The first time you run it, you may need to install the pretrainned models in transformers.

## Example:
running `search_hit.py` with query `what are the symptoms of Coronavirus`, results in:

(score:answer)

7.2868757247924805: respiratory , gastrointestinal , hepatic , and neurologic diseases

6.386914253234863: fever , fatigue , and dry cough

4.5584975481033325: pneumonia and renal failure

4.247128963470459: symptoms that resembled pneumonia

2.8038653135299683: symptoms are so mild that coronavirus infection is not suspected

## Examples:
query = what are the symptoms of Coronavirus


Paper doi: 10.3855/jidc.12425      

Abstract Answer: clinical isolates were found to contain a novel coronavirus with similarity to bat coronaviruses

Body Answer: with fever (greater than 38°c), malaise, dry cough, and shortness of breath

Abstract Summary (bart): A novel coronavirus (CoV) has emerged in Wuhan, China. This virus causes pneumonia of varying severity and has resulted in a high number of hospitalizations. There are in excess of 4,500 laboratory-confirmed cases, with > 100 known deaths. As with the SARS-CoV, infections in children appear to be rare. The initial infections with 2019-nCoV appears to be linked to contact with animals in wet markets. Even though human-to-human transmission seems to be the original source of infections, the most alarming development is that humanto- human transmission is now prevelant. Of particular concern is that many healthcare workers have been infected in the current epidemic. We offer a research perspective on the next steps for the generation of vaccines. We also present data on the use of in silico docking in gaining insight into 2019- nCoV Spike-receptor binding to aid in therapeutic development. Diagnostic PCR protocols can be found at https://www.who.int/health-topics/coronavirus/laboratory-diagnostics-for-novel-coronvirus. J Infect Dev Ctries 2020; 14(1):3-17.

Body Summary (bart): None



Paper doi: 10.1101/2020.03.10.20033738

Abstract Answer: with substantial variation in rates of transmission and severity of 17 associated disease

Body Answer: and has caused near 90,000 deaths of covid-19 worldwide

Abstract Summary (bart): SARS-CoV-2 has extended its range of transmission in all 16 parts of the world. Many countries have implemented social distancing as a measure to control further spread. We evaluate whether and under which conditions containment or slowing down 20 epidemics are possible by isolation and contact tracing.

Body Summary (bart): None

-------

query = Are people with high blood pressure (hypertension) at higher risk from COVID-19?

Abstract Answer: to analyze the potential mechanism of cardiovascular dysfunctions induced by coronavirus disease 201

Body Answer: *appears people over 65 with coronary heart diseases or hypertension is more likely to be infected and to develop more severe symptoms*                                       

Abstract Summary (bart): To analyze the potential mechanism of cardiovascular dysfunctions induced by Coronavirus Disease

Body Summary (bart): The pandemic of COVID-19 has been taking lives worldwide. It caused by a novel coronavirus which human being are lack of defensive function in whole population. It targets human's lung and causes serious damage of lungs. Based on early reports, for people with underlying heart issues, the concerns are serious. It appears people over 65 with coronary heart diseases or hypertension is more likely to be infected and to develop more severe symptoms. In addition, some of hospitalized CO VID-19 patients had cardiovascular diseases in China. It has been confirmed that a portion of the region at the amino terminal of SARS-CoV spike protein could bind to human angiotensin-converting enzyme 2(ACE2) to mediate the fusion of virus and host cell. ACE2 is expressed in human alveolar epithelial cells, and I which is not only the gateway of virus invasion, but also mediates lung injury and lung failure caused by virus infection. The invasion of lung surface cells directly causes lung inflammation and the invasion of cardiomyocytes will lead to edema, degeneration and necrosis of following cell lysis. Meanwhile, pro-inflammatory cytokines are released, such as interleukin-1 (IL-1), leading to hyoxemia, partial oxygenemia, and hypoxemia. The inflammatory response is also one of the most inflammatory factors inducing the formation of certain inflammatory factors, which can promote the development of certain types of cardiovascular diseases. The first is intensified, prone to cardiac dysfunction and heart failure. The second is intensified and prone to blood pump pump failure, leading to a certain amount of certain blood lactic acid and other metabolites in the body. The third is increased, prone, to heart pump failure and heart pump dysfunction, which in turn causes heart loading and hypertrophy and high blood pressure. In order to ensure the systemic supply of systemic metabolic energy demand, the whole body, including the whole myocardial cell, must supply the systemic metabolic cell energy demand in order for the body to survive and thrive. This is the first of a series of studies to look at the effects of the virus on the heart and vascular system. The authors conclude that the virus is likely to have similar infection pathways to SARS-CoV, in other words, ACE2 may also be the binding receptor of CoV-19. They conclude that ACE2 leads to excessive release of Ang II through RAS, which leads to elevated blood pressure and vascular remodeling in the cardiovascular system. They also suggest that the infection pathway may be similar to that of the SARS virus, which causes heart failure and lung injury. The study concludes that the potential mechanism of the disease is to better understand the impact of the CoV virus on cardiovascular diseases on the human body and the human heart and heart function. It also suggests that the disease may be linked to cardiovascular diseases such as heart failure, hypertension and heart-related deaths. The researchers conclude that this could be a potential treatment option for the CoVID- 19 pandemic. The results of the study will be published in the Journal of the American College of Cardiology (JACR) later this year or early in the year. It is hoped that the findings will shed light on the potential role of ACE2 in the virus-caused cardiovascular disease in the Coavid-19 pandemic, as well as how to treat the virus in the future. The findings could have implications for the treatment of heart and cardiovascular diseases and for the prevention of heart disease and stroke in the long-term. For confidential support, call the National Suicide Prevention Lifeline at 1-800-273-8255 or visit http://www.suicidepreventionlifeline.org/.

Paper doi: 10.1101/2020.03.16.20036723

Abstract Answer: creating models to identify individuals who are at the greatest risk for severe complications due to covid-19 will be useful for outreach campaigns to help mitigate the disease ' s worst effects. while information specific to covid-19 is limited, a model using complications due to other upper respiratory infections can be used as a proxy to help identify those individuals who are at the greatest risk

Abstract Summary (bart): COVID-19 is an acute respiratory disease that has been classified as a pandemic by the World Health Organization. It is known to have high mortality rates, particularly among individuals with preexisting medical conditions. Creating models to identify individuals who are at the greatest risk for severe complications will be useful for outreach campaigns to help mitigate the disease's worst effects.


Paper doi: 10.1101/2020.03.07.20031575

Abstract Answer: that patients with higher nt-probnp (above 88. 64 pg / ml) level had more risks of inhospital death

Body Answer: the percentage of acute cardiac injury and arrhythmia is even higher in severe patients

Abstract Summary (bart): Study initially enrolled 102 patients with severe COVID-19 pneumonia. After screening out the ineligible cases, 54 patients were analyzed in this study. Results found that patients with higher NT-proBNP (above 88.64 pg/mL) level had more risks of inhospital death. After adjusting for potential cofounders in separate modes, NT- proBNP presented as an independent risk factor of in-hospital death in patients withsevere CO VID-19.

Body Summary (bart): There is no research concerning whether the heart failure marker, N terminal pro B type natriuretic peptide (NT-proBNP) predicted outcome of COVID-19 patients. The study is a retrospective, observational registry with clinicaltrials.gov identifier NCT04292964. The primary outcome was in-hospital death defined as the case fatality rate. Patients in the higher group were significantly older with more hypertension and higher blood pressure levels than those in the lower group. All the data were collected using a same protocol by well-trained researchers with a doubleblind method. No reuse allowed without permission from the author/funder, who has granted medRxiv a license to display the preprint for this preprint (which was not peer-reviewed) http://www.medRxIV.org/10/15/1515/2020/2020.0715.3/preprint.html#storylink=cpy. SARS-CoV-2 has killed more people than SARS and MERS and the number keeps growing. The outbreak of coronavirus disease 2019 (COVID- 19) in China has been declared a public health emergency of international concern. The percentage of acute cardiac injury and arrhythmia is even higher in severe patients with 22.2% and 44.4% respectively. The severe patients also showed higher creatine kinase-MB (CK-MB) and hypersensitive troponin I (hs-TnI) levels than others 5. The peak value of TnI over 40 folds than normal value was found to be common in severe Patients. The best NT-probnP cut-off was that of the highest product of sensitivity and specificity for in- Hospital death prediction. It was determined according to the cut off determined in the ROCOC curve (Figure 1) according to NT- ProBNP levels (NTProBNP>88/64 pg/64/mL/mL) The study was conducted in Hubei General Hospital in China. It followed 102 patients with severe CO VID-19 pneumonia from a continuous sample during the management by national medical team. Patients who had stroke (n=2) and acute myocardial infarction (n=1) were excluded. To observe the risks of in- hospital death, patients were followed up from admission to discharge (1 to 15 days) for a period of 1-2 years. The follow-up data was collected from reviewing medical records by trained researchers using double blind method. Data are presented as mean ± SEM, frequency (%) or median (interquartile ranges) All the laboratory data were tested in a same laboratory with the same standard. A two-sided P<0.05 was considered statistically significant. The data were followed by SPSS 22.0 (SPSS, Chicago, IL, USA) and a two- sided P=0.01/0.07/10.0 was considered significant. All procedures were followed the instructions of local ethic committee (approval NO. 20200701). All procedures followed the Instructions of local Ethic committee (approved by local Ethical committee) for this study. The results were published in the journal The Journal of the American College of Cardiology (JAC) 1-4. The journal is published by the American Society for Cardiology, the American Heart Association (ASHA) and the American Journal of Cardiovascular Surgery (AJSC) 2-5. For confidential support call the National Suicide Prevention Lifeline at 1-800-273-8255 or visit www.acs.org.

Paper doi: 10.1101/2020.03.31.20038935

Body Answer: covid-19 has posed a great challenge to public health

Abstract Summary (bart): We aimed to evaluate the correlation of ARBs/ACEIs usage with the pathogenesis of COVID-19 in a retrospective, single-center study. 126 patients with preexisting hypertension at Hubei Provincial Hospital of Traditional Chinese Medicine (HPHTCM) in Wuhan from January 5 to February 22, 2020 were retrospectively allocated according to their antihypertensive medication. 125 patients without hypertension were randomly selected as non-hypertension controls. Epidemiological, demographic, clinical and laboratory data were collected, analyzed and compared.
