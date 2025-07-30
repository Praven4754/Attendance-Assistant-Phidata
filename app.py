from phi.assistant import Assistant
from tools.excel_util import store_entry_to_excel, check_existing_entry, fetch_timesheet, fetch_monthly_timesheet, clear_entry
from tools.send_email import send_attendance_email
from datetime import datetime
from tools.salary_utils import calculate_expected_salary
import calendar
from dotenv import load_dotenv
import gradio as gr
import os
from llm import llm as agent_llm
import re

load_dotenv(override=True)

def extract_status_and_remarks(prompt: str):
    lower_prompt = prompt.lower()
    if lower_prompt.strip() in ["hi", "hello", "hey"]:
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
    else:
        if "timesheet" in lower_prompt:
            month_match = re.search(r"(january|february|march|april|may|june|july|august|september|october|november|december)", lower_prompt)
            if month_match:
                return None, None, month_match.group(1).capitalize()
            return None, None, True

        if "absent" in lower_prompt:
            status = "Absent"
        elif "week off" in lower_prompt or "leave" in lower_prompt or "off" in lower_prompt:
            status = "Week Off"
        else:
            status = "Present"

    response = agent_llm.run(f"Extract only the work done from this: '{prompt}'. Do not include status or date.,dont include overwrite or update in remarks")
    remarks = response.content.strip()

    return status, remarks, False


def get_timesheet_file():
    filepath = "attendance.xlsx"
    return filepath if os.path.exists(filepath) else None

def extract_email_from_text(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match.group(0) if match else None

def handle_attendance(prompt: str) -> str:
    result = extract_status_and_remarks(prompt)
    lower_prompt = prompt.lower().strip()

    if "send mail" in lower_prompt or "send email" in lower_prompt or "email" in lower_prompt:
        to_email = extract_email_from_text(prompt)
        if not to_email:
            return "❌ Please include a valid recipient email in your message to send the report."

        result = send_attendance_email(
            subject="Attendance Report",
            content_text="Hi,\n\nPlease find the attached attendance report.\n\nRegards,\nAttendance Assistant",
            filepath=get_timesheet_file(),
            to_email=to_email
        )
        if result:
            return f"✅ Attendance report has been sent to {to_email}."
        else:
            return "❌ Failed to send attendance report. Please check your email configuration."

    if "salary" in lower_prompt or "expected salary" in lower_prompt:
        return calculate_expected_salary()

    result = extract_status_and_remarks(prompt)

    # Greeting
    if isinstance(result[0], str) and result[1] is None and result[2] is False:
        return result[0]

    today = datetime.today()
    date = today.strftime("%Y-%m-%d")
    day = calendar.day_name[today.weekday()]

    # Clear entry
    if "clear" in lower_prompt or "remove" in lower_prompt:
        try:
            clear_entry(date)
            return f"✅ Entry on {date} ({day}) has been cleared successfully."
        except Exception as e:
            return f"❌ Failed to clear entry: {e}"

    # Timesheet fetch logic
    if result[2] is True:
        try:
            return fetch_timesheet()
        except Exception as e:
            return f"Failed to fetch timesheet: {e}"

    if isinstance(result[2], str):
        try:
            return fetch_monthly_timesheet(result[2])
        except Exception as e:
            return f"Failed to fetch {result[2]} timesheet: {e}"

    # Normal attendance entry flow
    status, original_remarks, _ = result
    existing = check_existing_entry(date)

    if existing:
        if "overwrite" in lower_prompt or "update" in lower_prompt:
            try:
                _, clean_remarks, _ = extract_status_and_remarks(prompt)
                store_entry_to_excel(date, day, status, clean_remarks, overwrite=True)
                return f"✅ Existing entry on {date} ({day}) was successfully updated.\n➤ Status: {status}\n➤ New Remarks: {clean_remarks}"
            except Exception as e:
                return f"Failed to overwrite attendance: {e}"
        else:
            return f"⚠️ Duplicate entry found for {date}. Entry not stored.\nUse 'overwrite' or 'update' in your prompt to update the entry."

    try:
        store_entry_to_excel(date, day, status, original_remarks)
        return f"✅ {status} marked for {date} ({day}).\n➤ Remarks: {original_remarks}"
    except Exception as e:
        return f"Failed to store attendance: {e}"


app = Assistant(
    name="attendance-assistant",
    instructions=[
        "If the user says hi or hello, greet them back.",
        "You will help users mark their attendance as Present, Absent, or Week Off.",
        "You help users mark attendance as Present, Absent, or Week Off.",
        "You extract only the work done from user input and store it as remarks.",
        "You fetch the timesheet when the user asks for it.",
        "Skip the words like worked on, completed, done, etc. and extract only the actual work done.",
        "if the user asks to overwrite the existing entry, you will do so.",
        "You will not store duplicate entries for the same date.",
        "Generate invoice for AADHITHYA RAJA D N for July 2025",
        "If the user asks about expected salary, calculate it based on Present days (8 hrs each, ₹144/hr).",
    ],
    tools=[handle_attendance, send_attendance_email,calculate_expected_salary]
)

def chat_fn(message, history):
    reply = handle_attendance(message)
    return reply

def check_for_download(message):
    if "timesheet" in message.lower():
        file_path = get_timesheet_file()
        if file_path:
            return file_path, gr.update(visible=True)
    return None, gr.update(visible=False)

custom_css = """ """
if __name__ == "__main__":
    with gr.Blocks(title="Attendance Assistant", css=custom_css) as app:
        chatbot_ui = gr.ChatInterface(
            fn=chat_fn,
            title="Attendance Assistant",
            chatbot=gr.Chatbot(height=500),
            textbox=gr.Textbox(placeholder="Tell me what you worked on or ask for your timesheet...", show_label=False),
            theme=gr.themes.Glass(primary_hue="blue", secondary_hue="blue", radius_size="md"),
        )

        download_btn = gr.File(label="📥 Download Timesheet", visible=False)

        chatbot_ui.textbox.submit(
            fn=check_for_download,
            inputs=chatbot_ui.textbox,
            outputs=[download_btn, download_btn]
        )

    app.launch()






# import streamlit as st
# from model.model import llm
# from datetime import date, datetime
# from tools.excel_util import store_entry_to_excel, fetch_timesheet_df, fetch_monthly_timesheet
# from tools.send_email import send_attendance_email
# import os

# st.set_page_config(page_title="Attendance Assistant", layout="centered")

# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# if "show_download" not in st.session_state:
#     st.session_state.show_download = False

# st.title("📘 Attendance Assistant")
# user_input = st.chat_input("Tell me what you worked on or ask for your timesheet...")

# def handle_input(prompt):
#     if not prompt:
#         return None

#     # response, _, action = llm.run(prompt)
#     result = llm.run(prompt)

#     if isinstance(result, tuple):
#         if len(result) == 3:
#             response, _, action = result
#         elif len(result) == 2:
#             response, action = result
#         elif len(result) == 1:
#             response = result[0]
#             action = None
#     else:
#         response = result
#         action = None


#     if isinstance(response, str):
#         st.session_state.chat_history.append(("user", prompt))
#         st.session_state.chat_history.append(("ai", response))

#         if action is True:
#             st.session_state.show_download = True
#             try:
#                 df = fetch_timesheet_df()
#                 st.session_state.chat_history.append(("ai", df))
#                 return df
#             except Exception as e:
#                 return f"❌ Failed to fetch timesheet: {e}"

#         if isinstance(action, str):
#             st.session_state.show_download = True
#             try:
#                 df = fetch_monthly_timesheet(action)
#                 st.session_state.chat_history.append(("ai", df))
#                 return df
#             except Exception as e:
#                 return f"❌ Failed to fetch {action} timesheet: {e}"

#         return response

# if user_input:
#     result = handle_input(user_input)

# for role, msg in st.session_state.chat_history:
#     with st.chat_message(role):
#         if hasattr(msg, "columns"):
#             st.dataframe(msg, use_container_width=True)
#         else:
#             st.markdown(str(msg))

# if st.session_state.show_download and os.path.exists("attendance.xlsx"):
#     with open("attendance.xlsx", "rb") as f:
#         st.download_button(
#             label="📥 Download Timesheet",
#             data=f,
#             file_name="attendance.xlsx",
#             mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#         )


