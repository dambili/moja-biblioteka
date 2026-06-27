class Book:
    def __init__(self, tytul, autor, liczba_sztuk):
        self.tytul = tytul
        self.autor = autor
        self.liczba_sztuk = liczba_sztuk
        self._dostepne_sztuki = liczba_sztuk

    @property
    def dostepne_sztuki(self):
        return self._dostepne_sztuki

    def wypozycz(self):
        if self._dostepne_sztuki > 0:
            self._dostepne_sztuki -= 1
            return True
        return False

    def oddaj(self):
        if self._dostepne_sztuki < self.liczba_sztuk:
            self._dostepne_sztuki += 1
            return True
        return False

    def __str__(self):
        return f"Tytul: '{self.tytul}' | Autor: {self.autor} | Dostepne sztuki: {self.dostepne_sztuki}"


class User:
    def __init__(self, login, haslo, rola):
        self.login = login
        self._haslo = haslo
        self.rola = rola

    def sprawdz_haslo(self, haslo):
        return self._haslo == haslo

    def pokaz_menu(self):
        raise NotImplementedError("Ta metoda powinna byc nadpisana w klasie potomnej.")


class Reader(User):
    def __init__(self, login, haslo):
        super().__init__(login, haslo, "czytelnik")
        self.wypozyczenia = []
        self.prosby_o_przedluzenie = []

    def pokaz_menu(self):
        print("=== MENU CZYTELNIKA ===")
        print("1. Przegladaj katalog")
        print("2. Wypozycz ksiazke")
        print("3. Oddaj ksiazke")
        print("4. Moje wypozyczenia")
        print("5. Popros o przedluzenie")
        print("6. Wyloguj")


class Librarian(User):
    def __init__(self, login, haslo):
        super().__init__(login, haslo, "bibliotekarz")

    def pokaz_menu(self):
        print("=== MENU BIBLIOTEKARZA ===")
        print("1. Przegladaj katalog")
        print("2. Pokaz wszystkie wypozyczenia")
        print("3. Pokaz prosby o przedluzenie")
        print("4. Zaakceptuj prosbe")
        print("5. Odrzuc prosbe")
        print("6. Wyloguj")


class Library:
    def __init__(self):
        self.ksiazki = []
        self.uzytkownicy = []
        self.prosby_o_przedluzenie = []

    def dodaj_ksiazke(self, ksiazka):
        self.ksiazki.append(ksiazka)

    def dodaj_uzytkownika(self, uzytkownik):
        self.uzytkownicy.append(uzytkownik)

    def znajdz_ksiazke(self, tytul):
        for ksiazka in self.ksiazki:
            if ksiazka.tytul.lower() == tytul.lower():
                return ksiazka
        return None

    def zaloguj(self):
        proby = 3

        while proby > 0:
            login = input("Podaj login: ")
            haslo = input("Podaj haslo: ")

            for uzytkownik in self.uzytkownicy:
                if uzytkownik.login == login and uzytkownik.sprawdz_haslo(haslo):
                    print(f"Zalogowano pomyslnie! Witaj, {login}.\n")
                    return uzytkownik

            proby -= 1
            print(f"Bledne dane logowania. Pozostalo prob: {proby}\n")

        print("Wykorzystano wszystkie proby logowania.")
        return None

    def pokaz_katalog(self):
        print("\n--- KATALOG BIBLIOTEKI ---")

        for ksiazka in self.ksiazki:
            print(ksiazka)

        print("--------------------------\n")

    def wypozycz_ksiazke(self, czytelnik):
        tytul = input("Podaj tytul ksiazki, ktora chcesz wypozyczyc: ")
        ksiazka = self.znajdz_ksiazke(tytul)

        if ksiazka is None:
            print("Nie znaleziono takiej ksiazki w katalogu.\n")
            return

        if ksiazka in czytelnik.wypozyczenia:
            print("Masz juz wypozyczona te ksiazke.\n")
            return

        if ksiazka.wypozycz():
            czytelnik.wypozyczenia.append(ksiazka)
            print(f"Sukces! Wypozyczyles ksiazke: '{ksiazka.tytul}'.\n")
        else:
            print(f"Niestety, ksiazka '{ksiazka.tytul}' jest obecnie niedostepna.\n")

    def oddaj_ksiazke(self, czytelnik):
        if len(czytelnik.wypozyczenia) == 0:
            print("Nie masz zadnych ksiazek do oddania.\n")
            return

        self.pokaz_wypozyczenia_czytelnika(czytelnik)

        tytul = input("Podaj tytul ksiazki, ktora chcesz oddac: ")

        for ksiazka in czytelnik.wypozyczenia:
            if ksiazka.tytul.lower() == tytul.lower():
                czytelnik.wypozyczenia.remove(ksiazka)
                ksiazka.oddaj()
                print(f"Oddano ksiazke: '{ksiazka.tytul}'.\n")
                return

        print("Nie masz wypozyczonej takiej ksiazki.\n")

    def pokaz_wypozyczenia_czytelnika(self, czytelnik):
        print("\n--- TWOJE WYPOZYCZENIA ---")

        if len(czytelnik.wypozyczenia) == 0:
            print("Obecnie nie masz wypozyczonych zadnych ksiazek.")
        else:
            for ksiazka in czytelnik.wypozyczenia:
                print(f"- {ksiazka.tytul} ({ksiazka.autor})")

        print("--------------------------\n")

    def popros_o_przedluzenie(self, czytelnik):
        if len(czytelnik.wypozyczenia) == 0:
            print("Nie masz wypozyczonych ksiazek, wiec nie mozesz poprosic o przedluzenie.\n")
            return

        self.pokaz_wypozyczenia_czytelnika(czytelnik)

        tytul = input("Podaj tytul ksiazki do przedluzenia: ")

        for ksiazka in czytelnik.wypozyczenia:
            if ksiazka.tytul.lower() == tytul.lower():
                for prosba in self.prosby_o_przedluzenie:
                    if prosba["czytelnik"] == czytelnik and prosba["ksiazka"] == ksiazka:
                        print("Taka prosba juz zostala wyslana.\n")
                        return

                prosba = {
                    "czytelnik": czytelnik,
                    "ksiazka": ksiazka
                }

                self.prosby_o_przedluzenie.append(prosba)
                czytelnik.prosby_o_przedluzenie.append(prosba)

                print(f"Wyslano prosbe o przedluzenie ksiazki: '{ksiazka.tytul}'.\n")
                return

        print("Nie masz wypozyczonej takiej ksiazki.\n")

    def pokaz_wszystkie_wypozyczenia(self):
        print("\n--- WSZYSTKIE WYPOZYCZENIA ---")

        znaleziono = False

        for uzytkownik in self.uzytkownicy:
            if isinstance(uzytkownik, Reader) and len(uzytkownik.wypozyczenia) > 0:
                znaleziono = True
                print(f"{uzytkownik.login}:")
                for ksiazka in uzytkownik.wypozyczenia:
                    print(f"- {ksiazka.tytul}")

        if not znaleziono:
            print("Brak aktywnych wypozyczen.")

        print("------------------------------\n")

    def pokaz_prosby_o_przedluzenie(self):
        print("\n--- PROSBY O PRZEDLUZENIE ---")

        if len(self.prosby_o_przedluzenie) == 0:
            print("Brak prosb o przedluzenie.")
        else:
            for numer, prosba in enumerate(self.prosby_o_przedluzenie, start=1):
                czytelnik = prosba["czytelnik"]
                ksiazka = prosba["ksiazka"]
                print(f"{numer}. {czytelnik.login} prosi o przedluzenie ksiazki: '{ksiazka.tytul}'")

        print("-----------------------------\n")

    def wybierz_prosbe(self):
        if len(self.prosby_o_przedluzenie) == 0:
            print("Brak prosb do obsluzenia.\n")
            return None

        self.pokaz_prosby_o_przedluzenie()

        try:
            numer = int(input("Podaj numer prosby: "))
        except ValueError:
            print("Podano niepoprawny numer.\n")
            return None

        if numer < 1 or numer > len(self.prosby_o_przedluzenie):
            print("Nie ma prosby o takim numerze.\n")
            return None

        return self.prosby_o_przedluzenie[numer - 1]

    def zaakceptuj_prosbe(self):
        prosba = self.wybierz_prosbe()

        if prosba is None:
            return

        czytelnik = prosba["czytelnik"]
        ksiazka = prosba["ksiazka"]

        self.prosby_o_przedluzenie.remove(prosba)

        if prosba in czytelnik.prosby_o_przedluzenie:
            czytelnik.prosby_o_przedluzenie.remove(prosba)

        print(f"Zaakceptowano prosbe uzytkownika {czytelnik.login} dla ksiazki '{ksiazka.tytul}'.\n")

    def odrzuc_prosbe(self):
        prosba = self.wybierz_prosbe()

        if prosba is None:
            return

        czytelnik = prosba["czytelnik"]
        ksiazka = prosba["ksiazka"]

        self.prosby_o_przedluzenie.remove(prosba)

        if prosba in czytelnik.prosby_o_przedluzenie:
            czytelnik.prosby_o_przedluzenie.remove(prosba)

        print(f"Odrzucono prosbe uzytkownika {czytelnik.login} dla ksiazki '{ksiazka.tytul}'.\n")

    def menu_czytelnika(self, czytelnik):
        while True:
            czytelnik.pokaz_menu()
            wybor = input("Wybierz opcje (1-6): ")

            if wybor == "1":
                self.pokaz_katalog()
            elif wybor == "2":
                self.wypozycz_ksiazke(czytelnik)
            elif wybor == "3":
                self.oddaj_ksiazke(czytelnik)
            elif wybor == "4":
                self.pokaz_wypozyczenia_czytelnika(czytelnik)
            elif wybor == "5":
                self.popros_o_przedluzenie(czytelnik)
            elif wybor == "6":
                print("Wylogowano pomyslnie.\n")
                break
            else:
                print("Nieznana opcja. Wybierz cyfre od 1 do 6.\n")

    def menu_bibliotekarza(self, bibliotekarz):
        while True:
            bibliotekarz.pokaz_menu()
            wybor = input("Wybierz opcje (1-6): ")

            if wybor == "1":
                self.pokaz_katalog()
            elif wybor == "2":
                self.pokaz_wszystkie_wypozyczenia()
            elif wybor == "3":
                self.pokaz_prosby_o_przedluzenie()
            elif wybor == "4":
                self.zaakceptuj_prosbe()
            elif wybor == "5":
                self.odrzuc_prosbe()
            elif wybor == "6":
                print("Wylogowano pomyslnie.\n")
                break
            else:
                print("Nieznana opcja. Wybierz cyfre od 1 do 6.\n")


def przygotuj_biblioteke():
    biblioteka = Library()

    biblioteka.dodaj_ksiazke(Book("Wiedzmin", "Andrzej Sapkowski", 3))
    biblioteka.dodaj_ksiazke(Book("Lalka", "Boleslaw Prus", 1))
    biblioteka.dodaj_ksiazke(Book("Dziady", "Adam Mickiewicz", 0))
    biblioteka.dodaj_ksiazke(Book("Hobbit", "J.R.R. Tolkien", 5))
    biblioteka.dodaj_ksiazke(Book("Rok 1984", "George Orwell", 2))

    biblioteka.dodaj_uzytkownika(Reader("janek", "haslo123"))
    biblioteka.dodaj_uzytkownika(Reader("ania", "qwerty"))
    biblioteka.dodaj_uzytkownika(Reader("piotr", "admin1"))

    biblioteka.dodaj_uzytkownika(Librarian("admin", "admin"))

    return biblioteka


def main():
    biblioteka = przygotuj_biblioteke()

    print("Witamy w systemie bibliotecznym!")

    while True:
        print("=== SYSTEM BIBLIOTEKI ===")
        print("1. Zaloguj")
        print("2. Zakoncz")

        wybor = input("Wybierz opcje (1-2): ")

        if wybor == "1":
            zalogowany_uzytkownik = biblioteka.zaloguj()

            if zalogowany_uzytkownik is None:
                continue

            if isinstance(zalogowany_uzytkownik, Reader):
                biblioteka.menu_czytelnika(zalogowany_uzytkownik)
            elif isinstance(zalogowany_uzytkownik, Librarian):
                biblioteka.menu_bibliotekarza(zalogowany_uzytkownik)

        elif wybor == "2":
            print("Zamykanie programu. Do widzenia!")
            break
        else:
            print("Nieznana opcja. Wybierz 1 albo 2.\n")


if __name__ == "__main__":
    main()