from utils import load_json, save_json


def main():
    articles = load_json("data/articles.json")
    save_json(articles, "data/articles.bak.json")
    new_articles = articles.copy()
    for article_id, article in enumerate(articles):
        if "cite_list" not in article:
            continue
        cite_articles = article["cite_list"]
        for cite_article_id, cite_article in enumerate(cite_articles):
            title = cite_article["title"]
            clear_contents = [
                "[HTML][HTML] ",
                "[PDF][PDF] ",
                "[BOOK][B] ",
                "[CITATION][C] ",
                "[DOC][DOC] ",
                "[",
            ]
            for clear_content in clear_contents:
                title = title.replace(clear_content, "")
            new_articles[article_id]["cite_list"][cite_article_id]["title"] = title
    save_json(new_articles, "data/articles.json")


if __name__ == "__main__":
    main()
