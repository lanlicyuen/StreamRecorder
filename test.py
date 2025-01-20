import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import json
from streaming import check_live_status

def find_stream_link(url):
    # 设置Chrome选项
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 无头模式
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
    # 启用日志记录以捕获网络请求
    caps = DesiredCapabilities.CHROME.copy()
    caps['goog:loggingPrefs'] = {'performance': 'ALL'}
    
    # 启动Chrome浏览器
    service = Service('path/to/chromedriver')  # 替换为chromedriver的实际路径
    driver = webdriver.Chrome(service=service, options=chrome_options, desired_capabilities=caps)
    
    # 打开目标URL
    driver.get(url)
    time.sleep(10)  # 等待页面加载
    
    # 获取网络日志
    logs = driver.get_log('performance')
    
    # 查找推流链接
    for log in logs:
        log_message = json.loads(log['message'])['message']
        if log_message['method'] == 'Network.responseReceived':
            url_fragment = log_message['params']['response']['url']
            if 'sooplive.co.kr' in url_fragment and 'auth_playlist' in url_fragment:
                driver.quit()
                return url_fragment
    
    driver.quit()
    return None

if __name__ == "__main__":
    url = "https://live.douyin.com/980254586490"
    status = check_live_status(url)
    print(f"Live status: {status}")