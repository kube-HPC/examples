# Active Directory Demo Pipeline

This example contains a demonstration pipeline for handling Active Directory (AD) users. The pipeline consists of three algorithms, connected in the following order:

```
input_processor --> ad_disable --> send_mail
```

- `send_mail` only processes requests that succeeded in the previous step.
- `ws-mock-service` simulates notifications and acts as a sidecar for both `ad_disable` and `send_mail`.

## Repository Structure

- `input_processor/` – Node 1: Validates and preprocesses input.
- `ad_disable/` – Node 2: Disables AD accounts via LDAP and sends notifications.
- `send_mail/` – Node 3: Sends email via SMTP (MailHog) and notifies via WebSocket.
- `ws-mock-service/` – Mock WebSocket service for notifications.
- `specs/` – Specifications for each algorithm and pipeline in HKube.

## Running the Pipeline

### Prerequisites

- A Kubernetes cluster with LDAP deployed in the `ldap` namespace.

### Viewing Emails

Forward MailHog port from the `send_mail` pod:
```
kubectl port-forward <pod-name> 8025:8025
```
Open in your browser: [http://localhost:8025/](http://localhost:8025/)
Note - it's a sidecar of send_mail.

### Environment Variables

**input_processor:**
- `PROCESSING_TIME` – Seconds to simulate processing per user (default 10).

**ad_disable:**
- `LDAP_URI` – LDAP server URI.
- `LDAP_BASE_DN` – Base DN for LDAP users.
- `LDAP_ADMIN_DN` – Admin DN for LDAP.
- `LDAP_ADMIN_PASSWORD` – Admin password.
- `NOTIFY_WS_URL` – WebSocket URL for notifications.

**send_mail:**
- `NOTIFY_WS_URL` – WebSocket URL for notifications.
- `SMTP_HOST` – SMTP server host.
- `SMTP_PORT` – SMTP server port.
- `SMTP_FROM` – Sender email address.

### Changing WS Mock Service

If you modify `ws-mock-service.py` and want to use a custom image:

```bash
docker build -t hkube-mock-service:v1.1 .
docker push hkube-mock-service:v1.1
```

Update the sidecar image in both `send_mail` and `ad_disable` algorithm specs to use the new image.

## Usage Notes

- The `ws-mock-service` keeps the WebSocket alive to receive notifications from both `ad_disable` and `send_mail`.
- Only successful AD disable operations are sent to `send_mail`.
- The pipeline simulates processing time and sends real-time notifications via WebSocket mock.

---

This setup allows safe testing of AD operations and email notifications without affecting real users.

