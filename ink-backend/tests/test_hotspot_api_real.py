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

def test_real_get_hotspot_content():
    # First, get a valid hotspot URL from the hotspots list
    get_resp = requests.get(f"{BASE_URL}/api/hotspots")
    assert get_resp.status_code == 200
    hotspots = get_resp.json().get("hotspots", [])
    assert len(hotspots) > 0, "无法获取用于测试的热点列表。"

    # Find a hotspot with a valid URL
    test_url = None
    for spot in hotspots:
        if spot.get("url") and spot["url"].startswith("http"):
            test_url = spot["url"]
            break
    
    assert test_url is not None, "在热点列表中未找到可用的URL进行测试。"

    print(f"正在测试内容获取 API, URL: {test_url}")
    
    # Now test the content endpoint
    content_url = f"{BASE_URL}/api/hotspots/content"
    resp = requests.post(content_url, json={"url": test_url})
    
    print("/api/hotspots/content 状态码:", resp.status_code)
    print("返回:", resp.json())
    response_json = resp.json()
    if "content" in response_json:
        print("返回内容长度:", len(response_json.get("content", "")))
    else:
        print("返回:", response_json)
        
    assert resp.status_code == 200
    assert "content" in response_json

if __name__ == "__main__":
    test_real_get_hotspots()
    test_real_analyze_hotspots()
    test_real_get_hotspot_content() 