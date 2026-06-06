"""
Tech News Scraper
-----------------
A Python web scraper that collects top tech news from Hacker News.
Supports exporting to CSV and JSON formats.

Author: Annageldi Babayev
GitHub: https://github.com/BabaevvAnnageldi
"""

import requests
from bs4 import BeautifulSoup
import csv
import json
from datetime import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class Article:
    """Represents a news article from Hacker News."""
    rank: int
    title: str
    url: Optional[str]
    points: int
    author: str
    comments: int
    time_ago: str


class HackerNewsScraper:
    """
    A web scraper for Hacker News (news.ycombinator.com).

    Attributes:
        base_url (str): The base URL for Hacker News
        headers (dict): HTTP headers for requests
    """

    BASE_URL = "https://news.ycombinator.com"

    def __init__(self):
        """Initialize the scraper with default headers."""
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/91.0.4472.124 Safari/537.36"
        }
        self.articles: list[Article] = []

    def fetch_page(self, page: int = 1) -> str:
        """
        Fetch HTML content from Hacker News.

        Args:
            page: Page number to fetch (default: 1)

        Returns:
            HTML content as string

        Raises:
            requests.RequestException: If the request fails
        """
        url = self.BASE_URL if page == 1 else f"{self.BASE_URL}/news?p={page}"
        response = requests.get(url, headers=self.headers, timeout=10)
        response.raise_for_status()
        return response.text

    def parse_articles(self, html: str) -> list[Article]:
        """
        Parse articles from HTML content.

        Args:
            html: Raw HTML content from Hacker News

        Returns:
            List of Article objects
        """
        soup = BeautifulSoup(html, "html.parser")
        articles = []

        # Find all article rows
        rows = soup.select("tr.athing")

        for row in rows:
            try:
                article = self._parse_single_article(row)
                if article:
                    articles.append(article)
            except (AttributeError, ValueError) as e:
                # Skip malformed articles
                continue

        return articles

    def _parse_single_article(self, row) -> Optional[Article]:
        """
        Parse a single article from a table row.

        Args:
            row: BeautifulSoup element representing an article row

        Returns:
            Article object or None if parsing fails
        """
        # Get rank
        rank_elem = row.select_one("span.rank")
        rank = int(rank_elem.text.strip(".")) if rank_elem else 0

        # Get title and URL
        title_elem = row.select_one("span.titleline > a")
        if not title_elem:
            return None

        title = title_elem.text.strip()
        url = title_elem.get("href", "")

        # Handle relative URLs
        if url.startswith("item?"):
            url = f"{self.BASE_URL}/{url}"

        # Get metadata from the next row
        subtext_row = row.find_next_sibling("tr")
        if not subtext_row:
            return Article(rank, title, url, 0, "unknown", 0, "unknown")

        subtext = subtext_row.select_one("td.subtext")
        if not subtext:
            return Article(rank, title, url, 0, "unknown", 0, "unknown")

        # Parse points
        score_elem = subtext.select_one("span.score")
        points = 0
        if score_elem:
            points_text = score_elem.text.split()[0]
            points = int(points_text)

        # Parse author
        author_elem = subtext.select_one("a.hnuser")
        author = author_elem.text if author_elem else "unknown"

        # Parse comments
        comments = 0
        links = subtext.select("a")
        for link in links:
            if "comment" in link.text.lower():
                comments_text = link.text.split()[0]
                if comments_text.isdigit():
                    comments = int(comments_text)
                break

        # Parse time
        age_elem = subtext.select_one("span.age")
        time_ago = age_elem.text.strip() if age_elem else "unknown"

        return Article(
            rank=rank,
            title=title,
            url=url,
            points=points,
            author=author,
            comments=comments,
            time_ago=time_ago
        )

    def scrape(self, pages: int = 1) -> list[Article]:
        """
        Scrape multiple pages of articles.

        Args:
            pages: Number of pages to scrape (default: 1)

        Returns:
            List of all scraped Article objects
        """
        self.articles = []

        for page in range(1, pages + 1):
            print(f"Scraping page {page}...")
            html = self.fetch_page(page)
            page_articles = self.parse_articles(html)
            self.articles.extend(page_articles)
            print(f"  Found {len(page_articles)} articles")

        print(f"\nTotal articles scraped: {len(self.articles)}")
        return self.articles

    def export_to_csv(self, filename: str = "articles.csv") -> str:
        """
        Export scraped articles to a CSV file.

        Args:
            filename: Output filename (default: articles.csv)

        Returns:
            Path to the created file
        """
        if not self.articles:
            raise ValueError("No articles to export. Run scrape() first.")

        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Rank", "Title", "URL", "Points", "Author", "Comments", "Time"])

            for article in self.articles:
                writer.writerow([
                    article.rank,
                    article.title,
                    article.url,
                    article.points,
                    article.author,
                    article.comments,
                    article.time_ago
                ])

        print(f"Exported to {filename}")
        return filename

    def export_to_json(self, filename: str = "articles.json") -> str:
        """
        Export scraped articles to a JSON file.

        Args:
            filename: Output filename (default: articles.json)

        Returns:
            Path to the created file
        """
        if not self.articles:
            raise ValueError("No articles to export. Run scrape() first.")

        data = {
            "scraped_at": datetime.now().isoformat(),
            "total_articles": len(self.articles),
            "articles": [
                {
                    "rank": a.rank,
                    "title": a.title,
                    "url": a.url,
                    "points": a.points,
                    "author": a.author,
                    "comments": a.comments,
                    "time_ago": a.time_ago
                }
                for a in self.articles
            ]
        }

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"Exported to {filename}")
        return filename

    def get_top_articles(self, n: int = 10) -> list[Article]:
        """
        Get top N articles by points.

        Args:
            n: Number of articles to return (default: 10)

        Returns:
            List of top N articles sorted by points
        """
        return sorted(self.articles, key=lambda x: x.points, reverse=True)[:n]

    def display_articles(self, articles: list[Article] = None) -> None:
        """
        Display articles in a formatted table.

        Args:
            articles: List of articles to display (default: all scraped articles)
        """
        articles = articles or self.articles

        if not articles:
            print("No articles to display.")
            return

        print("\n" + "=" * 80)
        print(f"{'RANK':<6}{'POINTS':<8}{'COMMENTS':<10}{'TITLE':<50}")
        print("=" * 80)

        for article in articles:
            title = article.title[:47] + "..." if len(article.title) > 50 else article.title
            print(f"{article.rank:<6}{article.points:<8}{article.comments:<10}{title:<50}")

        print("=" * 80 + "\n")


def main():
    """Main entry point for the scraper."""
    print("=" * 50)
    print("   Tech News Scraper - Hacker News Edition")
    print("   Author: Annageldi Babayev")
    print("=" * 50 + "\n")

    # Initialize scraper
    scraper = HackerNewsScraper()

    # Scrape first 2 pages (60 articles)
    scraper.scrape(pages=2)

    # Display all articles
    print("\n--- All Articles ---")
    scraper.display_articles()

    # Show top 5 by points
    print("\n--- Top 5 Articles by Points ---")
    top_articles = scraper.get_top_articles(5)
    scraper.display_articles(top_articles)

    # Export to files
    scraper.export_to_csv("hacker_news_articles.csv")
    scraper.export_to_json("hacker_news_articles.json")

    print("\nScraping complete!")


if __name__ == "__main__":
    main()
