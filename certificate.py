# certificate.py
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from PIL import Image
from datetime import datetime, timedelta
import os
import io
import qrcode

QR_LINK = "https://t.me/DoctorJojiBot"
CERT_DIR = "certificates"
LOGO_PATH = "Logo.png"  # Make sure your high-res crisp Logo.png is placed here

os.makedirs(CERT_DIR, exist_ok=True)

def get_next_serial_id(today_str):
    counter_file = os.path.join(CERT_DIR, f"counter_{today_str}.txt")
    count = 1
    if os.path.exists(counter_file):
        with open(counter_file, "r") as f:
            count = int(f.read().strip()) + 1
    with open(counter_file, "w") as f:
        f.write(str(count))
    return count

def generate_clean_medical_certificate_v2(patient_name, nric, rest_days):
    today = datetime.now()
    today_str = today.strftime("%d%m%Y")
    date_formatted = today.strftime("%d %b %Y")
    serial_id = get_next_serial_id(today_str)
    cert_id = f"DRJOJI-{today_str}-{serial_id:06d}"

    # ✅ Correct way to add days even across months
    end_date = (today + timedelta(days=rest_days - 1)).strftime("%d %b %Y")

    pdf_path = os.path.join(CERT_DIR, f"{cert_id}.pdf")
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    # Set a clean white or slight off-white background
    c.setFillColor(HexColor("#f2f3f4"))
    c.rect(0, 0, width, height, fill=True, stroke=False)
    c.setFillColor("black")

    # Load and draw high-res logo
    if os.path.exists(LOGO_PATH):
        logo = Image.open(LOGO_PATH)
        logo = logo.resize((200, 200))  # 📸 Resizing logo to 200x200 for sharp print
        logo_io = io.BytesIO()
        logo.save(logo_io, format='PNG')
        logo_io.seek(0)
        c.drawImage(ImageReader(logo_io), width / 2 - 100, height - 180, width=200, height=200, mask='auto')

    # Centered Header
    def draw_centered(text, y, size=12, bold=False):
        c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        c.drawCentredString(width / 2, y, text)

    draw_centered("DrJoji Healthcare", height - 200, size=18, bold=True)
    draw_centered("Doctor Joji on Telegram", height - 220, size=12)

    y = height - 280
    draw_centered("Medical Certificate", y, size=16, bold=True)
    y -= 40

    # Labels and Values
    def draw_label_value(label, value, x, y):
        c.setFont("Helvetica-Bold", 11)
        c.drawString(x, y, label)
        c.setFont("Helvetica", 11)
        c.drawString(x + 170, y, value)

    draw_label_value("Medical Certificate ID:", cert_id, 70, y); y -= 18
    draw_label_value("Date of Consultation:", date_formatted, 70, y); y -= 18
    draw_label_value("Doctor:", "Doctor Joji", 70, y); y -= 18
    draw_label_value("Patient Name:", patient_name, 70, y); y -= 18
    draw_label_value("NRIC/FIN:", nric, 70, y); y -= 30

    c.setFont("Helvetica", 11)
    c.drawString(70, y, "This is to certify that the above-named patient has been given:")
    y -= 18
    c.drawString(70, y, f"Medical Certificate from {date_formatted} to {end_date} inclusive.")

    y -= 50
    c.setFont("Helvetica-Bold", 10)
    c.drawString(70, y, "This medical certificate is not valid at all.")
    y -= 16
    c.setFont("Helvetica", 10)
    c.drawString(70, y, "*This certificate is electronically generated. No signature is required.")

    # QR Code
    qr = qrcode.make(QR_LINK)
    qr_buf = io.BytesIO()
    qr.save(qr_buf, format='PNG')
    qr_buf.seek(0)
    c.drawImage(ImageReader(qr_buf), width - 120, 60, width=60, height=60)

    c.save()
    return pdf_path
