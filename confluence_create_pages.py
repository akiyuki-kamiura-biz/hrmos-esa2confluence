import re
import os
import glob
import json
import html
import markdown
import requests
from model.esa_post import EsaPost
from requests.auth import HTTPBasicAuth

from api_keys import CONFLUENCE_API_KEY, CONFLUENCE_API_USER


CONFLUENCE_API_CREATE_POST_URL = "https://bizreach.atlassian.net/wiki/rest/api/content"
CONFLUENCE_SPACE_KEY = "hrmosesaexport"
EXPORT_ROOT_DIRECTORY = "esa_posts"

failed_paths = []

def create_title(path):
    if path.endswith(".json"):
        path = path[:-5]

    parent_dirs = path.split("/")[1:-1]
    dir_name = path.split("/")[-1]
    title = dir_name
    if len(parent_dirs) != 0:
        title += " (in " + "/".join(parent_dirs) + ")"

    return title


def create_post(payload, path):
    res = requests.post(
        CONFLUENCE_API_CREATE_POST_URL,
        json=payload,
        auth=HTTPBasicAuth(CONFLUENCE_API_USER, CONFLUENCE_API_KEY)
    )

    if res.status_code == 200:
        return res.json().get('id', None)
    else:
        failed_paths.append(path)
        print("Confluence api returns error. path: {}, code: {}, message: {}".format(path, res.status_code, res.json()))

def create_html_from_markdown(markdown_text):
    html_escaped = html.escape(markdown_text)

    md = markdown.Markdown()
    converted = md.convert(html_escaped)

    close_tags = ["img", "input"]
    for tag in close_tags:
        converted = re.sub("<({}.*?)>".format(tag), r"<\1 />", converted)

    return converted


def dfs_file_node(path, parent_id):
    file_text = open(path, 'r')
    esa_post_json = json.load(file_text)
    esa_post = EsaPost(esa_post_json)

    content_html = "<p>esa記事から作成：<a href=\"{}\">{}</a>.</p><br />\n{}".format(
        esa_post.url,
        esa_post.url,
        create_html_from_markdown(esa_post.body_md)
    )

    payload = {
        "title": create_title(path),
        "type": "page",
        "space": {"key": CONFLUENCE_SPACE_KEY},
        "status": "current",
        "body": {
            "storage": {
                "value": content_html,
                "representation": "storage"
            }
        }
    }
    if parent_id is not None:
        payload["ancestors"] = [{"id": parent_id}]

    page_id = create_post(payload, path)
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

    page_id = create_post(payload, path)
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
    failed_paths = []
    dfs_tree(EXPORT_ROOT_DIRECTORY)

    print("=============")
    print("failed count: {}".format(len(failed_paths)))
    print("failed files: {}".format(", ".join(failed_paths)))