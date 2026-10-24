"""PriceWatch — Notification channels."""
from __future__ import annotations
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import httpx

from pricewatch.core.config import get_settings
from pricewatch.core.models import Alert


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
        r = await client.post(url, json={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
        })
    return r.status_code == 200


async def send_discord(webhook_url: str, text: str) -> bool:
    if not webhook_url:
        return False
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.post(webhook_url, json={"content": text})
    return r.status_code in (200, 204)


async def send_alert(alert: Alert, channels: list[str], recipient: str) -> dict[str, bool]:
    """Send alert via configured channels."""
    s = get_settings()
    subject = f"⚠️ PriceWatch Alert: {alert.product_name[:50]}"
    body = f"""
    <h2>🔔 Alerta de precio</h2>
    <p><b>Producto:</b> <a href="{alert.product_url}">{alert.product_name}</a></p>
    <p><b>Precio anterior:</b> ${alert.old_price}</p>
    <p><b>Precio nuevo:</b> ${alert.new_price}</p>
    <p><b>Diferencia:</b> -${alert.price_diff} ({alert.price_diff_percent}%)</p>
    <p><b>Condición:</b> {alert.condition.value}</p>
    <p style="margin-top:20px;color:#666;font-size:12px">PriceWatch Pro · self-hosted</p>
    """
    text_body = f"🔔 {alert.product_name}\nAntes: ${alert.old_price}\nAhora: ${alert.new_price}\nDiferencia: -${alert.price_diff} ({alert.price_diff_percent}%)\nURL: {alert.product_url}"

    results = {}
    for ch in channels:
        if ch == "email":
            results["email"] = await send_email(recipient, subject, body)
        elif ch == "telegram":
            results["telegram"] = await send_telegram(recipient, text_body)
        elif ch == "discord":
            results["discord"] = await send_discord(recipient or s.discord_webhook_url, text_body)
    return results
