import smtplib
import pandas as pd
import time
import signal
from email.message import EmailMessage
from pathlib import Path


EMAIL_ADDRESS = "karthikreddypeddala@gmail.com"
EMAIL_PASSWORD = "oxqbowxkxtruhbug"

CSV_PATH = "data/hr_contacts_all_from_pdf.csv"
RESUME_PATH = "resume/karthikCV.pdf"
EMAIL_TEMPLATE_PATH = "templates/email.txt"

MAX_EMAILS_PER_RUN = 25      # changed from 100
DELAY_SECONDS = 60           # changed from 120


paused = False
stop_requested = False


def toggle_pause(signum, frame):
    global paused
    paused = not paused
    state = "⏸️ PAUSED" if paused else "▶️ RESUMED"
    print(f"\n{state}. Press Ctrl+C again to toggle.")


def stop_program(signum, frame):
    global stop_requested
    stop_requested = True
    print("\n🛑 STOP requested. Exiting safely...")


signal.signal(signal.SIGINT, toggle_pause)    # Ctrl+C → pause/resume
signal.signal(signal.SIGQUIT, stop_program)  # Ctrl+\ → stop completely


df = pd.read_csv(
    CSV_PATH,
    engine="python",
    on_bad_lines="skip"
)
df.columns = df.columns.str.strip().str.lower()

required_columns = {"name", "email", "title", "company"}
missing = required_columns - set(df.columns)

if missing:
    raise Exception(f"❌ Missing required columns in CSV: {missing}")


template = Path(EMAIL_TEMPLATE_PATH).read_text()

sent_count = 0

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    for _, row in df.iterrows():

        if stop_requested:
            break

        if sent_count >= MAX_EMAILS_PER_RUN:
            break

        while paused:
            time.sleep(1)

        email = str(row["email"]).strip()
        name = str(row["name"]).strip()
        title = str(row["title"]).strip()
        company = str(row["company"]).strip()

        if "@" not in email:
            print(f"⚠️ Skipping invalid email: {email}")
            continue

        body = (
            template
            .replace("{{Name}}", name)
            .replace("{{Title}}", title)
            .replace("{{Company}}", company)
        )

        msg = EmailMessage()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = email
        msg["Subject"] = f"Application for Software Engineer / Full Stack Role at {company}"
        msg.set_content(body)

        with open(RESUME_PATH, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="pdf",
                filename="Karthik_Reddy_Resume.pdf"
            )

        server.send_message(msg)
        sent_count += 1
        print(f"✅ Sent {sent_count}/{MAX_EMAILS_PER_RUN} → {email}")

        time.sleep(DELAY_SECONDS)


remaining_df = df.iloc[sent_count:]
remaining_df.to_csv(CSV_PATH, index=False)

print(f"\n🎯 Done. Sent {sent_count} emails. Remaining: {len(remaining_df)}")