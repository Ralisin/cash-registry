# 🔧 Fix Dipendenze Backend

## Problema Rilevato

Errore di compatibilità tra `motor` e `pymongo`:
```
ImportError: cannot import name '_QUERY_OPTIONS' from 'pymongo.cursor'
```

## ✅ Soluzione Rapida

Ho aggiornato `requirements.txt` con le versioni corrette. Reinstalla le dipendenze:

### Windows

```bash
# Disattiva e riattiva venv
deactivate
.venv\Scripts\activate

# Disinstalla pacchetti problematici
pip uninstall motor pymongo beanie -y

# Reinstalla tutto
pip install -r requirements.txt

# Verifica installazione
pip list | findstr "motor pymongo beanie"
```

Dovresti vedere:
```
beanie                    1.24.0
motor                     3.3.2
pymongo                   4.6.1
```

### Linux/Mac

```bash
# Disattiva e riattiva venv
deactivate
source .venv/bin/activate

# Disinstalla pacchetti problematici
pip uninstall motor pymongo beanie -y

# Reinstalla tutto
pip install -r requirements.txt

# Verifica installazione
pip list | grep -E "motor|pymongo|beanie"
```

## 🚀 Riavvia Backend

```bash
uvicorn app.main:app --reload --port 8000
```

Dovresti vedere:
```
🚀 Starting Scout Finance API...
✅ Connected to MongoDB: scout_finance
📦 Initializing default categories...
✅ Created 9 default categories
✅ Application started successfully
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

## 🐛 Se Persiste l'Errore

### Opzione 1: Ricrea venv da zero

```bash
# Elimina venv esistente
rm -rf .venv  # Linux/Mac
rmdir /s .venv  # Windows

# Crea nuovo venv
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Installa dipendenze
pip install --upgrade pip
pip install -r requirements.txt
```

### Opzione 2: Usa versioni alternative

Se il problema persiste, prova versioni più recenti:

```bash
pip install pymongo==4.6.1 motor==3.4.0 beanie==1.25.0
```

## ✅ Test che Funziona

1. **Backend avviato:**
   ```
   INFO:     Uvicorn running on http://127.0.0.1:8000
   ```

2. **API Docs accessibili:**
   - Apri: http://localhost:8000/docs
   - Dovresti vedere Swagger UI con tutti gli endpoints

3. **Health check:**
   ```bash
   curl http://localhost:8000/health
   ```

   Risposta:
   ```json
   {"status":"healthy","database":"connected"}
   ```

## 📝 Note

- **Versioni testate e funzionanti:**
  - pymongo: 4.6.1
  - motor: 3.3.2
  - beanie: 1.24.0

- Il problema era causato da incompatibilità tra motor 3.3.2 e versioni più recenti di pymongo che hanno rimosso `_QUERY_OPTIONS`.

- Ho aggiunto esplicitamente `pymongo==4.6.1` in requirements.txt per forzare la versione compatibile.

---

**Dopo il fix, procedi con il setup nel QUICKSTART.md!**
