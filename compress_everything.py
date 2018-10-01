#!/usr/bin/env python3
import os
import time
import pathlib
import zipfile
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

ZIPNAME = "dotfiles.zip"


def make_zip():
    if os.path.exists(ZIPNAME):
        os.unlink(ZIPNAME)
    path = pathlib.Path()
    files = path.glob("**/*")
    files = filter(lambda i: "__pycache__" not in str(i), files)
    files = filter(lambda i:  not str(i).startswith(".git"), files)
    files = filter(lambda i: ".swp" not in str(i), files)
    files = filter(lambda i: ZIPNAME not in str(i), files)
    zipf = zipfile.ZipFile(ZIPNAME, "w", zipfile.ZIP_DEFLATED)
    for i in files:
        zipf.write(i)
        print(i)
    zipf.close()


def email_dotfiles():
    s = smtplib.SMTP("smtp.ord1.corp.rackspace.com", 587)
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "dotfiles {}".format(time.strftime("%F"))
    msg["From"] = from_email
    msg["To"] = to_email
    with open(ZIPNAME, "rb") as f:
        part = MIMEApplication(f.read(), Name=ZIPNAME)
        content_disposition = "attachment; filename={}".format(ZIPNAME)
        part["Content-Disposition"] = content_disposition
        msg.attach(part)
    status, details = s.starttls()
    assert status == 220
    status, details = s.ehlo()
    assert status == 250
    s.send_message(msg)
    status, details = s.quit()
    assert status == 221

def main():
    make_zip()
    email_dotfiles()

if __name__ == "__main__":
    main()
