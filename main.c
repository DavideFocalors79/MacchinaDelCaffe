#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h> // per sleep()

#define PORTATA 5 // ml
#define ACQUA_MINIMA 1000 // ml (1 litro)
#define CIALDE_MAX 10 // capacità serbatoio cialde

// Struttura per bevande
typedef struct {
    char nome[20];
    int volume; // ml
} Bevanda;

// Funzione per barra di avanzamento
void barraAvanzamento(int secondi, const char* messaggio) {
    printf("%s\n", messaggio);
    for (int i = 0; i < secondi; i++) {
        printf(">");
        fflush(stdout);
        sleep(1);
    }
   printf("\n");
}

int main() {
// Menu bevande
Bevanda menu[] = {
    {"Espresso", 50},
    {"Americano", 150},
    {"Cappuccino", 120},
    {"The", 200}
};
int numBevande = sizeof(menu) / sizeof(menu[0]);

int macchinaAccesa = 0;
int caldaiaPronta = 0;
int acquaDisponibile = 2000; // ml
int cialdeUsate = 0;

int scelta;

// Avvio macchina
printf("Accensione macchina...\n");
macchinaAccesa = 1;
barraAvanzamento(3, "Riscaldamento caldaia in corso...");
caldaiaPronta = 1;
printf("Macchina pronta all'uso!\n\n");

while (1) {
// Controlli preliminari
if (acquaDisponibile < ACQUA_MINIMA) {
printf("Errore: acqua insufficiente! (%.2f litri)\n", acquaDisponibile / 1000.0);
break;
}
if (cialdeUsate >= CIALDE_MAX) {
printf("Errore: serbatoio cialde pieno (%d/%d)\n", cialdeUsate, CIALDE_MAX);
break;
}
if (!caldaiaPronta) {
printf("Caldaia non pronta.\n");
break;
}

// Mostra menu
printf("\n--- Menu Bevande ---\n");
for (int i = 0; i < numBevande; i++) {
printf("%d) %s (%d ml)\n", i + 1, menu[i].nome, menu[i].volume);
}
printf("0) Spegni macchina\n");
printf("Seleziona una bevanda: ");
scanf("%d", &scelta);

if (scelta == 0) {
printf("Spegnimento macchina...\n");
break;
}
if (scelta < 1 || scelta > numBevande) {
printf("Scelta non valida.\n");
continue;
}

Bevanda selezionata = menu[scelta - 1];
printf("Hai scelto: %s (%d ml)\n", selezionata.nome, selezionata.volume);

// Preparazione
int tempoErogazione = selezionata.volume / PORTATA;
barraAvanzamento(tempoErogazione, "Preparazione in corso...");
acquaDisponibile -= selezionata.volume;
cialdeUsate++;

printf("%s pronta!\n", selezionata.nome);
printf("Acqua rimasta: %.2f litri | Cialde usate: %d/%d\n",
acquaDisponibile / 1000.0, cialdeUsate, CIALDE_MAX);
}

printf("Macchina spenta. Arrivederci!\n");
return 0;
}