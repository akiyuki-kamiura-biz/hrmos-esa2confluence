import re
import os
import glob
import json
import requests
from model.esa_post import EsaPost
from requests.auth import HTTPBasicAuth

from api_keys import CONFLUENCE_API_KEY, CONFLUENCE_API_USER


CONFLUENCE_API_CREATE_POST_URL = "https://bizreach.atlassian.net/wiki/rest/api/content"
CONFLUENCE_SPACE_KEY = "hrmosesaexport"
EXPORT_ROOT_DIRECTORY = "esa_posts"


def create_title(path):
    if path.endswith(".json"):
        path = path[:-5]

    parent_dirs = path.split("/")[1:-1]
    dir_name = path.split("/")[-1]
    title = dir_name
    if len(parent_dirs) != 0:
        title += " (in " + "/".join(parent_dirs) + ")"

    return title


def create_post(payload):
    res = requests.post(
        CONFLUENCE_API_CREATE_POST_URL,
        json=payload,
        auth=HTTPBasicAuth(CONFLUENCE_API_USER, CONFLUENCE_API_KEY)
    )

    if res.status_code == 200:
        return res.json().get('id', None)
    else:
        raise RuntimeError("Confluence api returns error. code: {}, message: {}".format(res.status_code, res.json()))


def reshape_html(html_text):
    print("html_text: {}".format(html_text))

    # NOTE: confluenceは「htmlのタグは必ず閉じろ」という仕様みたいなので置換対応
    close_tags = ["img", "br", "input", "hr"]
    for tag in close_tags:
        html_text = re.sub("<({}.*?)>".format(tag), r"<\1 />", html_text)

    # TODO: confluence側のコードを見やすくするための加工

    # TODO: confluence側でcheckboxがなくなってしまう問題への対応

    # TODO: confluence側で記事が横方向で真ん中に寄る場合と左による場合の差がわからないので調査して対応

    return html_text


def dfs_file_node(path, parent_id):
    file_text = open(path, 'r')
    esa_post_json = json.load(file_text)
    esa_post = EsaPost(esa_post_json)

    content_html = "<p>esa記事から作成：<a href=\"{}\">{}</a>.</p><br /><br />\n{}".format(
        esa_post.url,
        esa_post.url,
        reshape_html(esa_post.body_html)
    )

    payload = {
        "title": create_title(path),
        "type": "page",
        "space": {"key": CONFLUENCE_SPACE_KEY},
        "status": "current",
        "body": {
            "styled_view": {
                "value": content_html,
                "representation": "storage"
            }
        }
    }
    if parent_id is not None:
        payload["ancestors"] = [{"id": parent_id}]
    page_id = create_post(payload)

    print("created file page. path: {}".format(path))


def dfs_dir_node(path, parent_id):
    payload = {
        "title": create_title(path),
        "type": "page",
        "space": {"key": CONFLUENCE_SPACE_KEY},
        "status": "current",
        "body": {
            "storage": {
                "value": "",
                "representation": "storage"
            }
        }
    }
    if parent_id is not None:
        payload["ancestors"] = [{"id": parent_id}]

    page_id = create_post(payload)
    print("created dir page. path: {}, id: {}".format(path, page_id))
    dfs_tree(path, page_id)


def dfs_tree(path, parent_id=None):
    file_paths = glob.glob(path + "/*")

    for fpath in file_paths:
        if os.path.isfile(fpath):
            dfs_file_node(fpath, parent_id)
        elif os.path.isdir(fpath):
            dfs_dir_node(fpath, parent_id)


if __name__ == '__main__':
    dfs_tree(EXPORT_ROOT_DIRECTORY)