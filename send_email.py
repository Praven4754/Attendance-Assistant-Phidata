from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content, Attachment, FileContent, FileName, FileType, Disposition
import base64
import os
from dotenv import load_dotenv

load_dotenv(override=True)

def send_attendance_email(subject, content_text, filepath, to_email):
    api_key = os.getenv("SENDGRID_API_KEY")
    from_email = Email(os.getenv("FROM_EMAIL"))  # Verified sender email
    to_email = To(to_email)  # Wrap the *argument*, not env var
    content = Content("text/plain", content_text)

    mail = Mail(from_email, to_email, subject, content)

    with open(filepath, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data).decode()

    attached_file = Attachment(
        FileContent(encoded),
        FileName("attendance.xlsx"),
        FileType("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
        Disposition("attachment")
    )

    mail.attachment = attached_file

    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(mail)
        print(to_email)
        print("✅ Email sent successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False
