import os
import requests

BITBUCKET_API_URL = "https://api.bitbucket.org/2.0"
WORKSPACE = os.environ["BITBUCKET_WORKSPACE"]
REPO_SLUG = os.environ["BITBUCKET_REPO_SLUG"]
PR_ID = os.environ["BITBUCKET_PR_ID"]
USERNAME = os.environ["BB_USERNAME"]
APP_PASSWORD = os.environ["BB_APP_PASSWORD"]

def post_comment(filename, line, message):
    url = f"{BITBUCKET_API_URL}/repositories/{WORKSPACE}/{REPO_SLUG}/pullrequests/{PR_ID}/comments"
    payload = {
        "inline": {"path": filename, "to": line},
        "content": {"raw": message}
    }
    resp = requests.post(url, json=payload, auth=(USERNAME, APP_PASSWORD))
    if resp.status_code not in [200, 201]:
        print("Failed to post comment:", resp.text)

with open("flake8_output.txt") as f:
    for line in f:
        parts = line.strip().split(":", 3)
        if len(parts) < 4:
            continue
        file, line_no, col, msg = parts
        post_comment(file, int(line_no), msg)