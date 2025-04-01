import arxiv
import requests
import os
import time
import argparse
import json

# 历史记录文件
HISTORY_FILE = "download_history.json"

def load_history():
    """加载下载历史"""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return {"arxiv": {}}

def save_history(history):
    """保存下载历史"""
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def download_pdf(url, title, save_dir, source, paper_id, history, retries=3, delay=5):
    """下载PDF并记录历史"""
    if source == "arxiv" and paper_id in history["arxiv"]:
        print(f"Skipping {title}: Already downloaded (ArXiv ID: {paper_id})")
        return False

    for attempt in range(retries):
        try:
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            safe_title = "".join(c for c in title if c.isalnum() or c in " _-").strip()
            file_path = os.path.join(save_dir, f"{safe_title}.pdf")
            print(f"Saving to: {file_path}")
            response = requests.get(url, stream=True, timeout=10)
            response.raise_for_status()
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"== Downloaded: {safe_title}.pdf")
            if source == "arxiv":
                history["arxiv"][paper_id] = title
            save_history(history)
            return True
        except Exception as e:
            print(f"Attempt {attempt+1} failed for {title}: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                print(f"Failed to download {title} after {retries} attempts.")
                return False

def search_arxiv(query, max_results, save_dir, history):
    """搜索并下载ArXiv论文，确保下载数量达到目标"""
    print(f"Searching ArXiv for '{query}'...")
    client = arxiv.Client()
    downloaded_count = 0  # 记录实际下载的文献数量
    skipped_count = 0  # 记录被跳过的文献数量
    offset = 0  # 分页偏移量
    batch_size = max_results  # 初始批量大小

    while downloaded_count < max_results:
        # 动态调整batch_size：加上被跳过的数量
        current_batch_size = batch_size + skipped_count
        formatted_query = f'"{query}"'
        print(f"Formatted query: {formatted_query} (offset: {offset}, batch_size: {current_batch_size})")
        search = arxiv.Search(
            query=formatted_query,
            max_results=current_batch_size
        )

        results = list(client.results(search, offset=offset))
        if not results:
            print("No more results found on ArXiv. Trying alternative query format...")
            formatted_query = f'ti:"{query}" OR abs:"{query}"'
            print(f"Alternative query: {formatted_query} (offset: {offset}, batch_size: {current_batch_size})")
            search = arxiv.Search(
                query=formatted_query,
                max_results=current_batch_size
            )
            results = list(client.results(search, offset=offset))
            if not results:
                print("No more results found on ArXiv with alternative query.")
                break

        for result in results:
            pdf_url = result.pdf_url
            title = result.title
            arxiv_id = result.entry_id.split("/")[-1]
            abstract = result.summary[:200]
            print(f"== Found: {title}")
            print(f"Abstract: {abstract}...")
            if download_pdf(pdf_url, title, save_dir, "arxiv", arxiv_id, history):
                downloaded_count += 1
            else:
                skipped_count += 1
            if downloaded_count >= max_results:
                break
        offset += current_batch_size
        time.sleep(2)

    print(f"Total new papers downloaded: {downloaded_count}")
    print(f"Total papers skipped: {skipped_count}")

def main():
    parser = argparse.ArgumentParser(description="Batch download PDFs from ArXiv")
    parser.add_argument("--query", type=str, required=True, help="Search query (e.g., 'machine unlearning')")
    parser.add_argument("--max", type=int, default=10, help="Max number of new papers to download")
    parser.add_argument("--dir", type=str, default="./downloads", help="Download directory")
    args = parser.parse_args()

    save_dir = os.path.abspath(args.dir)
    print(f"Download directory (absolute): {save_dir}")
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    history = load_history()
    search_arxiv(args.query, args.max, save_dir, history)

    print(f"Download completed! Files saved in {save_dir}")

if __name__ == "__main__":
    main()