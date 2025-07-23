"""
import smtplib

email_sender = 'paranthagan2311@gmail.com'
email_password = 'lslo bbmw fsjx ajez'
session = {}

def send_otp_to_email(email, otp):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_sender, email_password)

    msg = f"Your New OTP is {otp}. Please Don't share this with anyone..."
    server.sendmail(email_sender, email, msg)

    server.quit()

def generate_otp():
    import random
    return random.randint(100000, 999999)

# Example usage
if __name__ == "__main__":
    recipient_email = 'satthish2610@gmail.com'
    otp = generate_otp()
    send_otp_to_email(recipient_email, otp)
    print(f"OTP {otp} sent to {recipient_email}")
"""

import smtplib

email_sender = 'paranthagan2311@gmail.com'
email_password = 'lslo bbmw fsjx ajez'

def send_otp_to_email(recipient_email):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_sender, email_password)

    msg = "Please Don't share this with anyone..."
    server.sendmail(email_sender, recipient_email, msg)

    server.quit()

# Example usage
if __name__ == "__main__":
    recipient_email = 'satthish2610@gmail.com'
    send_otp_to_email(recipient_email)
    print(f"Message sent to {recipient_email}")
