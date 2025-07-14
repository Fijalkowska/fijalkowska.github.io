import yfinance as yf
import pandas as pd
from datetime import date
import base64
import io
import matplotlib.pyplot as plt

# Lista spółek do analizy
akcje = [
    'AAPL', 'TSLA', 'MSFT', 'AMZN', 'META',
    'GOOGL', 'NVDA', 'PLTR', 'AMD', 'INTC',
    'KO', 'PEP', 'NKE', 'MCD', 'DIS',
    'CRM', 'ADBE', 'CSCO', 'PYPL', 'UBER'
]

def sprawdz_akcje(symbol: str):
    dane = yf.download(symbol, period="60d", interval="1d")
    dane['MA20'] = dane['Close'].rolling(window=20).mean()
    dane['MA50'] = dane['Close'].rolling(window=50).mean()

    ostatni = dane.tail(1)
    ma20 = ostatni['MA20'].item() if not pd.isna(ostatni['MA20'].item()) else None
    ma50 = ostatni['MA50'].item() if not pd.isna(ostatni['MA50'].item()) else None

    if ma20 is None or ma50 is None:
        return "neutral", "Brak danych"

    if ma20 > ma50:
        return "kupuj", "Potencjał wzrostowy"
    elif ma20 < ma50:
        return "sprzedaj", "Potencjał spadkowy"
    else:
        return "neutral", "Brak sygnału"

def generuj_sparkline(dane):
    fig, ax = plt.subplots(figsize=(2, 0.5))
    ax.plot(dane['Close'].tail(20), linewidth=1, color="#555")
    ax.axis('off')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0, dpi=100)
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

# Szablon HTML
naglowek_html = """<!DOCTYPE html>
<html lang="pl">
<head>
  <meta charset="UTF-8">
  <title>Rekomendacje</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
  <style>
    body {
      font-family: 'Inter', sans-serif;
      font-size: 16px;
      margin: 0;
      padding: 1rem;
      background: #fff;
      color: #222;
    }
    h2 {
      font-size: 1.4rem;
      margin-bottom: 1rem;
    }
    .rekomendacje-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 1rem;
    }
    .reko {
      padding: 1rem;
      border-radius: 10px;
      background: #f4f4f4;
      text-align: center;
      font-weight: 600;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .kupuj { background: #e6fbe9; color: #107c41; }
    .sprzedaj { background: #ffecec; color: #b30000; }
    .neutral { background: #fdfdfd; color: #555; }
    .sparkline {
      margin-top: 0.5rem;
      display: block;
      width: 100%;
    }
  </style>
</head>
<body>
"""

stopka_html = """
</body>
</html>
"""

html = f"{naglowek_html}<h2>Rekomendacje inwestycyjne – {date.today().strftime('%d.%m.%Y')}</h2>"
html += "<div class='rekomendacje-grid'>"

for symbol in akcje:
    dane = yf.download(symbol, period="60d", interval="1d")
    typ, opis = sprawdz_akcje(symbol)
    spark = generuj_sparkline(dane)
    html += f"<div class='reko {typ}'><strong>{symbol}</strong><br>{opis}<br><img class='sparkline' src='data:image/png;base64,{spark}' alt='trend'></div>"

html += "</div>" + stopka_html

with open("rekomendacje.html", "w", encoding="utf-8") as f:
    f.write(html)
