import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

df = pd.read_csv("clean_comments.csv")

# ── 1. Filtrer par médicament ──────────────────────────────────────────────────
chemical = "fluoxetine"  # viendra du UI plus tard
drug_df = df[df["chemical_name"] == chemical].copy()
print(f"Commentaires pour {chemical} : {len(drug_df)}")

# ── 2. TF-IDF ─────────────────────────────────────────────────────────────────
vectorizer = TfidfVectorizer(
    max_features = 5000,
    stop_words   = "english",
    ngram_range  = (1, 2),     # unigrammes + bigrammes
    min_df       = 2,          # ignorer les mots qui apparaissent < 2 fois
)
X = vectorizer.fit_transform(drug_df["clean_text"])

# ── 3. Trouver le bon k avec la méthode du coude ──────────────────────────────
inertias = []
K_range = range(2, 60)

for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X)
    inertias.append(km.inertia_)


# Plot

plt.scatter(K_range, inertias)
plt.plot(K_range, inertias, )
plt.xlabel("Valeur de K")
plt.ylabel("WCSS")
#plt.tight_layout()
plt.savefig("optimal_k.png")
plt.show()

# ── 4. KMeans avec le k optimal ───────────────────────────────────────────────
# Choisis k d'après le graphe — on suppose k=5 ici
OPTIMAL_K = 46

kmeans = KMeans(n_clusters=OPTIMAL_K, random_state=42, n_init=10)
drug_df["cluster"] = kmeans.fit_predict(X)

# ── 5. Identifier les thèmes de chaque cluster ────────────────────────────────
feature_names = vectorizer.get_feature_names_out()

print("\nMots dominants par cluster :")
for i in range(OPTIMAL_K):
    center    = kmeans.cluster_centers_[i]
    top_words = [feature_names[j] for j in center.argsort()[-10:][::-1]]
    count     = (drug_df["cluster"] == i).sum()
    print(f"\nCluster {i} ({count} commentaires) :")
    print("  ", ", ".join(top_words))

# ── 6. Nommer les clusters manuellement après inspection ──────────────────────
# Tu remplis ce dict après avoir regardé les mots dominants
cluster_names = {
    0: "Troubles du sommeil",
    1: "Prise de poids",
    2: "Humeur / émotions",
    3: "Dysfonction sexuelle",
    4: "Sevrage / arrêt",
}
drug_df["theme"] = drug_df["cluster"].map(cluster_names)

# ── 7. Résultat final ──────────────────────────────────────────────────────────
profile = drug_df.groupby("cluster").agg(
    theme        = ("theme", "first"),
    nb_mentions  = ("cluster", "count"),
).reset_index().sort_values("nb_mentions", ascending=False)

print(f"\nProfil d'effets secondaires — {chemical}")
print(profile[["theme", "nb_mentions"]])

# ── 8. Sauvegarder ────────────────────────────────────────────────────────────
drug_df.to_csv("comments_clustered.csv", index=False)

#print(f"La taille de la matrice TF-IDF pour le sertraline : {X.shape}")
#print(f"Les colonnes (mots) de la matrice : {vectorizer.get_feature_names_out()}")