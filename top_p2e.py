import requests
from bs4 import BeautifulSoup
import logging

log = logging.getLogger("top_p2e")

def fetch_top_p2e(limit=5):
    """
    Парсит playtoearn.net и возвращает список самых популярных P2E игр.
    """
    url = "https://playtoearn.net/blockchaingames"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
    except Exception as e:
        log.exception("Ошибка при загрузке TOP P2E: %s", e)
        return []

    soup = BeautifulSoup(r.text, "html.parser")

    # находим таблицу рейтинга
    items = soup.select(".game-item")
    if not items:
        log.warning("Не найдено ни одного .game-item")
        return []

    results = []
    for it in items[:limit]:
        title_el = it.select_one(".game-title")
        name = title_el.get_text(strip=True) if title_el else "Без названия"

        link_el = it.select_one("a")
        link = "https://playtoearn.net" + link_el["href"] if link_el and link_el.get("href") else "—"

        genre_el = it.select_one(".game-genre")
        genre = genre_el.get_text(strip=True) if genre_el else "—"

        # рейтинг — ищем число или звёзды
        rating_el = it.select_one(".game-ratings")
        rating = rating_el.get_text(strip=True) if rating_el else "—"

        results.append({
            "name": name,
            "genre": genre,
            "link": link,
            "rating": rating
        })

    return results
