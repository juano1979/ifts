Project: Playwright + API tests with Slack reporting

This repository contains example tests using Playwright (Python) and API tests using `requests` + `pytest`. Test results are produced as an HTML report stored at `reports/report.html` and may be uploaded to Slack by the CI workflow.

Quick start

- Create and activate a virtual environment, install dependencies, and install Playwright browsers:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
playwright install
```

- Run tests locally (creates `reports/report.html`):

```bash
pytest
```

Secrets and Slack

- GitHub repository secrets (add under Settings → Secrets):
	- `SLACK_TOKEN`: a Slack token with `files:write` permission (Bot token is typical).
	- `SLACK_CHANNEL`: the Slack channel ID to post the report to (e.g. `C01234567`).

- To test uploading a report locally, set env vars and use the provided script:

```bash
export SLACK_TOKEN="xoxb-..."
export SLACK_CHANNEL="C01234567"
python scripts/send_slack_report.py reports/report.html
```

Files and CI

- The GitHub Actions workflow is at `.github/workflows/ci.yml`. On each push/pull request it:
	- Installs Python and Playwright browsers
	- Runs `pytest` to produce `reports/report.html`
	- Uploads the report as an artifact
	- Attempts to post the report to Slack using `curl` with `SLACK_TOKEN` and `SLACK_CHANNEL` from repository secrets

Troubleshooting

- Playwright browser install: if `playwright install` fails on CI, try `playwright install --with-deps` for Linux runners.
- If `reports/report.html` is missing after `pytest`, ensure tests ran and `reports/` exists — run `mkdir -p reports` before `pytest`.
- Slack upload problems: verify `SLACK_TOKEN` has `files:write` scope and `SLACK_CHANNEL` is a channel ID (not name). You can test with a quick `curl`:

```bash
curl -F file=@reports/report.html -F channels="$SLACK_CHANNEL" -H "Authorization: Bearer $SLACK_TOKEN" https://slack.com/api/files.upload
```

Security notes

- Keep `SLACK_TOKEN` secret. Do not commit tokens to the repository.

Next steps

- To verify everything here, I can (choose):
	- run a local syntax check of Python files now, or
	- install deps and run the tests here (network required), or
	- help you set up GitHub secrets and trigger a workflow run.

Files added: tests, scripts/send_slack_report.py, pytest.ini, requirements.txt, .github/workflows/ci.yml
