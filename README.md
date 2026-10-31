# Pokémon 30 Jahre Radar


Kostenloses GitHub-Actions-Monitoring mit Telegram-Benachrichtigung und GitHub-Pages-Dashboard.


## Inbetriebnahme
1. GitHub Settings → Secrets and variables → Actions: TELEGRAM_BOT_TOKEN und TELEGRAM_CHAT_ID (bereits vom Nutzer hinterlegt).
2. Settings → Pages → Build and deployment → Source: GitHub Actions. Nach jedem Scan veröffentlicht der Radar das docs-Verzeichnis direkt als Pages-Artefakt.
3. Actions → Pokemon 30 Jahre Radar → Run workflow.
4. In watchlist.json ausschließlich manuell geprüfte direkte Produkt-URLs mit belegter UVP, Versandkosten und Händlerprüfung eintragen. Die Watchlist ist aktuell absichtlich leer.


Beispiel-Schema (nur Struktur, KEIN echtes Angebot):
```json
[{"id":"unique","name":"Produkt","shop":"Händler","language":"DE","url":"https://shop.example/product","uvp":99.99,"uvp_source":"Beleg-URL","shipping":4.99,"retailer_verified":true,"max_multiplier":1.2}]
```


Die Domain-Allowlist steht in monitor.py. Ohne verifizierte Einträge werden keine Preisalarme ausgelöst. Der Monitor verwendet strukturierte Produktdaten (JSON-LD), deren Bestandsangaben ungenau sein können; im Checkout prüfen. Amazon wird nicht automatisch auf Lagerbestand geprüft. GitHub-Zeitpläne können sich verspäten oder nach Inaktivität deaktiviert werden. Keine automatischen Käufe oder Registrierungen.


## Prüfung am 31.10.2026

Dashboard: https://whatsyourflaver.github.io/Pokemon-Radar/

Pages war bereits seit dem 29.10.2026 aus main /docs veröffentlicht. Abgemeldete Aufrufe der Repository-Einstellungen zeigten 404. Für die Einstellungen diese bereinigte Adresse nach Anmeldung verwenden: https://github.com/whatsyourflaver/Pokemon-Radar/settings/pages

Der Radar veröffentlicht jetzt direkt nach jedem Scan, da Bot-Commits mit GITHUB_TOKEN keinen weiteren Pages-Build auslösen. Das Dashboard zeigt den letzten Scan; mehr als eine Stunde alte Daten werden markiert. Telegram Test #2 wurde erfolgreich ausgeführt: https://github.com/whatsyourflaver/Pokemon-Radar/actions/runs/41161900266

Produktalarme bleiben aus, solange watchlist.json leer ist. Geprüfte Produktkandidaten bei KEEPSEVEN: Ditto Premium und Ultra Premium Nacht (DE). Produktseiten sowie Versandkosten sind erreichbar, aber dort wird kein Preis ausdrücklich als UVP belegt. Händlerpreise dürfen nicht als UVP übernommen werden. Smyths blockiert den automatisierten Zugriff. Deshalb wurden keine unvollständig verifizierten Alarmregeln aktiviert.

Zeitplan: alle fünf Minuten vorgesehen, Ausführung durch GitHub kann sich verzögern. Keine stündliche Telegram-Statusnachricht eingerichtet; Telegram meldet qualifizierte neue Produktangebote, sobald geprüfte Watchlist-Einträge vorliegen.
