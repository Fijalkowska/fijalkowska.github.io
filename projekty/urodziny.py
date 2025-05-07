from datetime import datetime

data = input("Podaj swoją datę urodzin (RRRR-MM-DD): ")
urodziny = datetime.strptime(data, "%Y-%m-%d")
dzis = datetime.now()
roznica = urodziny.replace(year=dzis.year) - dzis

if roznica.days < 0:
    urodziny = urodziny.replace(year=dzis.year + 1)
    roznica = urodziny - dzis

print("Do Twoich urodzin zostało:", roznica.days, "dni!")
