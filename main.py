import time
import tkinter as tk
from tkinter import messagebox

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
# Interfaccia grafica
# --------------------
class MacchinaCaffeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Macchina Caffè")

        self.menu = [
            Bevanda("Espresso", 50),
            Bevanda("Americano", 150),
            Bevanda("Ginseng", 50),
            Bevanda("Macchiato", 75),
            Bevanda("Cappuccino", 120),
            Bevanda("The", 200),
            Bevanda("Cioccolata", 200),
        ]

        self.cialde_disponibili = 10
        self.cialde_usate = 0
        self.acqua_disponibile = 2000  # ml
        self.caldaia_pronta = False
        self.macchina_accesa = True

        self.crea_widget()
        self.riscalda_caldaia()

    def crea_widget(self):
        # Frame stato
        self.frame_stato = tk.Frame(self.root)
        self.frame_stato.pack(pady=10)

        self.lbl_acqua = tk.Label(self.frame_stato, text=f"Acqua: {self.acqua_disponibile / 1000:.2f} L")
        self.lbl_acqua.grid(row=0, column=0, padx=10)
        self.lbl_cialde_disp = tk.Label(self.frame_stato, text=f"Cialde disponibili: {self.cialde_disponibili}")
        self.lbl_cialde_disp.grid(row=0, column=1, padx=10)
        self.lbl_cialde_usate = tk.Label(self.frame_stato, text=f"Cialde usate: {self.cialde_usate}/{CIALDE_MAX}")
        self.lbl_cialde_usate.grid(row=0, column=2, padx=10)
        self.lbl_stato = tk.Label(self.frame_stato, text="Macchina: Spenta")
        self.lbl_stato.grid(row=0, column=3, padx=10)

        # Frame menu bevande
        self.frame_menu = tk.Frame(self.root)
        self.frame_menu.pack(pady=10)

        self.btn_bevande = []
        for i, bevanda in enumerate(self.menu):
            btn = tk.Button(self.frame_menu, text=f"{bevanda.nome} ({bevanda.volume} ml)", width=20,
                            command=lambda b=bevanda: self.prepara_bevanda(b))
            btn.grid(row=i//2, column=i%2, padx=5, pady=5)
            self.btn_bevande.append(btn)

        # Frame operazioni extra
        self.frame_extra = tk.Frame(self.root)
        self.frame_extra.pack(pady=10)

        self.btn_carica_acqua = tk.Button(self.frame_extra, text="Carica Acqua", command=self.carica_acqua_popup)
        self.btn_carica_acqua.grid(row=0, column=0, padx=5)

        self.btn_svuota_cialde = tk.Button(self.frame_extra, text="Svuota Cialde Usate", command=self.svuota_cialde)
        self.btn_svuota_cialde.grid(row=0, column=1, padx=5)

        self.btn_carica_cialde = tk.Button(self.frame_extra, text="Carica Cialde Nuove", command=self.carica_cialde_popup)
        self.btn_carica_cialde.grid(row=0, column=2, padx=5)

        self.btn_spegni = tk.Button(self.root, text="Spegni Macchina", command=self.spegni_macchina, fg="red")
        self.btn_spegni.pack(pady=10)

        # Barra di avanzamento (label)
        self.lbl_progress = tk.Label(self.root, text="")
        self.lbl_progress.pack()

    def riscalda_caldaia(self):
        self.lbl_stato.config(text="Riscaldamento caldaia...")
        self.root.after(3000, self.caldaia_pronta_funzione)

    def caldaia_pronta_funzione(self):
        self.caldaia_pronta = True
        self.lbl_stato.config(text="Macchina pronta all'uso!")

    def aggiorna_stato(self):
        self.lbl_acqua.config(text=f"Acqua: {self.acqua_disponibile / 1000:.2f} L")
        self.lbl_cialde_disp.config(text=f"Cialde disponibili: {self.cialde_disponibili}")
        self.lbl_cialde_usate.config(text=f"Cialde usate: {self.cialde_usate}/{CIALDE_MAX}")

    def prepara_bevanda(self, bevanda):
        if not self.macchina_accesa:
            messagebox.showwarning("Attenzione", "La macchina è spenta.")
            return
        if self.acqua_disponibile < ACQUA_MINIMA:
            messagebox.showerror("Errore", "Acqua insufficiente!")
            return
        if self.cialde_disponibili <= 0:
            messagebox.showerror("Errore", "Nessuna cialda disponibile!")
            return
        if self.cialde_usate >= CIALDE_MAX:
            messagebox.showerror("Errore", "Serbatoio cialde usate pieno! Svuotalo.")
            return
        if not self.caldaia_pronta:
            messagebox.showerror("Errore", "Caldaia non pronta!")
            return
        if bevanda.volume > self.acqua_disponibile:
            messagebox.showerror("Errore", "Non c'è abbastanza acqua per questa bevanda!")
            return

        self.lbl_stato.config(text=f"Preparazione {bevanda.nome}...")
        self.disabilita_bottoni()
        tempo_erogazione = bevanda.volume // PORTATA
        self.progress_count = 0
        self.progress_max = tempo_erogazione
        self.prepara_step(bevanda)

    def prepara_step(self, bevanda):
        if self.progress_count < self.progress_max:
            self.lbl_progress.config(text="Preparazione: " + ">" * (self.progress_count + 1))
            self.progress_count += 1
            self.root.after(1000, lambda: self.prepara_step(bevanda))
        else:
            self.acqua_disponibile -= bevanda.volume
            self.cialde_usate += 1
            self.cialde_disponibili -= 1
            self.lbl_progress.config(text="")
            self.lbl_stato.config(text=f"{bevanda.nome} pronta!")
            self.aggiorna_stato()
            self.abilita_bottoni()

    def disabilita_bottoni(self):
        for btn in self.btn_bevande:
            btn.config(state=tk.DISABLED)
        self.btn_carica_acqua.config(state=tk.DISABLED)
        self.btn_svuota_cialde.config(state=tk.DISABLED)
        self.btn_carica_cialde.config(state=tk.DISABLED)
        self.btn_spegni.config(state=tk.DISABLED)

    def abilita_bottoni(self):
        for btn in self.btn_bevande:
            btn.config(state=tk.NORMAL)
        self.btn_carica_acqua.config(state=tk.NORMAL)
        self.btn_svuota_cialde.config(state=tk.NORMAL)
        self.btn_carica_cialde.config(state=tk.NORMAL)
        self.btn_spegni.config(state=tk.NORMAL)

    def carica_acqua_popup(self):
        if not self.macchina_accesa:
            messagebox.showwarning("Attenzione", "La macchina è spenta.")
            return

        def conferma():
            try:
                aggiunta = int(entry.get())
                if aggiunta <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Errore", "Inserisci un numero valido (positivo).")
                return
            self.acqua_disponibile += aggiunta
            messagebox.showinfo("Info", f"Acqua caricata. Totale ora: {self.acqua_disponibile / 1000:.2f} litri")
            self.aggiorna_stato()
            popup.destroy()

        popup = tk.Toplevel(self.root)
        popup.title("Carica Acqua")
        tk.Label(popup, text="Quanti ml di acqua vuoi aggiungere?").pack(padx=10, pady=10)
        entry = tk.Entry(popup)
        entry.pack(padx=10, pady=5)
        tk.Button(popup, text="Conferma", command=conferma).pack(pady=10)

    def carica_cialde_popup(self):
        if not self.macchina_accesa:
            messagebox.showwarning("Attenzione", "La macchina è spenta.")
            return

        def conferma():
            try:
                aggiunta = int(entry.get())
                if aggiunta <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Errore", "Inserisci un numero valido (positivo).")
                return

            self.cialde_disponibili += aggiunta
            if self.cialde_disponibili > CIALDE_SCORTA_MAX:
                self.cialde_disponibili = CIALDE_SCORTA_MAX
                messagebox.showinfo("Info", f"Hai raggiunto la capacità massima della scorta ({CIALDE_SCORTA_MAX} cialde).")

            messagebox.showinfo("Info", f"Cialde caricate. Totale disponibili: {self.cialde_disponibili}")
            self.aggiorna_stato()
            popup.destroy()

        popup = tk.Toplevel(self.root)
        popup.title("Carica Cialde")
        tk.Label(popup, text="Quante cialde vuoi aggiungere?").pack(padx=10, pady=10)
        entry = tk.Entry(popup)
        entry.pack(padx=10, pady=5)
        tk.Button(popup, text="Conferma", command=conferma).pack(pady=10)

    def svuota_cialde(self):
        if not self.macchina_accesa:
            messagebox.showwarning("Attenzione", "La macchina è spenta.")
            return

        self.cialde_usate = 0
        messagebox.showinfo("Info", "Serbatoio cialde usate svuotato.")
        self.aggiorna_stato()

    def spegni_macchina(self):
        if messagebox.askyesno("Conferma", "Vuoi davvero spegnere la macchina?"):
            self.macchina_accesa = False
            self.lbl_stato.config(text="Macchina spenta.")
            self.disabilita_bottoni()
            self.lbl_progress.config(text="")
            messagebox.showinfo("Info", "Macchina spenta. Arrivederci!")

# --------------------
# Avvio programma
# --------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = MacchinaCaffeApp(root)
    root.mainloop()
