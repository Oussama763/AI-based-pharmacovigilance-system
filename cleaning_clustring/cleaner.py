import pandas as pd
import re


df = pd.read_csv("../scraping/merged_raw.csv")

def clean_text(text):
    text = text.lower()                          # tout en minuscules
    text = re.sub(r'http\S+', '', text)          # supprimer les URLs
    text = re.sub(r'\[.*?\]\(.*?\)', '', text)   # supprimer les liens markdown
    text = re.sub(r'[^a-z\s]', '', text)         # garder uniquement les lettres
    text = re.sub(r'\s+', ' ', text).strip()     # normaliser les espaces
    return text

df['clean_text'] = df['text'].apply(clean_text)
df = df[df['clean_text'].str.len() > 20]         # supprimer les textes vides

df = df[["chemical_name", "brand_names", "clean_text"]]

df.to_csv('clean_comments.csv', index=False)     #creer le nouveau .csv exploitable