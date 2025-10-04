#include <stdlib.h>
#include <string.h>
#include <unistd.h> // Per la funzione sleep()
#include <stdio.h>  // Necessario per printf/scanf

// --------------------
// Costanti di sistema
// --------------------

#define PORTATA 5           // Portata della macchina: 5 ml al secondo
#define ACQUA_MINIMA 1000   // Soglia minima di acqua disponibile: 1000 ml (1 litro)
#define CIALDE_MAX 10 
#define CIALDE_SCORTA_MAX 50 // massima scorta disponibile



// --------------------
// Struttura per una bevanda
// --------------------
typedef struct {
    char nome[20];     // Nome della bevanda
    int volume;        // Volume della bevanda in ml
} Bevanda;

// --------------------
// Funzione per caricare le cialde nuove
// --------------------
void caricaCialde(int* cialdeDisponibili) {
    int aggiunta;
    printf("Quante cialde vuoi aggiungere? ");
    scanf("%d", &aggiunta);

    if (aggiunta <= 0) {
        printf("Numero non valido.\n");
        return;
    }

    *cialdeDisponibili += aggiunta;

    if (*cialdeDisponibili > CIALDE_SCORTA_MAX) {
        *cialdeDisponibili = CIALDE_SCORTA_MAX;
        printf("Hai raggiunto la capacità massima della scorta (%d cialde).\n", CIALDE_SCORTA_MAX);
    }

    printf("Cialde caricate. Totale disponibili: %d\n", *cialdeDisponibili);
}


// --------------------
// Funzione per caricare acqua
// --------------------
void caricaAcqua(int* acquaDisponibile) {
    int aggiunta;
    printf("Quanta acqua vuoi aggiungere (in ml)? ");
    scanf("%d", &aggiunta);

    if (aggiunta <= 0) {
        printf("Quantità non valida.\n");
        return;
    }

    *acquaDisponibile += aggiunta;
    printf("Acqua caricata. Totale ora: %.2f litri\n", *acquaDisponibile / 1000.0);
}

// --------------------
// Funzione per svuotare serbatoio cialde
// --------------------
void svuotaCialde(int* cialdeUsate) {
    *cialdeUsate = 0;
    printf("Serbatoio cialde svuotato.\n");
}

// --------------------
// Funzione per la barra di avanzamento
// Simula il progresso con una barra che avanza ogni secondo
// --------------------
void barraAvanzamento(int secondi, const char* messaggio) {
    printf("%s\n", messaggio);
    for (int i = 0; i < secondi; i++) {
        printf(">");
        fflush(stdout); // Forza la stampa immediata su console
        sleep(1);       // Pausa di 1 secondo
    }
    printf("\n");
}

// --------------------
// Funzione principale
// --------------------
int main() {
    // --------------------
    // Inizializzazione del menu bevande
    // --------------------
    Bevanda menu[] = {
        {"Espresso", 50},
        {"Americano", 150},
        {"Ginseng", 50},
        {"Macchiato", 75},
        {"Cappuccino", 120},
        {"The", 200},
        {"Cioccolata", 200},
    };
    int numBevande = sizeof(menu) / sizeof(menu[0]);

    // --------------------
    // Variabili di stato della macchina
    // --------------------
    int cialdeDisponibili = 10;   // Capacità massima del serbatoio di cialde usate
    int macchinaAccesa = 0;       // Stato macchina: 0 = spenta, 1 = accesa
    int caldaiaPronta = 0;        // Stato caldaia: 0 = non pronta, 1 = pronta
    int acquaDisponibile = 2000;  // Acqua disponibile (in ml), inizialmente 2 litri
    int cialdeUsate = 0;          // Conteggio cialde usate

    int scelta;                   // Variabile per memorizzare la scelta utente

    // --------------------
    // Accensione macchina
    // --------------------
    printf("Accensione macchina...\n");
    macchinaAccesa = 1;
    barraAvanzamento(3, "Riscaldamento caldaia in corso...");
    caldaiaPronta = 1;
    printf("Macchina pronta all'uso!\n\n");

    // --------------------
    // Ciclo principale della macchina
    // --------------------
    while (1) {
        // Controlli preliminari
        if (acquaDisponibile < ACQUA_MINIMA) {
            printf("Errore: acqua insufficiente! (%.2f litri)\n", acquaDisponibile / 1000.0);
            break;
        }

        if (cialdeDisponibili <= 0) {
            printf("Errore: nessuna cialda disponibile.\n");
            continue;
        }

        if (cialdeUsate >= CIALDE_MAX) {
            printf("Errore: serbatoio cialde pieno (%d/%d)\n", cialdeUsate, CIALDE_MAX);
            continue;
        }

        if (!caldaiaPronta) {
            printf("Caldaia non pronta.\n");
            break;
        }

        // --------------------
        // Mostra il menu delle bevande
        // --------------------
        printf("\n--- Menu Bevande ---\n");
        for (int i = 0; i < numBevande; i++) {
            printf("%d) %s (%d ml)\n", i + 1, menu[i].nome, menu[i].volume);
        }
    
        printf("8) carica Aqcua\n");
        printf("9) svuota cialde\n");
        printf("10) Carica cialde nuove\n");
        printf("11) Spegni macchina\n");
        printf("Seleziona una bevanda: ");
        scanf("%d", &scelta);

        // --------------------
        // Gestione della scelta utente
        // --------------------

         // Gestione ricarica acqua
        if (scelta == 8) {
            caricaAcqua(&acquaDisponibile);
            continue;
        }

        // Gestione svuotamento cialde usate
        if (scelta == 9) {
            svuotaCialde(&cialdeUsate);
            continue;
        }
        if (scelta == 10) {
            caricaCialde(&cialdeDisponibili);
            continue;
        }

        if (scelta == 11) {
            printf("Spegnimento macchina...\n");
            break;
        }

        if (scelta < 1 || scelta > numBevande) {
            printf("Scelta non valida.\n");
            continue;
        }

        // --------------------
        // Preparazione della bevanda scelta
        // --------------------
        Bevanda selezionata = menu[scelta - 1];
        printf("Hai scelto: %s (%d ml)\n", selezionata.nome, selezionata.volume);

        // Calcolo del tempo di erogazione in base al volume e portata
        int tempoErogazione = selezionata.volume / PORTATA;

        // Simulazione preparazione
        barraAvanzamento(tempoErogazione, "Preparazione in corso...");

        // Aggiornamento stato macchina
        acquaDisponibile -= selezionata.volume;
        cialdeUsate++;

        printf("%s pronta!\n", selezionata.nome);
        printf("Acqua rimasta: %.2f litri | Cialde usate: %d/%d\n",
               acquaDisponibile / 1000.0, cialdeUsate, CIALDE_MAX);
    }

    // --------------------
    // Spegnimento della macchina
    // --------------------
    printf("Macchina spenta. Arrivederci!\n");
    return 0;
}