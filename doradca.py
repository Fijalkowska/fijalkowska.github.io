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

# Pobierz pełne nazwy spółek (można rozbudować lub użyć API w przyszłości)
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
    ma20 = ostatni['MA20'].item() if not pd.isna(ostatni['MA20'].item()) else None
    ma50 = ostatni['MA50'].item() if not pd.isna(ostatni['MA50'].item()) else None
    cena = ostatni['Close'].item() if not pd.isna(ostatni['Close'].item()) else None

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
<html lang="pl">
<head>
  <meta charset="UTF-8">
  <title>Rekomendacje</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
  <style>
    body {
      font-family: 'Inter', sans-serif;
      font-size: 15px;
      margin: 0;
      padding: 1rem;
      background: #1b1c1f;
      color: #eee;
    }
    h2 {
      font-size: 1.3rem;
      margin-bottom: 0.8rem;
    }
    .opis {
      font-size: 0.9rem;
      margin-bottom: 1.5rem;
      color: #ccc;
    }
    .rekomendacje-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 1rem;
    }
    .reko {
      padding: 1rem;
      border-radius: 10px;
      background: #2a2b2f;
      text-align: center;
      font-weight: 500;
      box-shadow: 0 1px 3px rgba(0,0,0,0.2);
    }
    .kupuj { border-left: 5px solid #2ecc71; }
    .sprzedaj { border-left: 5px solid #e74c3c; }
    .neutral { border-left: 5px solid #7f8c8d; }
    .sparkline {
      margin-top: 0.5rem;
      width: 100%;
    }
    .cena {
      font-size: 0.85rem;
      margin-top: 0.2rem;
      color: #aaa;
    }
    .nazwa {
      font-size: 0.9rem;
      margin-top: 0.2rem;
      color: #ccc;
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
<div class='opis'>Analiza opiera się na porównaniu dwóch średnich kroczących:
 <strong>MA20</strong> (średnia z ostatnich 20 dni) i <strong>MA50</strong> (średnia z 50 dni).
 Gdy MA20 przebija MA50 z dołu – sugeruje trend wzrostowy. Odwrotnie – sygnał spadkowy.</div>
<div class='rekomendacje-grid'>
"""

for symbol in akcje:
    dane = yf.download(symbol, period="60d", interval="1d")
    typ, opis, cena = sprawdz_akcje(symbol)
    spark = generuj_sparkline(dane)
    pelna_nazwa = nazwy_spolek.get(symbol, symbol)
    html += f"""
    <div class='reko {typ}'>
        <strong>{symbol}</strong>
        <div class='nazwa'>{pelna_nazwa}</div>
        <div>{opis}</div>
        <div class='cena'>Cena: ${cena:.2f}</div>
        <img class='sparkline' src='data:image/png;base64,{spark}' alt='trend'>
    </div>
    """

html += "</div>" + stopka_html

with open("rekomendacje.html", "w", encoding="utf-8") as f:
    f.write(html)
