import anthropic
import csv
import json
from pathlib import Path

CARTELLA = Path(__file__).parent  # la cartella dove si trova questo script

ETICHETTE = ["costi", "personale", "credito", "domanda", "burocrazia", "altro"]

ISTRUZIONI = """Classifica la risposta di un questionario alla domanda:
"Qual è la maggior difficoltà che ha riscontrato nella sua azienda nell'ultimo anno?"
Scegli UNA sola etichetta. Se la risposta cita più difficoltà, vale la prima citata.

costi: aumento di energia, materie prime, trasporti, carburanti, affitti, ricambi o altri costi di produzione.
personale: difficoltà a trovare, assumere, formare o trattenere dipendenti, o mancanza di competenze nel team.
credito: prestiti e fidi negati, ritardi di pagamento dei clienti, problemi di liquidità.
domanda: calo di ordini, clienti, vendite o fatturato, anche per la concorrenza.
burocrazia: adempimenti, permessi, normative, fisco, certificazioni, controlli.
altro: nessuna difficoltà, cause esterne non previste, risposte vaghe o non pertinenti."""

SCHEMA = {
    "type": "object",
    "properties": {
        "etichetta": {"type": "string", "enum": ETICHETTE}
    },
    "required": ["etichetta"],
    "additionalProperties": False,
}

client = anthropic.Anthropic()


def classifica(risposta):
    message = client.messages.create(
        model="claude-haiku-5-5",
        max_tokens=1000,
        system=ISTRUZIONI,
        messages=[{"role": "user", "content": risposta}],
        output_config={"format": {"type": "json_schema", "schema": SCHEMA}},
    )

    testo = next((b.text for b in message.content if b.type == "text"), None)
    if message.stop_reason != "end_turn":
        print("   attenzione, stop_reason =", message.stop_reason)
    try:
        return json.loads(testo)["etichetta"].lower()
    except (TypeError, ValueError, KeyError):
        print("   risposta non valida:", repr(testo))
        return "errore"


with open(CARTELLA / "risposte_questionario.csv", encoding="utf-8") as f:
    righe = list(csv.DictReader(f, delimiter=";"))

risultati = []
for riga in righe:
    etichetta = classifica(riga["risposta"])
    print(riga["id"], etichetta)
    risultati.append({"id": riga["id"], "etichetta_modello": etichetta})

with open(CARTELLA / "risultati_modello.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "etichetta_modello"])
    writer.writeheader()
    writer.writerows(risultati)