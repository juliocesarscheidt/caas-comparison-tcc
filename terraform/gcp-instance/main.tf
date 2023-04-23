terraform {
  backend "local" {
  }
}

provider "google" {
  credentials = file("GOOGLE_CLOUD_KEYFILE_JSON.json")
  project     = var.project_id
  region      = var.region
  zone        = var.zone
}

resource "google_compute_instance" "vm_instance" {
  name           = "vm-instance"
  machine_type   = var.instance_type
  zone           = var.zone
  can_ip_forward = true
  boot_disk {
    auto_delete = true
    device_name = "vm-instance" # /dev/disk/by-id/google-{{device_name}}
    source      = google_compute_disk.compute_disk.self_link
  }
  network_interface {
    subnetwork = google_compute_subnetwork.compute_subnetwork.self_link
    access_config {}
  }
  metadata_startup_script = <<EOF
exec > >(tee -a /tmp/init-script-log | logger -t user-data -s 2>/dev/console) 2>&1
  sudo apt-get update -y
  sudo apt-get install -y git-core curl build-essential openssl libssl-dev
  cd /home/google
  curl -L https://nodejs.org/dist/v18.16.0/node-v18.16.0-linux-x64.tar.xz \
    --output node-v18.16.0-linux-x64.tar.xz
  sudo tar -xvf node-v18.16.0-linux-x64.tar.xz
  sudo rm -f node-v18.16.0-linux-x64.tar.xz
  sudo mv node-v18.16.0-linux-x64/bin/* /usr/bin/
  sudo rm -rf node-v18.16.0-linux-x64/
  curl -L https://npmjs.org/install.sh | sudo sh
  sudo npm install -g artillery
EOF
  lifecycle {
    ignore_changes = [attached_disk]
  }
  tags     = []
  metadata = {}
  depends_on = [
    google_compute_disk.compute_disk,
    google_compute_subnetwork.compute_subnetwork
  ]
}

output "instance_ip" {
  value = google_compute_instance.vm_instance.network_interface.*.access_config[0].*.nat_ip[0]
}

resource "google_compute_network" "compute_network" {
  name                    = "compute-network"
  auto_create_subnetworks = "false"
  mtu                     = 1500
}

resource "google_compute_subnetwork" "compute_subnetwork" {
  name          = "compute-subnetwork"
  ip_cidr_range = "10.100.0.0/24"
  region        = var.region
  network       = google_compute_network.compute_network.id
  depends_on    = [google_compute_network.compute_network]
}

resource "google_compute_firewall" "compute_firewall_ingress" {
  name      = "vm-compute-firewall-ingress"
  network   = google_compute_network.compute_network.name
  direction = "INGRESS"
  priority  = 1000
  allow {
    protocol = "icmp"
  }
  allow {
    protocol = "tcp"
    ports    = ["22"]
  }
  # source_tags = []
  source_ranges = ["0.0.0.0/0"]
  depends_on    = [google_compute_network.compute_network]
}

resource "google_compute_disk" "compute_disk" {
  name                      = "compute-disk"
  type                      = "pd-ssd"
  zone                      = var.zone
  image                     = var.instance_image
  physical_block_size_bytes = 4096 # 4GB
  labels                    = {}
}

resource "tls_private_key" "tls_rsa_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

locals {
  metadata_ssh_content = "${var.instance_username}:${tls_private_key.tls_rsa_key.public_key_openssh}"
}

output "private_key" {
  value     = tls_private_key.tls_rsa_key.private_key_pem
  sensitive = true
}

resource "google_compute_project_metadata" "metadata_ssh" {
  metadata = {
    ssh-keys = local.metadata_ssh_content
  }
}
