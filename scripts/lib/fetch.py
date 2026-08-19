'''

# Note.ms Fetch

A library designed to use Note.ms efficiently and elegantly.

Designed and Tested by @politetrex.

'''
from curl_cffi import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
}

def normalize(article: str) -> str:
    if (article[-3:]=='.md'):
        # remove .md suffix to plain text
        article=article[:-3]
    if (article[-4:]=='.txt'):
        # remove .txt suffix to plain text
        article=article[:-4]
    return article


def get_session():
    # 可以在这里维护一个会话，以保持 Cookie 等状态
    return requests.Session()

def fetchContent(article: str) -> str:
    article = normalize(article)
    url = f"https://note.ms/{article}"
    try:
        response = requests.get(url, impersonate="chrome")
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
        session.get(url, impersonate="chrome")
        
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
            impersonate="chrome"  # 保持 TLS 指纹伪装
        )
        
        # 5. 调试信息：打印请求和响应的关键部分
        print("POST Status:", response.status_code)
        print("POST Response Preview:", response.text[:200])
        
        return response.status_code == 200
    except Exception as e:
        print("Exception:", e)
        return False

if __name__=="__main__":
    # Testing
    print(writeContent(input(), "0Hz_Test"))