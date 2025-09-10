# Active Directory Demo Pipeline

This example demonstrates a pipeline for handling Active Directory (AD) users.  
The pipeline consists of three algorithms, connected in this order:

```
input_processor --> ad_disable --> send_mail
```

* `send_mail` only processes requests that succeeded in the previous step.
* `ws-service` simulates notifications and acts as a sidecar for both `ad_disable` and `send_mail`.

## Repository Structure

* `input_processor/` – Node 1: Validates and preprocesses input.
* `ad_disable/` – Node 2: Disables AD accounts via LDAP and sends notifications.
* `send_mail/` – Node 3: Sends email via SMTP (MailHog) and notifies via WebSocket.
* `ws-service/` – WebSocket service for notifications.
* `specs/` – Specifications for each algorithm and pipeline in HKube.

## Running the Pipeline

### Prerequisites

* Kubernetes cluster with LDAP deployed in the `ldap` namespace.
* Running MailHog pod and service (for SMTP simulation) in the `mailhog` namespace.

### Creating MailHog Pod & Service

Inside `/specs`, deploy the provided YAMLs:

```bash
kubectl apply -f mailhog_namespace.yaml
kubectl apply -f mailhog_deployment.yaml
kubectl apply -f mailhog_service.yaml
```

### Determining the Cluster Domain

Both LDAP and MailHog rely on the cluster domain for their hostnames.

* For LDAP in `ldap` namespace:

```bash
kubectl run dns-test --rm -i --tty --image=busybox --restart=Never --namespace=ldap \
  -- sh -c 'grep search /etc/resolv.conf | awk "{print \$2}"'
```

* For MailHog in `mailhog` namespace:

```bash
kubectl run dns-test --rm -i --tty --image=busybox --restart=Never --namespace=mailhog \
  -- sh -c 'grep search /etc/resolv.conf | awk "{print \$2}"'
```
This will print: `<namespace>.svc.<CLUSTER_DOMAIN>`  
You can then set:

* `LDAP_URI` → `ldap://<ldap-pod>.<ldap-namespace>.svc.<CLUSTER_DOMAIN>:389` (389 is ldap service port)
* `SMTP_HOST` → `mailhog.<namespace>.svc.<CLUSTER_DOMAIN>`

### Viewing Emails

Forward MailHog port from the `send_mail` pod:

```bash
kubectl port-forward <pod-name> 8025:8025
```

Open in your browser: [http://localhost:8025/](http://localhost:8025/)

### Environment Variables

**input\_processor:**

* `PROCESSING_TIME` – Seconds to simulate processing per user (default: 10).

**ad\_disable:**

* `LDAP_URI` – LDAP server URI (use cluster domain as above).
* `LDAP_BASE_DN` – Base DN for LDAP users.
* `LDAP_ADMIN_DN` – Admin DN for LDAP.
* `LDAP_ADMIN_PASSWORD` – Admin password.
* `NOTIFY_WS_URL` – WebSocket URL for notifications.

**send\_mail:**

* `NOTIFY_WS_URL` – WebSocket URL for notifications.
* `SMTP_HOST` – SMTP server host (use cluster domain as above).
* `SMTP_PORT` – SMTP server port.
* `SMTP_FROM` – Sender email address.

### Changing WS Service

If you modify `ws-service.py` and want to use a custom image:

```bash
docker build -t myrepo/hkube-service:v1.1 .
docker push myrepo/hkube-service:v1.1
```

> Update the sidecar image in both `send_mail` and `ad_disable` algorithm specs.
> Replace `myrepo` with your container registry.

## Usage Notes

* `ws-service` keeps the WebSocket alive to receive notifications from both `ad_disable` and `send_mail`.
* Only successful AD disable operations are sent to `send_mail`.
* The pipeline simulates processing time and sends real-time notifications via local WebSocket.

---

Safe testing of AD operations and email notifications without affecting real users.
