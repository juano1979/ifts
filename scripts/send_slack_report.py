#!/usr/bin/env python3
"""Upload a local report file to Slack using a token and channel ID.

Usage:
  SLACK_TOKEN and SLACK_CHANNEL env vars required.
  python scripts/send_slack_report.py reports/report.html
"""
import os
import sys
import requests


def upload_file(token: str, channel: str, file_path: str) -> None:
    url = "https://slack.com/api/files.upload"
    with open(file_path, "rb") as f:
        files = {"file": f}
        data = {"channels": channel}
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.post(url, headers=headers, data=data, files=files)
    resp.raise_for_status()
    j = resp.json()
    if not j.get("ok", False):
        raise SystemExit(f"Slack API error: {j}")
    print("Uploaded report to Slack successfully")


def main():
    if len(sys.argv) < 2:
        print("Usage: send_slack_report.py <report-path>")
        sys.exit(2)
    path = sys.argv[1]
    token = os.environ.get("SLACK_TOKEN")
    channel = os.environ.get("SLACK_CHANNEL")
    if not token or not channel:
        print("Environment variables SLACK_TOKEN and SLACK_CHANNEL are required")
        sys.exit(2)
    if not os.path.exists(path):
        print(f"Report not found: {path}")
        sys.exit(2)
    upload_file(token, channel, path)


if __name__ == "__main__":
    main()
