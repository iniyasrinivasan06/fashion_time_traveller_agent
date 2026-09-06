"""
tools.py
Defines the 3 tools used by the Fashion Trend Time-Traveler agent:
1. scrape_fashion_history   - finds a garment's origin era via web search
2. cycle_pattern_analyzer   - counts decade mentions in scraped text
3. celebrity_adoption_tracker - finds when celebrities revived the style
"""

import re
from collections import Counter
from ddgs import DDGS
from langchain_core.tools import tool


@tool
def scrape_fashion_history(garment: str) -> str:
    """
    Searches the web for the historical origin and era of a clothing item
    or fashion trend. Use this when you need to find out which decade a
    garment (e.g. 'oversized blazer', 'mom jeans', 'chunky sneakers')
    originally comes from or was revived in.
    Input should be a short garment or style name.
    """
    query = f"{garment} fashion history decade trend origin"
    results = DDGS().text(query, max_results=5)

    if not results:
        return f"No results found for '{garment}'."

    snippets = [r["body"] for r in results if r.get("body")]
    return "\n\n".join(snippets)


@tool
def cycle_pattern_analyzer(scraped_text: str) -> str:
    """
    Analyzes scraped fashion history text and counts mentions of each decade
    (e.g. 1980s, 1990s, 2000s) to determine which era(s) a garment is most
    associated with. Use this AFTER scrape_fashion_history, passing in the
    text it returned, to figure out the dominant decade(s).
    """
    pattern = r"(19[0-9]0s|20[0-9]0s|'\d0s)"
    matches = re.findall(pattern, scraped_text)

    if not matches:
        return "No clear decade mentions found in the text."

    # Normalize shorthand like '90s -> 1990s
    normalized = []
    for m in matches:
        if m.startswith("'"):
            digit = m[1]
            decade = f"19{digit}0s" if int(digit) >= 3 else f"20{digit}0s"
            normalized.append(decade)
        else:
            normalized.append(m)

    counts = Counter(normalized)
    total = sum(counts.values())

    result_lines = [
        f"{decade}: {count} mentions ({round((count / total) * 100)}%)"
        for decade, count in counts.most_common()
    ]
    return "\n".join(result_lines)


@tool
def celebrity_adoption_tracker(garment: str) -> str:
    """
    Searches the web for celebrities or public figures who wore a specific
    garment or fashion style, and extracts the years they were seen wearing it.
    Use this to pinpoint WHEN a style was revived/popularized in modern times,
    as opposed to when it originally existed.
    Input should be a short garment or style name.
    """
    query = f"{garment} celebrity wore street style year"
    results = DDGS().text(query, max_results=5)

    if not results:
        return f"No celebrity adoption data found for '{garment}'."

    combined_text = "\n\n".join(r["body"] for r in results if r.get("body"))

    # Strip publish-date patterns like "Mar 19, 2024 ·" before extracting years,
    # so article publish dates aren't mistaken for fashion-relevant years
    publish_date_pattern = r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+\d{1,2},\s+\d{4}\s*·"
    cleaned_text = re.sub(publish_date_pattern, "", combined_text)

    year_pattern = r"\b(19[5-9]\d|20[0-2]\d)\b"
    years_found = re.findall(year_pattern, cleaned_text)

    if not years_found:
        return f"Raw findings (no specific years detected):\n{combined_text}"

    year_counts = Counter(years_found)
    year_summary = ", ".join(
        f"{year} ({count}x)" for year, count in sorted(year_counts.items())
    )
    return f"Years mentioned: {year_summary}\n\nContext:\n{combined_text}"