# Tech News Scraper

A Python web scraper that collects top tech news from [Hacker News](https://news.ycombinator.com). Built with `requests` and `BeautifulSoup4`.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## Features

- Scrape articles from multiple pages
- Extract title, URL, points, author, comments, and timestamp
- Export data to CSV and JSON formats
- Get top articles sorted by points
- Clean, well-documented object-oriented code
- Type hints for better code quality

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/BabaevvAnnageldi/tech-news-scraper.git
   cd tech-news-scraper
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

Run the scraper:

```bash
python scraper.py
```

This will:
- Scrape the first 2 pages of Hacker News (60 articles)
- Display all articles in a formatted table
- Show top 5 articles by points
- Export data to `hacker_news_articles.csv` and `hacker_news_articles.json`

### As a Module

```python
from scraper import HackerNewsScraper

# Initialize scraper
scraper = HackerNewsScraper()

# Scrape 3 pages
articles = scraper.scrape(pages=3)

# Get top 10 articles by points
top_articles = scraper.get_top_articles(10)

# Export to files
scraper.export_to_csv("news.csv")
scraper.export_to_json("news.json")

# Display in terminal
scraper.display_articles()
```

## Output Example

### Terminal Output

```
==================================================
   Tech News Scraper - Hacker News Edition
   Author: Annageldi Babayev
==================================================

Scraping page 1...
  Found 30 articles
Scraping page 2...
  Found 30 articles

Total articles scraped: 60

================================================================================
RANK  POINTS  COMMENTS  TITLE
================================================================================
1     342     156       Show HN: I built a tool to track startup funding
2     289     94        The Future of AI in Software Development
3     267     203       Why Rust is Taking Over Systems Programming
================================================================================
```

### CSV Output

```csv
Rank,Title,URL,Points,Author,Comments,Time
1,Show HN: I built a tool...,https://example.com,342,johndoe,156,3 hours ago
2,The Future of AI...,https://example.com,289,janedoe,94,5 hours ago
```

### JSON Output

```json
{
  "scraped_at": "2024-01-15T10:30:00",
  "total_articles": 60,
  "articles": [
    {
      "rank": 1,
      "title": "Show HN: I built a tool...",
      "url": "https://example.com",
      "points": 342,
      "author": "johndoe",
      "comments": 156,
      "time_ago": "3 hours ago"
    }
  ]
}
```

## Project Structure

```
tech-news-scraper/
├── scraper.py          # Main scraper module
├── requirements.txt    # Python dependencies
├── .gitignore          # Git ignore rules
└── README.md           # Documentation
```

## Technologies Used

- **Python 3.8+** - Programming language
- **Requests** - HTTP library for fetching web pages
- **BeautifulSoup4** - HTML parsing library
- **Dataclasses** - For clean data structures

## Skills Demonstrated

- Web scraping and HTML parsing
- Object-Oriented Programming (OOP)
- Data export (CSV, JSON)
- Type hints and documentation
- Error handling
- Clean code principles

## License

This project is open source and available under the [MIT License](LICENSE).

## Author

**Annageldi Babayev**
- GitHub: [@BabaevvAnnageldi](https://github.com/BabaevvAnnageldi)
- Portfolio: [babaevvannageldi.github.io](https://babaevvannageldi.github.io)

---

*Built for educational purposes and portfolio demonstration.*
