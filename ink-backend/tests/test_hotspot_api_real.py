import requests

BASE_URL = "http://127.0.0.1:3000"

def test_real_get_hotspots():
    url = f"{BASE_URL}/api/hotspots"
    resp = requests.get(url)
    print("/api/hotspots 状态码:", resp.status_code)
    print("返回:", resp.json())
    assert resp.status_code == 200
    assert "hotspots" in resp.json()

def test_real_analyze_hotspots():
    url = f"{BASE_URL}/api/hotspots/analyze"
    resp = requests.post(url, json={})
    print("/api/hotspots/analyze 状态码:", resp.status_code)
    print("返回:", resp.json())
    assert resp.status_code == 200
    assert "report" in resp.json()

if __name__ == "__main__":
    test_real_get_hotspots()
    test_real_analyze_hotspots() 