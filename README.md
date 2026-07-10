# Face Recognition Access Control System

Biometric access control system that logs entries and exits to a government data center using facial recognition with anti-spoofing, featuring a secure web administration panel.

> **Status:** Active development — functional system, not yet deployed to production.

## Features
### Access Control
- Real-time facial recognition (InsightFace)
- Anti-spoofing detection prevents photo and screen attacks
- Entry / exit logging with photographic evidence
- Business rule validation (no duplicate open visits, no exit without entry)
- Multi-photo enrollment with quality validation (single-face detection, confidence
  threshold, liveness check)
### Authentication & Security
- Two-factor operator login (facial recognition + PIN)
- Separate credentials for on-site (PIN) and remote (password) access
- Password hashing with bcrypt
- JWT-based session management for the web panel
- Role-based access control (admin / operator)
### Administration
- Web panel for real-time monitoring
- Complete audit trail (who registered what, and when)
- Full traceability: visitor, authorizer, and operator for every movement

## Architecture
### Deployment
```
┌──────────────────────────┐
│  On-site laptop (webcam) │
│  - Camera station        │
│  - Face recognition      │
│  - Operator login        │
└────────────┬─────────────┘
             │ writes
             ▼
┌──────────────────────────┐
│  Server / VM             │
│  - Database              │
│  - FastAPI backend       │
└────────────┬─────────────┘
             │ HTTP (browser)
     ┌───────┴────────┐
     ▼                ▼
┌─────────┐     ┌──────────┐
│ Admin PC│     │  Mobile  │
└─────────┘     └──────────┘
```
### Code Layers
```
vision/    → Camera, face detection, recognition, anti-spoofing
logica/    → Business rules (visit validation, audit)
datos/     → Data access layer (CRUD)
api/       → Web backend (FastAPI) + frontend
utils/     → Shared utilities
config.py  → Centralized paths and settings
```

Dependencies flow in one direction: presentation → logic → data. Lower layers never depend on higher ones.

Face recognition runs locally on the on-site laptop (it requires physical camera access), while the administration panel is served over the network so it can be accessed from any device.

## Requirements & Constraints
Requirements defined for the system (see full requirements document):

### Functional
- Enroll new visitors capturing name, department / vendor, face, email, official ID,
  and signature
- Assign a default authorizer to each person
- Register entries and exits via facial recognition, with photographic evidence
- Manual entry / exit registration as fallback when recognition fails
- Notify the operator when an unrecognized person requires enrollment
- Copy the current authorizer into each visit record at creation time
- Display who is currently inside the data center
- Export the logbook to Excel
- Role-based permissions (admin / operator) with distinct capabilities
- Record who performed every action, with date and time
- Individual credentials for login
- Email the signed privacy notice to the visitor's registered address

### Non-functional
- Recognize a person in under 5 seconds
- 24/7 availability, including on emergency power
- Encrypted database, accessible only with credentials
- No data loss on power failure

### Constraints 
- **Access logging, not door control.** Physical access is handled by existing 
  infrastructure and on-site personnel.
- **Windows deployment** on the existing on-site hardware.
- **Sensitive biometric data** under Mexican law — requires privacy notice and 
  restricted handling.

## Design Decisions
**Layered architecture.** Considered alternatives: a single monolithic script 
(unmaintainable once the web panel needed to reuse the camera station's business 
rules), MVC (a poor fit for the camera station's continuous capture loop, which 
is not request-driven), and microservices (unjustified complexity for a 
single-camera deployment). Layers keep business rules in one place, consumed by 
two very different presentation layers: an OpenCV camera station and a web panel.

**Local recognition, remote panel.** Face recognition requires physical camera 
access, so it runs on-site. The panel is web-based, meeting the requirement of 
remote access without installing software on each machine.

**FastAPI for the backend.** Considered Flask (simpler, more familiar) and rewriting the backend in Spring (my primary stack). FastAPI was chosen because it reuses the existing Python business logic without rewriting, generates interactive API documentation automatically, and runs on Windows without friction. Rewriting in Spring would have meant maintaining the vision layer in Python anyway.

**SQLite for development.** PostgreSQL planned for deployment. SQLite requires no server and keeps the development setup trivial, but it does not handle concurrent network access, which the distributed deployment requires.

**JWT over server-side sessions.** Considered server-side sessions, which are easier to revoke. JWT was chosen because the server stores no session state and each request carries its own signed proof, simplifying the eventual networked deployment. Trade-off: tokens cannot be invalidated before expiry, mitigated by a short (60-minute) lifetime.

**bcrypt for credentials.** Considered SHA-256 (fast, built into Python) but rejected: fast hashing is a liability for passwords. Also considered Argon2 (newer, memory-hard) but bcrypt is battle-tested, widely audited, and has better library support on Windows.

**Separate credentials for camera and panel.** Considered a single credential (simpler for users) but rejected: it forces choosing between a PIN too weak for network exposure, or a password impractical to type on a shared on-site terminal.

**Anti-spoofing before every registration.** Both entry and exit verify liveness 
before writing to the log. Without it, a printed photo could generate a false 
record — unacceptable for an access log used as evidence.

**Pre-trained anti-spoofing model.** Considered training a custom liveness model, but a pre-trained ONNX model (Apache-2.0) provides validated performance without requiring a dataset, training infrastructure, or the risk of a worse result. The model runs on CPU, keeping the on-site hardware requirements minimal.

**Photos on disk, paths in the database.** Considered storing images as BLOBs (atomic backups, single source of truth) but rejected: the database would grow by tens of megabytes per day, complicating backups and the planned PostgreSQL migration.

**Frozen authorizer name.** The authorizer's name is copied as text into each visit. 
Historical records must not change if an authorizer is later renamed or removed — 
the log is evidence, not a live view.

**Multi-photo enrollment with averaged embeddings.** Five validated photos are 
averaged into a single embedding, improving recognition reliability across 
lighting and angle variations.

**Human signature verification.** Automated signature comparison is unreliable, 
especially between a scanned reference and a touchscreen capture. Identity is 
already established biometrically; the operator visually validates the signature 
as a secondary check.

## Tech Stack

| Layer | Technology |
|---|---|
| Face detection & recognition | InsightFace (buffalo_l) |
| Anti-spoofing | ONNX Runtime |
| Computer vision | OpenCV |
| Backend | FastAPI + Uvicorn |
| Database | SQLite (PostgreSQL planned) |
| Authentication | bcrypt, python-jose (JWT) |
| Frontend | HTML, CSS, JavaScript |
| Language | Python 3.9+ |

## Requirements
- Python 3.9 or higher
- Webcam (for the camera station)
- Anti-spoofing ONNX model — [face-antispoof-onnx](https://github.com/johnraivenolazo/face-antispoof-onnx) (Apache-2.0), not included in this repository
- Windows, macOS, or Linux

## Installation
```bash
git clone <repository-url>
cd Prototipo-Reconocimiento_Facial

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt
```
Create a `.env` file in the project root:
```
SECRET_KEY=<your-secret-key>
```
Generate a key with:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```
Download the anti-spoofing model into `models/`, then initialize the database:
```bash
python -m datos.crear_bd
```
## Usage
Note: registration is currently performed via command-line scripts. Web-based enrollment through the admin panel is planned (see Roadmap).

### Register an administrator or operator
```bash
python -m vision.registrar_operador
```
Captures five validated photos and stores hashed credentials: a PIN for the camera 
station and a password for the web panel.

### Register a visitor
```bash
python -m vision.registrar_persona
```

### Run the camera station
```bash
python -m vision.reconocer_desde_bd
```
The operator authenticates with face + PIN. Keys: `e` register entry, `s` register 
exit, `c` close session, `q` quit.

### Run the web panel
```bash
uvicorn api.main:app --reload
```
Panel at `http://127.0.0.1:8000` — interactive API docs at `/docs`

## Project Structure

```
├── api/                 FastAPI backend and web panel
│   ├── main.py          Endpoints
│   ├── seguridad.py     JWT and session verification
│   └── static/          Frontend (HTML, CSS, JS)
├── datos/               Data access layer
├── logica/              Business rules
├── vision/              Camera, recognition, anti-spoofing
├── utils/               Shared utilities
├── pruebas/             Test and maintenance scripts
├── config.py            Centralized paths
└── requirements.txt
```

## Security Considerations

- Credentials are hashed with bcrypt; plaintext passwords are never stored
- The JWT signing key is loaded from an environment variable, never committed
- All endpoints exposing log data require a valid token
- Anti-spoofing runs before every registration
- Foreign key constraints are enforced on every database connection
- **This system processes biometric data**, classified as sensitive personal data 
  under Mexican law (LFPDPPP). Deployment requires a privacy notice, explicit 
  consent, and a data retention policy — pending legal review
- Database encryption at rest is a pending requirement

## Roadmap

- [ ] Regulation signing module (versioned regulations, visitor signatures)
- [ ] Manual entry/exit registration (fallback when recognition fails)
- [ ] Excel export of the logbook
- [ ] Admin edit/delete operations with audit trail
- [ ] Web-based visitor enrollment
- [ ] PostgreSQL migration
- [ ] Database encryption at rest
- [ ] HTTPS for the web panel
- [ ] Privacy notice and consent flow
- [ ] Deployment to the on-site environment

## Author

**Javier Alejandro Santiago Salinas**  
Software Engineering student · [GitHub](https://github.com/Sjaviercito)


