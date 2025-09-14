## Debugging OpenLDAP

To inspect and debug the LDAP server, you can use the following commands:

### Start an LDAP Debug Pod

```bash
kubectl run ldap-debug --rm -it --image=bitnami/openldap:2.6.9-debian-12-r9 --env LDAP_ADMIN_PASSWORD=<passwordFromSecret> -- bash
```

This will start a temporary pod with an interactive shell and the correct LDAP tools.

### Search LDAP Entries

Inside the debug pod, run:

```bash
ldapsearch -x -H ldap://<LDAP_URI>:389 -D "cn=admin,dc=example,dc=org" -w "$LDAP_ADMIN_PASSWORD" -b "ou=People,dc=example,dc=org" "(uid=user2)" uid cn userPassword pwdAccountLockedTime
```

Replace `<LDAP_URI>` and credentials as needed.  
This command will show details for the user with `uid=user2`.
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
* `specs/` – Specifications for each algorithm and pipeline in HKube:
  * `node1-processor.json` – Input processor node spec
  * `node2-ad-disable.json` – AD disable node spec
  * `node3-send-mail.json` – Send mail node spec
  * `demo-mvp.json` – Example pipeline spec
  * `mailhog/` – Mailhog deployment YAMLs:
    * `mailhog_namespace.yaml`
    * `mailhog_deployment.yaml`
    * `mailhog_service.yaml`
  * `openldap/` – OpenLDAP deployment YAMLs:
    * `ldap_cm.yaml`
    * `ldap_deployment_service.yaml`
    * `ldap_secret.yaml`

## Running the Demo App

A Node.js demo application is provided in the `demo-app/` folder. This app allows you to interact with the pipeline, trigger executions, and view results via a simple web interface.


### Setup & Usage

```bash
cd demo-app
npm install
node server.js
```

The app will start on [http://localhost:3000](http://localhost:3000).

**Purpose:**  
The demo app provides endpoints to trigger pipeline runs, check job status, and view parsed job graphs. It is useful for testing and visualizing pipeline executions without using the HKube UI directly.

## Running the Pipeline

### Prerequisites

* Kubernetes cluster
* Access to deploy services in the cluster
* OpenLDAP deployed in the `ldap` namespace (see instructions below)
* MailHog pod and service (for SMTP simulation) in the `mailhog` namespace (see instructions below)


### Creating MailHog Pod & Service

Inside `/specs/mailhog`, deploy the provided YAMLs:

```bash
kubectl apply -f mailhog/mailhog_namespace.yaml
kubectl apply -f mailhog/mailhog_deployment.yaml
kubectl apply -f mailhog/mailhog_service.yaml
```

This will deploy Mailhog in the `mailhog` namespace.

### Creating LDAP Pod & Service

Inside `/specs/openldap`, deploy the provided YAMLs:

```bash
kubectl apply -f openldap/ldap_namespace.yaml
kubectl apply -f openldap/ldap_cm.yaml
kubectl apply -f openldap/ldap_secret.yaml
kubectl apply -f openldap/ldap_deployment_service.yaml
```

This will create the `ldap` namespace and deploy an OpenLDAP server with preloaded users in it.

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

* `LDAP_URI` → `ldap://<ldap-service>.<namespace>.svc.<CLUSTER_DOMAIN>:389` (389 is ldap service port)
* `SMTP_HOST` → `<mailhog_service>.<namespace>.svc.<CLUSTER_DOMAIN>`

> If followed closely, `<mailhog_service>` suppose to be `mailhog`, `<namespace>`=`default`  
> For LDAP, `<ldap-service>` suppose to be `ldap-service`, `<namespace>`=`ldap`

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
