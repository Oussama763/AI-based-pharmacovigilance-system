import pandas as pd
import time
from datetime import datetime
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from driver_setup import build_driver
from config import DRUG_DATABASE


# ── URL mapping: chemical -> list of (brand, condition) slugs ─────────────────
# Format: https://www.drugs.com/comments/{chemical}/{brand}-for-{condition}.html
DRUG_URLS = {
    # SSRIs
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
    "fluvoxamine":     [("luvox",      "ocd")],

    # SNRIs
    "venlafaxine":     [("effexor",    "depression"),
                        ("effexor",    "anxiety")],
    "duloxetine":      [("cymbalta",   "depression"),
                        ("cymbalta",   "anxiety")],
    "desvenlafaxine":  [("pristiq",    "depression")],

    # Atypical antidepressants
    "bupropion":       [("wellbutrin", "depression")],
    "mirtazapine":     [("remeron",    "depression")],
    "trazodone":       [("desyrel",    "depression")],
    "vortioxetine":    [("trintellix", "depression")],

    # TCAs
    "amitriptyline":   [("elavil",     "depression")],
    "nortriptyline":   [("pamelor",    "depression")],

    # Benzodiazepines
    "alprazolam":      [("xanax",      "anxiety")],
    "clonazepam":      [("klonopin",   "anxiety")],
    "diazepam":        [("valium",     "anxiety")],
    "lorazepam":       [("ativan",     "anxiety")],

    # Antipsychotics
    "quetiapine":      [("seroquel",   "depression"),
                        ("seroquel",   "bipolar-disorder")],
    "aripiprazole":    [("abilify",    "depression"),
                        ("abilify",    "bipolar-disorder")],
    "olanzapine":      [("zyprexa",    "bipolar-disorder")],
    "risperidone":     [("risperdal",  "bipolar-disorder")],
    "lurasidone":      [("latuda",     "bipolar-disorder")],

    # Mood stabilizers
    "lamotrigine":     [("lamictal",   "bipolar-disorder")],
    "lithium":         [("lithobid",   "bipolar-disorder")],
    "valproate":       [("depakote",   "bipolar-disorder")],

    # ADHD
    "methylphenidate": [("ritalin",    "adhd")],
    "amphetamine":     [("adderall",   "adhd")],
    "lisdexamfetamine":[("vyvanse",    "adhd")],
    "atomoxetine":     [("strattera",  "adhd")],
}


def get_total_pages(driver, url_base):
    """Detecte le nombre total de pages disponibles."""
    try:
        driver.get(f"{url_base}?page=1")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.ddc-comment.ddc-box")
            )
        )
        soup     = BeautifulSoup(driver.page_source, "html.parser")
        # Chercher le dernier numero de page dans la pagination
        pager    = soup.find("nav", class_=lambda c: c and "ddc-pager" in c)
        if not pager:
            return 1
        page_links = pager.find_all("a")
        pages = []
        for link in page_links:
            try:
                pages.append(int(link.get_text(strip=True)))
            except:
                continue
        return max(pages) if pages else 1
    except:
        return 1


def scrape_url(driver, chemical_name, brand, condition, max_pages=20):
    """Scrape all pages for a given chemical/brand/condition URL."""
    url_base = f"https://www.drugs.com/comments/{chemical_name}/{brand}-for-{condition}.html"
    reviews  = []

    # Detecter le nombre reel de pages
    total_pages = get_total_pages(driver, url_base)
    total_pages = min(total_pages, max_pages)
    print(f"    {url_base} — {total_pages} pages")

    for page in range(1, total_pages + 1):
        url = f"{url_base}?page={page}"

        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div.ddc-comment.ddc-box")
                )
            )

            soup         = BeautifulSoup(driver.page_source, "html.parser")
            review_cards = soup.find_all(
                "div",
                class_=lambda c: c and "ddc-comment" in c and "ddc-box" in c
            )

            if not review_cards:
                break

            for card in review_cards:
                # ── Texte ─────────────────────────────────────────────────────
                text_el = card.find("p")
                if not text_el:
                    continue
                text = text_el.get_text(strip=True)
                if len(text) < 30:
                    continue

                # ── Note ──────────────────────────────────────────────────────
                rating_el = card.find("div", class_="ddc-rating-summary")
                rating    = rating_el.get_text(strip=True) if rating_el else None

                # ── Condition et duree ────────────────────────────────────────
                header_condition, duration = None, None
                header_el = card.find(
                    "ul", class_=lambda c: c and "ddc-comment-header" in c
                )
                if header_el:
                    for item in header_el.find_all("li"):
                        item_text = item.get_text(strip=True).lower()
                        if "condition" in item_text:
                            header_condition = item.get_text(strip=True)
                        if any(w in item_text for w in ["month", "year", "week", "duration"]):
                            duration = item.get_text(strip=True)

                reviews.append({
                    "chemical_name": chemical_name,
                    "brand":         brand,
                    "condition":     header_condition or condition,
                    "duration":      duration,
                    "text":          text,
                    "rating":        rating,
                    "source_url":    url,
                    "scraped_at":    datetime.now().isoformat(),
                })

            print(f"      Page {page}/{total_pages} — {len(review_cards)} avis | total: {len(reviews)}")
            time.sleep(1.2)

        except Exception as e:
            print(f"      Page {page} erreur : {e}")
            continue

    return reviews


def rating_to_severity(rating):
    try:
        r = int(float(str(rating).strip()))
        if r <= 3:   return 2
        elif r <= 6: return 1
        else:        return 0
    except:
        return None


def run():
    driver      = build_driver(headless=True)
    all_reviews = []
    seen_texts  = set()

    try:
        for chemical, url_list in DRUG_URLS.items():
            print(f"\n{'='*55}")
            print(f"  {chemical}")
            print(f"{'='*55}")

            for brand, condition in url_list:
                reviews = scrape_url(driver, chemical, brand, condition, max_pages=20)

                # Deduplication
                new = 0
                for r in reviews:
                    norm = " ".join(r["text"].lower().split())
                    if norm in seen_texts:
                        continue
                    seen_texts.add(norm)
                    all_reviews.append(r)
                    new += 1

                print(f"    → {new} nouveaux avis")
                time.sleep(2)

    finally:
        driver.quit()

    if not all_reviews:
        print("Aucun avis collecté — vérifier les sélecteurs CSS")
        return

    df = pd.DataFrame(all_reviews)

    # ── drug_class et brand_names depuis config ───────────────────────────────
    df["drug_class"]  = df["chemical_name"].map(
        lambda c: DRUG_DATABASE.get(c, {}).get("class", "Unknown")
    )
    df["brand_names"] = df["chemical_name"].map(
        lambda c: ", ".join(DRUG_DATABASE.get(c, {}).get("brands", []))
    )

    # ── Severite ──────────────────────────────────────────────────────────────
    df["severity"] = df["rating"].apply(rating_to_severity)

    # ── Nettoyage final ───────────────────────────────────────────────────────
    df = df.drop_duplicates(subset=["text"])
    df = df[df["text"].str.len() >= 30]
    df = df.reset_index(drop=True)
    df.insert(0, "id", df.index.map(lambda i: f"CMT_{i:06d}"))

    # ── Colonnes finales ──────────────────────────────────────────────────────
    df = df[[
        "id", "chemical_name", "drug_class", "brand_names", "brand",
        "condition", "duration", "rating", "severity",
        "text", "source_url", "scraped_at"
    ]]

    df.to_csv("comments_new.csv", index=False)

    # ── Resume ────────────────────────────────────────────────────────────────
    print(f"\n{'='*55}")
    print(f"  DONE")
    print(f"  Total avis       : {len(df)}")
    print(f"  Médicaments      : {df['chemical_name'].nunique()}")
    print(f"  Avec note        : {df['rating'].notna().sum()}")
    print(f"\n  Avis par médicament :")
    counts = (
        df.groupby(["chemical_name", "drug_class"])["text"]
        .count()
        .sort_values(ascending=False)
    )
    for (drug, cls), count in counts.head(15).items():
        print(f"    {drug:<20} ({cls:<15}) : {count}")
    print(f"{'='*55}")


if __name__ == "__main__":
    run()