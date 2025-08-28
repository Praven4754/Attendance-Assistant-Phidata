

````
````
# 🧠 Attendance Assistant System
````
An AI-powered smart assistant to help you track daily attendance, generate monthly timesheets, and create salary invoices — all through natural language.

---
````
## 🚀 Built With
````
- 🧩 Phidata — Agent framework
- 🗣️ Gemini Pro LLM — Natural language understanding
- 📄 OpenPyXL — Excel-based attendance tracking
- 📬 SendGrid — Emailing attendance summaries
- 📂 SQLite — Storing invoice data
- 🌐 Gradio — User interface

---
````
## ✨ Features
````
✅ Mark attendance with natural language  
✅ Auto-fill date, day, and extract work remarks  
✅ Duplicate detection with merge/edit options  
✅ Prefill timesheet for the entire month  
✅ View or download attendance report  
✅ Send attendance for approval via email  
✅ Generate invoice PDF from database records  
```
---
````
## 📦 Installation

**### 1. Clone the Repository**

```bash
git clone https://github.com/your-username/attendance-assistant.git
cd attendance-assistant
````

### 2. Create & Activate Virtual Environment

```bash
python -m venv aienv
source aienv/bin/activate       # Linux/macOS
# or
aienv\Scripts\activate          # Windows
```

### 3. Install Dependencies

```bash
uv pip install -r requirements.txt
uv sync
```

---

## ⚙️ .env Configuration

Create a `.env` file in the root folder with the following content:

```env
SENDGRID_API_KEY=your_sendgrid_api_key
SENDER_EMAIL=your_verified_sender_email@example.com
GOOGLE_API_KEY=your_gemini_pro_api_key
```

---

## 🏃 Run the App

```bash
uv run app.py
```

Once started, Gradio will show a link to access the web UI.

---

## 📁 Folder Structure

```
attendance-assistant/
│
├── app.py                   # Main app with Gradio UI
├── model/
│   └── model.py             # Gemini Pro LLM setup
├── tools/
│   ├── excel_util.py        # Attendance Excel functions
│   ├── send_email.py        # Emailing attendance
│   ├── db_utils.py          # Invoice DB init + insert
│   └── invoice_utils.py     # Invoice generation logic
├── attendance.xlsx          # Stores attendance records
├── invoice_data.db          # Stores salary data
├── .env                     # API keys and config
├── requirements.txt         # Dependencies
└── README.md                # You are here!
```

---

## 💬 Example Prompts

Here are some natural language commands you can use:

* 🟢 “Mark me present. I worked on bug fixing.”
* 🟢 “Mark July 23 as week off.”
* 📄 “Show my timesheet.”
* 📧 “Send attendance for this month.”
* 🧾 “Generate invoice for AADHITHYA RAJA D N for July 2025”    """"////////////// Still Working on dont try /////////////""""
* 🔁 “Reset and prefill attendance for July 2025”

---

## 📌 Notes

* All attendance data is saved in `attendance.xlsx`.
* Invoices are generated as PDFs from a local `SQLite` database.
* Emailing requires a verified SendGrid sender and proper `.env` config.
---
