# ad_disable.py
# Node 2 - disable AD account via HTTP API and notify external app via WebSocket.

import json
import time
from time import sleep
import random, string
from websocket import create_connection
from ldap3 import Server, Connection, ALL, MODIFY_REPLACE
import os

LDAP_URI = os.getenv("LDAP_URI", "ldap://openldap.ldap.svc.cluster.local:389")
LDAP_BASE_DN = os.getenv("LDAP_BASE_DN", "dc=example,dc=org")
LDAP_ADMIN_DN = os.getenv("LDAP_ADMIN_DN", "cn=admin,dc=example,dc=org")
LDAP_ADMIN_PASSWORD = os.getenv("LDAP_ADMIN_PASSWORD", "adminpassword")
NOTIFY_WS_URL = os.getenv("NOTIFY_WS_URL", "ws://localhost:5000/ws")

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

def _disable_ad_user(username):
    """
    Connect to LDAP and disable the given user by setting pwdAccountLockedTime.
    """
    try:
        server = Server(LDAP_URI, get_info=ALL)
        conn = Connection(server, LDAP_ADMIN_DN, LDAP_ADMIN_PASSWORD, auto_bind=True)
        user_dn = f"uid={username},ou=People,{LDAP_BASE_DN}"
        # Generate a random password to effectively lock the account
        random_pass = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        changes = {'userPassword': [(MODIFY_REPLACE, [random_pass])]}
        success = conn.modify(user_dn, changes)

        if success:
            print(f"[AD] User {username} disabled")
            return {"success": True, "action": "disabled", "user": username}
        else:
            print(f"[AD] Failed to disable user {username}: {conn.result}")
            return {"success": False, "user": username, "error": conn.result}

    except Exception as e:
        print(f"[AD] Exception while disabling user {username}: {e}")
        return {"success": False, "user": username, "error": str(e)}

def start(args, hkube_api):
    users = args["input"][0]
    user_names = [it.get("user") for it in users]
    print(f"[start] users: {user_names}")

    results = []
    for it in users:
        username = it.get("user")
        email = it.get("email")
        activity_description = it.get("activity_description")
        case = it.get("case")

        ad_result = _disable_ad_user(username)
        notify_payload = {
            "user": username,
            "ad_result": ad_result
        }
        sleep(1)
        _notify_external("ad_disable", notify_payload)

        if ad_result.get("success"):
            results.append({
                "user": username,
                "email": email,
                "ad_disabled": True,
                "ad_result": ad_result,
                "activity_description": activity_description,
                "case": case,
                "failed": False
            })
        # else: Commented because not needed to send mail if it fails.
        #     results.append({
        #         "user": username,
        #         "email": email,
        #         "ad_disabled": False,
        #         "ad_result": ad_result,
        #         "notify_ack": notify_ack,
        #         "activity_description": activity_description,
        #         "case": case,
        #         "failed": True
        #     })
    sleep(1)
    print(f"[start] results: {results}")
    return results