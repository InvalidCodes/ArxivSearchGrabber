# ArXiv Downloader

A simple tool to batch download ArXiv PDFs based on a search query. Yahoo~~~

## Features
- Search and download papers from ArXiv.
- Name files by article titles.
- Avoid duplicate downloads by tracking download history (`download_history.json`).
- If papers are skipped (already downloaded), continue searching until the target number of new papers is downloaded.
- Configurable via command-line arguments.

## Usage
1. Create environment: 
`conda create -n arxiv_download`
`conda activate arxiv_download`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the script: `python downloader.py --query "machine unlearning" --max 10 --dir ./downloads`

## With Docker
1. Build the image: `docker build -t arxiv-downloader .`
2. Run the container: `docker run -v /path/to/local/dir:/app/downloads arxiv-downloader --query "machine unlearning" --max 10`

## Requirements
- Python 3.9+
- See `requirements.txt` for dependencies