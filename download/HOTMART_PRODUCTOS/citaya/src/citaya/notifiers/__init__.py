"""CitaYa — Notification channels."""
from __future__ import annotations
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import httpx
from citaya.core.config import get_settings


async def send_email(to: str, subject: str, body: str) -> bool:
    s = get_settings()
    if not all([s.smtp_host, s.smtp_user, s.smtp_password, s.email_from]):
        return False
    msg = MIMEMultipart("alternative")
    msg["From"] = s.email_from
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html", "utf-8"))
    try:
        with smtplib.SMTP(s.smtp_host, s.smtp_port, timeout=15) as server:
            server.starttls()
            server.login(s.smtp_user, s.smtp_password)
            server.sendmail(s.email_from, [to], msg.as_string())
        return True
    except Exception:
        return False


async def send_whatsapp(to: str, text: str) -> bool:
    s = get_settings()
    if not s.whatsapp_access_token:
        return False
    # Simplified — would need WA Cloud API phone_number_id
    return False  # placeholder


async def send_telegram(chat_id: str, text: str) -> bool:
    s = get_settings()
    if not s.telegram_bot_token:
        return False
    url = f"https://api.telegram.org/bot{s.telegram_bot_token}/sendMessage"
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.post(url, json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"})
    return r.status_code == 200


async def send_appointment_confirmation(appointment, professional, business_name: str):
    """Send confirmation via all configured channels."""
    subject = f"✓ Cita confirmada — {business_name}"
    body = f"""
    <h2>✓ Tu cita está confirmada</h2>
    <p><b>{business_name}</b></p>
    <p><b>Profesional:</b> {professional.name}</p>
    <p><b>Servicio:</b> {appointment.service_name}</p>
    <p><b>Fecha:</b> {appointment.start_at.strftime('%d/%m/%Y')}</p>
    <p><b>Hora:</b> {appointment.start_at.strftime('%H:%M')} - {appointment.end_at.strftime('%H:%M')}</p>
    <p><b>Código:</b> {appointment.id}</p>
    <p style="margin-top:20px;color:#666;font-size:12px">Para cancelar, responde a este email.</p>
    """
    text = f"✓ Cita confirmada\n{business_name}\n{professional.name}\n{appointment.service_name}\n{appointment.start_at.strftime('%d/%m/%Y %H:%M')}\nCódigo: {appointment.id}"

    results = {}
    if appointment.customer_email:
        results["email"] = await send_email(appointment.customer_email, subject, body)
    if appointment.customer_phone:
        # Try Telegram (assume phone is chat_id for demo)
        results["telegram"] = await send_telegram(appointment.customer_phone, text)
    return results
