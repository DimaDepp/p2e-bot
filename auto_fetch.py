import requests
from bs4 import BeautifulSoup
import logging

log = logging.getLogger("auto_fetch")

def fetch_new_p2e(limit=5):
    """
    Парсит playtoearn.net и возвращает список новых P2E игр.
    """
    url = "https://playtoearn.net/blockchaingames"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
    except Exception as e:
        log.exception("Ошибка при загрузке P2E-данных: %s", e)
        return []

    soup = BeautifulSoup(r.text, "html.parser")

    # актуальные селекторы по состоянию на 2025 год
    items = soup.select(".game-card")[:limit]
    results = []

    for it in items:
        title_el = it.select_one(".game-card__title")
        name = title_el.get_text(strip=True) if title_el else "Без названия"

        link_el = it.select_one("a")
        link = "https://playtoearn.net" + link_el["href"] if link_el and link_el.get("href") else "—"

        genre_el = it.select_one(".game-card__category")
        genre = genre_el.get_text(strip=True) if genre_el else "—"

        results.append({
            "name": name,
            "genre": genre,
            "link": link
        })

    return results
