from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup
from googlesearch import search
from janome.tokenizer import Tokenizer

app = FastAPI()

# CORS許可（フロントから叩けるように）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_weblio_meaning(word: str):
    url = f"https://www.weblio.jp/content/{word}"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    tag = soup.find("div", {"class": "kiji"})
    return tag.get_text(strip=True) if tag else None

def tokenize(text: str):
    t = Tokenizer()
    return [tok.surface for tok in t.tokenize(text) if tok.surface.strip()]

@app.get("/")
def home():
    return {"msg": "検索アプリへようこそ"}

@app.get("/search")
def search_query(query: str):
    # Google検索（1件だけ）
    urls = list(search(query, num_results=1, lang="ja"))
    answer = "富士山"  # TODO: 本当は結果から抽出する処理を追加

    # 入力文の語彙意味
    words = tokenize(query)
    meanings = {w: get_weblio_meaning(w) for w in words}

    # 答えの意味
    answer_meaning = get_weblio_meaning(answer)

    # Google画像検索URL
    image_url = f"https://www.google.com/search?tbm=isch&q={answer}"

    return {
        "answer": answer,
        "meanings": meanings,
        "answer_meaning": answer_meaning,
        "image_url": image_url,
        "source_url": urls[0] if urls else None
    }