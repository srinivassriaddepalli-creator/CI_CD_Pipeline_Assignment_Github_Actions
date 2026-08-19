# CI/CD Pipeline Assignment – GitHub Actions, Docker, AWS ECR & EC2

## 1. Project Overview

This project demonstrates an end-to-end **CI/CD pipeline** for a Flask application using **GitHub Actions**, **Docker**, **Amazon ECR**, **Amazon EC2**, and **MongoDB Atlas**.

The pipeline automatically:

1. Validates the Flask application.
2. Runs automated tests and code-quality checks.
3. Builds a Docker image.
4. Pushes the image to Amazon Elastic Container Registry (ECR).
5. Connects to an Amazon EC2 instance through SSH.
6. Pulls the newly created Docker image.
7. Stops and removes the previous application container.
8. Starts the new application container.
9. Passes the MongoDB connection string securely to the container.
10. Performs an application health check.
11. Fails the deployment if the health check does not pass.
12. Sends an email notification based on deployment success or failure.

The overall flow is:

```text
Developer
    |
    | git push
    v
GitHub Repository
    |
    v
GitHub Actions
    |
    +----------------------+
    |                      |
    v                      v
Flake8                 Pytest
    |                      |
    +----------+-----------+
               |
               v
        Docker Image Build
               |
               v
          Amazon ECR
               |
               v
        SSH into EC2
               |
               v
        Docker Pull Image
               |
               v
      Stop Old Container
               |
               v
       Start New Container
               |
               v
       /health Endpoint
               |
        +------+------+
        |             |
      PASS           FAIL
        |             |
        v             v
    Success         Failure
     Email           Email
```

---

# 2. Project Objective

The objective of this assignment is to implement a reliable automated CI/CD pipeline that takes application code from a GitHub repository and deploys it to a production-like AWS environment.

The pipeline should demonstrate:

* Source code management using GitHub.
* Continuous Integration using GitHub Actions.
* Automated code validation.
* Automated testing.
* Docker containerization.
* Docker image versioning.
* Amazon ECR integration.
* Amazon EC2 deployment.
* Secure secret management.
* MongoDB Atlas integration.
* Automated deployment verification.
* Health-check-based deployment gating.
* Success/failure notifications.

---

# 3. Technologies Used

| Technology     | Purpose                            |
| -------------- | ---------------------------------- |
| Python         | Application programming language   |
| Flask          | Web application framework          |
| Flask-PyMongo  | MongoDB integration                |
| PyMongo        | MongoDB driver                     |
| Pytest         | Automated testing                  |
| Flake8         | Python code-quality validation     |
| Docker         | Application containerization       |
| GitHub         | Source code repository             |
| GitHub Actions | CI/CD automation                   |
| Amazon ECR     | Docker image registry              |
| Amazon EC2     | Application hosting                |
| AWS CLI        | AWS resource interaction           |
| MongoDB Atlas  | Cloud MongoDB database             |
| SSH            | Secure EC2 deployment              |
| Gunicorn       | Recommended production WSGI server |
| SMTP/Gmail     | Email notification                 |

---

# 4. Application Architecture

The application is a Flask-based web application connected to MongoDB.

```text
                  Internet
                     |
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

The Docker container exposes port `5000`.

```text
EC2 Port 5000
      |
      v
Docker Port 5000
      |
      v
Flask Application
```

---

# 5. Repository Structure

A typical repository structure is:

```text
CI_CD_Pipeline_Assignment_Github_Actions/
│
├── .github/
│   └── workflows/
│       └── deploy.yml
│
├── app.py
├── test_app.py
├── requirements.txt
├── Dockerfile
├── .gitignore
└── README.md
```

## Important files

### `app.py`

Contains the Flask application and MongoDB configuration.

### `test_app.py`

Contains automated tests for the Flask application.

### `requirements.txt`

Contains Python dependencies required by the application.

### `Dockerfile`

Defines how the Flask application is packaged into a Docker image.

### `.github/workflows/deploy.yml`

Defines the complete CI/CD workflow.

### `README.md`

Contains project documentation and deployment instructions.

---

# 6. Flask Application

The application uses Flask and Flask-PyMongo.

The MongoDB connection is obtained from the `MONGO_URI` environment variable rather than hard-coding credentials in the source code.

Example:

```python
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
```

The application also provides a health-check endpoint:

```python
@app.route("/health")
def health():
    return {"status": "healthy"}, 200
```

The health endpoint is important because the CI/CD pipeline uses it to determine whether the newly deployed container is functioning correctly.

---

# 7. Health Check

The deployment pipeline executes:

```bash
curl --fail \
  --silent \
  --show-error \
  --connect-timeout 5 \
  --max-time 15 \
  http://localhost:5000/health
```

A successful response should be:

```json
{
  "status": "healthy"
}
```

The pipeline considers the deployment successful only when this endpoint returns HTTP status `200`.

If the endpoint returns `404`, `500`, times out, or cannot be reached, the deployment is marked as failed.

This provides a deployment safety gate.

---

# 8. Docker Configuration

The application is containerized using Docker.

A typical Dockerfile is:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

The Docker image packages:

* Python runtime
* Flask application
* Python dependencies
* Application source code

---

# 9. Local Docker Testing

Build the image:

```bash
docker build -t flask-practice-app:latest .
```

Run the container:

```bash
docker run -d \
  --name flask_app_container \
  -p 5000:5000 \
  -e MONGO_URI="$MONGO_URI" \
  flask-practice-app:latest
```

Verify:

```bash
docker ps
```

Test:

```bash
curl http://localhost:5000/health
```

Expected:

```json
{"status":"healthy"}
```

---

# 10. MongoDB Atlas Configuration

MongoDB Atlas is used as the cloud database.

The application requires the following environment variable:

```text
MONGO_URI
```

The URI follows this general structure:

```text
mongodb+srv://USERNAME:PASSWORD@CLUSTER/DATABASE
```

The actual database credentials must never be committed to Git.

---

# 11. GitHub Secrets

Sensitive credentials are stored using GitHub Actions Secrets.

The pipeline uses secrets such as:

```text
MONGO_URI
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
EC2_HOST_IP
EC2_SSH_KEY
MAIL_USERNAME
MAIL_PASSWORD
NOTIFICATION_EMAIL
```

These values are referenced from GitHub Actions using:

```yaml
${{ secrets.MONGO_URI }}
```

Secrets are not hard-coded into the repository.

---

# 12. GitHub Actions Workflow

The workflow is divided into multiple stages.

## Stage 1 – Checkout

GitHub Actions checks out the latest source code.

```yaml
uses: actions/checkout@v4
```

---

# 13. Stage 2 – Python Environment

The workflow configures Python and installs application dependencies.

Typical steps include:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Development/test dependencies such as Pytest and Flake8 are also installed.

---

# 14. Stage 3 – Automated Test Suite

The workflow performs code-quality validation using Flake8.

Example:

```bash
flake8 . \
  --count \
  --select=E9,F63,F7,F82 \
  --show-source \
  --statistics
```

The automated test suite is then executed:

```bash
python3 -m pytest -v test_app.py
```

If either Flake8 or Pytest fails, the pipeline stops and the application is not deployed.

---

# 15. Stage 4 – AWS Authentication

The workflow configures AWS credentials using:

```yaml
aws-actions/configure-aws-credentials@v4
```

The AWS credentials are retrieved from GitHub Secrets.

The workflow uses the AWS region:

```text
us-east-1
```

---

# 16. Stage 5 – Amazon ECR Login

The Docker image is pushed to Amazon Elastic Container Registry.

The workflow obtains an ECR authentication token using:

```bash
aws ecr get-login-password
```

and authenticates Docker against ECR.

Example:

```bash
aws ecr get-login-password --region us-east-1 |
docker login \
  --username AWS \
  --password-stdin "$ECR_REGISTRY"
```

---

# 17. Stage 6 – Docker Image Build

The application is packaged into a Docker image.

The image is tagged using the Git commit SHA:

```text
${{ github.sha }}
```

Example:

```text
flask-app:eb2014e7d07b130973be412d12fd77bacef6e15e
```

Using the commit SHA provides a unique and traceable image version.

This makes it possible to identify exactly which Git commit is running in production.

---

# 18. Stage 7 – Push Image to ECR

The Docker image is pushed to Amazon ECR.

Example image structure:

```text
545931885961.dkr.ecr.us-east-1.amazonaws.com/flask-app:<commit-sha>
```

This allows EC2 to retrieve the exact image produced by the CI pipeline.

---

# 19. Stage 8 – EC2 Deployment

GitHub Actions connects to the EC2 instance using SSH.

The deployment uses:

```text
appleboy/ssh-action
```

The workflow passes the following environment variables:

```text
ECR_REGISTRY
ECR_REPOSITORY
IMAGE_TAG
MONGO_URI
```

The MongoDB URI is therefore available to the remote deployment script without exposing it in source code.

---

# 20. EC2 Deployment Process

The EC2 deployment performs the following operations.

### Validate variables

The script verifies that required variables exist:

```bash
if [ -z "$ECR_REGISTRY" ]; then
    echo "ERROR: ECR_REGISTRY is missing."
    exit 1
fi

if [ -z "$MONGO_URI" ]; then
    echo "ERROR: MONGO_URI GitHub Secret is missing."
    exit 1
fi
```

### Verify Docker

```bash
docker --version
```

### Verify AWS CLI

```bash
aws --version
```

### Login to ECR

```bash
aws ecr get-login-password \
  --region us-east-1 |
  docker login \
  --username AWS \
  --password-stdin "$ECR_REGISTRY"
```

### Stop the previous container

```bash
docker stop flask_app_prod || true
docker rm flask_app_prod || true
```

The `|| true` ensures the deployment does not fail if the container does not already exist.

### Pull the new image

```bash
docker pull \
  "$ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG"
```

### Start the new container

```bash
docker run -d \
  --restart unless-stopped \
  -p 5000:5000 \
  --name flask_app_prod \
  -e "MONGO_URI=$MONGO_URI" \
  "$ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG"
```

---

# 21. Deployment Health Check

After starting the container, the workflow waits for the Flask application to initialize:

```bash
sleep 10
```

It then checks whether the container is running.

If the container is not running, the workflow displays:

* Container status
* Container logs

The workflow then executes:

```bash
curl --fail \
  --silent \
  --show-error \
  --connect-timeout 5 \
  --max-time 15 \
  http://localhost:5000/health
```

A successful response results in:

```text
DEPLOYMENT HEALTH CHECK PASSED
```

and:

```text
EC2 DEPLOYMENT COMPLETED SUCCESSFULLY
```

---

# 22. Failure Handling

If the container crashes or the health check fails, the workflow reports:

```text
DEPLOYMENT HEALTH CHECK FAILED
```

The workflow then collects:

```bash
docker ps -a
```

and:

```bash
docker logs flask_app_prod
```

This makes troubleshooting easier.

For example, if `/health` does not exist, the application returns:

```text
404
```

and the deployment is correctly marked as failed.

This demonstrates that the pipeline does not blindly consider a container launch to be a successful deployment.

---

# 23. Email Notifications

The workflow sends email notifications after deployment.

A success notification is triggered when the pipeline completes successfully.

A failure notification is triggered when the deployment fails.

The SMTP configuration uses Gmail.

The credentials are stored in GitHub Secrets:

```text
MAIL_USERNAME
MAIL_PASSWORD
NOTIFICATION_EMAIL
```

No email password is stored in the source code.

---

# 24. Complete CI/CD Flow

The complete process is:

```text
1. Developer modifies application
            |
            v
2. git push
            |
            v
3. GitHub Actions starts
            |
            v
4. Checkout source code
            |
            v
5. Install Python dependencies
            |
            v
6. Run Flake8
            |
            v
7. Run Pytest
            |
       Tests pass?
        /       \
      No         Yes
      |           |
      v           v
    STOP      Build Docker image
                  |
                  v
             Tag with SHA
                  |
                  v
             Push to ECR
                  |
                  v
              SSH to EC2
                  |
                  v
            Login to ECR
                  |
                  v
             Stop old app
                  |
                  v
             Pull new image
                  |
                  v
          Start new container
                  |
                  v
            Check container
                  |
                  v
             GET /health
                  |
             +----+----+
             |         |
           200       Failure
             |         |
             v         v
        Deployment   Show logs
         Success      + Fail
             |
             v
       Success Email
```

---

# 25. Security Considerations

The project follows several security practices.

### Secrets are not stored in source code

MongoDB credentials, AWS credentials, SSH keys, and email credentials are stored as GitHub Secrets.

### MongoDB URI is passed through environment variables

The application accesses:

```text
MONGO_URI
```

at runtime.

### Docker receives MongoDB configuration at runtime

The deployment uses:

```bash
-e "MONGO_URI=$MONGO_URI"
```

rather than embedding the URI in the Docker image.

### Git commit SHA is used for image tagging

This provides traceability between:

```text
Git commit
    |
    v
Docker image
    |
    v
EC2 deployment
```

### Sensitive values are not printed

The deployment logs only report:

```text
MongoDB configuration: available
```

rather than printing the actual MongoDB URI.

---

# 26. Required GitHub Secrets

Configure the following secrets under:

```text
GitHub Repository
→ Settings
→ Secrets and variables
→ Actions
→ Repository secrets
```

| Secret                  | Purpose                         |
| ----------------------- | ------------------------------- |
| `MONGO_URI`             | MongoDB Atlas connection string |
| `AWS_ACCESS_KEY_ID`     | AWS authentication              |
| `AWS_SECRET_ACCESS_KEY` | AWS authentication              |
| `EC2_HOST_IP`           | EC2 public IP address           |
| `EC2_SSH_KEY`           | SSH private key                 |
| `MAIL_USERNAME`         | SMTP username                   |
| `MAIL_PASSWORD`         | SMTP password/app password      |
| `NOTIFICATION_EMAIL`    | Notification recipient          |

Never commit these values into Git.

---

# 27. Local Development

Create and activate a Python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Set the MongoDB connection:

```bash
export MONGO_URI='your-mongodb-connection-string'
```

Run the application:

```bash
python app.py
```

Test the application:

```bash
curl http://127.0.0.1:5000/
```

Test the health endpoint:

```bash
curl http://127.0.0.1:5000/health
```

Expected health response:

```json
{
  "status": "healthy"
}
```

---

# 28. Testing

Run Flake8:

```bash
flake8 . \
  --count \
  --select=E9,F63,F7,F82 \
  --show-source \
  --statistics
```

Run Pytest:

```bash
python3 -m pytest -v test_app.py
```

Both checks must pass before the application is deployed.

---

# 29. Deployment

The normal deployment process is simply:

```bash
git add .
git commit -m "your commit message"
git push origin main
```

GitHub Actions automatically starts the CI/CD pipeline.

No manual Docker image build or EC2 deployment is required.

---

# 30. Troubleshooting

## `MONGO_URI GitHub Secret is missing`

Verify that:

```text
MONGO_URI
```

exists under GitHub:

```text
Settings
→ Secrets and variables
→ Actions
→ Repository secrets
```

The workflow should contain:

```yaml
MONGO_URI: ${{ secrets.MONGO_URI }}
```

and:

```yaml
envs: ECR_REGISTRY,ECR_REPOSITORY,IMAGE_TAG,MONGO_URI
```

---

## MongoDB DNS error

If the application reports:

```text
The DNS query name does not exist:
_mongodb._tcp.your_cluster.mongodb.net
```

the MongoDB URI is using an invalid or placeholder cluster hostname.

Retrieve the correct connection string from MongoDB Atlas.

---

## Port 5000 already in use

Check:

```bash
sudo ss -ltnp | grep ':5000'
```

Check Docker:

```bash
docker ps
```

Stop a local container if necessary:

```bash
docker stop flask_app_container
```

---

## Health check returns 404

Verify that Flask contains:

```python
@app.route("/health")
def health():
    return {"status": "healthy"}, 200
```

Then test:

```bash
curl http://localhost:5000/health
```

---

## Container is not running

Check:

```bash
docker ps -a
```

Then inspect logs:

```bash
docker logs flask_app_prod
```

---

## ECR image pull fails

Verify:

* AWS credentials
* AWS region
* ECR repository name
* EC2 IAM permissions
* ECR login

---

# 31. CI/CD Benefits

This pipeline provides several benefits.

### Automation

Every push can automatically trigger validation and deployment.

### Consistency

The same Docker image built by CI is deployed to EC2.

### Traceability

Each image is tagged with the Git commit SHA.

### Security

Sensitive configuration is managed through GitHub Secrets.

### Reliability

The deployment does not automatically succeed just because the Docker container started.

The `/health` endpoint must return HTTP `200`.

### Faster deployment

Manual SSH, Docker pulls, and container restarts are replaced by an automated workflow.

### Failure visibility

Container status and logs are collected when deployment fails.

---

# 32. Future Improvements

The current implementation can be improved further by:

1. Replacing Flask's development server with Gunicorn.
2. Adding Docker image vulnerability scanning.
3. Adding dependency vulnerability scanning.
4. Using AWS IAM roles instead of long-lived AWS access keys where possible.
5. Using AWS Systems Manager instead of SSH for EC2 deployment.
6. Implementing blue-green or rolling deployments.
7. Adding CloudWatch monitoring and alerts.
8. Adding HTTPS through an Application Load Balancer.
9. Adding a staging environment before production.
10. Adding automated rollback if the health check fails.
11. Using Docker health checks.
12. Adding stronger test coverage.

---

# 33. Final Deployment Verification

A successful deployment should finish with output similar to:

```text
Starting EC2 Deployment

ECR Registry: <ECR_REGISTRY>
ECR Repository: flask-app
Image Tag: <GIT_COMMIT_SHA>
MongoDB configuration: available

Checking Docker...
Docker version ...

Checking AWS CLI...
aws-cli/...

ECR login successful.

Pulling new Docker image...
Docker image pulled successfully.

Starting new Flask application container...
New container started.

Application container is running.

Running deployment health check...

{"status":"healthy"}

==========================================
DEPLOYMENT HEALTH CHECK PASSED
==========================================

==========================================
EC2 DEPLOYMENT COMPLETED SUCCESSFULLY
==========================================
```

---

# 34. Conclusion

This project implements a complete CI/CD pipeline for a Flask application using GitHub Actions and AWS.

The pipeline automatically validates application code, runs tests, builds and versions a Docker image, pushes the image to Amazon ECR, deploys it to Amazon EC2, provides MongoDB configuration securely through GitHub Secrets, and verifies the running application through a health-check endpoint.

The health-check gate ensures that a deployment is considered successful only when the application is actually running and responding correctly.

The implementation therefore demonstrates the key principles of modern CI/CD:

```text
Code
  ↓
Build
  ↓
Test
  ↓
Package
  ↓
Publish
  ↓
Deploy
  ↓
Verify
  ↓
Notify
```

This provides an automated, repeatable, traceable, and secure deployment process for the Flask application.
