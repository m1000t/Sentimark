import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from transformers import pipeline
import feedparser
import yfinance as yf
from datetime import datetime, timedelta

# ----------------------------------
# FinBERT Sentiment Setup
# ----------------------------------
finbert = pipeline("sentiment-analysis", model="yiyanghkust/finbert-tone")

def analyze_sentiment(text):
    result = finbert(text)[0]
    label = result['label'].lower()
    score = result['score']
    return score if label == 'positive' else -score if label == 'negative' else 0.0

# ----------------------------------
# Get News Headlines with Sentiment
# ----------------------------------
def get_headlines(ticker, limit=20):
    rss_map = {
        "AAPL": "https://feeds.finance.yahoo.com/rss/2.0/headline?s=AAPL&region=US&lang=en-US",
        "MSFT": "https://feeds.finance.yahoo.com/rss/2.0/headline?s=MSFT&region=US&lang=en-US",
        "GOOGL": "https://feeds.finance.yahoo.com/rss/2.0/headline?s=GOOGL&region=US&lang=en-US"
    }

    url = rss_map.get(ticker)
    if not url:
        return pd.DataFrame()

    feed = feedparser.parse(url)
    seven_days_ago = datetime.now() - timedelta(days=7)

    data = []
    for entry in feed.entries:
        try:
            published_date = datetime(*entry.published_parsed[:6])
        except:
            continue

        if published_date >= seven_days_ago:
            sentiment = analyze_sentiment(entry.title.strip())
            data.append({
                "headline": entry.title.strip(),
                "published": published_date.strftime("%Y-%m-%d %H:%M"),
                "score": sentiment
            })

    return pd.DataFrame(data)

# ----------------------------------
# Get Stock Price Data
# ----------------------------------
def get_stock_data(ticker):
    stock = yf.download(ticker, period="5d", interval="1d")
    stock.reset_index(inplace=True)

    if isinstance(stock.columns, pd.MultiIndex):
        stock.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in stock.columns]

    return stock

# ----------------------------------
# Dash App Setup
# ----------------------------------
app = dash.Dash(__name__)
app.title = "Investment Insight Dashboard"

app.layout = html.Div(style={'fontFamily': 'Arial', 'backgroundColor': '#f4f4f4', 'padding': '40px'}, children=[
    html.H1("📊 Investment Sentiment Dashboard", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Choose a Stock:"),
        dcc.Dropdown(
            id='ticker-dropdown',
            options=[
                {'label': 'Apple (AAPL)', 'value': 'AAPL'},
                {'label': 'Microsoft (MSFT)', 'value': 'MSFT'},
                {'label': 'Google (GOOGL)', 'value': 'GOOGL'},
            ],
            value='AAPL',
            clearable=False,
            style={'width': '300px', 'marginBottom': '30px'}
        )
    ]),

    html.Div([
        html.H2("Sentiment Recommendation:"),
        html.Div(id='recommendation-box')
    ]),

    dcc.Graph(id='price-chart'),
    dcc.Graph(id='sentiment-chart'),

    html.H3("📰 Headlines", style={'marginTop': '30px'}),
    html.Ul(id='headline-list', style={
        'backgroundColor': '#fff',
        'padding': '20px',
        'borderRadius': '8px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
        'maxHeight': '300px',
        'overflowY': 'auto'
    })
])

# ----------------------------------
# Callback for Dynamic Ticker Updates
# ----------------------------------
@app.callback(
    [Output('price-chart', 'figure'),
     Output('sentiment-chart', 'figure'),
     Output('recommendation-box', 'children'),
     Output('recommendation-box', 'style'),
     Output('headline-list', 'children')],
    [Input('ticker-dropdown', 'value')]
)
def update_dashboard(ticker):
    # Stock Data
    df_price = get_stock_data(ticker)
    x_col = "Date" if "Date" in df_price.columns else "Date_"
    y_col = "Close" if "Close" in df_price.columns else f"Close_{ticker}"

    fig_price = px.line(df_price, x=x_col, y=y_col, title=f"📈 {ticker} Stock Price (Last 5 Days)")

    # Sentiment Data
    df_sentiment = get_headlines(ticker)
    avg_score = df_sentiment['score'].mean() if not df_sentiment.empty else 0

    if avg_score > 0.05:
        rec = "👍 Positive sentiment — consider investing"
        bg = "#d4edda"; color = "#155724"
    elif avg_score < -0.05:
        rec = "👎 Negative sentiment — be cautious"
        bg = "#f8d7da"; color = "#721c24"
    else:
        rec = "⚠️ Neutral sentiment — wait and watch"
        bg = "#fff3cd"; color = "#856404"

    fig_sentiment = px.bar(df_sentiment, x="published", y="score",
                           title="🧠 Sentiment on Latest Headlines",
                           color="score", color_continuous_scale=["red", "gray", "green"])

    headlines = [
        html.Li(f"{row['published']} — {row['headline']}") for _, row in df_sentiment.iterrows()
    ]

    return fig_price, fig_sentiment, rec, {
        'backgroundColor': bg,
        'color': color,
        'padding': '15px',
        'fontWeight': 'bold',
        'borderRadius': '10px',
        'textAlign': 'center',
        'marginBottom': '30px'
    }, headlines

# ----------------------------------
# Run App
# ----------------------------------
if __name__ == "__main__":
    app.run(debug=True)
