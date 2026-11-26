# AI-Based Smart Queue and Notification System

A professional, full-stack web application designed for civic service desks, healthcare reception areas, clinics, college offices, and billing centers.

The system modernizes token management by allowing customers to issue digital tokens via web kiosk or QR code, track their queue progress in real time with AI-estimated wait times, and receive automated email alerts. Administrators control actual token calling, skipping, and completion through a secure dashboard, preserving the core principle: **AI predicts waiting time; human staff controls queue progression.**

---

## 🌟 Key Features

### 👤 Customer-Facing Portal
- **Self-Service Token Issuance**: Customers input name, email, optional phone, service category, and optional notes with explicit consent validation.
- **Mobile QR Code Kiosk**: Scan QR codes on-site or from displays to open the token issuance kiosk on mobile browsers.
- **Unique Token & Position Assignment**: Immediate alphanumeric token generation (e.g., `A-001`, `B-002`) with real-time queue position.
- **Dynamic Waiting Time Estimation**: Instant wait estimate in minutes based on real-time backlog, active counter throughput, and machine learning models.
- **Privacy-Preserving Tracking**: Secure private lookup link and token verification code preventing unauthorized access to customer records.
- **Live Auto-Refreshing Tracker**: Status updates every 12 seconds with status badges (`Waiting`, `Approaching`, `Now Serving`, `Completed`, `Skipped`, `Cancelled`).
- **Self-Service Cancellation**: Customers can voluntarily release their spot if they decide to leave.

### 🛡️ Administrative Portal & Operations
- **Secure Authentication**: Protected admin portal with PBKDF2/SHA-256 password hashing, session guards, and CSRF protection on state-changing requests.
- **Operational Overview**: Real-time KPI cards (tokens created today, currently waiting, now serving, completed today, average actual wait time, average desk service duration) backed by live database queries.
- **Visual Analytics**: Interactive Chart.js graphs showing hourly queue volume peaks and status breakdowns.
- **Live Queue Manager**: Searchable and filterable queue table by status, category, or customer name.
- **Safe Staff Actions**:
  - **Call Next (FIFO)**: Automatically pulls the oldest waiting customer to an active counter desk.
  - **Direct Desk Calling & Repeat Call**: Announce and re-call tokens with auditory/visual prompts.
  - **Complete Service**: Records actual counter service duration and wait time to service history.
  - **Skip / Cancel with Confirmation**: Modal confirmation recording skip reasons and removing tokens from the active queue.
- **Service Desk Settings**: Real-time toggling of physical counter desks, threshold configuration for approaching-turn alerts, and category management.

### 🧠 Two-Tier AI Waiting-Time Engine
- **Tier 1: Transparent Algorithmic Baseline**:
  $$\text{Est. Wait} = \left\lceil \frac{\text{People Ahead}}{\text{Active Counters}} \times \text{Median Historical Service Duration} \right\rceil$$
  Used for cold-starts and fallback when history has fewer than 15 completed transactions.
- **Tier 2: Supervised Machine Learning (`RandomForestRegressor`)**:
  - Evaluated on completed service history using features: `derived_people_ahead`, `counter_count`, `category_code`, `hour_of_day`.
  - 80/20 train/test split with held-out Mean Absolute Error (MAE) evaluated against baseline.
  - Artifact persisted to `app/ml/model.joblib`.
  - **No Fabricated Accuracy**: Admin AI Insights page displays real training size, model MAE, and baseline MAE.

### ✉️ Multi-Channel Notification Engine
- **Four Notification Events**:
  1. *Token Acknowledgement*: Dispatched upon token creation with direct tracking URL.
  2. *Turn Approaching Alert*: Triggered when position reaches configured threshold (e.g., $\le 2$ people ahead).
  3. *Now Serving Call*: Triggered when staff calls customer to a specific counter desk.
  4. *Queue Update*: Dispatched upon significant recalculations.
- **Dual Operating Modes**:
  - **Demo/Log Mode (Default)**: Safely simulates and logs deliveries locally without external SMTP dependencies.
  - **Live SMTP Mode**: Connects via TLS to standard SMTP providers (Gmail, Outlook, SendGrid, Amazon SES).
- **Deduplication Engine**: Unique database constraint on `deduplication_key` guarantees customers never receive duplicate approaching alerts.
- **Masked PII**: Recipient emails are masked in logs (e.g., `s***r@example.com`) to protect customer privacy.

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Backend** | Python 3.11+, Flask 3.0+, Jinja2 Templates, python-dotenv |
| **Database** | SQLite3 with foreign keys, transactional integrity, and indexing |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript, Bootstrap 5.3, Bootstrap Icons |
| **Machine Learning** | scikit-learn 1.3+ (`RandomForestRegressor`), pandas, numpy, joblib |
| **Visualizations** | Chart.js 4.4, qrcodejs |
| **Testing** | pytest 8.0+, pytest-anyio, Flask Test Client |

---

## 📁 Project Structure

```text
smart-queue-system/
│
├── app/
│   ├── __init__.py                # Flask application factory, CSRF middleware & CLI commands
│   ├── config.py                  # Environment-driven configuration
│   ├── database.py                # SQLite schema, indices, connection teardown & seeding
│   ├── routes/
│   │   ├── public.py              # Landing page, How It Works
│   │   ├── customer.py            # Get token, confirmation, secure tracking & cancellation
│   │   └── admin.py               # Dashboard, live queue, AI insights, reports, settings
│   ├── services/
│   │   ├── queue_service.py       # FIFO logic, transitions, recalculations & atomic calls
│   │   ├── wait_time_service.py   # Two-tier estimation engine (ML + baseline)
│   │   ├── notification_service.py# Notification dispatcher, deduplication & SMTP
│   │   └── report_service.py      # Aggregations, Chart.js metrics & CSV export
│   ├── ml/
│   │   ├── train_model.py         # RandomForestRegressor training & evaluation pipeline
│   │   └── predict.py             # Inference loader with caching
│   ├── templates/
│   │   ├── base.html              # Customer master layout with QR & navbar
│   │   ├── admin_base.html        # Admin sidebar layout
│   │   ├── public/                # index.html, how_it_works.html
│   │   ├── customer/              # get_token.html, token_confirmation.html, track_token.html
│   │   ├── admin/                 # dashboard.html, live_queue.html, ai_insights.html, reports.html, settings.html, notifications.html, token_detail.html
│   │   └── email/                 # acknowledgement.html, approaching.html, now_serving.html, wait_update.html
│   └── static/
│       ├── css/custom.css         # Professional design system tokens & responsive CSS
│       └── js/
│           ├── main.js            # Modals, clipboard copy, live countdown & QR code setup
│           └── charts.js          # Chart.js initialization for traffic & status breakdown
│
├── tests/
│   ├── conftest.py                # Test fixtures (in-memory SQLite, test client, admin session)
│   ├── test_admin_auth.py         # Admin authentication, route guards, CSRF & reports tests
│   ├── test_customer_flow.py      # Token issuance, tracking security & cancellation tests
│   ├── test_queue_logic.py        # FIFO calling, completion duration & skipping tests
│   ├── test_wait_time_and_ai.py   # Baseline formula & RandomForestRegressor training tests
│   └── test_notifications.py      # Masking, deduplication & template rendering tests
│
├── instance/
│   └── smart_queue.sqlite         # SQLite database file (auto-created)
├── .env.example                   # Environment configuration template
├── .env                           # Local environment file
├── requirements.txt               # Python package dependencies
├── run.py                         # Application runner script
└── README.md                      # Comprehensive project documentation
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.11 or 3.12 installed on your system.
- Git (optional).

### 1. Clone or Open Workspace
```bash
cd smart-queue-system
```

### 2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
# Windows PowerShell
copy .env.example .env

# Linux / macOS
cp .env.example .env
```

Review `.env`:
```ini
FLASK_APP=run.py
FLASK_DEBUG=1
FLASK_SECRET_KEY=smartqueue-secret-key-dev-2026-production-grade
DATABASE_PATH=instance/smart_queue.sqlite
SERVICE_CENTRE_NAME=Civic & Healthcare Service Hub
ACTIVE_COUNTERS=2
APPROACHING_THRESHOLD=2
FALLBACK_SERVICE_DURATION_MINUTES=5
APP_DEMO_MODE=True
```

### 5. Initialize Database & Seed Default Admin
The application automatically creates the database and default admin on first startup. You can also run the CLI commands manually:
```bash
flask init-db
flask seed-admin --username admin --email admin@smartqueue.local --password admin123
```

Default administrator credentials:
- **Username**: `admin`
- **Password**: `admin123`

---

## 🏃 Running the Application

Launch the local development server:
```bash
python run.py
```
Open your browser and navigate to:
```text
http://127.0.0.1:5000
```

---

## 🧪 Running Automated Tests

Run the full automated test suite covering authentication, customer workflows, queue FIFO transitions, AI training/evaluation, and notification deduplication:
```bash
python -m pytest -v
```

All 14 tests run synchronously against an isolated in-memory test database:
- `test_admin_auth.py`: Route protection, login/logout, settings updates, CSV export.
- `test_customer_flow.py`: Token creation, secure verification lookup, customer cancellation.
- `test_queue_logic.py`: FIFO calling order, service duration calculation, skipping logic.
- `test_wait_time_and_ai.py`: Baseline math, insufficient data guard, RandomForestRegressor training and prediction.
- `test_notifications.py`: Email masking, deduplication preventing double-alerts, HTML template rendering.

---

## 🎓 Viva / Demo Walkthrough Guide

Follow this step-by-step walkthrough to demonstrate the full end-to-end functionality in a project presentation or college viva:

### Step 1: Landing Page & QR Code Access
1. Open `http://127.0.0.1:5000/`.
2. Point out the live counter desk preview (`Serving Token`, `Waiting Ahead`, `Est. Wait Time`).
3. Click **"Scan QR"**: Explain how customers can scan this code with their smartphone camera at the entrance to access the kiosk on their personal devices.

### Step 2: Customer Issues Tokens
1. Open `http://127.0.0.1:5000/get-token` in Tab 1:
   - Name: `Alice Walker`, Email: `alice@example.com`, Category: `General Inquiry`.
   - Submit: Alice receives token **`A-001`** with position **#1**.
   - Note the **"Private Tracking Link"** and the **"Scan with phone"** QR code.
2. Issue a second token in Tab 1:
   - Name: `Bob Davis`, Email: `bob@example.com`, Category: `Documents & Certificates`.
   - Bob receives token **`B-001`** with position **#2** and wait estimate $\sim 5$ minutes.
3. Issue a third token:
   - Name: `Charlie Evans`, Email: `charlie@example.com`, Category: `Specialist Support`.
   - Charlie receives token **`D-001`** with position **#3** and wait estimate $\sim 10$ minutes.

### Step 3: Admin Sign In & Live Queue FIFO Calling
1. Open `http://127.0.0.1:5000/admin/login` in Tab 2:
   - Log in with `admin` / `admin123`.
2. Go to **"Operational Overview"**:
   - Show the cards: 3 tokens created today, 3 currently waiting, 0 serving.
3. Click **"Call Next Token (FIFO)"**:
   - The system automatically selects `A-001` (Alice Walker) as the earliest waiting token.
   - Status transitions to **"Now Serving"** and assigns `Counter 1`.
   - Bob (`B-001`) automatically advances to position **#1** and transitions to **"Approaching"**.
4. Check **"Notification Log"**:
   - Demonstrate the dispatched notifications:
     - Acknowledgement for `A-001`, `B-001`, `D-001`.
     - Approaching Alert for `B-001`.
     - Now Serving Call for `A-001` directing Alice to Counter 1.
   - Note masked emails (`a***e@example.com`) for customer privacy.

### Step 4: Completing Service & Dynamic Recalculation
1. In Live Queue, click **"Mark Completed"** for `A-001`:
   - System records the exact completion timestamp, calculated queue wait, and actual service duration into `service_history`.
   - Counter 1 is freed.
2. In Tab 1, observe the customer tracking screen:
   - The countdown timer automatically refreshes to reflect latest queue state.

### Step 5: AI & Machine Learning Insights
1. Go to **"AI & Wait Insights"** in the Admin sidebar:
   - Review the transparent **Baseline Estimation Formula** and active desk parameters.
   - Click **"Seed Demo History (Viva Ready)"**: Populates 34 realistic historical service records across different categories.
   - The system automatically trains a **RandomForestRegressor** with an 80/20 train/test split.
   - Point out the **Test MAE vs. Baseline MAE** comparison: Demonstrates true evaluation metrics rather than fabricated percentages.

### Step 6: Reports & Analytics
1. Go to **"Reports & Analytics"**:
   - View aggregated metrics: total tokens, completion rate %, average actual wait time, median wait time, and average desk service duration.
   - Examine the **"Peak Queue Volumes by Hour of Day"** Chart.js graph.
   - Click **"Export CSV"** to download the complete audit spreadsheet for record keeping.

---

## 🔒 Security & Privacy Implementation

- **No Plaintext Passwords**: All admin passwords hashed using `werkzeug.security.generate_password_hash`.
- **CSRF Defense**: All POST requests validated with secret token comparison via `@app.before_request`.
- **Private Token Tracking**: Direct URL tracking requires a cryptographically secure 16-byte tracking key (`secrets.token_urlsafe(16)`). Direct searches require email verification matching.
- **PII Protection**: Customer phone numbers and emails are masked in administrative audit tables and never exposed publicly.
- **Idempotency & Race Condition Prevention**: Database transactions and rowcount checks ensure two concurrent "Call Next" requests never call the same customer twice.
- **Secret Isolation**: All credentials and sensitive keys loaded from environment variables (`.env`), omitted from version control via `.gitignore`.

---

## ⚖️ Known Limitations & Future Roadmap

- **SMS Carrier Integration**: Current version logs phone numbers; direct SMS delivery can be integrated using Twilio or AWS SNS.
- **Multi-Branch Hierarchy**: Current architecture supports single-branch multi-counter deployments; multi-branch enterprise support can be added with tenant partitioning.
- **Audio Synthesizer**: Visual and email chimes are included; text-to-speech lobby audio announcements can be added via the Web Speech API.

---

## 📄 License
This project is developed as an open-source educational mini-project for smart civic services and healthcare queue operations.
