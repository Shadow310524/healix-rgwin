import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from app.core.logging_config import get_logger

logger = get_logger("healix.email")

def send_enquiry_email(name: str, email: str, message: str, phone: str = None, product_name: str = None):
    """
    Sends an email notification to the admin when a new enquiry is received.
    Requires SMTP_EMAIL and SMTP_PASSWORD environment variables.
    """
    smtp_email = os.getenv("SMTP_EMAIL")
    smtp_password = os.getenv("SMTP_PASSWORD")
    
    if not smtp_email or not smtp_password:
        logger.warning("Email notifications skipped: SMTP_EMAIL or SMTP_PASSWORD not configured.")
        return False
        
    try:
        msg = MIMEMultipart()
        msg['From'] = smtp_email
        msg['To'] = smtp_email  # Send to self (the admin)
        
        subject = f"New Enquiry from {name}"
        if product_name:
            subject += f" regarding {product_name}"
        msg['Subject'] = subject
        
        body = f"""
        You have received a new enquiry via the Healix website.
        
        Name: {name}
        Email: {email}
        Phone: {phone or 'Not provided'}
        Product: {product_name or 'General Enquiry'}
        
        Message:
        {message}
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(smtp_email, smtp_password)
        server.send_message(msg)
        server.quit()
        
        logger.info(f"Email notification successfully sent for enquiry from {email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email notification: {str(e)}", exc_info=True)
        return False
