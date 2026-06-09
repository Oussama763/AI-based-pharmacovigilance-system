import csv
import time
from datetime import datetime, timezone

import config
from driver_setup import build_driver
from test import collect_post_links, extract_comments_from_post


def run():
    driver = build_driver(headless=True)
    all_comments = []
    seen_texts = set()
    total_posts_visited = 0

    # CSV columns
    FIELDS = ["chemical_name", "drug_class", "brand_names", "subreddit",
              "sort", "text", "source_url", "scraped_at"]

    try:
        for subreddit in config.SEARCH_SUBREDDITS:
            for sort_mode in config.SORT_MODES:
                print(f"\n{'='*55}")
                print(f"  r/{subreddit}  [{sort_mode}]")
                print(f"{'='*55}")

                post_links = collect_post_links(driver, subreddit, sort_mode)
                post_links = list(post_links)[:config.MAX_POSTS_PER_SORT]
                print(f"  Collected {len(post_links)} post links")

                sub_new = 0
                for i, link in enumerate(post_links):
                    comments = extract_comments_from_post(driver, link)

                    new = 0
                    for item in comments:
                        text = item["text"]
                        norm = " ".join(text.lower().split())
                        if norm in seen_texts:
                            continue
                        seen_texts.add(norm)

                        # One row per drug mentioned in the comment
                        for chemical in item["drugs_mentioned"]:
                            drug_info = config.DRUG_DATABASE[chemical]
                            all_comments.append({
                                "chemical_name": chemical,
                                "drug_class":    drug_info["class"],
                                "brand_names":   ", ".join(drug_info["brands"]),
                                "subreddit":     subreddit,
                                "sort":          sort_mode,
                                "text":          text,
                                "source_url":    link,
                                "scraped_at":    datetime.now(timezone.utc).isoformat(),
                            })
                        new += 1

                    sub_new += new
                    total_posts_visited += 1
                    print(
                        f"  Post {i+1:>3}/{len(post_links)} "
                        f"| +{new:>3} comments "
                        f"| Total rows: {len(all_comments)}"
                    )
                    time.sleep(config.SLEEP_BETWEEN_POSTS)

                print(f"  → {sub_new} new comments from r/{subreddit} [{sort_mode}]")

    finally:
        driver.quit()

    # ── Save CSV ───────────────────────────────────────────────────────────────
    with open(config.OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(all_comments)

    # ── Summary ────────────────────────────────────────────────────────────────
    from collections import Counter
    drug_counts = Counter(row["chemical_name"] for row in all_comments)

    print(f"\n{'='*55}")
    print(f"  DONE")
    print(f"  Posts visited  : {total_posts_visited}")
    print(f"  Total CSV rows : {len(all_comments)}")
    print(f"  Output file    : {config.OUTPUT_FILE}")
    print(f"\n  Comments per drug (top 15):")
    for drug, count in drug_counts.most_common(15):
        drug_class = config.DRUG_DATABASE[drug]["class"]
        print(f"    {drug:<20} ({drug_class:<15}) : {count}")
    print(f"{'='*55}")


if __name__ == "__main__":
    run()