import pandas as pd
import os

def calculate_expected_salary():
    file_path = "attendance.xlsx"
    if not os.path.exists(file_path):
        return "❌ Timesheet file not found."

    try:
        df = pd.read_excel(file_path)
        present_days = df[df["Status"].str.lower() == "present"]
        num_days = len(present_days)
        total_hours = num_days * 8
        hourly_rate = 144
        total_salary = total_hours * hourly_rate

        return (
            f"📊 Based on your timesheet:\n"
            f"➤ Present Days: {num_days}\n"
            f"➤ Total Hours: {total_hours} hrs\n"
            f"➤ Hourly Rate: ₹{hourly_rate}\n"
            f"💰 Expected Salary: ₹{total_salary}\n"
            f"📝 *Note: This is the gross salary without TDS deduction.*"
        )

    except Exception as e:
        return f"❌ Failed to calculate salary: {e}"
