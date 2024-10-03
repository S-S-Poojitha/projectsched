import streamlit as st
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

SERVICE_ACCOUNTS_DIR = 'service_accounts'
SCOPES = ["https://www.googleapis.com/auth/calendar", "https://www.googleapis.com/auth/calendar.readonly"]

def send_email(event_summary, recipient_email):
    # Set up SMTP server
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  # For SSL: 465, For TLS: 587

    # Sender and receiver email addresses
    sender_email = 'poojithasarvamangala@gmail.com'  # Change this to your email address

    # Email content
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Suject']='Proposed Event'
    body = event_summary
    message.attach(MIMEText(body, 'plain'))

    # Connect to SMTP server and send email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Enable TLS encryption
            server.login(sender_email, 'ferm bqim epzj xdlc')  # Change this to your password
            server.sendmail(sender_email, recipient_email, message.as_string())
        st.success('Email sent successfully!')
    except Exception as e:
        st.error(f"Failed to send email: {e}")

def main():
    user_email = st.text_input("Enter recipient's email address")
    event_summary='https://calendaragent-in9q9eyyt68upneayywhom.streamlit.app/'
    if st.button('Send Email'):
        if user_email:
            send_email(event_summary, user_email)
        else:
            st.error('Please enter a recipient email address.')

if __name__ == "__main__":
    main()
