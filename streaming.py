import requests
from bs4 import BeautifulSoup

def check_live_status(link):
    """检查直播状态"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Referer': 'https://play.sooplive.co.kr/'
        }

        # 获取主页面
        response = requests.get(link, headers=headers, timeout=5)
        print(f"Initial response status: {response.status_code}")
        print(f"Response URL: {response.url}")
        
        if response.status_code == 200:
            # 检查响应URL是否包含"null"
            if "null" in response.url:
                print("Stream appears to be offline (URL contains 'null')")
                return "Offline"
            
            # 检查响应URL是否包含数字
            if any(char.isdigit() for char in response.url.split('/')[-1]):
                print("Stream appears to be online (URL contains digits)")
                return "Online"
            
            print(f"Default to offline - no positive indicators found")
            return "Offline"
            
    except Exception as e:
        print(f"Error checking status: {str(e)}")
        return "Error"