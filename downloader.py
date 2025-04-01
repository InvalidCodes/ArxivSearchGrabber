import arxiv
import requests
import os
import time
import argparse

def download_pdf(url, title, save_dir):
    try:
        safe_title = "".join(c for c in title if c.isalnum() or c in " _-").strip()
        file_path = os.path.join(save_dir, f"{safe_title}.pdf")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded: {safe_title}.pdf")
    except Exception as e:
        print(f"Error downloading {title}: {e}")

def main():
    # 设置命令行参数
    parser = argparse.ArgumentParser(description="Batch download ArXiv PDFs")
    parser.add_argument("--query", type=str, required=True, help="Search query (e.g., 'machine unlearning')")
    parser.add_argument("--max", type=int, default=10, help="Max number of papers to download")
    parser.add_argument("--dir", type=str, default="./downloads", help="Download directory")
    args = parser.parse_args()

    # 创建下载目录
    if not os.path.exists(args.dir):
        os.makedirs(args.dir)

    # 搜索并下载
    print(f"Searching ArXiv for '{args.query}'...")
    search = arxiv.Search(
        query=args.query,
        max_results=args.max,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending
    )

    for result in search.results():
        pdf_url = result.pdf_url
        title = result.title
        print(f"Found: {title}")
        download_pdf(pdf_url, title, args.dir)
        time.sleep(2)

    print(f"Download completed! Files saved in {args.dir}")

if __name__ == "__main__":
    main()