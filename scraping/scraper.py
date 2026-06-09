import time
from selenium.webdriver.common.by import By
import config

# ─── Selectors ────────────────────────────────────────────────────────────────
POST_LINK_SELECTORS = [
    "a[slot='full-post-link']",
    "a[data-click-id='body']",
    "a[href*='/comments/']",
]

COMMENT_SELECTORS = [
    "shreddit-comment",
    "div[id^='t1_']",
    "[data-testid='comment']",
    "div.Comment",
]

MORE_COMMENT_XPATHS = [
    "//*[contains(text(),'more comment')]",
    "//*[contains(text(),'More Comments')]",
    "//*[contains(text(),'Continue this thread')]",
    "//*[contains(text(),'load more')]",
]


def _scroll(driver, times, pause):
    for _ in range(times):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause)


def _click_more_comments(driver):
    for _ in range(config.CLICK_MORE_ROUNDS):
        clicked = False
        for xpath in MORE_COMMENT_XPATHS:
            try:
                for btn in driver.find_elements(By.XPATH, xpath)[:5]:
                    try:
                        driver.execute_script("arguments[0].scrollIntoView();", btn)
                        driver.execute_script("arguments[0].click();", btn)
                        time.sleep(config.SLEEP_AFTER_CLICK)
                        clicked = True
                    except Exception:
                        pass
            except Exception:
                pass
        if not clicked:
            break


def _detect_drugs_in_text(text: str) -> list[str]:
    """Return list of chemical names mentioned in the text."""
    text_lower = text.lower()
    found = set()
    for chemical, info in config.DRUG_DATABASE.items():
        # Match chemical name
        if chemical in text_lower:
            found.add(chemical)
        # Match any brand name
        for brand in info["brands"]:
            if brand in text_lower:
                found.add(chemical)
    return list(found)


def _is_junk(text: str) -> bool:
    if text.strip() in config.JUNK_BODIES:
        return True
    if len(text.strip()) < config.MIN_COMMENT_LENGTH:
        return True
    for phrase in config.BOT_PHRASES:
        if phrase.lower() in text.lower():
            return True
    return False


def collect_post_links(driver, subreddit: str, sort_mode: str) -> set:
    url = f"https://www.reddit.com/r/{subreddit}/{sort_mode}/"
    if sort_mode == "top":
        url += "?t=all"
    try:
        driver.get(url)
        time.sleep(3)
    except Exception:
        return set()

    _scroll(driver, config.SCROLL_FEED_TIMES, config.SLEEP_SCROLL)

    links = set()
    for selector in POST_LINK_SELECTORS:
        elements = driver.find_elements(By.CSS_SELECTOR, selector)
        for el in elements:
            href = el.get_attribute("href") or ""
            if "/comments/" in href:
                links.add(href.split("?")[0])
        if links:
            break
    return links


def extract_comments_from_post(driver, url: str) -> list[dict]:
    """
    Visit a post, extract all comments, detect which drug(s) each
    comment mentions, and return only relevant ones.
    """
    try:
        driver.get(url)
        time.sleep(2)
    except Exception:
        return []

    # Quick pre-check: does this page mention ANY drug at all?
    try:
        page_text = driver.find_element(By.TAG_NAME, "body").text.lower()
        if not any(
            chemical in page_text or
            any(brand in page_text for brand in info["brands"])
            for chemical, info in config.DRUG_DATABASE.items()
        ):
            return []
    except Exception:
        return []

    _scroll(driver, config.SCROLL_POST_TIMES, config.SLEEP_SCROLL)
    _click_more_comments(driver)
    _scroll(driver, 3, config.SLEEP_SCROLL)

    # Extract raw comment elements
    raw_elements = []
    for selector in COMMENT_SELECTORS:
        elements = driver.find_elements(By.CSS_SELECTOR, selector)
        if elements:
            raw_elements = elements
            break

    results = []
    for el in raw_elements:
        try:
            text = driver.execute_script(
                "return arguments[0].shadowRoot ? "
                "(arguments[0].shadowRoot.querySelector('[slot=comment]') ? "
                "arguments[0].shadowRoot.querySelector('[slot=comment]').innerText : "
                "arguments[0].innerText) : arguments[0].innerText;",
                el
            ) or el.text
        except Exception:
            text = el.text or ""

        text = text.strip()
        if _is_junk(text):
            continue

        drugs_mentioned = _detect_drugs_in_text(text)
        if not drugs_mentioned:
            continue

        results.append({
            "text": text,
            "drugs_mentioned": drugs_mentioned,
        })

    return results