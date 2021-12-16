# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import os
import requests
from model.esa_post import EsaPost

from api_keys import ESA_API_ACCESS_TOKEN

ESA_API_LIST_POSTS_URL = "http://api.esa.io/v1/teams/hrmos/posts"
MAX_PAGE = 10 # TODO: 75に戻す
POSTS_PER_PAGE = 100 # TODO: 100に戻す

EXPORT_ROOT_DIRECTORY = "esa_posts"


def download_esa_posts_per_page(page):
    print("* start to fetch page: {}".format(page))

    headers = {'Authorization': 'Bearer {}'.format(ESA_API_ACCESS_TOKEN)}
    url = ESA_API_LIST_POSTS_URL + "?include=comments&q=-category:confluence_export&per_page={}&page={}".format(POSTS_PER_PAGE, page)
    res = requests.get(url, headers=headers)

    if res.status_code == 200:
        json_dict = res.json()
        next_page = json_dict.get('next_page', None)
        posts = [EsaPost(post) for post in json_dict['posts']]
        print("  -> fetched {} posts from page: {}".format(len(posts), page))
        return (next_page, posts)
    else:
        raise RuntimeError("esa api returns error")


def make_root_dir():
    if not os.path.exists(EXPORT_ROOT_DIRECTORY):
        os.makedirs(EXPORT_ROOT_DIRECTORY)


if __name__ == '__main__':
    posts = []
    current_page = 1

    while current_page <= MAX_PAGE:
        next_page, posts_per_page = download_esa_posts_per_page(current_page)
        posts.extend(posts_per_page)
        if next_page is None: break
        current_page = next_page

    print("***** result: {} posts got".format(len(posts)))

    for post in posts:
        post.save_json(EXPORT_ROOT_DIRECTORY)

    print("***** result: {} posts successfully saved".format(len(posts)))