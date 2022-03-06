from utils import load_json, save_json
from pathlib import Path
from bs4 import BeautifulSoup
import time
import requests
import sys

DBLP_BASE_URL = 'http://dblp.uni-trier.de/'
PUB_SEARCH_URL = DBLP_BASE_URL + "search/publ/"


def main():
    parallel_id = int(sys.argv[1])
    parallel_count = int(sys.argv[2])

    save_path = Path("data/articles_id_{}.json".format(parallel_id))
    if not save_path.exists():
        base_path = Path("data/articles.json")
    else:
        base_path = save_path
    articles = load_json(base_path)
    new_articles = articles.copy()

    for article_id, article in enumerate(articles):
        if article_id % parallel_count != parallel_id:
            continue
        if "cite_list" not in article:
            continue
        cite_articles = article["cite_list"]
        for cite_article_id, cite_article in enumerate(cite_articles):
            if "author" in cite_article:
                continue
            title = cite_article["title"]
            while True:
                try:
                    authors = query(title)
                    break
                except Exception as e:
                    print(e)
                    time.sleep(1)
            print("{}/{} {} {}".format(cite_article_id, len(cite_articles), title, " ".join(authors)))
            new_articles[article_id]["cite_list"][cite_article_id]["author"] = authors
            save_json(new_articles, save_path)


def query(title):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:26.0) Gecko/20100101 Firefox/26.0',
        'Cookie': 'GSP=CF=4'
    }
    resp = requests.get(PUB_SEARCH_URL, headers=headers, params={'q': [title]})
    time.sleep(1)
    d = BeautifulSoup(resp.content, "html.parser")
    # d = BeautifulSoup(open('D://b.html',encoding='utf-8'),features='html.parser')
    pub_list_raw = d.find(name="ul", attrs={"class": "publ-list"})
    authors = []
    for pub_data in pub_list_raw.children:
        if pub_data.attrs.get('class')[0] == 'year':
            continue
        author_items = pub_data.findAll(name="span", attrs={"itemprop": "author"})
        for author_item in author_items:
            authors.append(author_item.text)
        break
    return authors



if __name__ == "__main__":
    main()
