AI Resume Analyzer Deployment

This repository contains the Python application code, Terraform Infrastructure as Code (IaC), Kubernetes manifests, and Cloud Build pipeline definition for deploying a serverless, highly-available AI Resume Analyzer on Google Kubernetes Engine (GKE).

The solution utilizes the Gemini API to analyze uploaded resumes.

Deployment Instructions (User Manual)

The entire environment can be deployed with just three commands, assuming GCP authentication is established and the repository is linked.

Step 1: Provision Infrastructure (IaC)

This step uses Terraform to create the Google Kubernetes Engine (GKE) Cluster and the underlying network components.

Navigate to the Terraform directory:

cd terraform/


Initialize the workspace:

    >> terraform init


Apply the infrastructure plan (create the GKE cluster):

    >> terraform apply --auto-approve


Configure kubectl to connect to the new cluster:

    >> gcloud container clusters get-credentials resume-analyzer-gke-clust

Step 2: Configure Secrets

The application requires the Gemini API Key to function. This is stored securely as a Kubernetes Secret.

Manual Secret Creation: Create the Kubernetes Secret from your API key. (NOTE: This must be done once before the first Deployment.)

kubectl create secret generic api-key-secret --from-literal=GEMINI_API_KEY='<YOUR_API_KEY>'


Verify the Secret:

kubectl get secret api-key-secret


Step 3: Trigger the CI/CD Pipeline

The Continuous Integration/Continuous Delivery (CI/CD) pipeline is fully automated and triggered by a commit to the master branch.

Make a Change: Ensure you have made and committed a minor change (e.g., updating a version number in app/app.py).

Activate Pipeline: Push the new commit to GitHub.

    >> git push origin master


Monitor Deployment: Monitor the Cloud Build History for the three sequential stages: Build, Push, and Deploy to GKE.

Confirm Rolling Update Status: Verify the deployment update is successful and the Pods are stable:

    >> kubectl rollout status deployment/portfolio-deployment

Live Application Access

Once the CI/CD pipeline completes:

Retrieve the public LoadBalancer External IP by checking the Service status:

    >> kubectl get svc

The application will be accessible via the External IP shown in the output. The service maps port 80 externally to port 5000 on the Pods.