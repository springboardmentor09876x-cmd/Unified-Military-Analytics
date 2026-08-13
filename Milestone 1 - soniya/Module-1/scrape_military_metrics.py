"""
scrape_military_metrics.py
---------------------------
Week 1 deliverable for the Unified Military Analytics Dashboard project.

Reads a list of GlobalFirepower.com country detail-page URLs from
links_for_military_data.txt (one URL per line), scrapes each page,
and writes the raw extracted metrics to military_raw_data.csv.

Usage:
    python scrape_military_metrics.py

Requires:
    pip install requests beautifulsoup4
"""

import re
import csv
import time
import logging
from pathlib import Path

import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
INPUT_URL_FILE = "links_for_military_data.txt"
OUTPUT_CSV = "military_raw_data.csv"
DEBUG_HTML_DIR = Path("debug_html")   # per-country raw HTML, for troubleshooting
REQUEST_DELAY_SECONDS = 1.5           # be polite to the server
REQUEST_TIMEOUT = 15
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Regex patterns for each metric we want to pull out of the page's plain text.
# Each pattern is applied to the full visible text of the page (whitespace-
# normalized), which is far more resilient to markup/class-name changes than
# scraping by CSS selector.
# ---------------------------------------------------------------------------
NUM = r"([\d,]+(?:\.\d+)?)"

PATTERNS = {
    "power_index_rank": re.compile(r"ranked\s+(\d+)\s+of\s+(\d+)", re.I),
    "power_index_score": re.compile(r"PwrIndx\*?\s+score\s+of\s+([\d.]+)", re.I),
    "total_population": re.compile(r"Total Population:?\s*" + NUM, re.I),
    "active_personnel": re.compile(r"Active Personnel\s*" + NUM, re.I),
    "reserve_personnel": re.compile(r"Reserve Personnel\s*" + NUM, re.I),
    "total_aircraft": re.compile(r"Aircraft Total:\s*Stock:\s*" + NUM, re.I),
    "total_tanks": re.compile(r"Tanks:\s*Stock:\s*" + NUM, re.I),
    "total_navy_assets": re.compile(r"Total Assets:\s*" + NUM, re.I),
    "defense_budget_usd": re.compile(r"Defense Budget:\s*\$" + NUM, re.I),
    "purchasing_power_parity_usd": re.compile(r"Purchasing Power Parity:\s*\$" + NUM, re.I),
    "square_land_area_km": re.compile(r"Square Land Area:\s*" + NUM, re.I),
}


def load_urls(path: str) -> list[str]:
    """Read and validate the URL list. Skips blanks and comment lines."""
    urls = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            urls.append(line)
    log.info("Loaded %d URLs from %s", len(urls), path)
    return urls


def country_id_from_url(url: str) -> str:
    match = re.search(r"country_id=([\w-]+)", url)
    return match.group(1) if match else url


def fetch_page(url: str) -> str | None:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        return resp.text
    except requests.RequestException as e:
        log.warning("Request failed for %s: %s", url, e)
        return None


def extract_metrics(html: str) -> dict:
    """Pull every metric in PATTERNS out of the page's visible text."""
    soup = BeautifulSoup(html, "html.parser")

    # Collapse all visible text into one whitespace-normalized string.
    text = soup.get_text(separator=" ")
    text = re.sub(r"\s+", " ", text)

    row = {}

    rank_match = PATTERNS["power_index_rank"].search(text)
    if rank_match:
        row["power_index_rank"] = rank_match.group(1)
        row["countries_considered"] = rank_match.group(2)
    else:
        row["power_index_rank"] = ""
        row["countries_considered"] = ""

    for key, pattern in PATTERNS.items():
        if key == "power_index_rank":
            continue
        match = pattern.search(text)
        row[key] = match.group(1) if match else ""

    return row


def scrape_all(urls: list[str]) -> list[dict]:
    DEBUG_HTML_DIR.mkdir(exist_ok=True)
    results = []
    success_count = 0

    for i, url in enumerate(urls, start=1):
        country_id = country_id_from_url(url)
        log.info("[%d/%d] Fetching %s", i, len(urls), country_id)

        html = fetch_page(url)
        if html is None:
            results.append({"country_id": country_id, "source_url": url, "scrape_status": "FAILED"})
            time.sleep(REQUEST_DELAY_SECONDS)
            continue

        # Save raw HTML for debugging per the project's Module 1 spec.
        (DEBUG_HTML_DIR / f"{country_id}.html").write_text(html, encoding="utf-8")

        metrics = extract_metrics(html)
        metrics["country_id"] = country_id
        metrics["source_url"] = url
        metrics["scrape_status"] = "OK"
        results.append(metrics)
        success_count += 1

        time.sleep(REQUEST_DELAY_SECONDS)

    success_rate = (success_count / len(urls)) * 100 if urls else 0
    log.info("Done. %d/%d succeeded (%.1f%%)", success_count, len(urls), success_rate)
    if success_rate < 95:
        log.warning("Success rate is below the 95%% target set in the project spec.")

    return results


def write_csv(rows: list[dict], path: str) -> None:
    if not rows:
        log.warning("No rows to write.")
        return

    # Union of all keys across rows, with a sensible, stable column order.
    preferred_order = [
        "country_id", "power_index_rank", "countries_considered",
        "power_index_score", "total_population", "active_personnel",
        "reserve_personnel", "total_aircraft", "total_tanks",
        "total_navy_assets", "defense_budget_usd",
        "purchasing_power_parity_usd", "square_land_area_km",
        "scrape_status", "source_url",
    ]
    all_keys = set().union(*(r.keys() for r in rows))
    fieldnames = [k for k in preferred_order if k in all_keys]
    fieldnames += [k for k in all_keys if k not in fieldnames]

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    log.info("Wrote %d rows to %s", len(rows), path)


def main():
    urls = load_urls(INPUT_URL_FILE)
    rows = scrape_all(urls)
    write_csv(rows, OUTPUT_CSV)


if __name__ == "__main__":
    main()
