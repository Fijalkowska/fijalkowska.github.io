import yfinance as yf
import pandas as pd
from datetime import date

def sprawdz_akcje(symbol: str):
    dane = yf.download(symbol, period="60d", interval="1d")
    dane['MA20'] = dane['Close'].rolling(window=20).mean()
    dane['MA50'] = dane['Close'].rolling(window=50).mean()

    ostatni = dane.tail(1).iloc[0]  # Bezpieczny sposób pobrania ostatniego wiersza

    # Zabezpieczenie przed brakiem danych
    if pd.isna(ostatni['MA20']) or pd.isna(ostatni['MA50']):
        return "⚪ ZBYT MAŁO DANYCH"

    if float(ostatni['MA20']) > float(ostatni['MA50']):
        return "🟢 KUP (MA20 > MA50)"
    elif float(ostatni['MA20']) < float(ostatni['MA50']):
        return "🔴 SPRZEDAJ (MA20 < MA50)"
    else:
        return "⚪ NIC NIE RÓB (MA20 ≈ MA50)"

# Lista spółek
akcje = ['AAPL', 'TSLA', 'MSFT']

# Generuj rekomendacje
html = f"<h2>Rekomendacje inwestycyjne – {date.today().strftime('%d.%m.%Y')}</h2><ul>"
for symbol in akcje:
    decyzja = sprawdz_akcje(symbol)
    html += f"<li><strong>{symbol}:</strong> {decyzja}</li>"
html += "</ul>"

# Zapisz do pliku
with open("rekomendacje.html", "w", encoding="utf-8") as f:
    f.write(html)
