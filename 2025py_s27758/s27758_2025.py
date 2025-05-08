#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys  # import do wychodzenia z programu w przypadku krytycznego błędu
import random  # import do losowego wyboru nukleotydów i pozycji wstawienia imienia
import logging  # import modułu logowania do konsoli dla łatwiejszej diagnostyki
import datetime  # import do pobrania znacznika daty i czasu generacji sekwencji

"""
Program: Generator sekwencji DNA w formacie FASTA z wbudowanym imieniem w sekwencji - narzędzie bioinformatyczne do szybkiego tworzenia losowych sekwencji DNA do testów i analiz.
"""

# Konfiguracja logowania: tylko komunikaty od poziomu INFO
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Maksymalna długość wiersza w pliku FASTA – ułatwia ewentualną zmianę standardu zawijania
MAX_LINE_LENGTH = 80  # MODIFIED (aby łatwo dostosować szerokość wiersza FASTA bez szukania "magic number")

# Pobranie od użytkownika długości sekwencji z walidacją wejścia
# ORIGINAL:
# length = int(input("Podaj długość sekwencji: "))
# MODIFIED (walidacja dodatniej liczby całkowitej – zapobiega wprowadzeniu zera, wartości ujemnych lub nie‑liczb):
while True:
    try:
        length = int(input("Podaj długość sekwencji: "))  # odczyt i konwersja na int
        if length > 0:
            break  # warunek wyjścia przy poprawnej wartości
        else:
            print("Długość musi być większa od zera.")  # informacja dla użytkownika
    except ValueError:
        print("Proszę podać poprawną liczbę całkowitą.")  # obsługa nie‑liczbowego inputu

# Pobranie od użytkownika ID i opisu sekwencji
sequence_id = input("Podaj ID sekwencji: ")  # używane jako nazwa pliku i nagłówek FASTA
description = input("Podaj opis sekwencji: ")  # dowolny opis w nagłówku FASTA

# Pobranie imienia do wstawienia w sekwencji z walidacją liter
# ORIGINAL:
# name = input("Podaj imię: ")
# MODIFIED (sprawdzenie, że imię zawiera wyłącznie litery – eliminuje spacje, cyfry i znaki specjalne):
while True:
    name = input("Podaj imię: ")  # odczyt imienia
    if name.isalpha():  # walidacja literowa
        break  # akceptujemy dane
    else:
        print("Imię powinno zawierać tylko litery.")  # precyzyjna informacja o wymaganiach

# Definicja listy nukleotydów DNA
nucleotides = ['A', 'C', 'G', 'T']

# Generowanie losowej sekwencji nukleotydów o zadanej długości
sequence_list = [random.choice(nucleotides) for _ in range(length)]

# Wstawienie imienia w losowym miejscu sekwencji
insert_pos = random.randint(0, length)  # losowa pozycja w zakresie 0–length inclusive, aby każda pozycja była możliwa

# ORIGINAL:
# sequence_list.insert(insert_pos, name)
# MODIFIED (łączymy listę w string, by umożliwić łatwe dzielenie i wstawianie bez wielokrotnego wstawiania elementów listy):
sequence = ''.join(sequence_list)  # połączenie listy nukleotydów w jeden łańcuch
sequence = sequence[:insert_pos] + name + sequence[insert_pos:]  # wstawienie imienia bez zmiany indeksów list

# Przygotowanie zapisu do pliku FASTA z obsługą wyjątków
filename = f"{sequence_id}.fasta"  # nazwa pliku oparta na ID sekwencji

# ORIGINAL:
# with open(filename, 'w', encoding='utf-8') as file:
#     file.write(f">{sequence_id} {description}\n")
#     file.write(sequence)
# MODIFIED (dodanie daty generacji, zawijanie wierszy i obsługa błędów IO – poprawia czytelność i odporność na błędy):
try:
    with open(filename, 'w', encoding='utf-8') as file:
        header = (
            f">{sequence_id} {description} "
            f"(wygenerowano: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n"
        )  # dodatek znacznika czasu – ułatwia śledzenie historii pliku
        file.write(header)  # zapis nagłówka FASTA
        for i in range(0, len(sequence), MAX_LINE_LENGTH):
            file.write(sequence[i:i+MAX_LINE_LENGTH] + '\n')  # zawijanie co MAX_LINE_LENGTH znaków
    logging.info(f"Sekwencja została zapisana do pliku {filename}")  # informacja o powodzeniu operacji
except IOError as e:
    logging.error(f"Wystąpił błąd przy zapisie pliku: {e}")  # wyświetlenie komunikatu o błędzie IO
    sys.exit(1)  # zakończenie programu z kodem błędu

# Obliczanie statystyk sekwencji (pomijając wstawione imię)
seq_only = ''.join(ch for ch in sequence if ch in nucleotides)  # usuwamy litery imienia, pozostają tylko nukleotydy
counts = {n: seq_only.count(n) for n in nucleotides}  # zliczenie każdego typu nukleotydu
total = len(seq_only)  # całkowita liczba nucleotydów
percentages = {n: (counts[n] / total * 100) for n in nucleotides}  # procentowy udział każdego nukleotydu
cg_ratio = (counts['C'] + counts['G']) / (counts['A'] + counts['T']) * 100  # stosunek CG do AT w procentach

# Wyświetlanie statystyk w przejrzystym formacie
def print_stats():
    print("Statystyki sekwencji:")  # nagłówek sekcji
    for n in nucleotides:
        print(f"{n}: {percentages[n]:.1f}%")  # wypisanie procentu każdej zasady
    print(f"%CG: {cg_ratio:.1f}")  # wypisanie stosunku CG/AT

# Główna funkcja wywołująca statystyki
def main():
    print_stats()  # prezentacja wyników dla użytkownika

if __name__ == '__main__':
    main()  # uruchomienie programu
