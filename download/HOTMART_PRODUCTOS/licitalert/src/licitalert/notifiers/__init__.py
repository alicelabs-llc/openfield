"""LicitAlert — Notifications."""
from __future__ import annotations
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import httpx

from licitalert.core.config import get_settings
from licitalert.core.models import TenderMatch


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


async def send_telegram(chat_id: str, text: str) -> bool:
    s = get_settings()
    if not s.telegram_bot_token:
        return False
    url = f"https://api.telegram.org/bot{s.telegram_bot_token}/sendMessage"
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.post(url, json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"})
    return r.status_code == 200


async def send_matches_alert(matches: list[TenderMatch], channels: list[str], recipient: str) -> dict[str, bool]:
    """Send alert with matched tenders."""
    if not matches:
        return {}

    subject = f"🔔 LicitAlert: {len(matches)} licitaciones nuevas"
    rows_html = ""
    rows_text = ""
    for m in matches:
        t = m.tender
        rows_html += f"""
        <tr>
            <td>{t.country.value.upper()}</td>
            <td><a href="{t.url}">{t.title[:60]}</a></td>
            <td>{t.entity}</td>
            <td>{'$' + str(t.budget) if t.budget else 'N/A'}</td>
            <td>{m.score}%</td>
        </tr>
        """
        rows_text += f"• [{t.country.value.upper()}] {t.title[:50]} — {t.entity}\n"

    body = f"""
    <h2>🔔 {len(matches)} licitaciones que coinciden con tus alertas</h2>
    <table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse;">
        <tr style="background:#f0f0f0;">
            <th>País</th><th>Título</th><th>Entidad</th><th>Presupuesto</th><th>Score</th>
        </tr>
        {rows_html}
    </table>
    """
    text_body = f"LicitAlert: {len(matches)} nuevas licitaciones\n\n{rows_text}"

    results = {}
    for ch in channels:
        if ch == "email":
            results["email"] = await send_email(recipient, subject, body)
        elif ch == "telegram":
            results["telegram"] = await send_telegram(recipient, text_body)
    return results
