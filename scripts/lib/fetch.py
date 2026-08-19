'''

# Note.ms Fetch

A library designed to use Note.ms efficiently and elegantly.

Designed and Tested by @politetrex.

'''
from curl_cffi import requests
import random

def normalize(article: str) -> str:
    if (article[-3:]=='.md'):
        # remove .md suffix to plain text
        article=article[:-3]
    if (article[-4:]=='.txt'):
        # remove .txt suffix to plain text
        article=article[:-4]
    return article

import random

def randomImpersonate():
    """返回当前 curl_cffi 版本真正支持的浏览器指纹和对应的 User-Agent"""
    browsers = [
        # Chrome 系列 (11个)
        ("chrome99", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"),
        ("chrome100", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36"),
        ("chrome101", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36"),
        ("chrome104", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36"),
        ("chrome107", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.87 Safari/537.36"),
        ("chrome110", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.77 Safari/537.36"),
        ("chrome116", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.96 Safari/537.36"),
        ("chrome119", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.123 Safari/537.36"),
        ("chrome120", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.109 Safari/537.36"),
        ("chrome123", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.58 Safari/537.36"),
        ("chrome124", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.60 Safari/537.36"),
        # Edge 系列 (2个)
        ("edge99", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.36"),
        ("edge101", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36 Edg/101.0.1210.32"),
        # Safari 系列 (3个)
        ("safari15_3", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Safari/605.1.15"),
        ("safari15_5", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15"),
        ("safari17_0", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"),
        # Firefox 系列 (1个)
        ("firefox133", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0"),
    ]
    return random.choice(browsers)

def get_session():
    # 可以在这里维护一个会话，以保持 Cookie 等状态
    return requests.Session()

def fetchContent(article: str) -> str:
    article = normalize(article)
    url = f"https://note.ms/{article}"
    try:
        browser, user_agent = randomImpersonate()
        response = requests.get(url, impersonate=browser)
        html = response.text
        
        # 找到 <textarea> 的起始和结束位置
        start = html.find('<textarea class="content">') + len('<textarea class="content">')
        end = html.find('</textarea>', start)
        
        if start != -1 and end != -1:
            return html[start:end]
        else:
            return "Error: Content not found in page"
            
    except Exception as e:
        return f"Error fetching content: {e}"
    
def writeContent(article: str, content: str) -> bool:
    article = normalize(article)
    url = f"https://note.ms/{article}"
    try:
        # 1. 使用 Session 维持 Cookie
        session = requests.Session()
        
        # 2. 先 GET 一次页面，获取必要的 Cookie 和 Cloudflare 验证
        browser, user_agent = randomImpersonate()
        session.get(url, impersonate=browser)
        
        # 3. 构造与浏览器 AJAX 请求完全一致的头部
        headers = {
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Referer": url,
            "Origin": "https://note.ms",
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }
        
        # 4. 发送 POST 请求，数据格式为 "t=内容"
        response = session.post(
            url,
            data={"t": content},
            headers=headers,
            impersonate=browser  # 保持 TLS 指纹伪装
        )
        
        # 5. 调试信息：打印请求和响应的关键部分
        print("POST Status:", response.status_code)
        print("POST Response Preview:", response.text[:210])
        
        return response.status_code == 200
    except Exception as e:
        print("Exception:", e)
        return False

if __name__=="__main__":
    # Testing
    print(writeContent(input(), "0Hz_Test"))