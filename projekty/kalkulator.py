def kalkulator(a, b, dzialanie):
    if dzialanie == "+":
        return a + b
    elif dzialanie == "-":
        return a - b
    elif dzialanie == "*":
        return a * b
    elif dzialanie == "/":
        return a / b
    else:
        return "Nieznana operacja"

print(kalkulator(4, 2, "*"))
