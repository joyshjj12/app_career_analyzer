# 1. Configure the Google Cloud Provider
# This tells Terraform how to connect to your GCP account.
provider "google" {
  project = "strange-firefly-475810-h9"  # <--- REPLACE with your Project ID
  region  = "us-central1"          # <--- REPLACE with your desired region (e.g., europe-west1)
  zone    = "us-central1-c"        # <--- REPLACE with your desired zone
}

# 2. Networking: Create a Virtual Private Cloud (VPC) Network
# This is the isolated network environment for the cluster.
resource "google_compute_network" "vpc_network" {
  name = "resume-analyzer-vpc"
  auto_create_subnetworks = true  # Simplifies networking for this example
}

# 3. GKE Cluster: Define the Kubernetes Control Plane
# This is the managed Kubernetes service.
resource "google_container_cluster" "app_cluster" {
  name     = "resume-analyzer-gke-cluster"
  location = "us-central1" # Must match the provider region

  # Link to the network created above
  network    = google_compute_network.vpc_network.name
  subnetwork = google_compute_network.vpc_network.name
  deletion_protection = false
  # Configuration for the control plane
  initial_node_count = 1
  
  # Define the default node pool (worker nodes)
  node_config {
    machine_type = "e2-medium"
    disk_size_gb = 30 
    oauth_scopes = [ # Scopes needed for GKE
      "https://www.googleapis.com/auth/compute",
      "https://www.googleapis.com/auth/devstorage.read_only",
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring",
    ]
  }

  # Ensure the cluster can run applications
  ip_allocation_policy {
    cluster_ipv4_cidr_block  = "/19"
    services_ipv4_cidr_block = "/22"
  }
}

# 4. Define the output (Needed for connecting kubectl and Jenkins)
output "cluster_name" {
  value = google_container_cluster.app_cluster.name
}

output "cluster_endpoint" {
  value = google_container_cluster.app_cluster.endpoint
}