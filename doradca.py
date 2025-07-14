import yfinance as yf
import pandas as pd
from datetime import date
import base64
import io
import matplotlib.pyplot as plt

akcje = [
    'AAPL', 'TSLA', 'MSFT', 'AMZN', 'META',
    'GOOGL', 'NVDA', 'PLTR', 'AMD', 'INTC',
    'KO', 'PEP', 'NKE', 'MCD', 'DIS',
    'CRM', 'ADBE', 'CSCO', 'PYPL', 'UBER'
]

nazwy_spolek = {
    'AAPL': 'Apple Inc.',
    'TSLA': 'Tesla Inc.',
    'MSFT': 'Microsoft Corporation',
    'AMZN': 'Amazon.com, Inc.',
    'META': 'Meta Platforms, Inc.',
    'GOOGL': 'Alphabet Inc.',
    'NVDA': 'NVIDIA Corporation',
    'PLTR': 'Palantir Technologies',
    'AMD': 'Advanced Micro Devices',
    'INTC': 'Intel Corporation',
    'KO': 'The Coca-Cola Company',
    'PEP': 'PepsiCo, Inc.',
    'NKE': 'Nike, Inc.',
    'MCD': "McDonald's Corporation",
    'DIS': 'The Walt Disney Company',
    'CRM': 'Salesforce, Inc.',
    'ADBE': 'Adobe Inc.',
    'CSCO': 'Cisco Systems, Inc.',
    'PYPL': 'PayPal Holdings, Inc.',
    'UBER': 'Uber Technologies, Inc.'
}

def sprawdz_akcje(symbol: str):
    dane = yf.download(symbol, period="60d", interval="1d")
    dane['MA20'] = dane['Close'].rolling(window=20).mean()
    dane['MA50'] = dane['Close'].rolling(window=50).mean()

    ostatni = dane.tail(1)
    ma20 = ostatni['MA20'].values[0] if not pd.isna(ostatni['MA20'].values[0]) else None
    ma50 = ostatni['MA50'].values[0] if not pd.isna(ostatni['MA50'].values[0]) else None
    cena = float(ostatni['Close'].values[0]) if not pd.isna(ostatni['Close'].values[0]) else None

    if ma20 is None or ma50 is None or cena is None:
        return "neutral", "Brak danych", cena

    if ma20 > ma50:
        return "kupuj", "Potencjał wzrostowy (MA20 > MA50)", cena
    elif ma20 < ma50:
        return "sprzedaj", "Potencjał spadkowy (MA20 < MA50)", cena
    else:
        return "neutral", "Brak sygnału (MA20 ≈ MA50)", cena

def generuj_sparkline(dane):
    fig, ax = plt.subplots(figsize=(2, 0.5))
    ax.plot(dane['Close'].tail(20), linewidth=1, color="#888")
    ax.axis('off')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0, dpi=100)
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

naglowek_html = """<!DOCTYPE html>
<html lang=\"pl\">
<head>
  <meta charset=\"UTF-8\">
  <title>Rekomendacje</title>
  <link href=\"https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap\" rel=\"stylesheet\">
  <style>
    body {
      font-family: 'Inter', sans-serif;
      font-size: 15px;
      margin: 0;
      padding: 1rem;
      background: #1b1c1f;
      color: #eee;
      transition: background 0.3s, color 0.3s;
    }
    h2, h1, h3 {
      font-size: 1.5rem;
      margin-bottom: 1rem;
      color: #f2f2f2;
    }
    .opis {
      font-size: 1rem;
      margin-bottom: 2rem;
      color: #ccc;
      max-width: 1000px;
    }
    .rekomendacje-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 1.2rem;
      width: 100%;
    }
    .reko {
      padding: 1rem;
      border-radius: 12px;
      background: #2c2d33;
      text-align: center;
      font-weight: 500;
      border-left: 6px solid #888;
      box-shadow: 0 2px 6px rgba(0,0,0,0.3);
      transition: background 0.3s, color 0.3s;
    }
    .kupuj { border-left-color: #2ecc71; }
    .sprzedaj { border-left-color: #e74c3c; }
    .neutral { border-left-color: #7f8c8d; }
    .sparkline {
      margin-top: 0.5rem;
      width: 100%;
    }
    .cena {
      font-size: 0.85rem;
      margin-top: 0.4rem;
      color: #aaa;
    }
    .nazwa {
      font-size: 0.9rem;
      margin-top: 0.2rem;
      color: #ccc;
    }
    @media (prefers-color-scheme: light) {
      body {
        background: #f5f5f5;
        color: #111;
      }
      h2, h1, h3, .opis, .nazwa, .cena {
        color: #222;
      }
      .reko {
        background: #fff;
        box-shadow: 0 1px 4px rgba(0,0,0,0.1);
      }
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
html += """
<div class='opis'>Strategia opiera się na porównaniu dwóch średnich kroczących:
 <strong>MA20</strong> (20-dniowa) i <strong>MA50</strong> (50-dniowa).
 Gdy MA20 przecina MA50 od dołu – to sygnał kupna. Gdy odwrotnie – sygnał sprzedaży.</div>
<div class='rekomendacje-grid'>
"""

for symbol in akcje:
    dane = yf.download(symbol, period="60d", interval="1d")
    typ, opis, cena = sprawdz_akcje(symbol)
    spark = generuj_sparkline(dane)
    pelna_nazwa = nazwy_spolek.get(symbol, symbol)
    cena_text = f"${cena:.2f}" if cena is not None else "brak danych"

    html += f"""
    <div class='reko {typ}'>
        <strong>{symbol}</strong>
        <div class='nazwa'>{pelna_nazwa}</div>
        <div>{opis}</div>
        <div class='cena'>Cena: {cena_text}</div>
        <img class='sparkline' src='data:image/png;base64,{spark}' alt='trend'>
    </div>
    """

html += "</div>" + stopka_html

with open("rekomendacje.html", "w", encoding="utf-8") as f:
    f.write(html)
