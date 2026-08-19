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

def randomImpersonate() -> tuple[str,str]:
    # Randomly select a User-Agent string to impersonate different browsers
    user_agents = [
        ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36","Chrome"),
        ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15","Safari"),
        ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36","Chrome"),
        ("Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1","Safari"),
        ("Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1","Safari"),
        ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59","Edge"),
        ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0","Firefox"),
        ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36","Chrome")
    ]
    return random.choice(user_agents)

def get_session():
    # 可以在这里维护一个会话，以保持 Cookie 等状态
    return requests.Session()

def fetchContent(article: str) -> str:
    article = normalize(article)
    url = f"https://note.ms/{article}"
    try:
        user_agent, browser = randomImpersonate()
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
        user_agent, browser = randomImpersonate()
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