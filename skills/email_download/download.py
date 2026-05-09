import imaplib
import email
from email.header import decode_header
import os
import yaml
from pathlib import Path

# Load configuration
CONFIG_PATH = Path(__file__).resolve().parent.parent.parent / "config" / "config.yaml"
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

EMAIL = config["email"]["address"]
PASSWORD = config["email"]["password"]
IMAP_SERVER = config["email"]["imap_server"]
DOWNLOAD_FOLDER = config["paths"]["download_folder"]

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def download_new_pof_pdf():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, PASSWORD)
        mail.select("inbox")
        # Search for POF emails (avoid Unicode in IMAP search)
        status, messages = mail.search(None, 'FROM "pof@journal.org"')
        pdf_files = []

        for num in messages[0].split():
            status, data = mail.fetch(num, '(RFC822)')
            msg = email.message_from_bytes(data[0][1])
            for part in msg.walk():
                if part.get_content_type() == "application/pdf":
                    filename = decode_header(part.get_filename())[0][0]
                    if isinstance(filename, bytes):
                        filename = filename.decode()
                    filepath = os.path.join(DOWNLOAD_FOLDER, filename)
                    with open(filepath, "wb") as f:
                        f.write(part.get_payload(decode=True))
                    pdf_files.append(filepath)
        
        mail.close()
        mail.logout()
        return pdf_files
    except Exception as e:
        print(f"Error downloading PDFs: {e}")
        return []

if __name__ == "__main__":
    files = download_new_pof_pdf()
    print("Downloaded PDFs:", files)
