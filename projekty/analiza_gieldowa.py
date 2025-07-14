import csv
import sys
from statistics import mean, pstdev


def wczytaj_ceny(plik):
    """Wczytaj ceny zamknięcia z pliku CSV."""
    ceny = []
    with open(plik, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ceny.append(float(row["close"]))
    return ceny


def dzienne_zmiany(ceny):
    """Oblicz dzienne procentowe zmiany cen."""
    zmiany = []
    for i in range(1, len(ceny)):
        poprzednia = ceny[i - 1]
        aktualna = ceny[i]
        zmiany.append((aktualna - poprzednia) / poprzednia * 100)
    return zmiany


def analiza(plik):
    ceny = wczytaj_ceny(plik)
    zmiany = dzienne_zmiany(ceny)
    print("\nAnaliza wahań cen")
    print("Średnia dziennej zmiany: ", round(mean(zmiany), 2), "%")
    print("Odchylenie standardowe zmian: ", round(pstdev(zmiany), 2), "%")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Użycie: python analiza_gieldowa.py dane.csv")
    else:
        analiza(sys.argv[1])
