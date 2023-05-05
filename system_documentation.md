# Currency Ratio Alerter (CRA)
### System Documentation

## Overview
Currency Ratio Alerter is a web application that alerts users when the ratio of a pair of currencies crosses specified treshold. It implements the following capabilities:
1. Users can register by providing their username, password and email address. A verification email is sent, and the user account is not registered until the link in that email is clicked/followed.
2. Users can log in and log out.
3. Logged in users can see their specified alerts (as well as the current ratio of the currencies specified in the alert), they can delete alerts, and they can specify new alerts by
    - selecting two currencies (denoted by the standard currency symbols), and
    - entering a treshold value as a decimal number.
4. Once a day a script is run on the backend that retrieves currency prices from https://exchangerate.host/ (a free to use API), and sends emails for each alert with the threshold value between the ratios of the currency rates from the previous run and today.

## System
The system consists of 4 subsystems:
- frontend,
- backend,
- database, and
- messaging.

All communication between frontend, backend and database is accomplished by sending and receiving messages through the messaging subsystem.

We started by creating Oracle VirtualBox Ubuntu virtual machines on 4 different laptops for each subsystem, but that required all 4 laptops to be on and connected for the system to work. We then switched to cloud virtual machines (AWS EC2 Ubuntu instances) which we could control from our laptops using the AWS Console or SSH. We wrote AWS CLI shell scripts (aws_provision.sh in all 4 top folders in the Git repository) to provision this infrastrructure, as well as shell scripts (aws_ssh.sh) to make it convenient to connect to the EC2 instances from our laptops. We also have a service_composer/service_composer.sh script that connects to each EC2 instance and runs the code for each subsystem in the background. This assumes that the latest code is already on each EC2 instance. (Git repository is cloned into the home folder and `git pull` is performed to get the latest code including the messaging system URL which is updated by messaging/aws_rmq_endpoint.sh script.)

### Frontend
Frontened subsystem is implemented as a Gunicorn WSGI server running `craui` Flask application on port 7007.

### Backend
Backend subsystem consists of two parts:
- `bermq` module that listens to "send_email" and "get_currency_rates" queues, and processes the request messages sent to those queues by connecting to the Google SMTP server and the https://exchangerate.host/ API.
- `process_alerts.py` script which is scheduled using crontab (`schedule_process_alerts.sh`) to
    - retrieve all users and their alerts from the database,
    - retrieve all relevant currency rates from https://exchangerate.host/ API, and
    - send emails for alerts which are triggered because the ratio of the currency rates crossed the specified threshold.

### Database
Database subsystem consists of two parts:
- MySQL server (which was originally installed and run on the database EC2 instance) cluster managed by AWS RDS. The cluster consists of two instances running in different availability zones (AWS data centers on independednt and redundant power grid and Internet connections, different flood plains, earthquake fault lines, etc.). One of the instances is used for reading and writing to the database, while the other can be used as a read replica. The read replica is automatically promoted to primary (that can be used for both reading and writing to the database) if the primary becomes unavailable for any reason, and AWS RDS will then automatically start another read replica in a new availability zone.
- `dbrmq.py` that listens to "get_user", "get_users", "register_user", "get_alerts", "set_alert", "update_alert" and "delete_alert" queues, and processes the request messages sent to those queues by connecting to the database server above and executing SQL queries/statements. This could also be part of the backend subsystem, but our understanding was that all communication between backend and database subsystems should go through the messaging subsystem.

### Messaging
Messaging subsystem is implemented as Amazon MQ RabbitMQ cluster. (It was originally a single RabbitMQ server running on a Ubuntu virtual machine.) The cluster consists of three instances running in different availability zones, and remains available as long as at least one of those instances is available.

## Connection
There are several different connections to consider.

Internally, the subsystems are connected by frontend, backend and database each connecting to the messaging subsystem and sending and receiving messages.

The backend also connects to the the Google SMTP server and the https://exchangerate.host/ API.

The users connect using a browser to the frontend on port 7007.

AWS API can be accessed by using AWS Console, AWS CLI, one of many AWS SDKs, or even by making raw HTTP requests. We have scripted almost everything using AWS CLI, but still rely on AWS Console for some things like rebooting EC2 instances.

We are also connecting to the EC2 instances using SSH and a shared SSH key, and downloading the code to those instances from GitHub over the Internet.

## Flowchart

```mermaid
graph TD;
    UserBrowser-->Frontend;
    Frontend-->Messaging;
    Backend-->Messaging;
    Database-->Messaging;
    Backend-->GoogleSMTP;
    Backend-->ExchangeRateHost;
    GoogleSMTP-->UserEmailInbox;
```

## Source Code
The source code in the Git repository is organized by subsystem in the frontend, backend, database and messaging folders. Another top level folder service_composer contains `service_composer.sh` script that connects to each machine using SSH and starts the code running in the background. Another way to categorize the code is into scripts used for provisionsing infrastructure in AWS and generally being executed at build time, and the Python code genertally being executed at run time.

### Build Time Scripts
`generate_ssh_key.sh` was run only once by one of us, and the .zip file it created was shared by email, so that we would all be able to run the next script...<br>
`import_ssh_key.sh` uses the .zip file with both public and private SSH key that was shared by email to install it into each developer's local development environment (usually the Oracle VirtualBox Ubuntu virtual machine that we initially created on our laptops). Other scripts including the `service_composer.sh` rely on the presence of this SSH key.<br>
`aws_provision.sh` for each subsystem uses AWS CLI to provision the infrastructure needed for that subsystem including the SSH key, security group (firewall for EC2 instances) and EC2 instance (or RabbitMQ cluster in case of messaging). This script also writes the public IP address of the provisioned EC2 instance into the `ip.txt` files that are used by `service_composer.sh` and the next script...<br>
`aws_ssh.sh` is a convenience script to connect to each EC2 instance using the shared SSH key.<br>
There are also `compose.sh` and `run.sh` scripts for each system that we used when we were running the system on Oracle VirtualBox Ubuntu virtual machines on our laptops, and later for local testing.<br>
There are also some additional miscellaneous and convenience scripts like `aws_delete_broker.sh`, `aws_provision_single.sh` and `aws_rmq_endpoint.sh` for messaging, and `aws_scp_craappgoogle.sh` and `schedule_process_alerts.sh` for backend subsystem.<br>
All scripts assume that they are being run from the folder they are in, and should be run by executing `source ./<script name>`

### Run Time Code
There is no code in the messaging subsystem, but after initially having a lot of duplicated code for interacting with the messaging subsystem in the other three subsystems, we developed `rmqrpc.py` which is used by frontend, backend and database subsystems. It contains two class definitions:
- `RMQRPCClient` (copied almost exactly from the [RabbitMQ RPC Tutorial](https://www.rabbitmq.com/tutorials/tutorial-six-python.html)), and
- `Listener` which may have been better named RMQRPCServer, and

utility functions imported and used by other code:
- `call` to send requests to a named queue and wait for the response, and
- `listen` to register the functions that can process requests and send responses.

This code assumes that the handler function names are equal to the request queue names and that all request parameters are passed as keyword arguments to `call`. The best way to understand how they are used is by example in:
- `backend/bermq/__main__.py`,
- `databas/dbrmq.py`, and
- `frontend\craui\fermq.py`.

#### Frontend code
The frontend is a simple Flask application developed by following the [Tutorial](https://flask.palletsprojects.com/en/2.2.x/tutorial/) in the Flask documentation almost exactly, and just replacing blog posts with currency ratio alerts. The `craui` Flask application consists of two blueprints:
- `auth.py` that handles user registration (including email verification), authentication, and authorization, and
- `alerts.py` that handles viewing, creating and deleting currency ratio alerts for each logged in user.

#### Backend code
The backend code consists of
- `bermq` module whose `__main__.py` runs continusly to handle sending email (`smtp.py`) and retrieving currency rates (`currency_rates.py`), and
- `process_alerts.py` script which runs once a day, retrieves all users and their alerts from the database, retrieves all relevant currency rates, and send emails for alerts which are triggered because the ratio of the currency rates crossed the specified threshold.

#### Database code (that could run on the backend subsystem)
This is the only code that connects to the MySQL database server. `cradb.py` initializes the `cra` database and creates `users` and `alerts` tables if they do not exist. `dbrmq.py` converts requests from RabbitMQ queues into SQL queries/statements, executes them, and then converts the results into responses that it sends back using RabbitMQ.

Along with `listen` from `rmqrpc.py`, the `execute` function in `dbrmq.py` has helped us eliminate a lot of duplicated code. SQL queries (that start with 'SELECT') return the results as JSON objects that use table column names as keys, and other SQL statements return 'DONE'.

## Trobleshooting
There is very little exception handling implemented so far, and when something fails, the system will generally stop functioning. You can reset everything (without loosing any data in the database) with the following procedure:
1. The easiest way to stop the code running in background on EC2 instances is to reboot them.
2. If the problem was caused by a bad request sent to a RabbitMQ queue, those messages should be purged so that they do not cause the same problem when the code starts running again even if the code that sent a bad request has been fixed.
3. Fix code defects.
4. Verify that the latest versions of the following files pushed to GitHub contain the correct configuration values:
- `database/dbrmq.py` (db_host, db_user and db_password)
- `frontend/craui/rmq_url.py` (RabbitMQ endpoint URL)
- `backend/bermq/rmq_url.py` (RabbitMQ endpoint URL)
- `database/rmq_url.py` (RabbitMQ endpoint URL)
- `frontend/ip.txt`
- `backend/ip.txt`
- `database/ip.txt`
5. Log into frontend, backend and database EC2 instances using `aws_ssh.sh` and ensure that the latest code from GitHub has been downloaded. (`git pull`)
6. Execute `service_composer.sh` script to start everything up again.
7. Test, rinse and repeat.

## Glossary
- CRA: Currency Ratio Alerter, the web application that monitors currency ratios and sends alerts.
- API: Application Programming Interface, a set of rules that allow different software applications to communicate with each other.
- AWS: Amazon Web Services, a cloud computing platform that provides various services like EC2, RDS, and messaging.
- EC2: Amazon Elastic Compute Cloud, a web service that provides resizable compute capacity in the cloud.
- RDS: Amazon Relational Database Service, a web service that makes it easier to set up, operate, and scale a relational database in the cloud.
- RabbitMQ: An open-source message broker that implements the Advanced Message Queuing Protocol (AMQP).
- Gunicorn: A Python Web Server Gateway Interface (WSGI) HTTP server, used to serve the frontend CRA application.
- WSGI: Web Server Gateway Interface, a standard interface between web servers and Python web applications or frameworks.
- SMTP: Simple Mail Transfer Protocol, a communication protocol used for sending email messages over the internet.
- SSH: Secure Shell, a cryptographic network protocol used for secure communication over an unsecured network.
- SQL: Structured Query Language, a programming language used to communicate with and manipulate databases.
- Crontab: A Unix-based utility that allows you to schedule tasks to run automatically at specified intervals.

## Architecture Improvements
If we were designing a system like this outside of a college course, we would rely on [AWS Serverless](https://aws.amazon.com/serverless/) architecture, and used services like SQS instead of RabbitMQ, Lambda instead of EC2, and DynamoDB instead of MySQL. This would make the system almost infinitely (and effortlessly) scalable both up (if we had millions of users) and down (to $0 if we had no users). We would also use [AWS CDK](https://aws.amazon.com/cdk/) instead of AWS CLI.
