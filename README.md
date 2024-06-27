# rag
## installation

```bash
poetry install
```

## usage

lancer le serveur :
```bash
poetry run python rag.py
```

lancer un projet de pdf par exemple
```bash
curl -F 'file=@uno.pdf' http://localhost:3030/pdf
```

curl -F 'file=@uno.pdf' http://localhost:3030/pdf
curl -H 'Content-Type : application/json' http://localhost:3030/ai -d '{"query": "Quel est le but du jeu au UNO ?"}'
curl -H 'Content-Type : application/json' http://localhost:3030/ask_pdf -d '{"query": "Quel est le but du jeu au UNO ?"}' 
