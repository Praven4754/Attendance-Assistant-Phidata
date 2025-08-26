from phi.assistant import Assistant
from excel_util import (
    store_entry_to_excel,
    check_existing_entry,
    fetch_timesheet,
    fetch_monthly_timesheet,
    clear_entry,
)
from send_email import send_attendance_email
from salary_utils import calculate_expected_salary
from datetime import datetime
import calendar
import os
import re
import gradio as gr
from llm import llm as agent_llm

# ✅ Read environment variables directly (from GitHub Secrets in Docker)
API_KEY = os.getenv("API_KEY")
OTHER_KEY = os.getenv("OTHER_KEY")
PORT = int(os.getenv("PORT", 7860))  # Default to 7860 if not set

# ✅ Extract status and remarks
def extract_status_and_remarks(prompt: str):
    lower_prompt = prompt.lower().strip()
    if lower_prompt in ["hi", "hello", "hey"]:
        welcome_message = (
            "👋 Hello! Welcome to your Attendance Assistant.\n"
            "I'm here to help you:\n"
            "➤ Mark attendance (Present / Absent / Week Off)\n"
            "➤ Extract what work you did as remarks\n"
            "➤ Fetch or download your timesheet\n"
            "➤ Update or clear previous entries\n"
            "➤ Generate invoice for AADHITHYA RAJA D N for July 2025\n"
            "How can I assist you today?"
        )
        return welcome_message, None, False

    if "timesheet" in lower_prompt:
        match = re.search(
            r"(january|february|march|april|may|june|july|august|september|october|november|december)",
            lower_prompt,
        )
        return None, None, match.group(1).capitalize() if match else True

    status = "Present"
    if "absent" in lower_prompt:
        status = "Absent"
    elif "week off" in lower_prompt or "leave" in lower_prompt or "off" in lower_prompt:
        status = "Week Off"

    response = agent_llm.run(
        f"Extract only the work done from this: '{prompt}'. Do not include status or date. Skip overwrite or update in remarks."
    )
    remarks = response.content.strip()
    return status, remarks, False

# ✅ File path helper
def get_timesheet_file():
    path = "attendance.xlsx"
    return path if os.path.exists(path) else None

# ✅ Email extractor
def extract_email_from_text(text):
    match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
    return match.group(0) if match else None

# ✅ Main business logic
def handle_attendance(prompt: str) -> str:
    lower_prompt = prompt.lower().strip()

    # Email flow
    if "email" in lower_prompt or "send mail" in lower_prompt:
        to_email = extract_email_from_text(prompt)
        if not to_email:
            return "❌ Please include a valid recipient email in your message."

        result = send_attendance_email(
            subject="Attendance Report",
            content_text="Hi,\n\nPlease find the attached attendance report.\n\nRegards,\nAttendance Assistant",
            filepath=get_timesheet_file(),
            to_email=to_email,
        )
        return f"✅ Attendance report sent to {to_email}." if result else "❌ Failed to send email."

    # Salary calculator
    if "salary" in lower_prompt:
        return calculate_expected_salary()

    # Clear entry flow
    if "clear" in lower_prompt or "remove" in lower_prompt:
        try:
            date = datetime.today().strftime("%Y-%m-%d")
            clear_entry(date)
            return f"✅ Entry on {date} cleared successfully."
        except Exception as e:
            return f"❌ Failed to clear entry: {e}"

    # Process status & remarks
    result = extract_status_and_remarks(prompt)
    if isinstance(result[0], str) and result[1] is None and result[2] is False:
        return result[0]

    # Timesheet fetch
    if result[2] is True:
        try:
            return fetch_timesheet()
        except Exception as e:
            return f"❌ Failed to fetch timesheet: {e}"
    elif isinstance(result[2], str):
        try:
            return fetch_monthly_timesheet(result[2])
        except Exception as e:
            return f"❌ Failed to fetch {result[2]} timesheet: {e}"

    # Entry insert/update logic
    today = datetime.today()
    date = today.strftime("%Y-%m-%d")
    day = calendar.day_name[today.weekday()]
    status, remarks, _ = result

    if check_existing_entry(date):
        if "overwrite" in lower_prompt or "update" in lower_prompt:
            try:
                _, clean_remarks, _ = extract_status_and_remarks(prompt)
                store_entry_to_excel(date, day, status, clean_remarks, overwrite=True)
                return f"✅ Updated entry on {date} ({day}) with:\n➤ Status: {status}\n➤ Remarks: {clean_remarks}"
            except Exception as e:
                return f"❌ Failed to update entry: {e}"
        else:
            return f"⚠️ Duplicate found for {date}. Use 'overwrite' or 'update' to modify it."

    try:
        store_entry_to_excel(date, day, status, remarks)
        return f"✅ {status} marked for {date} ({day}).\n➤ Remarks: {remarks}"
    except Exception as e:
        return f"❌ Failed to store attendance: {e}"

# ✅ Phi Assistant wrapper
app = Assistant(
    name="attendance-assistant",
    instructions=[
        "Greet the user if they say hi.",
        "Help mark attendance: Present, Absent, or Week Off.",
        "Extract only the actual work done as remarks.",
        "Fetch or download the timesheet when asked.",
        "Update entries when asked using keywords like overwrite or update.",
        "Prevent duplicate entries unless explicitly asked.",
        "Generate invoice for AADHITHYA RAJA D N for July 2025.",
        "Calculate salary from Present days (₹144/hr for 8 hrs).",
    ],
    tools=[handle_attendance, send_attendance_email, calculate_expected_salary],
)

# ✅ Gradio UI Functions
def chat_fn(message, history):
    return handle_attendance(message)

def check_for_download(message):
    if "timesheet" in message.lower():
        file_path = get_timesheet_file()
        return (file_path, gr.update(visible=True)) if file_path else (None, gr.update(visible=False))
    return None, gr.update(visible=False)

custom_css = ""  # Add any custom CSS if needed

# ✅ Launch app
if __name__ == "__main__":
    with gr.Blocks(title="Attendance Assistant", css=custom_css) as ui:
        chatbot_ui = gr.ChatInterface(
            fn=chat_fn,
            title="Attendance Assistant",
            chatbot=gr.Chatbot(height=500),
            textbox=gr.Textbox(
                placeholder="Tell me what you worked on or ask for your timesheet...",
                show_label=False,
            ),
            theme=gr.themes.Glass(primary_hue="blue", secondary_hue="blue", radius_size="md"),
        )

        download_btn = gr.File(label="📥 Download Timesheet", visible=False)

        chatbot_ui.textbox.submit(
            fn=check_for_download,
            inputs=chatbot_ui.textbox,
            outputs=[download_btn, download_btn],
        )

    ui.launch(server_name="0.0.0.0", server_port=PORT)
