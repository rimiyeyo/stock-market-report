<h1 align="center">stock-market-report</h1>

<p align="center">A project that generates a stock market report by calling LLM APIs.</p>
<p align="center"><a href="https://github.com/f-lab-edu/stock-market-report/actions/workflows/ci.yml/badge.svg" target="_blank"><img alt="Python CI" src="https://github.com/f-lab-edu/stock-market-report/actions/workflows/ci.yml/badge.svg"/></a></p>

## Overview

This project generates a stock market report based on a user query. It utilizes an LLM to consolidate and summarize web search results and real-time stock price information.

## Directory Structure

```plaintext
stock-market-report/
├── .github/workflows/ci.yml
├── main.py
├── run.sh
├── settings/
│   └── settings.py
├── test.sh
└── tests/
    └── test_main.py
```

### Installation

```bash
brew install pyenv # (macOS)
pyenv install 3.11.3
pyenv virtualenv 3.11.3 stock
pyenv activate stock
```
Install dependencies:

```bash
pip install -r requirements.txt
```
And, this project uses [`pre-commit`](https://pre-commit.com/).
You need to setup pre-commit before to get started.

```bash
pre-commit install
```

> Note: You may need to add requirements.txt if not already present.

### Running

Ensure any API keys or secrets are handled securely using environment variables or a `.env` file.

Usage
To generate a report:
```bash
bash run.sh
```


### Testing

To run tests locally:

```bash
bash test.sh
```

This executes the test suite using pytest. Make sure your environment is properly set up before running.

### CI
This project uses GitHub Actions for Continuous Integration. Every push or pull request triggers the workflow defined in:

```yaml
.github/workflows/ci.yml
```

It automatically runs all tests and checks for code quality.

### Requirements
- Python 3.11+
- yfinance
