import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import json
import sys
from utils import load_json, save_json


def main():
    start_article_id = int(sys.argv[1])
    d = open_browser()
    articles = load_json("data/articles.json")
    new_articles = articles.copy()
    for article_id, info in enumerate(articles):
        if article_id < start_article_id:
            continue
        base_url = info["cite_url"]
        name = info["name"]
        get_all_cite_name_list(d, base_url, name, article_id, new_articles)


def get_all_cite_name_list(d, base_url, name, article_id, new_articles):
    all_cite_name_list = []
    for start in range(0, 100000, 10):
        print("Page {}".format(start // 10))
        url = get_specify_url(base_url, start)
        enter_url(d, url)
        cite_name_list = get_cite_name_list(d)
        if len(cite_name_list) == 0:
            break
        all_cite_name_list.extend(cite_name_list)

        new_articles[article_id]["cite_list"] = []
        for cite_name in all_cite_name_list:
            new_articles[article_id]["cite_list"].append({"title": cite_name})
            print(cite_name)
        save_json(new_articles, "data/articles.json")


def open_browser():
    print("start openning browser")
    config = load_json("config.json")
    d = webdriver.Chrome(executable_path=config["driver_path"])
    d.set_window_size(1400, 800)
    print("finish openning browser")
    return d


def get_specify_url(base_url, start):
    url = base_url.replace("oi=bibs", "start={}".format(start))
    return url


def enter_url(d, url):
    print("start getting url", url)
    d.get(url)
    time.sleep(1)
    print("finish getting url", url)
    check_verification_code(d)


def check_verification_code(d):
    print("start checking_verification_code url")
    while True:
        find_code = False
        try:
            content = d.find_element(by=By.ID, value="gs_captcha_f")
            find_code = True
        except selenium.common.exceptions.NoSuchElementException as e:
            pass

        try:
            content = d.find_element(by=By.ID, value="recaptcha")
            find_code = True
        except selenium.common.exceptions.NoSuchElementException as e:
            pass

        if find_code:
            print("Plesse input verification_code")
            time.sleep(2)
        else:
            break
    print("finish checking_verification_code url")


def get_cite_name_list(d):
    text = d.find_element_by_xpath("//*").get_attribute("outerHTML")
    soup = BeautifulSoup(text, "html.parser")
    main_element = soup.find(name="div", attrs={"id": "gs_res_ccl_mid"})
    articles = main_element.find_all(name="div", attrs={"class": "gs_r"})
    cite_name_list = []
    for article in articles:
        name = article.find_all(name="h3", attrs={"class": "gs_rt"})[0].text
        cite_name_list.append(name)
    return cite_name_list


if __name__ == "__main__":
    main()
