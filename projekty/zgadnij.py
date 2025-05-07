import random

tajna = random.randint(1, 10)
proba = int(input("Zgadnij liczbę od 1 do 10: "))

if proba == tajna:
    print("Brawo, zgadłeś!")
else:
    print("Nie tym razem. To była", tajna)
