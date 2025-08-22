# QR-Info-Portal für Labor Pattaya

Ein modernes Web-Portal für ein Labor in Pattaya, Thailand. Besucher können via QR-Code den aktuellen Status, Öffnungszeiten und Kontaktinformationen abrufen.

## Features

- 📊 **Status-Anzeige**: Anwesend, Urlaub, Kongress, etc.
- 🕐 **Öffnungszeiten**: Tages-, Wochen- und Monatsansicht
- 🌐 **Mehrsprachig**: Deutsch, Thai, Englisch
- 📱 **QR-Code Generator**: Für einfachen Zugang
- 🖥️ **Kiosk-Modus**: Für Vor-Ort-Bildschirme
- 🔐 **Admin-Interface**: Zur Verwaltung aller Inhalte

## Technologie-Stack

- **Backend**: Python 3.11, Flask
- **Datenbank**: SQLite mit SQLModel ORM
- **Frontend**: Tailwind CSS (CDN), HTMX
- **QR-Codes**: qrcode[pil] für PNG/SVG Generation

## Quick Start

### Voraussetzungen

- Python 3.11 oder höher
- pip (Python Package Manager)

### Installation

1. Repository klonen:
```bash
git clone https://github.com/Ralle1976/qr-info-portal.git
cd qr-info-portal
```

2. Virtuelle Umgebung erstellen:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oder
venv\Scripts\activate  # Windows
```

3. Dependencies installieren:
```bash
pip install -r requirements.txt
```

4. Umgebungsvariablen konfigurieren:
```bash
cp .env.example .env
# .env Datei bearbeiten und Werte anpassen
```

5. Anwendung starten:
```bash
python run.py
```

Die Anwendung ist dann erreichbar unter:
- Lokal: http://localhost:5000
- Im LAN: http://[IHRE-IP]:5000

## LAN-IP ermitteln

**Windows:**
```bash
ipconfig | findstr IPv4
```

**Linux/Mac:**
```bash
hostname -I | awk '{print $1}'
# oder
ip addr show | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | cut -d/ -f1
```

**macOS alternativ:**
```bash
ipconfig getifaddr en0
```

## Konfiguration

Die Hauptkonfiguration erfolgt über `config.yml`:
- Standortdaten (Adresse, Koordinaten)
- Kontaktinformationen
- Standard-Öffnungszeiten
- Verfügbare Sprachen

## Struktur

```
qr-info-portal/
├── app/
│   ├── models.py          # Datenbank-Modelle
│   ├── routes_public.py   # Öffentliche Routen
│   ├── routes_admin.py    # Admin-Routen
│   ├── services/          # Business Logic
│   ├── templates/         # Jinja2 Templates
│   └── static/            # CSS, Bilder, QR-Codes
├── config.yml             # Hauptkonfiguration
├── requirements.txt       # Python Dependencies
└── run.py                # Startskript
```

## Deployment

### Docker

```bash
docker build -t qr-info-portal .
docker run -p 5000:5000 --env-file .env qr-info-portal
```

### Production

Für den Produktivbetrieb empfiehlt sich:
- Gunicorn als WSGI Server
- Nginx als Reverse Proxy
- SSL/TLS Zertifikat

## Lizenz

Entwickelt von Ralle1976

## Support

Bei Fragen oder Problemen bitte ein Issue auf GitHub erstellen.