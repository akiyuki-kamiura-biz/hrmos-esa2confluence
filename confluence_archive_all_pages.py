import requests
import tqdm
from requests.auth import HTTPBasicAuth

from api_keys import CONFLUENCE_API_KEY, CONFLUENCE_API_USER

CONFLUENCE_SPACE_KEY = "hrmosesaexport"

if __name__ == '__main__':
    get_url = "https://bizreach.atlassian.net/wiki/rest/api/content?spaceKey={}&limit=10000".format(CONFLUENCE_SPACE_KEY)
    res = requests.request(
        "GET",
        get_url,
        headers={
            "Accept": "application/json"
        },
        auth=HTTPBasicAuth(CONFLUENCE_API_USER, CONFLUENCE_API_KEY)
    )

    results = res.json().get("results", [])
    content_ids = [int(page.get("id", None)) for page in results]

    print("page ids in space: {}".format(content_ids))

    for page_id in tqdm.tqdm(content_ids):
        delete_url = "https://bizreach.atlassian.net/wiki/rest/api/content/{}".format(page_id)
        res = requests.request(
            "DELETE",
            delete_url,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            auth=HTTPBasicAuth(CONFLUENCE_API_USER, CONFLUENCE_API_KEY)
        )