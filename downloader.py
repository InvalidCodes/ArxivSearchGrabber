import arxiv
import requests
import os
import time
import argparse

def download_pdf(url, title, save_dir, retries=3, delay=5):
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
            return
        except Exception as e:
            print(f"Attempt {attempt+1} failed for {title}: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                print(f"Failed to download {title} after {retries} attempts.")

def main():
    parser = argparse.ArgumentParser(description="Batch download ArXiv PDFs")
    parser.add_argument("--query", type=str, required=True, help="Search query (e.g., 'machine unlearning')")
    parser.add_argument("--max", type=int, default=10, help="Max number of papers to download")
    parser.add_argument("--dir", type=str, default="./downloads", help="Download directory")
    args = parser.parse_args()

    save_dir = os.path.abspath(args.dir)
    print(f"Download directory (absolute): {save_dir}")
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    print(f"Searching ArXiv for '{args.query}'...")
    client = arxiv.Client()
    # 用引号包裹短语，确保精确匹配
    formatted_query = f'"{args.query}"'
    print(f"Formatted query: {formatted_query}")
    search = arxiv.Search(
        query=formatted_query,
        max_results=args.max,
        # 暂时移除排序，测试是否返回结果
        # sort_by=arxiv.SortCriterion.SubmittedDate,
        # sort_order=arxiv.SortOrder.Descending
    )

    # 获取搜索结果
    results = list(client.results(search))
    if not results:
        print("No results found for the query. Trying alternative query format...")
        # 尝试按标题和摘要分别搜索
        formatted_query = f'ti:"{args.query}" OR abs:"{args.query}"'
        print(f"Alternative query: {formatted_query}")
        search = arxiv.Search(
            query=formatted_query,
            max_results=args.max
        )
        results = list(client.results(search))
        if not results:
            print("Still no results found. Try a different keyword or check your network.")
            return

    for result in results:
        pdf_url = result.pdf_url
        title = result.title
        abstract = result.summary[:200]
        print(f"== Found: {title}")
        print(f"Abstract: {abstract}...")
        download_pdf(pdf_url, title, save_dir, retries=3, delay=5)
        time.sleep(2)

    print(f"Download completed! Files saved in {save_dir}")

if __name__ == "__main__":
    main()