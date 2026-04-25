# Dane początkowe zapisane na sztywno za pomocą list i słowników
ksiazki = [
    {"tytul": "Wiedzmin", "autor": "Andrzej Sapkowski", "sztuk": 3},
    {"tytul": "Lalka", "autor": "Boleslaw Prus", "sztuk": 1},
    {"tytul": "Dziady", "autor": "Adam Mickiewicz", "sztuk": 0},
    {"tytul": "Hobbit", "autor": "J.R.R. Tolkien", "sztuk": 5},
    {"tytul": "Rok 1984", "autor": "George Orwell", "sztuk": 2}
]

uzytkownicy = [
    {"login": "janek", "haslo": "haslo123", "rola": "czytelnik", "wypozyczenia": []},
    {"login": "ania", "haslo": "qwerty", "rola": "czytelnik", "wypozyczenia": []},
    {"login": "piotr", "haslo": "admin1", "rola": "czytelnik", "wypozyczenia": []}
]


def zaloguj(lista_uzytkownikow):
    # Funkcja obsługująca logowanie, daje maksymalnie 3 próby
    proby = 3
    while proby > 0:
        login = input("Podaj login: ")
        haslo = input("Podaj haslo: ")
        
        # Sprawdzanie czy dane pasują do kogoś na liście
        for uzytkownik in lista_uzytkownikow:
            if uzytkownik["login"] == login and uzytkownik["haslo"] == haslo:
                print(f"Zalogowano pomyslnie! Witaj, {login}.\n")
                return uzytkownik
                
        proby -= 1
        print(f"Bledne dane logowania. Pozostalo prob: {proby}\n")
        
    print("Wykorzystano wszystkie proby logowania. Zamykanie programu.")
    return None


def pokaz_katalog(lista_ksiazek):
    # Wyświetla wszystkie książki w bibliotece
    print("\n--- KATALOG BIBLIOTEKI ---")
    for ksiazka in lista_ksiazek:
        print(f"Tytul: '{ksiazka['tytul']}' | Autor: {ksiazka['autor']} | Dostepne sztuki: {ksiazka['sztuk']}")
    print("--------------------------\n")


def wypozycz_ksiazke(aktualny_uzytkownik, lista_ksiazek):
    # Logika wypożyczania ze sprawdzaniem dostępności
    tytul_do_wypozyczenia = input("Podaj tytul ksiazki, ktora chcesz wypozyczyc: ")
    
    for ksiazka in lista_ksiazek:
        # Zmieniamy na małe litery, żeby uniknąć problemów z wielkością liter wpisywanych przez usera
        if ksiazka["tytul"].lower() == tytul_do_wypozyczenia.lower():
            if ksiazka["sztuk"] > 0:
                ksiazka["sztuk"] -= 1
                aktualny_uzytkownik["wypozyczenia"].append(ksiazka["tytul"])
                print(f"Sukces! Wypozyczyles ksiazke: '{ksiazka['tytul']}'.\n")
            else:
                print(f"Niestety, ksiazka '{ksiazka['tytul']}' jest obecnie niedostepna (brak sztuk).\n")
            return
            
    print("Nie znaleziono takiej ksiazki w naszym katalogu.\n")


def pokaz_moje_wypozyczenia(aktualny_uzytkownik):
    # Wypisuje książki przypisane do danego czytelnika
    print("\n--- TWOJE WYPOZYCZENIA ---")
    lista_wypozyczen = aktualny_uzytkownik["wypozyczenia"]
    
    if len(lista_wypozyczen) == 0:
        print("Obecnie nie masz wypozyczonych zadnych ksiazek.")
    else:
        for tytul in lista_wypozyczen:
            print(f"- {tytul}")
    print("--------------------------\n")


def main():
    print("Witamy w systemie bibliotecznym!")
    
    # Próba zalogowania
    zalogowany_uzytkownik = zaloguj(uzytkownicy)
    
    # Jeśli funkcja zwróciła None, to znaczy że wyczerpano próby - kończymy działanie
    if zalogowany_uzytkownik is None:
        return
        
    # Główna pętla programu - menu
    while True:
        print("=== MENU GLOWNE ===")
        print("1. Przegladaj katalog")
        print("2. Wypozycz ksiazke")
        print("3. Moje wypozyczenia")
        print("4. Wyloguj")
        
        wybor = input("Wybierz opcje (1-4): ")
        
        if wybor == "1":
            pokaz_katalog(ksiazki)
        elif wybor == "2":
            wypozycz_ksiazke(zalogowany_uzytkownik, ksiazki)
        elif wybor == "3":
            pokaz_moje_wypozyczenia(zalogowany_uzytkownik)
        elif wybor == "4":
            print("Wylogowano pomyslnie. Do widzenia!")
            break
        else:
            print("Nieznana opcja. Wybierz cyfre od 1 do 4.\n")

# Uruchomienie programu
main()