# send_mail.py
# Node 3 - send email using SMTP (MailHog) and notify external app via WebSocket.

import json
import time
import os
import smtplib
from time import sleep
from email.mime.text import MIMEText
from websocket import create_connection  # from websocket-client

NOTIFY_WS_URL = os.getenv("NOTIFY_WS_URL", "ws://localhost:5000/ws")
SMTP_HOST = os.getenv("SMTP_HOST", "localhost")
SMTP_PORT = int(os.getenv("SMTP_PORT", "1025"))
SMTP_FROM = os.getenv("SMTP_FROM", "example@gmail.com")


def _notify_external(event_type, payload):
    try:
        ws = create_connection(NOTIFY_WS_URL, timeout=5)
        message = {
            "event": event_type,
            "timestamp": int(time.time()),
            "payload": payload
        }
        ws.send(json.dumps(message))

        try:
            ack = ws.recv()
            print(f"[notify] Notification Sent")
        except Exception as e:
            print(f"Exception caught: {e}")
            ack = None
            return ack
        finally:
            ws.close()

        return ack
    except Exception as e:
        print(f"[notify] error: {e}")
        return {"notify_error": str(e)}


def _send_mail(to_email, subject, body):
    """
    Send email via SMTP (MailHog sidecar).
    """
    try:
        if not to_email:
            return {"sent": False, "error": "No recipient email"}

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = SMTP_FROM
        msg["To"] = to_email

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.sendmail(SMTP_FROM, [to_email], msg.as_string())

        print(f"[mail] sent OK → to={to_email}, subject={subject}")
        return {"sent": True}
    except Exception as e:
        print(f"[mail] error while sending: {e}")
        return {"sent": False, "error": str(e)}


def start(args, hkube_api):
    users = args.get("input", [])[0]
    usernames = [it[0].get("user") for it in users if it and isinstance(it, list) and len(it) > 0]
    print(f"[start] users: {usernames}")

    results = []
    for idx, it in enumerate(users):
        if len(it) == 0: pass
        to_email = it[0].get("email")
        user = it[0].get("user")
        case_id = it[0].get("case")
        activity = it[0].get("activity_description")
        ad_disabled = it[0].get("ad_disabled")
        failed = it[0].get("failed")

        subject = f"Notification for {case_id} - {user}"
        extra = "(Failed disabling)" if failed else ""
        body = f"User: {user}\nCase: {case_id}\nActivity: {activity}\nIs AD Disabled: {ad_disabled} {extra}"

        mail_result = _send_mail(to_email, subject, body)

        notify_payload = {
            "user": user,
            "email": to_email,
            "case": case_id,
            "mail_result": mail_result
        }
        notify_ack = _notify_external("mail_sent", notify_payload)

        result_item = {
            "user": user,
            "email": to_email,
            "mail_result": mail_result,
            "notify_ack": notify_ack,
            "sent": mail_result.get("sent", False)
        }

        sleep(1)
        print(f"[start] processed user={user}")
        results.append(result_item)

    sleep(1)
    print(f"[start] all results={results}")
    return results


def stop():
    print("[stop] called")
    return None
