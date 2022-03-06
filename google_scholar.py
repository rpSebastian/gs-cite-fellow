#!/usr/bin/env python

"""
    google_scholar: This module contains the GoogleScholarUser class that
    is used to scrape the articles available in google scholar of a
    certain user.
"""

from __future__ import print_function
import time
import requests
from bs4 import BeautifulSoup


class GoogleScholarUser():
    """
        This class scrapes the articles of a certain user on google scholar,
        organises the articles in possible categories and makes them available
        under the variable publications.
    """
    start_page = 0
    end_page = 100
    base_url = "https://scholar.google.co.in/citations?"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
    }
    payload = {
        'json': 1
    }
    session = requests.Session()

    def __init__(self, user_id):
        """
            Initialize the necessary variables.

            Definitions:
            - user_id: User ID of the user to scrape
            - url: URL used to for post/get requests
            - articles: Raw scrape data
            - response: Response object after get/post request
        """
        self.user_id = user_id
        self.url = self.base_url + 'user=' + self.user_id
        self.articles = None
        self.response = None

    # Generate the URL based on page count
    def __frame_url(self):
        """
            Generate appropriate URL based on start and
            end pages to scrape.
        """
        self.url = self.base_url + 'user=' + self.user_id
        self.url += '&hl=en&oi=ao&cstart=' + str(self.start_page)
        self.url += '&pagesize=' + str(self.end_page)

    # This function fetches all google scholar articles
    def get_scholar_articles(self):
        """
            Populate the raw articles.
        """
        # Generate the URLs
        self.__frame_url()
        # Fetch the data
        self.response = self.session.post(self.url, headers=self.headers, data=self.payload)
        if not self.response.ok:
            raise Exception('Gone :/')

        # Sanitize the fetched data
        self.response = self.response.json()
        self.articles = BeautifulSoup(self.response['B'], 'html.parser')
        self.articles = self.articles.find_all('tr')

        # Google scholar return only 100 articles at most.
        # So we repeat the loop for every 100 articles
        while len(self.articles) == self.end_page:
            self.start_page += 100
            self.end_page += 100
            time.sleep(2)  # Make sure we don't query too many times

            self.__frame_url()
            self.response = self.session.post(self.url, headers=self.headers, data=self.payload)
            if not self.response.ok:
                raise Exception('Gone :/')

            self.response = self.response.json()
            current_fetch = BeautifulSoup(self.response['B'], 'html.parser')

            # Append the current articles to the past ones
            for article in current_fetch.find_all('tr'):
                self.articles.append(article)
                