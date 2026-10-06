import pytest
import logging
from models import ArtObject, SearchResponse

BASE_URL_OBJECTS = "https://collectionapi.metmuseum.org/public/collection/v1"
BASE_URL_SEARCH = "https://collectionapi.metmuseum.org/public/collection/v1.1"

@pytest.mark.parametrize("object_id", [1, 10, 12345])
def test_get_object_by_id(base_url, session, object_id):
    url = f"{BASE_URL_OBJECTS}/objects/{object_id}"
    logging.info(f"GET {url}")
    r = session.get(url)
    logging.info(f"Status: {r.status_code}, Body: {r.text[:200]}")

    if r.status_code == 200:
        data = r.json()
        obj = ArtObject(**data)
        assert obj.objectID == object_id
        assert isinstance(obj.title, str) and len(obj.title) > 0
    elif r.status_code == 404:
        pass
    else:
        pytest.fail(f"Unexpected status: {r.status_code}")

def test_search_with_keyword(session):
    keyword = "gold"
    url = f"{BASE_URL_SEARCH}/search"
    params = {"q": keyword}
    logging.info(f"GET {url}?q={keyword}")
    r = session.get(url, params=params)
    logging.info(f"Status: {r.status_code}, Body: {r.text[:200]}")
    assert r.status_code == 200
    data = r.json()
    resp = SearchResponse(**data)
    assert resp.total >= 0
    assert len(resp.objectIDs) >= 0

def test_search_without_query(session):
    url = f"{BASE_URL_SEARCH}/search"
    logging.info(f"GET {url} (no query)")
    r = session.get(url)
    logging.info(f"Status: {r.status_code}, Body: {r.text[:200]}")
    # Для пустого запроса API может вернуть 400, если это ожидаемо
    assert r.status_code in (200, 400)

def test_pagination_limit(session):
    url = f"{BASE_URL_SEARCH}/search"
    params = {"q": "silver", "limit": 10}
    logging.info(f"GET {url} with limit=10")
    r = session.get(url, params=params)
    logging.info(f"Status: {r.status_code}, Body: {r.text[:200]}")
    assert r.status_code == 200
    data = r.json()
    resp = SearchResponse(**data)
    assert 0 <= len(resp.objectIDs) <= 10
