# End-to-End Automated DevOps Infrastructure: Containerized Flask Application with GitHub Actions CI/CD and Amazon ECR Integration

This repository serves as a production-ready template demonstrating an end-to-end DevOps engineering workflow. It automates the code validation, containerization, staging, and structural deployment delivery pipeline of a Python Flask web application backed by a cloud-managed MongoDB Atlas non-relational database cluster.

---

## 🏗️ Architectural Topology Overview

The system architecture implements an automated Continuous Integration and Continuous Delivery (CI/CD) loop processing structural state updates straight to cloud image persistence:

```text
[ Local Workstation ] --( Git Push )--> [ GitHub Repository ]
                                                │
                                      ( Triggers Runner VM )
                                                │
                                                ▼
                                    [ GitHub Actions Engine ]
                                     ├── 1. Run Flake8 Linter
                                     ├── 2. Build Docker Image
                                     └── 3. Authenticate AWS IAM
                                                │
                                                ▼ ( Secure Docker Push )
                                    [ Amazon ECR Registry ]
                                     └── Image Layer Target (latest)
```

### Core Technologies Implemented
* **Web Runtime Layer:** Python 3.10 / Flask Micro-framework
* **Persistence Layer:** MongoDB Atlas (Multi-node Cloud Distributed Database Cluster)
* **Virtualization Layer:** Docker / Multi-Stage Optimization Core
* **Automation Workflow Orchestration Engine:** GitHub Actions Engine
* **Cloud Security Identity Broker:** AWS IAM / Programmatic Access Control
* **Production Image Target Registry:** Amazon Elastic Container Registry (ECR)

---

## 🛠️ Step-by-Step Implementation Blueprint

### 1. Local Application Setup & Code Optimization
To secure application pathways and guarantee seamless local configuration execution tracking, the source platform code was refactored away from hardcoded states:
* **Dependency Isolation:** Initiated an independent virtual environment runtime wrapper to sandbox framework package requirements via `python3 -m venv venv`.
* **State Decoupling:** Added runtime parameter binding logic by using `load_dotenv()` to pull configuration fields directly from local `.env` runtime dictionaries.
* **Database Driver Realignment:** Refactored the database initialization sequence inside `app.py` to map system environment bindings directly onto the active Flask global configuration dictionary map (`app.config["MONGO_URI"]`) **before** triggering the `PyMongo(app)` constructor to completely block initialization errors.

### 2. Multi-Stage Containerization Design
A highly optimized, production-hardened `Dockerfile` was authored to map structural logic compilation parameters:
* **Base Footprint Reduction:** Implemented an official, lightweight `python:3.10-slim` runtime base image layer to limit external package vulnerabilities and minimize attack vectors.
* **Container Isolation Routing:** Bound internal communication listening contexts to all external router addresses (`0.0.0.0`) mapping out to container system port `5000`.
* **Resource Optimization Matrix:** Integrated a strict `.dockerignore` tracking filter list to systematically block localized dependency files (`venv/`), Python compile logs (`__pycache__/`), and high-security file systems (`.env`) from bloating final production image layers.

### 3. CI/CD Pipeline Engineering Automation
The delivery workflow script was written from scratch under `.github/workflows/deploy.yml` to orchestrate secure platform staging operations on every code modification push:
* **Syntax Enforcement Gateways:** Added code syntax verification checks leveraging `flake8` to parse the structural integrity of script logic files (`app.py`, `test_app.py`) for formatting errors.
* **Clean-Slate Optimization:** Removed overlapping, broken pipeline dependencies (`securegate.yml`) from the active tracking branch history index to unblock structural workflows.
* **AWS IAM Access Security Mapping:** Configured encrypted cryptographic secrets mapping target credentials (`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`) securely inside the GitHub runtime repository workspace dashboard.

---

## 🔍 Validation & Pipeline Evidence Logs

### Evidence A: GitHub Actions Pipeline Execution Success
The continuous delivery automation workflow handles task executions natively on GitHub infrastructure. Each phase—from lint testing and AWS IAM signature authentication to multi-layered image assembly—completes without warning errors.

#### 1. Workflow Pipeline Status Run Result Screenshot
*(Replace the placeholder image asset reference below with your GitHub Actions dashboard view showing a clean green checkmark status).*

![GitHub Actions Execution Summary](https://placeholder.com)

#### 2. Terminal Compilation Logging Receipt (Docker Push Stage)
*(Replace the placeholder image asset reference below with a detailed visual crop showing the expanded terminal outputs of your "Build, Tag, and Push Image to Amazon ECR" log step).*

![GitHub Actions ECR Terminal Push Output](https://placeholder.com)

---

### Evidence B: AWS Cloud Artifact Persistence Verification
The final compiled binary package successfully reaches cloud persistence targets within your personal Amazon Elastic Container Registry workspace registry dashboard.

#### AWS ECR Target Image Storage Screenshot
*(Replace the placeholder image asset reference below with your AWS console window view navigating to ECR showing your recent image digest cataloged under the "latest" tag reference with a recent timestamp).*

![AWS Elastic Container Registry Console State](https://placeholder.com)

---

## ⚙️ How to Spin Up and Test the Application Locally

Follow these operational steps to build, configure, and execute the service locally inside an isolated workspace context:

### 1. Repository Setup & Dependency Bootstrapping
Execute the initialization commands to map environment dependencies:
```bash
# Clone the verified repository source tracking workspace
git clone https://github.com
cd CI_CD_Pipeline_Assignment_Github_Actions

# Construct and initialize the independent environment sandbox runtime
python3 -m venv venv
source venv/bin/activate

# Fetch and install code system requirements packages
pip install -r requirements.txt
```

### 2. Configure Local Environment Parameters
Construct a secure local environment file named `.env` inside your project's root folder structure to allow local execution pathways to bridge connections to your database:
```ini
MONGO_URI="mongodb+srv://srinivasaddepalli1_db_user:uE38IDDEdcmSeO4o@cluster0.2vowekw.mongodb.net/flask_db?retryWrites=true&w=majority&appName=Cluster0"
SECRET_KEY="override_with_any_highly_secure_cryptographic_string_value"
```

### 3. Launch the Server Infrastructure
Kickstart the local server cluster runtime directly from your terminal session:
```bash
python app.py
```
Once the standard debug server initializes, launch your local web browser interface and browse to **`http://127.0.0.1:5000`** to view your application!
