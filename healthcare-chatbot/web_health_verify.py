"""
Web Health Verification Module
Cross-references medical information from trusted web sources
before presenting to the user.
"""
import requests
import re
import streamlit as st

# Map internal disease names to better search terms
SEARCH_NAME_MAP = {
    "Drug Reaction": "Adverse drug reaction",
    "GERD": "Gastroesophageal reflux disease",
    "(vertigo) Paroymsal  Positional Vertigo": "Benign paroxysmal positional vertigo",
    "Dimorphic hemmorhoids(piles)": "Hemorrhoids",
    "Peptic ulcer diseae": "Peptic ulcer disease",
    "Osteoarthristis": "Osteoarthritis",
    "hepatitis A": "Hepatitis A",
    "Diabetes ": "Diabetes mellitus",
    "Hypertension ": "Hypertension",
    "Chicken pox": "Chickenpox",
    "Paralysis (brain hemorrhage)": "Intracerebral hemorrhage",
    "Bronchial Asthma": "Asthma",
}


def _clean_name(disease_name):
    """Get a clean search-friendly disease name."""
    return SEARCH_NAME_MAP.get(disease_name, disease_name.strip())


def search_wikipedia(disease_name):
    """Get disease summary from Wikipedia REST API."""
    clean = _clean_name(disease_name)
    url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + requests.utils.quote(clean)
    try:
        resp = requests.get(url, timeout=6, headers={"User-Agent": "HealthChatBot/1.0"})
        if resp.status_code == 200:
            data = resp.json()
            extract = data.get("extract", "")
            if extract and len(extract) > 60:
                page_url = data.get("content_urls", {}).get("desktop", {}).get("page", "")
                return {
                    "source": "Wikipedia",
                    "snippet": extract[:500],
                    "url": page_url,
                }
    except Exception:
        pass
    return None


def search_duckduckgo(query):
    """Use DuckDuckGo Instant Answer API for health info."""
    url = "https://api.duckduckgo.com/"
    params = {"q": query, "format": "json", "no_html": 1, "skip_disambig": 1}
    try:
        resp = requests.get(url, params=params, timeout=6, headers={"User-Agent": "HealthChatBot/1.0"})
        if resp.status_code == 200:
            data = resp.json()
            results = []
            if data.get("Abstract"):
                results.append({
                    "source": data.get("AbstractSource", "Web"),
                    "snippet": data["Abstract"][:500],
                    "url": data.get("AbstractURL", ""),
                })
            for topic in data.get("RelatedTopics", [])[:3]:
                if isinstance(topic, dict) and "Text" in topic:
                    results.append({
                        "source": "DuckDuckGo",
                        "snippet": topic["Text"][:300],
                        "url": topic.get("FirstURL", ""),
                    })
            return results
    except Exception:
        pass
    return []


@st.cache_data(ttl=3600, show_spinner=False)
def search_health_info(disease_name):
    """
    Cross-reference disease info across web sources.
    Returns list of dicts with source, snippet, url.
    """
    results = []
    clean = _clean_name(disease_name)

    # 1. Wikipedia
    wiki = search_wikipedia(disease_name)
    if wiki:
        results.append(wiki)

    # 2. DuckDuckGo - home remedies
    ddg = search_duckduckgo(f"{clean} home remedies precautions")
    results.extend(ddg)

    # 3. DuckDuckGo - treatment
    ddg2 = search_duckduckgo(f"{clean} treatment prevention")
    for item in ddg2:
        # Avoid duplicates
        if not any(item["snippet"][:80] == r["snippet"][:80] for r in results):
            results.append(item)

    return results
