# 📊 Scalable News Sentiment Dashboard

A real-time dashboard that helps investors make smarter decisions by analyzing news sentiment using state-of-the-art NLP (FinBERT). This tool scrapes financial headlines, scores their sentiment, and combines it with recent stock price data to generate investment insights for top tech stocks.

---

## 🧠 What It Does

- Scrapes the **latest Yahoo Finance headlines** for selected stocks.
- Applies **FinBERT** (finance-specific transformer) to analyze sentiment.
- Aggregates sentiment scores and displays an **investment recommendation** (Buy / Hold / Avoid).
- Shows recent **5-day stock prices** using real-time data from Yahoo Finance.
- Provides a clean, interactive **Dash dashboard** with sentiment bars and price trends.

---

## 🔧 Tech Stack

| Component          | Details                                                                 |
|-------------------|-------------------------------------------------------------------------|
| **Frontend/UI**   | [Dash](https://dash.plotly.com/) + Plotly (interactive charts)          |
| **NLP Model**      | [FinBERT](https://huggingface.co/yiyanghkust/finbert-tone) via 🤗 Transformers |
| **News Scraping** | [feedparser](https://pythonhosted.org/feedparser/) from Yahoo Finance RSS feeds |
| **Stock Data**     | [yfinance](https://github.com/ranaroussi/yfinance) for real-time stock prices |
| **Python Packages**| `dash`, `plotly`, `transformers`, `feedparser`, `yfinance`, `pandas`   |

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/news-sentiment-dashboard.git
cd news-sentiment-dashboard
