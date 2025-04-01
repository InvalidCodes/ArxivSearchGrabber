# ArXiv Downloader

A simple tool to batch download ArXiv PDFs based on a search query. The downloaded files are named by article titles. Yahoo~~~

## Usage
1. Install dependencies: `pip install -r requirements.txt`
2. Run the script: `python downloader.py --query "machine unlearning" --max 10 --dir ./downloads`

## With Docker
1. Build the image: `docker build -t arxiv-downloader .`
2. Run the container: `docker run -v /path/to/local/dir:/app/downloads arxiv-downloader --query "machine unlearning" --max 10`

## Requirements
- Python 3.9+
- See `requirements.txt` for dependencies