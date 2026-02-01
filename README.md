# Cold Email Automation Bot

This project is a Python-based cold email automation tool that sends personalized emails using a CSV file while following safe rate limits and data privacy practices.

---

## What this project does

- Sends personalized cold emails using Python
- Reads HR / recruiter details from a CSV file
- Uses Gmail SMTP with App Password authentication
- Adds delays between emails to avoid spam
- Attaches a resume automatically
- Protects sensitive data by excluding real email lists from GitHub

---

## Project structure
cold_email_bot/
├── send_emails.py
├── templates/
│   └── email.txt
├── resume/
│   └── resume.pdf
├── data/
│   └── sample_hr_contacts.csv
├── .gitignore
└── README.md



---

## Important note about data privacy

The actual CSV file containing HR email contacts is NOT included in this repository.

It has been intentionally excluded using `.gitignore` because it contains private contact information.

A sample CSV file is provided only to demonstrate the required format.

---

## Sample CSV format

SNo,Name,email,Title,Company
1,Sample HR,hr@example.com,HR Manager,Example Corp


---

## How to run the project

1. Clone the repository


git clone https://github.com/krikare/cold-email-bot.git

2. Go into the project folder

cd cold-email-bot

3. Install required library

pip install pandas

4. Run the script

python3 send_emails.py

---

## Notes

- This project is for learning and demonstration purposes
- Users should follow email provider policies and local regulations
- Do not use this project for spam or unethical email campaigns
