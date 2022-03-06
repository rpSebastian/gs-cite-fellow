import sys
from utils import save_json, load_json
from pathlib import Path


def main():
    parallel_count = int(sys.argv[1])

    articles = load_json("data/articles.json")

    for article_id, article in enumerate(articles):
        parallel_id = article_id % parallel_count
        new_path = Path("data/articles_id_{}.json".format(parallel_id))
        print(new_path)
        if new_path.exists():
            new_article = load_json(new_path)[article_id]
            articles[article_id] = new_article
    save_json(articles, "result/articles.json")


if __name__ == "__main__":
    main()
