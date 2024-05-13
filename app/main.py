import logging
import re
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, HttpUrl

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

app = FastAPI(
    title="Word Counter",
    description="Word Counter - Counts how many times a word exists in a webpage source.",
    version="0.0.1",
)

class KeywordRequest(BaseModel):
    keyword: str
    url: HttpUrl

class KeywordResponse(BaseModel):
    keyword: str
    url: HttpUrl
    count: int

word_counts = []

def fetch_webpage_content(url: str) -> str:
    """Access and validate the url provided"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except:
        logging.error(f"Failed to fetch webpage content from {url}")
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Failed to fetch webpage content from {url}")
        
def count_word_occurrences(text: str, word: str) -> int:
    """Count the given keyword on a webpage"""
    soup = BeautifulSoup(text, 'html.parser')
    text = soup.get_text()
    occurences = len(re.findall(rf"\b{word}\b", text, re.IGNORECASE))
    return occurences


@app.get("/word-count", tags=["Word Count"])
def get_word_count():
    """Return a list of all counted words"""

    logging.info("Retrieving word counts...")
    return word_counts

@app.post("/word-count", tags=["Word Count"])
def post_word_count(data: KeywordRequest) -> KeywordResponse:
    """Get the occurences of the keyword on a webpage and append it on word_counts dictionary"""
    logging.info("Processing keyword request...")
    keyword = data.keyword
    url = data.url

    response = fetch_webpage_content(url)

    logging.info(f"Searching for keyword '{keyword}'...")
    occurences = count_word_occurrences(response, keyword)

    result = KeywordResponse(
        keyword=data.keyword,
        url=url,
        count=occurences
    )

    logging.info(f"Keyword '{keyword}' found {occurences} times.")
    
    word_counts.append(result)

    return result