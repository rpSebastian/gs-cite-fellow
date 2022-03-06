import pandas as pd
from utils import load_txt, load_json
from collections import defaultdict


def main():
    articles = load_json("result/articles.json")
    ieee_fellow = load_txt("fellow/IEEE fellow list_v2.txt")
    acm_fellow = load_txt("fellow/ACM fellow list_v2.txt")
    aaai_fellow = load_txt("fellow/AAAI fellow list_v2.txt")
    iapr_fellow = load_txt("fellow/IAPR fellow list_v2.txt")

    fellow_dict = {
        "IEEE": ieee_fellow,
        "ACM": acm_fellow,
        "AAAI": aaai_fellow,
        "IAPR": iapr_fellow,
    }

    df = pd.DataFrame(
        columns=["article", "cite_article", "fellow", "fellow_conference"]
    )
    fellow_result = defaultdict(set)
    my_articles = [a["name"] for a in articles]
    for article_id, article in enumerate(articles):
        if "cite_list" not in article:
            continue
        article_title = article["name"]
        cite_articles = article["cite_list"]
        for cite_article in cite_articles:
            if not "author" in cite_article:
                continue
            authors = cite_article["author"]
            cite_article_title = cite_article["title"]
            for author in authors:
                conference_list = []
                for conference, fellow in fellow_dict.items():
                    if author in fellow:
                        conference_list.append(conference)
                        fellow_result[author].add(conference)
                if len(conference_list) == 0:
                    continue
                if cite_article_title in my_articles:
                    continue
                conference_list.sort()
                df.loc[df.shape[0]] = {
                    "article": article_title,
                    "cite_article": cite_article_title,
                    "fellow": author,
                    "fellow_conference": " ".join(conference_list),
                }

    writer = pd.ExcelWriter("result/result.xls")
    df.to_excel(
        writer,
        columns=["article", "cite_article", "fellow", "fellow_conference"],
        index=False,
        encoding="utf-8",
        sheet_name="Sheet1",
    )
    writer.save()

    df = pd.DataFrame(columns=["author", "conference"])
    for author, conference_set in fellow_result.items():
        conference_list = list(conference_set)
        conference_list.sort()
        df.loc[df.shape[0]] = {
            "author": author,
            "conference": " ".join(conference_list),
        }
    writer = pd.ExcelWriter("result/fellow.xls")
    df.to_excel(writer, index=False, encoding="utf-8", sheet_name="Sheet1")
    writer.save()


if __name__ == "__main__":
    main()
