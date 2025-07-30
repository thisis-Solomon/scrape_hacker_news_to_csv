
import requests
from bs4 import BeautifulSoup
import csv

CSV_FILE = "fetch_hacker_news_top_posts.csv"
URL = "https://news.ycombinator.com/"

def fetch_hacker_news_top_posts():
    try:
        res = requests.get(URL, timeout=10)
        res.raise_for_status()
    except requests.RequestException as e:
        print(f"Network error: {e}")
        return []
    
    soup = BeautifulSoup(res.text, "html.parser")
    post_link = soup.select("span.titleline > a")

    top_posts = []
    for link in post_link[:20]:  # Get only the top 20 posts
        title = link.get_text()
        url = link.get("href")
        top_posts.append({"title": title, "url": url})

    return top_posts

def save_to_csv(posts):
    if not posts:
        print("No posts to save.")
        return
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["title", "url"])
        writer.writeheader()
        writer.writerows(posts)

        print(f"Saved {len(posts)} posts to {CSV_FILE}")

def main():
    print("Fetching Hacker News top posts...")
    top_posts = fetch_hacker_news_top_posts()
    print(f"Found {len(top_posts)} top posts.")
    save_to_csv(top_posts)  

if __name__ == "__main__":
    main()