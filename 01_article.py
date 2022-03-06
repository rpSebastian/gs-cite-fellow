from utils import save_json, load_json
import json
from google_scholar import GoogleScholarUser


def fetch():
    config = load_json("config.json")
    user_id = config["scholar_id"]
    scraper = GoogleScholarUser(user_id)
    scraper.get_scholar_articles()
    articles = scraper.articles

    article_infos = []
    for article_id, article in enumerate(articles):
        info = {
            "article_id": article_id,
            "name": article.find_all('a')[0].text,
            "cite_url": article.find_all('a')[1]['href']
        }
        article_infos.append(info)
    save_json(article_infos, "data/articles.json")


if __name__ == '__main__':
    fetch()

