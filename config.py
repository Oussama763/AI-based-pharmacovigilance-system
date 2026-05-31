# ─── Drug Database ────────────────────────────────────────────────────────────
# Structure: chemical_name -> { brands, drug_class, search_keywords }
# search_keywords = terms we look for IN comment text to confirm relevance
# brands = used for brand->chemical lookup from the UI

DRUG_DATABASE = {
    # ── SSRIs ──────────────────────────────────────────────────────────────────
    "fluoxetine":       {"brands": ["prozac", "sarafem"],                        "class": "SSRI"},
    "sertraline":       {"brands": ["zoloft"],                                   "class": "SSRI"},
    "escitalopram":     {"brands": ["lexapro", "cipralex"],                      "class": "SSRI"},
    "citalopram":       {"brands": ["celexa"],                                   "class": "SSRI"},
    "paroxetine":       {"brands": ["paxil", "seroxat"],                         "class": "SSRI"},
    "fluvoxamine":      {"brands": ["luvox"],                                    "class": "SSRI"},

    # ── SNRIs ──────────────────────────────────────────────────────────────────
    "venlafaxine":      {"brands": ["effexor"],                                  "class": "SNRI"},
    "desvenlafaxine":   {"brands": ["pristiq"],                                  "class": "SNRI"},
    "duloxetine":       {"brands": ["cymbalta"],                                 "class": "SNRI"},
    "levomilnacipran":  {"brands": ["fetzima"],                                  "class": "SNRI"},

    # ── TCAs ───────────────────────────────────────────────────────────────────
    "amitriptyline":    {"brands": ["elavil"],                                   "class": "TCA"},
    "nortriptyline":    {"brands": ["pamelor"],                                  "class": "TCA"},
    "imipramine":       {"brands": ["tofranil"],                                 "class": "TCA"},
    "clomipramine":     {"brands": ["anafranil"],                                "class": "TCA"},
    "desipramine":      {"brands": ["norpramin"],                                "class": "TCA"},

    # ── MAOIs ──────────────────────────────────────────────────────────────────
    "phenelzine":       {"brands": ["nardil"],                                   "class": "MAOI"},
    "tranylcypromine":  {"brands": ["parnate"],                                  "class": "MAOI"},
    "isocarboxazid":    {"brands": ["marplan"],                                  "class": "MAOI"},
    "selegiline":       {"brands": ["emsam"],                                    "class": "MAOI"},

    # ── Atypical Antidepressants ───────────────────────────────────────────────
    "bupropion":        {"brands": ["wellbutrin", "zyban"],                      "class": "Atypical"},
    "mirtazapine":      {"brands": ["remeron"],                                  "class": "Atypical"},
    "trazodone":        {"brands": ["desyrel"],                                  "class": "Atypical"},
    "vortioxetine":     {"brands": ["trintellix"],                               "class": "Atypical"},
    "vilazodone":       {"brands": ["viibryd"],                                  "class": "Atypical"},

    # ── Benzodiazepines ────────────────────────────────────────────────────────
    "alprazolam":       {"brands": ["xanax"],                                    "class": "Benzodiazepine"},
    "clonazepam":       {"brands": ["klonopin"],                                 "class": "Benzodiazepine"},
    "diazepam":         {"brands": ["valium"],                                   "class": "Benzodiazepine"},
    "lorazepam":        {"brands": ["ativan"],                                   "class": "Benzodiazepine"},
    "temazepam":        {"brands": ["restoril"],                                 "class": "Benzodiazepine"},

    # ── Atypical Antipsychotics ────────────────────────────────────────────────
    "risperidone":      {"brands": ["risperdal"],                                "class": "Antipsychotic"},
    "olanzapine":       {"brands": ["zyprexa"],                                  "class": "Antipsychotic"},
    "quetiapine":       {"brands": ["seroquel"],                                 "class": "Antipsychotic"},
    "aripiprazole":     {"brands": ["abilify"],                                  "class": "Antipsychotic"},
    "ziprasidone":      {"brands": ["geodon"],                                   "class": "Antipsychotic"},
    "lurasidone":       {"brands": ["latuda"],                                   "class": "Antipsychotic"},
    "paliperidone":     {"brands": ["invega"],                                   "class": "Antipsychotic"},
    "clozapine":        {"brands": ["clozaril"],                                 "class": "Antipsychotic"},

    # ── Typical Antipsychotics ─────────────────────────────────────────────────
    "haloperidol":      {"brands": ["haldol"],                                   "class": "Antipsychotic"},
    "chlorpromazine":   {"brands": ["thorazine"],                                "class": "Antipsychotic"},
    "fluphenazine":     {"brands": ["prolixin"],                                 "class": "Antipsychotic"},

    # ── Mood Stabilizers ───────────────────────────────────────────────────────
    "lithium":          {"brands": ["lithobid", "eskalith"],                     "class": "MoodStabilizer"},
    "valproate":        {"brands": ["depakote"],                                 "class": "MoodStabilizer"},
    "lamotrigine":      {"brands": ["lamictal"],                                 "class": "MoodStabilizer"},
    "carbamazepine":    {"brands": ["tegretol"],                                 "class": "MoodStabilizer"},
    "oxcarbazepine":    {"brands": ["trileptal"],                                "class": "MoodStabilizer"},

    # ── ADHD Stimulants ────────────────────────────────────────────────────────
    "methylphenidate":  {"brands": ["ritalin", "concerta"],                      "class": "ADHD_Stimulant"},
    "amphetamine":      {"brands": ["adderall"],                                 "class": "ADHD_Stimulant"},
    "lisdexamfetamine": {"brands": ["vyvanse"],                                  "class": "ADHD_Stimulant"},

    # ── ADHD Non-Stimulants ────────────────────────────────────────────────────
    "atomoxetine":      {"brands": ["strattera"],                                "class": "ADHD_NonStimulant"},
    "guanfacine":       {"brands": ["intuniv"],                                  "class": "ADHD_NonStimulant"},
    "clonidine":        {"brands": ["kapvay"],                                   "class": "ADHD_NonStimulant"},
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
    "panic", "suicidal", "agitation", "irritable", "crying", "flat",
]

# ─── Scraping limits ──────────────────────────────────────────────────────────
SORT_MODES           = ["hot", "new", "top"]
MAX_POSTS_PER_SORT   = 50
SCROLL_FEED_TIMES    = 15
SCROLL_POST_TIMES    = 8
CLICK_MORE_ROUNDS    = 5
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