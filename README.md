# Codifica di risposte aperte con un LLM
Claude Haiku 5.5 via API su 50 risposte sintetiche, 6 categorie, una per risposta.
- Accordo con la mia codifica: 86% (43/50, IC 95% 74%–93%), kappa 0,83. Me vs Claude: 88%, kappa 0,85.
- Limiti: dati sintetici e più puliti del reale, solo 50 risposte, una sola esecuzione.
- Non del tutto stabile: con i default una risposta è cambiata tra due esecuzioni.
- Prossimi passi: tre run con temperature=0, secondo modello, poi RAG.
