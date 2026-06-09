# ─── Drug Database ────────────────────────────────────────────────────────────
# Structure: chemical_name -> { brands, drug_class, search_keywords }
# search_keywords = terms we look for IN comment text to confirm relevance
# brands = used for brand->chemical lookup from the UI

DRUG_DATABASE = {
    # ── SSRIs ──────────────────────────────────────────────────────────────────
    "fluoxetine":       {"brands": ["prozac", "sarafem", "Symbyax", "Selfemra", "Rapiflux"],                                   "class": "SSRI"},
    "sertraline":       {"brands": ["zoloft", "Lustral", "Serenata", "Serlift", "Selectra"],                                   "class": "SSRI"},
    "escitalopram":     {"brands": ["lexapro", "cipralex"],                                                                    "class": "SSRI"},
    "citalopram":       {"brands": ["celexa", "Cipramil"],                                                                     "class": "SSRI"},
    "paroxetine":       {"brands": ["paxil", "seroxat", "Xetanor"],                                                            "class": "SSRI"},
    "fluvoxamine":      {"brands": ["luvox", "faverin", "dumyrox"],                                                            "class": "SSRI"},

    # ── SNRIs ──────────────────────────────────────────────────────────────────
    "venlafaxine":      {"brands": ["effexor", "effexor xr", "vandral"],                                                       "class": "SNRI"},
    "desvenlafaxine":   {"brands": ["pristiq", "khedezla"],                                                                    "class": "SNRI"},
    "duloxetine":       {"brands": ["cymbalta", "yentreve", "dulane"],                                                         "class": "SNRI"},
    "levomilnacipran":  {"brands": ["fetzima", "fetzima er"],                                                                  "class": "SNRI"},

    # ── TCAs ───────────────────────────────────────────────────────────────────
    "amitriptyline":    {"brands": ["elavil", "endep", "vanatrip"],                                                            "class": "TCA"},
    "nortriptyline":    {"brands": ["pamelor", "aventyl"],                                                                     "class": "TCA"},
    "imipramine":       {"brands": ["tofranil", "janimine"],                                                                   "class": "TCA"},
    "clomipramine":     {"brands": ["anafranil", "clopram"],                                                                   "class": "TCA"},
    "desipramine":      {"brands": ["norpramin", "pertofrane"],                                                                "class": "TCA"},

    # ── MAOIs ──────────────────────────────────────────────────────────────────
    "phenelzine":       {"brands": ["nardil", "nardelzine"],                                                                   "class": "MAOI"},
    "tranylcypromine":  {"brands": ["parnate", "parstelin"],                                                                   "class": "MAOI"},
    "isocarboxazid":    {"brands": ["marplan", "marplazid"],                                                                   "class": "MAOI"},
    "selegiline":       {"brands": ["emsam", "eldepryl", "zelapar"],                                                           "class": "MAOI"},

    # ── Atypical Antidepressants ───────────────────────────────────────────────  
    "bupropion":        {"brands": ["wellbutrin", "zyban", "aplenzin", "forfivo xl"],                                          "class": "Atypical"},
    "mirtazapine":      {"brands": ["remeron", "remeron soltab"],                                                              "class": "Atypical"},
    "trazodone":        {"brands": ["desyrel", "oleptro"],                                                                     "class": "Atypical"},
    "vortioxetine":     {"brands": ["trintellix", "brintellix"],                                                               "class": "Atypical"},
    "vilazodone":       {"brands": ["viibryd", "viibryd starter pack"],                                                        "class": "Atypical"},

    # ── Benzodiazepines ────────────────────────────────────────────────────────
    "alprazolam":       {"brands": ["xanax", "xanax xr", "niravam"],                                                           "class": "Benzodiazepine"},
    "clonazepam":       {"brands": ["klonopin", "rivotril"],                                                                   "class": "Benzodiazepine"},
    "diazepam":         {"brands": ["valium", "diastat"],                                                                      "class": "Benzodiazepine"},
    "lorazepam":        {"brands": ["ativan", "temesta"],                                                                      "class": "Benzodiazepine"},
    "temazepam":        {"brands": ["restoril", "normison"],                                                                   "class": "Benzodiazepine"},

    # ── Atypical Antipsychotics ────────────────────────────────────────────────
    "risperidone":      {"brands": ["risperdal", "risperdal consta", "perseris"],                                              "class": "Antipsychotic"},
    "olanzapine":       {"brands": ["zyprexa", "Symbyax", "zydis"],                                                            "class": "Antipsychotic"},
    "quetiapine":       {"brands": ["seroquel", "seroquel xr"],                                                                "class": "Antipsychotic"},
    "aripiprazole":     {"brands": ["abilify", "abilify maintena", "aristada"],                                                "class": "Antipsychotic"},
    "ziprasidone":      {"brands": ["geodon", "zeldox"],                                                                       "class": "Antipsychotic"},
    "lurasidone":       {"brands": ["latuda", "latuda tablets"],                                                               "class": "Antipsychotic"},
    "paliperidone":     {"brands": ["invega", "invega sustenna", "invega trinza"],                                             "class": "Antipsychotic"},
    "clozapine":        {"brands": ["clozaril", "fazaclo", "versacloz"],                                                       "class": "Antipsychotic"},

    # ── Typical Antipsychotics ─────────────────────────────────────────────────
    "haloperidol":      {"brands": ["haldol", "haldol decanoate"],                                                             "class": "Antipsychotic"},
    "chlorpromazine":   {"brands": ["thorazine", "largactil"],                                                                 "class": "Antipsychotic"},
    "fluphenazine":     {"brands": ["prolixin", "modecate"],                                                                   "class": "Antipsychotic"},

    # ── Mood Stabilizers ───────────────────────────────────────────────────────
    "lithium":          {"brands": ["lithobid", "eskalith", "priadel"],                                                        "class": "MoodStabilizer"},
    "valproate":        {"brands": ["depakote", "epilim", "depakene"],                                                         "class": "MoodStabilizer"},
    "lamotrigine":      {"brands": ["lamictal", "lamictal xr"],                                                                "class": "MoodStabilizer"},
    "carbamazepine":    {"brands": ["tegretol", "carbatrol", "equetro"],                                                       "class": "MoodStabilizer"},
    "oxcarbazepine":    {"brands": ["trileptal", "oxtellar xr"],                                                               "class": "MoodStabilizer"},

    # ── ADHD Stimulants ────────────────────────────────────────────────────────
    "methylphenidate":  {"brands": ["ritalin", "concerta", "methylin"],                                                        "class": "ADHD_Stimulant"},
    "amphetamine":      {"brands": ["adderall", "adderall xr", "evekeo"],                                                      "class": "ADHD_Stimulant"},
    "lisdexamfetamine": {"brands": ["vyvanse", "elvanse"],                                                                     "class": "ADHD_Stimulant"},

    # ── ADHD Non-Stimulants ────────────────────────────────────────────────────
    "atomoxetine":      {"brands": ["strattera", "attentin"],                                                                  "class": "ADHD_NonStimulant"},
    "guanfacine":       {"brands": ["intuniv", "tenex"],                                                                       "class": "ADHD_NonStimulant"},
    "clonidine":        {"brands": ["kapvay", "catapres"],                                                                     "class": "ADHD_NonStimulant"},
}

# ─── Build reverse lookup: brand -> chemical ──────────────────────────────────
BRAND_TO_CHEMICAL = {}
for chemical, info in DRUG_DATABASE.items():
    for brand in info["brands"]:
        BRAND_TO_CHEMICAL[brand.lower()] = chemical
    BRAND_TO_CHEMICAL[chemical.lower()] = chemical  # chemical maps to itself too

# ─── Subreddits to search in ──────────────────────────────────────────────────
# These are broad mental health communities where users discuss medications
SEARCH_SUBREDDITS = [
    "prozac",
    "saraffem",
    "zoloft",
    "lexapro",
    "cipralex",
    "celexa",
    "paxil",
    "seroxat",
    "luvox", 
    "faverin", 
    "dumyrox",
    "effexor", 
    "vandral",
    "pristiq", 
    "khedezla",
    "cymbalta", 
    "yentreve", 
    "dulane",
    "fetzima",
    "elavil", 
    "endep", 
    "vanatrip",
    "pamelor", 
    "aventyl",
    "tofranil", 
    "janimine",
    "anafranil", 
    "clopram",
    "norpramin", 
    "pertofrane",
    "nardil", 
    "nardelzine",
    "parnate", 
    "parstelin",
    "marplan", 
    "marplazid",
    "emsam", 
    "eldepryl", 
    "zelapar",
    "wellbutrin", 
    "zyban", 
    "aplenzin", 
    "remeron", 
    "desyrel", 
    "oleptro",
    "trintellix", 
    "brintellix",
    "viibryd",
    "xanax",  
    "niravam",
    "klonopin", 
    "rivotril",
    "valium", 
    "diastat",
    "ativan", 
    "temesta",
    "restoril", 
    "normison",
    "risperdal",
    "perseris",
    "zyprexa", 
    "symbyax", 
    "zydis",
    "seroquel",
    "abilify",  
    "aristada",
    "geodon", 
    "zeldox",
    "latuda",
    "invega",
    "clozaril", 
    "fazaclo", 
    "versacloz",
    "haldol",
    "thorazine", 
    "largactil",
    "prolixin", 
    "modecate",
    "lithobid", 
    "eskalith", 
    "priadel",
    "depakote", 
    "epilim", 
    "depakene",
    "lamictal",
    "tegretol", 
    "carbatrol", 
    "equetro",
    "trileptal",
    "ritalin", 
    "concerta", 
    "metadate", 
    "daytrana",
    "adderall",  
    "evekeo",
    "vyvanse", 
    "elvanse",
    "strattera", 
    "attentin",
    "intuniv", 
    "tenex",
    "kapvay", 
    "catapres"
    "depression",
    "anxiety",
    "mentalhealth",
    "bipolarreddit",
    "schizophrenia",
    "OCD",
    "ADHD",
    "antidepressants",
    "ssri",
    "benzodiazepines",
    "ptsd",
    "BPD",
    "psychopharmacology",
]

# ─── Side effect keywords — used to confirm a comment is about side effects ───
SIDE_EFFECT_KEYWORDS = [
    "side effect", "side effects", "withdrawal", "stopped", "started",
    "dose", "dosage", "mg", "week", "month", "nausea", "headache",
    "dizzy", "tired", "fatigue", "sleep", "insomnia", "weight",
    "anxiety", "mood", "emotion", "numb", "blunt", "sex", "libido",
    "sweat", "dry mouth", "appetite", "tremor", "shaking", "heart",
    "palpitation", "rash", "itch", "memory", "concentration", "foggy",
    "panic", "suicidal", "suicid", "agitation", "irritable", "crying", "flat", "apathy",
    "vomit", "orgasm"
]

# ─── Scraping limits ──────────────────────────────────────────────────────────
SORT_MODES           = ["hot", "top"]
MAX_POSTS_PER_SORT   = 100
SCROLL_FEED_TIMES    = 20
SCROLL_POST_TIMES    = 15
CLICK_MORE_ROUNDS    = 10
MIN_COMMENT_LENGTH   = 40

# ─── Politeness ───────────────────────────────────────────────────────────────
SLEEP_BETWEEN_POSTS  = 1.5
SLEEP_SCROLL         = 1.2
SLEEP_AFTER_CLICK    = 1.0

# ─── Output ───────────────────────────────────────────────────────────────────
OUTPUT_FILE = "comments.csv"

# ─── Bot / junk filters ───────────────────────────────────────────────────────
BOT_PHRASES = [
    "I am a bot",
    "performed automatically",
    "contact the moderators",
    "Your post has been successfully submitted",
]
JUNK_BODIES = {"[removed]", "[deleted]", ""}