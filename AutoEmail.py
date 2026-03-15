import smtplib
from email.message import EmailMessage

def send_email(subject, body, to_email, to_email2, to_email3):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['To'] = to_email
    msg['Cc'] = to_email2, to_email3

    user = "scrambelbob@gmail.com"
    msg['From'] = user
    password = "pqvkwrpjbrpxkuaf"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()

if __name__ == "__main__":
    send_email("Test Email","This is a test email sent from Python.", "arvindbijulal@gmail.com", "sarafshaheed78@gmail.com", "laiyipeng03@gmail.com")