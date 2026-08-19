# CI/CD Pipeline for Flask Application

## Flask + MongoDB + Docker + GitHub Actions + AWS ECR + AWS EC2

---

## 1. Project Overview

This project demonstrates an end-to-end **CI/CD pipeline** for a Python Flask web application.

The application is a simple **Student Management System** that uses MongoDB as its database. The application is containerized using Docker and automatically deployed to an Amazon EC2 instance using GitHub Actions.

The CI/CD pipeline automatically performs:

1. Source code checkout
2. Python dependency installation
3. Flake8 code validation
4. Automated testing using Pytest
5. AWS credential configuration
6. Docker image creation
7. Docker image push to Amazon ECR
8. SSH deployment to Amazon EC2
9. Docker container replacement
10. Application health check
11. Deployment success/failure verification

---

# 2. Project Objective

The main objective of this project is to implement an automated CI/CD pipeline where a developer can push code to GitHub and the application is automatically:

```text
GitHub
   |
   v
GitHub Actions
   |
   +---- Code Checkout
   |
   +---- Install Dependencies
   |
   +---- Flake8 Validation
   |
   +---- Pytest
   |
   +---- Docker Build
   |
   +---- Push Image to Amazon ECR
   |
   +---- SSH to Amazon EC2
   |
   +---- Pull Docker Image
   |
   +---- Start Flask Container
   |
   +---- Health Check
   |
   v
Production Application
````

This eliminates the need to manually build, transfer, and deploy the application after every code change.

---

# 3. Technologies Used

| Technology     | Purpose                          |
| -------------- | -------------------------------- |
| Python         | Application programming language |
| Flask          | Web application framework        |
| MongoDB Atlas  | Cloud database                   |
| PyMongo        | MongoDB integration              |
| Pytest         | Automated testing                |
| Mongomock      | MongoDB mocking during tests     |
| Flake8         | Code validation                  |
| Docker         | Application containerization     |
| GitHub         | Source-code repository           |
| GitHub Actions | CI/CD automation                 |
| Amazon ECR     | Docker image registry            |
| Amazon EC2     | Application hosting              |
| SSH            | Secure EC2 deployment            |
| curl           | Application health check         |

---

# 4. Application Features

The Flask application provides a Student Management System.

The application supports:

* Displaying students
* Adding students
* Updating students
* Deleting students
* MongoDB database integration
* Application health monitoring

---

# 5. Application Routes

| Route                  | Method   | Description              |
| ---------------------- | -------- | ------------------------ |
| `/`                    | GET      | Display all students     |
| `/health`              | GET      | Application health check |
| `/add`                 | GET/POST | Add a student            |
| `/update/<student_id>` | GET/POST | Update a student         |
| `/delete/<student_id>` | GET      | Delete a student         |

---

# 6. Health Check Endpoint

The application provides a dedicated health endpoint:

```python
@app.route("/health")
def health():
    return {"status": "healthy"}, 200
```

The CI/CD pipeline uses this endpoint to verify that the deployed application is working correctly.

A successful health check returns:

```json
{
  "status": "healthy"
}
```

The deployment is considered successful only after the health check returns HTTP `200`.

---

# 7. Project Structure

The project structure is:

```text
flask_Practice/
│
├── app.py
├── test_app.py
├── requirements.txt
├── Dockerfile
├── .gitignore
├── .env
│
├── templates/
│   ├── index.html
│   ├── add_student.html
│   └── update_student.html
│
└── .github/
    └── workflows/
        └── deploy.yml
```

---

# 8. Important Files

## `app.py`

Contains the Flask application, MongoDB configuration, routes, and health-check endpoint.

## `test_app.py`

Contains automated tests for the Flask application.

## `requirements.txt`

Contains Python dependencies required by the application.

## `Dockerfile`

Contains instructions to build the Docker image.

## `.github/workflows/deploy.yml`

Contains the complete GitHub Actions CI/CD pipeline.

## `.env`

Contains local environment variables.

> Never commit `.env` to GitHub.

---

# 9. MongoDB Configuration

The application uses MongoDB Atlas.

The MongoDB connection string is provided through an environment variable:

```text
MONGO_URI
```

Example format:

```text
mongodb+srv://username:password@cluster.mongodb.net/student_db
```

The actual MongoDB credentials must not be hard-coded in the source code.

The Flask application reads the variable using:

```python
from dotenv import load_dotenv
import os

load_dotenv()

app.config["MONGO_URI"] = os.getenv("MONGO_URI")
```

MongoDB is accessed through Flask-PyMongo:

```python
mongo = PyMongo(app, tlsCAFile=certifi.where())
```

---

# 10. MongoDB Collection

Student records are stored in the:

```text
students
```

collection.

The application performs the following MongoDB operations:

### Read

```python
mongo.db.students.find()
```

### Insert

```python
mongo.db.students.insert_one(...)
```

### Update

```python
mongo.db.students.update_one(...)
```

### Delete

```python
mongo.db.students.delete_one(...)
```

---

# 11. Local Development Setup

## Step 1 – Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd flask_Practice
```

---

## Step 2 – Create a Virtual Environment

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

---

## Step 3 – Install Dependencies

```bash
pip install -r requirements.txt
```

Development/test dependencies should include:

```text
pytest
mongomock
flake8
```

---

# 12. Configure Environment Variables

Create a `.env` file:

```text
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/student_db
SECRET_KEY=your-secret-key
```

Do not commit this file.

Add `.env` to `.gitignore`:

```text
.env
venv/
__pycache__/
.pytest_cache/
```

---

# 13. Run Flask Application Locally

Run:

```bash
python app.py
```

The application starts on:

```text
http://127.0.0.1:5000
```

Open the application in a browser:

```text
http://127.0.0.1:5000/
```

---

# 14. Test the Health Endpoint Locally

Run:

```bash
curl --fail http://localhost:5000/health
```

Expected output:

```json
{"status": "healthy"}
```

This confirms that the Flask application is responding successfully.

---

# 15. Automated Testing

Run the test suite:

```bash
python3 -m pytest -v test_app.py
```

A successful test execution should show the tests passing.

The purpose of the automated tests is to ensure that application changes do not introduce regressions.

---

# 16. Flake8 Validation

Run Flake8 against the project source code:

```bash
flake8 . \
  --exclude=venv \
  --count \
  --select=E9,F63,F7,F82 \
  --show-source \
  --statistics
```

The `venv` directory should be excluded because it contains third-party packages rather than project source code.

Flake8 checks for serious Python errors including:

* Syntax errors
* Undefined names
* Invalid Python constructs
* Other critical code issues

---

# 17. Docker Configuration

The application is containerized using Docker.

The Docker image packages:

* Python
* Flask
* Application source code
* Python dependencies
* HTML templates
* Required runtime configuration

---

# 18. Build Docker Image

Build the Docker image:

```bash
docker build -t flask-practice-app:latest .
```

Verify the image:

```bash
docker images
```

Expected image:

```text
flask-practice-app
```

---

# 19. Run Docker Container Locally

Run:

```bash
docker run -d \
  --name flask_app_container \
  -p 5000:5000 \
  -e MONGO_URI="$MONGO_URI" \
  flask-practice-app:latest
```

Check the running container:

```bash
docker ps
```

Expected port mapping:

```text
0.0.0.0:5000->5000/tcp
```

---

# 20. Test Docker Application

Run:

```bash
curl --fail http://localhost:5000/health
```

Expected:

```json
{"status": "healthy"}
```

This confirms that the application is working inside the Docker container.

---

# 21. Docker Container Name Conflict

If Docker displays:

```text
Conflict. The container name "/flask_app_container" is already in use
```

check existing containers:

```bash
docker ps -a
```

Remove the old container:

```bash
docker rm -f flask_app_container
```

Then start the new container again.

---

# 22. Port 5000 Conflict

If Flask displays:

```text
Address already in use
Port 5000 is in use
```

check running containers:

```bash
docker ps
```

If an existing Docker container is already using port 5000, test it using:

```bash
curl http://localhost:5000/health
```

If the response is:

```json
{"status": "healthy"}
```

the existing container is already serving the application.

---

# 23. AWS Architecture

The deployment uses the following AWS architecture:

```text
GitHub Actions
       |
       | Docker Image
       v
Amazon ECR
       |
       | docker pull
       v
Amazon EC2
       |
       v
Docker Container
       |
       v
Flask Application
       |
       v
MongoDB Atlas
```

---

# 24. Amazon ECR

Amazon Elastic Container Registry is used to store Docker images.

The repository used by the pipeline is:

```text
flask-app
```

The Docker image is tagged using the Git commit SHA.

Example:

```text
flask-app:eb2014e7d07b130973be412d12fd77bacef6e15e
```

Using the commit SHA provides version traceability.

Every deployed Docker image can be associated with a specific Git commit.

---

# 25. Amazon EC2

Amazon EC2 is used as the production deployment server.

The EC2 instance contains:

* Docker
* AWS CLI
* curl
* Required application runtime

The Flask Docker container runs on:

```text
Port 5000
```

The container uses:

```text
5000:5000
```

to expose the Flask application.

---

# 26. GitHub Actions

The CI/CD workflow is located at:

```text
.github/workflows/deploy.yml
```

The workflow automates the entire deployment process.

---

# 27. CI Pipeline Stages

The CI pipeline performs:

```text
Checkout
   |
   v
Install Dependencies
   |
   v
Flake8
   |
   v
Pytest
```

If either Flake8 or Pytest fails, deployment should not continue.

---

# 28. CD Pipeline Stages

After CI succeeds:

```text
Configure AWS
     |
     v
Login to ECR
     |
     v
Build Docker Image
     |
     v
Push Docker Image
     |
     v
SSH to EC2
     |
     v
Stop Existing Container
     |
     v
Pull New Image
     |
     v
Start New Container
     |
     v
Health Check
```

---

# 29. GitHub Actions Secrets

The following GitHub Secrets are required.

| Secret                  | Description                     |
| ----------------------- | ------------------------------- |
| `MONGO_URI`             | MongoDB Atlas connection string |
| `AWS_ACCESS_KEY_ID`     | AWS access key                  |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key                  |
| `EC2_HOST_IP`           | EC2 public IP                   |
| `EC2_SSH_KEY`           | EC2 SSH private key             |
| `MAIL_USERNAME`         | Email username                  |
| `MAIL_PASSWORD`         | Email password                  |
| `NOTIFICATION_EMAIL`    | Notification recipient          |

Secrets are accessed inside GitHub Actions using:

```yaml
${{ secrets.MONGO_URI }}
```

For example:

```yaml
MONGO_URI: ${{ secrets.MONGO_URI }}
```

---

# 30. AWS ECR Authentication

The EC2 deployment logs into Amazon ECR using:

```bash
aws ecr get-login-password \
  --region us-east-1 | \
  docker login \
  --username AWS \
  --password-stdin "$ECR_REGISTRY"
```

Successful authentication produces:

```text
Login Succeeded
```

---

# 31. Docker Image Deployment

The deployment pulls the exact image associated with the current Git commit:

```bash
docker pull \
  "$ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG"
```

This guarantees that EC2 runs the image generated by the current CI/CD workflow.

---

# 32. Production Container

The production container is named:

```text
flask_app_prod
```

It is started with:

```bash
docker run -d \
  --restart unless-stopped \
  -p 5000:5000 \
  --name flask_app_prod \
  -e "MONGO_URI=$MONGO_URI" \
  "$ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG"
```

---

# 33. Container Verification

After starting the container, the deployment verifies that it is running:

```bash
docker ps \
  --filter "name=flask_app_prod" \
  --filter "status=running"
```

If the container is not running, the deployment displays:

```bash
docker ps -a
```

and:

```bash
docker logs flask_app_prod
```

The GitHub Actions job then fails.

---

# 34. Deployment Health Check

The final deployment gate is:

```bash
curl \
  --fail \
  --silent \
  --show-error \
  --connect-timeout 5 \
  --max-time 15 \
  http://localhost:5000/health
```

Successful response:

```json
{"status": "healthy"}
```

The pipeline prints:

```text
==========================================
DEPLOYMENT HEALTH CHECK PASSED
==========================================

==========================================
EC2 DEPLOYMENT COMPLETED SUCCESSFULLY
==========================================
```

---

# 35. Deployment Failure Handling

If the health check fails, the deployment prints:

```text
==========================================
DEPLOYMENT HEALTH CHECK FAILED
==========================================
```

It then displays the container status:

```bash
docker ps -a
```

and container logs:

```bash
docker logs flask_app_prod
```

Finally:

```bash
exit 1
```

causes the GitHub Actions deployment stage to fail.

This prevents an unhealthy deployment from being reported as successful.

---

# 36. Example Deployment Flow

A successful deployment follows:

```text
Developer
    |
    | git push
    v
GitHub
    |
    v
GitHub Actions
    |
    +--> Checkout
    |
    +--> Install Dependencies
    |
    +--> Flake8
    |
    +--> Pytest
    |
    +--> Configure AWS
    |
    +--> Login to ECR
    |
    +--> Docker Build
    |
    +--> Docker Push
    |
    +--> SSH to EC2
    |
    +--> Stop Old Container
    |
    +--> Pull New Image
    |
    +--> Start New Container
    |
    +--> Check Container
    |
    +--> /health
    |
    v
Production Deployment
```

---

# 37. Git Workflow

Check the repository:

```bash
git status
```

Add changes:

```bash
git add .
```

Commit:

```bash
git commit -m "Update application"
```

Push:

```bash
git push
```

After the push, GitHub Actions automatically starts the CI/CD pipeline.

---

# 38. Handling Git Push Rejection

If Git reports:

```text
Updates were rejected because the remote contains work
that you do not have locally.
```

first fetch the remote changes:

```bash
git fetch origin
```

Review the difference:

```bash
git log --oneline --left-right HEAD...origin/main
```

Then integrate the remote changes:

```bash
git pull --rebase origin main
```

If there are conflicts, resolve them and continue the rebase.

Finally:

```bash
git push
```

---

# 39. CI/CD Verification

The following evidence can be used to demonstrate that the pipeline works.

### Local Application

```bash
curl --fail http://localhost:5000/health
```

Expected:

```json
{"status": "healthy"}
```

### Docker

```bash
docker ps
```

Expected:

```text
flask_app_container
```

### Production EC2

```bash
docker ps
```

Expected:

```text
flask_app_prod
```

### Production Health Check

```bash
curl --fail http://localhost:5000/health
```

Expected:

```json
{"status": "healthy"}
```

### GitHub Actions

The Actions page should show a successful workflow run.

### Amazon ECR

The ECR repository should contain the Docker image tagged with the Git commit SHA.

---

# 40. Screenshot Evidence

The following screenshots should be included as evidence for the project.

## Screenshot 1 – GitHub Repository

Capture the GitHub repository showing:

* Source files
* Dockerfile
* Requirements file
* GitHub Actions workflow

**Caption:**

> GitHub repository containing the Flask application and CI/CD configuration.

---

## Screenshot 2 – Flask Application

Capture:

```bash
sed -n '1,80p' app.py
```

The screenshot should show:

```python
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
```

and:

```python
@app.route("/health")
def health():
    return {"status": "healthy"}, 200
```

**Caption:**

> Flask application configured with MongoDB and a deployment health-check endpoint.

---

## Screenshot 3 – Pytest

Run:

```bash
python3 -m pytest -v test_app.py
```

Capture the successful test result.

**Caption:**

> Automated Pytest test suite executed successfully.

---

## Screenshot 4 – Flake8

Run:

```bash
flake8 . \
  --exclude=venv \
  --count \
  --select=E9,F63,F7,F82 \
  --show-source \
  --statistics
```

Capture the successful result.

**Caption:**

> Flake8 code validation completed successfully.

---

## Screenshot 5 – Docker Image

Run:

```bash
docker images
```

Capture the image:

```text
flask-practice-app
```

**Caption:**

> Docker image successfully created for the Flask application.

---

## Screenshot 6 – Docker Container

Run:

```bash
docker ps
```

Capture:

```text
flask_app_container
```

and:

```text
0.0.0.0:5000->5000/tcp
```

**Caption:**

> Flask application running inside a Docker container.

---

## Screenshot 7 – Local Health Check

Run:

```bash
curl --fail http://localhost:5000/health
```

Capture:

```json
{"status": "healthy"}
```

**Caption:**

> Local Docker application successfully passes the health check.

---

## Screenshot 8 – GitHub Actions

Open:

```text
GitHub → Repository → Actions
```

Open the latest workflow run.

Capture the successful workflow.

**Caption:**

> GitHub Actions CI/CD workflow completed successfully.

---

## Screenshot 9 – Amazon ECR

Open:

```text
AWS Console → ECR → Repositories → flask-app
```

Capture the Docker image and tag.

**Caption:**

> Docker image successfully stored in Amazon ECR.

---

## Screenshot 10 – EC2 Container

SSH into EC2 and run:

```bash
docker ps
```

Capture:

```text
flask_app_prod
```

and:

```text
0.0.0.0:5000->5000/tcp
```

**Caption:**

> Production Flask container successfully running on Amazon EC2.

---

## Screenshot 11 – EC2 Health Check

On EC2 run:

```bash
curl --fail http://localhost:5000/health
```

Expected:

```json
{"status": "healthy"}
```

**Caption:**

> Production Flask application successfully passes the EC2 health check.

---

## Screenshot 12 – Live Application

Open:

```text
http://EC2_PUBLIC_IP:5000/
```

Capture the running Student Management System.

**Caption:**

> Flask Student Management application successfully deployed and accessible from the EC2 server.

---

# 41. Recommended Screenshot Order

For the final assignment/documentation, use this order:

```text
1. GitHub Repository
2. Flask Application Code
3. Pytest Results
4. Flake8 Results
5. Docker Image
6. Docker Container
7. Local Health Check
8. GitHub Actions Successful Run
9. Amazon ECR Image
10. EC2 Docker Container
11. EC2 Health Check
12. Live Application
```

This provides evidence for the complete CI/CD lifecycle.

---

# 42. Troubleshooting

## MongoDB URI Missing

If the application reports:

```text
ValueError:
You must specify a URI or set the MONGO_URI Flask config variable
```

check:

```bash
echo "$MONGO_URI"
```

Make sure the environment variable is configured.

---

## Invalid MongoDB Cluster

If the application reports:

```text
The DNS query name does not exist:
_mongodb._tcp.your_cluster.mongodb.net
```

the MongoDB connection string is still using a placeholder or incorrect cluster address.

Replace it with the actual MongoDB Atlas connection string.

---

## MongoDB Database Name Missing

Verify the URI contains the database name:

```text
mongodb+srv://username:password@cluster.mongodb.net/student_db
```

The database portion should be:

```text
student_db
```

---

## Port 5000 Already in Use

Check:

```bash
docker ps
```

Stop the existing container if required:

```bash
docker stop flask_app_container
```

Remove it:

```bash
docker rm flask_app_container
```

Then start the new container.

---

## Container Not Running

Check:

```bash
docker ps -a
```

Then:

```bash
docker logs flask_app_container
```

For production:

```bash
docker logs flask_app_prod
```

---

## Health Check Returns 404

If:

```bash
curl http://localhost:5000/health
```

returns:

```text
404
```

verify that `app.py` contains:

```python
@app.route("/health")
def health():
    return {"status": "healthy"}, 200
```

Then rebuild and redeploy the Docker image.

---

# 43. Security Best Practices

The following security practices are followed:

* MongoDB credentials are stored as secrets.
* AWS credentials are stored as GitHub Secrets.
* SSH private keys are stored as GitHub Secrets.
* `.env` is excluded from Git.
* Credentials are not hard-coded into Python source code.
* Credentials are not printed in deployment logs.
* Docker images are versioned using Git commit SHA.
* Production deployment is verified using a health check.

---

# 44. Benefits of the CI/CD Pipeline

This implementation provides several benefits.

### Automation

Deployment happens automatically after a successful Git push.

### Consistency

The same deployment process is executed every time.

### Faster Delivery

Developers do not need to manually build and deploy Docker images.

### Quality Control

Automated tests and Flake8 checks run before deployment.

### Traceability

Docker images are tagged using Git commit SHA.

### Reliability

The deployment includes a health-check gate.

### Failure Detection

Container logs are automatically displayed when deployment fails.

### Security

Sensitive configuration is stored in GitHub Secrets.

---

# 45. Final CI/CD Architecture

```text
                         DEVELOPER
                             |
                             | git push
                             v
                    +-------------------+
                    | GitHub Repository  |
                    +-------------------+
                             |
                             v
                    +-------------------+
                    | GitHub Actions     |
                    +-------------------+
                             |
             +---------------+---------------+
             |               |               |
             v               v               v
        Flake8            Pytest       Docker Build
             |               |               |
             +---------------+---------------+
                             |
                             v
                    +-------------------+
                    |   Amazon ECR       |
                    |   flask-app        |
                    +-------------------+
                             |
                             | docker pull
                             v
                    +-------------------+
                    |    Amazon EC2      |
                    +-------------------+
                             |
                             v
                    +-------------------+
                    | Docker Container   |
                    | flask_app_prod    |
                    +-------------------+
                             |
                             v
                    +-------------------+
                    | Flask Application  |
                    +-------------------+
                             |
                             v
                    +-------------------+
                    |   MongoDB Atlas    |
                    +-------------------+

                             |
                             v
                    /health → HTTP 200
                             |
                             v
                    DEPLOYMENT SUCCESS
```

---

# 46. Conclusion

The project successfully implements an end-to-end CI/CD pipeline for a Flask application.

The pipeline automatically:

```text
Code
 ↓
Test
 ↓
Validate
 ↓
Build
 ↓
Push
 ↓
Deploy
 ↓
Verify
```

The Flask application is containerized using Docker, stored in Amazon ECR, deployed to Amazon EC2, connected to MongoDB Atlas, and verified using an automated `/health` endpoint.

The final result is a repeatable and automated deployment process where every successful Git push can be validated and deployed without manually performing each deployment step.

---

## Final Evidence

The most important final evidence is:

```text
✓ Pytest passed
✓ Flake8 passed
✓ Docker image created
✓ Docker image pushed to ECR
✓ EC2 container running
✓ /health returned {"status": "healthy"}
✓ GitHub Actions workflow succeeded
✓ Flask application accessible from browser
```

**This demonstrates a complete working CI/CD pipeline from source-code commit to production deployment.**

```
```
