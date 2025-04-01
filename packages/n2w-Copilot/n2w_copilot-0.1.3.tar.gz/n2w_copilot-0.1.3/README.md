# n2w_Copilot

n2w_Copilot è un modulo Python che converte numeri in parole. Supporta numeri fino a 15 cifre e include una modalità di test per verificare la conversione di numeri inseriti dall'utente. Utilizza dizionari per la conversione di numeri da 1 a 99 e gestisce le migliaia, milioni, miliardi, ecc.Questo progetto è un esempio di come creare e distribuire un pacchetto Python utilizzando `setuptools` e `wheel`.

## Funzionalità
- Conversione di numeri in parole
- Conversione di numeri in parole fino a 15 cifre.
- Modalità di test per verificare la conversione di numeri.
- Gestione di numeri con centinaia, decine e unità.
- Test automatici

## Installazione

```python
import n2w_Copilot

print (n2w_Copilot.num2words('123'))  # Output: one hundred twenty three