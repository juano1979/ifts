import requests


def test_httpbin_get():
    resp = requests.get("https://httpbin.org/get", timeout=10)
    assert resp.status_code == 200
    data = resp.json()
    assert "url" in data
