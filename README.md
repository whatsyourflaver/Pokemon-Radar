# Pokémon 30 Jahre Radar

Kostenloses GitHub-Actions-Monitoring mit Telegram-Benachrichtigung und GitHub-Pages-Dashboard.

## Inbetriebnahme
1. GitHub Settings → Secrets and variables → Actions: TELEGRAM_BOT_TOKEN und TELEGRAM_CHAT_ID (bereits vom Nutzer hinterlegt).
2. Settings → Pages → Build and deployment → Deploy from a branch → main → /docs → Save.
3. Actions → Pokemon 30 Jahre Radar → Run workflow.
4. In watchlist.json ausschließlich manuell geprüfte direkte Produkt-URLs mit belegter UVP, Versandkosten und Händlerprüfung eintragen. Die Watchlist ist aktuell absichtlich leer.

Beispiel-Schema (nur Struktur, KEIN echtes Angebot):
```json
[{"id":"unique","name":"Produkt","shop":"Händler","language":"DE","url":"https://shop.example/product","uvp":99.99,"uvp_source":"Beleg-URL","shipping":4.99,"retailer_verified":true,"max_multiplier":1.2}]
```

Die Domain-Allowlist steht in monitor.py. Ohne verifizierte Einträge werden keine Preisalarme ausgelöst. Der Monitor verwendet strukturierte Produktdaten (JSON-LD), deren Bestandsangaben ungenau sein können; im Checkout prüfen. Amazon wird nicht automatisch auf Lagerbestand geprüft. GitHub-Zeitpläne können sich verspäten oder nach Inaktivität deaktiviert werden. Keine automatischen Käufe oder Registrierungen.
