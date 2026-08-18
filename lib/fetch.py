'''

# Note.ms Fetch

A library designed to use Note.ms efficiently and elegantly.

'''
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
}

def normalize(article: str) -> str:
    if (article[-3:]=='.md'):
        # remove .md suffix to plain text
        article=article[:-3]
    return article


def fetchContent(article: str):
    '''
    Read content from a specific article.
    '''
    article = normalize(article)
    url = f"https://note.ms/{article}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error fetching content: {e}"

def writeContent(article: str, content: str):
    article = normalize(article)
    url = f"https://note.ms/{article}"
    try:
        response = requests.post(url, data={"content": content},  headers=headers)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        return False

if __name__=="__main__":
    # Testing
    print(fetchContent(input()))