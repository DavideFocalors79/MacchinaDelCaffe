import time
import tkinter as tk


# --------------------
# Costanti di sistema
# --------------------
PORTATA = 5                 # ml al secondo
ACQUA_MINIMA = 1000         # ml
CIALDE_MAX = 10
CIALDE_SCORTA_MAX = 50

# --------------------
# Classe Bevanda
# --------------------
class Bevanda:
    def __init__(self, nome, volume):
        self.nome = nome
        self.volume = volume

# --------------------
# Funzioni operative
# --------------------
def carica_cialde(cialde_disponibili):
    try:
        aggiunta = int(input("Quante cialde vuoi aggiungere? "))
    except ValueError:
        print("Input non valido.")
        return cialde_disponibili

    if aggiunta <= 0:
        print("Numero non valido.")
        return cialde_disponibili

    cialde_disponibili += aggiunta

    if cialde_disponibili > CIALDE_SCORTA_MAX:
        cialde_disponibili = CIALDE_SCORTA_MAX
        print(f"Hai raggiunto la capacità massima della scorta ({CIALDE_SCORTA_MAX} cialde).")

    print(f"Cialde caricate. Totale disponibili: {cialde_disponibili}")
    return cialde_disponibili

def carica_acqua(acqua_disponibile):
    try:
        aggiunta = int(input("Quanta acqua vuoi aggiungere (in ml)? "))
    except ValueError:
        print("Input non valido.")
        return acqua_disponibile

    if aggiunta <= 0:
        print("Quantità non valida.")
        return acqua_disponibile

    acqua_disponibile += aggiunta
    print(f"Acqua caricata. Totale ora: {acqua_disponibile / 1000:.2f} litri")
    return acqua_disponibile

def svuota_cialde():
    print("Serbatoio cialde svuotato.")
    return 0

def barra_avanzamento(secondi, messaggio):
    print(messaggio)
    for _ in range(secondi):
        print(">", end="", flush=True)
        time.sleep(1)
    print("\n")
   

# --------------------
# Funzione principale
# --------------------
def main():
    # Menu bevande
    menu = [
        Bevanda("Espresso", 50),
        Bevanda("Americano", 150),
        Bevanda("Ginseng", 50),
        Bevanda("Macchiato", 75),
        Bevanda("Cappuccino", 120),
        Bevanda("The", 200),
        Bevanda("Cioccolata", 200),
    ]

    cialde_disponibili = 10
    macchina_accesa = True
    caldaia_pronta = False
    acqua_disponibile = 2000  # ml
    cialde_usate = 0

    # Accensione
    print("Accensione macchina...")
    barra_avanzamento(3, "Riscaldamento caldaia in corso...")
    caldaia_pronta = True
    print("Macchina pronta all'uso!\n")

    # Ciclo principale
    while macchina_accesa:
        # Controlli preliminari
        if acqua_disponibile < ACQUA_MINIMA:
            print(f"Errore: acqua insufficiente! ({acqua_disponibile / 1000:.2f} litri)")
            break

        if cialde_disponibili <= 0:
            print("Errore: nessuna cialda disponibile.")
            continue

        if cialde_usate >= CIALDE_MAX:
            print(f"Errore: serbatoio cialde pieno ({cialde_usate}/{CIALDE_MAX})")
            continue

        if not caldaia_pronta:
            print("Caldaia non pronta.")
            break

        # Mostra menu
        print("\n--- Menu Bevande ---")
        for i, bevanda in enumerate(menu, start=1):
            print(f"{i}) {bevanda.nome} ({bevanda.volume} ml)")
        print("8) Carica acqua")
        print("9) Svuota cialde usate")
        print("10) Carica cialde nuove")
        print("11) Spegni macchina")

        try:
            scelta = int(input("Seleziona una bevanda: "))
        except ValueError:
            print("Input non valido.")
            continue

        # Gestione scelte extra
        if scelta == 8:
            acqua_disponibile = carica_acqua(acqua_disponibile)
            continue
        elif scelta == 9:
            cialde_usate = svuota_cialde()
            continue
        elif scelta == 10:
            cialde_disponibili = carica_cialde(cialde_disponibili)
            continue
        elif scelta == 11:
            print("Spegnimento macchina...")
            break

        # Selezione bevanda
        if 1 <= scelta <= len(menu):
            selezionata = menu[scelta - 1]
            print(f"Hai scelto: {selezionata.nome} ({selezionata.volume} ml)")
            tempo_erogazione = selezionata.volume // PORTATA
            barra_avanzamento(tempo_erogazione, "Preparazione in corso...")

            acqua_disponibile -= selezionata.volume
            cialde_usate += 1
            cialde_disponibili -= 1

            print(f"{selezionata.nome} pronta!")
            print(f"Acqua rimasta: {acqua_disponibile / 1000:.2f} litri | Cialde usate: {cialde_usate}/{CIALDE_MAX}")
        else:
            print("Scelta non valida.")

    print("Macchina spenta. Arrivederci!")

# --------------------
# Avvio programma
# --------------------
if __name__ == "__main__":
    main()
