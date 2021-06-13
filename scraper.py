import argparse
from bs4 import BeautifulSoup
from itertools import zip_longest
import requests
import re
import sys
from typing import List
from queue import Queue

from post import Post
from database import Database


class PostParser:

    __BASE_URL = 'https://news.ycombinator.com/'

    @classmethod
    def fetch_posts(cls, pages=5) -> List[Post]:
        posts = []
        for page in range(1, pages+1):
            print(f'Fetching page {page}...')
            url = f'{cls.__BASE_URL}?p={page}'
            response = requests.get(url)
            page_posts = cls.parse(response.text)
            posts.extend(page_posts)

        return posts

    @classmethod
    def parse(cls, data: str) -> List[Post]:
        soup = BeautifulSoup(data, features='html.parser')

        # Rank, title and website is on first row.
        ranks = soup.find_all('span', class_='rank')
        titles = soup.find_all('a', class_='storylink')
        websites = soup.find_all('span', class_='sitestr')

        # The rest are on second row and under subtext.
        # This extra division into subtext is required because the comments
        # are not tagged, so we use indices to find them.
        subtext = soup.find_all('td', class_='subtext')

        scores = []
        users = []
        ages = []
        comments = []

        for section in subtext:
            scores.append(section.find('span', class_='score'))
            users.append(section.find('a', class_='hnuser'))
            ages.append(section.find('span', class_='age'))
            comments.append(list(section)[-2])

        attributes = zip_longest(ranks, titles, websites, scores, users, ages, comments)
        posts = cls._create_posts(attributes)

        return posts

    @classmethod
    def _parse_age(cls, post):
        """ Parses the age into minutes. """
        age = int(post.age.split(' ')[0])

        if 'hours' in post.age:
            age *= 60
        else:
            age *= 60 * 24

        post.age = age

    @classmethod
    def _parse_score(cls, post):
        try:
            post.score = int(post.score.split(' ')[0])
        except:
            post.score = 0

    @classmethod
    def _create_posts(cls, attributes):
        posts = []
        for attr in attributes:
            posts.append(cls._create_post(attr))
        return posts

    @classmethod
    def _create_post(cls, attribute):
        rank, title, site, score, user, age, comment = attribute
        post = Post(rank=rank.text[:-1])
        cls._add_attribute(post, 'title', title)
        cls._add_attribute(post, 'site', site)
        cls._add_attribute(post, 'score', score)
        cls._add_attribute(post, 'user', user)
        cls._add_attribute(post, 'age', age)
        cls._add_attribute(post, 'comment', comment)
        cls._parse_age(post)
        cls._parse_score(post)
        return post

    @classmethod
    def _add_attribute(cls, post, attribute_name, attribute):
        if hasattr(attribute, 'text'):
            setattr(post, attribute_name, attribute.text)


def argparser():
    parser = argparse.ArgumentParser('Simple data fetcher from Hacker News.')
    parser.add_argument('-p', '--pages', type=int, help='Amount of pages to fetch data from.',
                        default=3, required=False)
    parser.add_argument('-s', '--save', help='Flag if you want to save to database or not.',
                        default=False, action='store_true', required=False)
    return parser.parse_args()



if __name__ == '__main__':
    args = argparser()

    posts = PostParser.fetch_posts(pages=args.pages)
    print('Done fetching data.')

    if args.save:
        with Database() as db:
            db.save(posts)
        print('Saved to database.')
    else:
        print('Not posts saving to database.')