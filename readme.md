# ArXiv Downloader

A simple tool to batch download ArXiv PDFs based on a search query. Yahoo~~~

你是否有arxiv标签堆满浏览器的烦恼？你是否有下载文档名是一串数字，完全分不清文献的烦恼？别担心，Arxiv Search Grabber 来帮忙！

只需一个命令行窗口，即可完成搜索 - 批量下载 - 自动更改文档名为文章名！

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