import requests
import json
from requests.auth import HTTPBasicAuth

from api_keys import CONFLUENCE_API_KEY, CONFLUENCE_API_USER

CONFLUENCE_SPACE_KEY = "hrmosesaexport"

# if __name__ == '__main__':
#     url = "https://bizreach.atlassian.net/wiki/rest/api/content?spaceKey={}".format(CONFLUENCE_SPACE_KEY)
#
#     headers = {
#         "Accept": "application/json",
#         "Authorization": "Bearer {}".format(CONFLUENCE_API_KEY)
#     }
#
#     response = requests.request(
#         "GET",
#         url,
#         headers=headers,
#         auth = HTTPBasicAuth(CONFLUENCE_API_USER, CONFLUENCE_API_KEY)
#     )
#
#     print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))