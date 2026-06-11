import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
import random

DRUG_URLS = {
    "SSRI": {
    "fluoxetine":      [("prozac",     "depression"),
                        ("prozac",     "anxiety"),
                        ("prozac",     "ocd")],
    "sertraline":      [("zoloft",     "depression"),
                        ("zoloft",     "anxiety"),
                        ("zoloft",     "ocd")],
    "escitalopram":    [("lexapro",    "depression"),
                        ("lexapro",    "anxiety")],
    "citalopram":      [("celexa",     "depression"),
                        ("celexa",     "anxiety")],
    "paroxetine":      [("paxil",      "depression"),
                        ("paxil",      "anxiety")],
    "fluvoxamine":     [("luvox",      "ocd")]},

    "SNRI": {
    "venlafaxine":     [("effexor",    "depression"),
                        ("effexor",    "anxiety")],
    "duloxetine":      [("cymbalta",   "depression"),
                        ("cymbalta",   "anxiety")],
    "desvenlafaxine":  [("pristiq",    "depression")]},

    "Atypical": {
    "bupropion":       [("wellbutrin", "depression")],
    "mirtazapine":     [("remeron",    "depression")],
    "trazodone":       [("desyrel",    "depression")],
    "vortioxetine":    [("trintellix", "depression")]},

    "TCA": {
    "amitriptyline":   [("elavil",     "depression")],
    "nortriptyline":   [("pamelor",    "depression")]},

    "Benzodiazepines": {
    "alprazolam":      [("xanax",      "anxiety")],
    "clonazepam":      [("klonopin",   "anxiety")],
    "diazepam":        [("valium",     "anxiety")],
    "lorazepam":       [("ativan",     "anxiety")]},

    "Antipsychotics":{
    "quetiapine":      [("seroquel",   "depression"),
                        ("seroquel",   "bipolar-disorder")],
    "aripiprazole":    [("abilify",    "depression"),
                        ("abilify",    "bipolar-disorder")],
    "olanzapine":      [("zyprexa",    "bipolar-disorder")],
    "risperidone":     [("risperdal",  "bipolar-disorder")],
    "lurasidone":      [("latuda",     "bipolar-disorder")]},

    "MoodStabilizers":{
    "lamotrigine":     [("lamictal",   "bipolar-disorder")],
    "lithium":         [("lithobid",   "bipolar-disorder")],
    "valproate":       [("depakote",   "bipolar-disorder")]},

    "ADHD": {
    "methylphenidate": [("ritalin",    "adhd")],
    "amphetamine":     [("adderall",   "adhd")],
    "lisdexamfetamine":[("vyvanse",    "adhd")],
    "atomoxetine":     [("strattera",  "adhd")]}
}

#reviews_txt_list = []
df = {}
k = 0
for drug_class in DRUG_URLS:
    for chemical_name in DRUG_URLS[drug_class]:
        brand_cond = DRUG_URLS[drug_class][chemical_name]
        for j in range(len(brand_cond)):
            brand = brand_cond[j][0]
            condition = brand_cond[j][1]
            for i in range(1,6):
                time.sleep(random.uniform(1,3))

                url = f"https://www.drugs.com/comments/{chemical_name}/{brand}-for-{condition}.html?page={i}"
                print(url)
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
                session = requests.Session() 
                session.headers.update(headers)
                response = session.get(url)
                print(response.status_code)
                source = response.text
                soup = BeautifulSoup(source, 'html.parser')

                review_text = soup.find_all("div", {"class": "ddc-comment ddc-box ddc-mgb-2"})
                for review in review_text:
                    review = BeautifulSoup(str(review), 'html.parser')
                    review_txt_content = review.p.text
                    df[str(k)] = [drug_class, chemical_name, brand, review_txt_content]
                    k += 1
            

df = pd.DataFrame.from_dict(df, orient="index", columns=["drug_class", "chemical_name", "brand_names", "text"])
df.to_csv("more_comments.csv", index=False)