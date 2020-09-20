provider "google" {
  project = var.project_id
  region  = "australia-southeast1"
  zone    = "australia-southeast1-b"
}

######### ENABLE APIS #######
resource "google_project_service" "compute-api" {
  project = var.project_id
  service = "compute.googleapis.com"
}

resource "google_project_service" "iam-cred-api" {
  project = var.project_id
  service = "iamcredentials.googleapis.com"
}

resource "google_project_service" "secrets-api" {
    project = var.project_id
    service = "secretmanager.googleapis.com"
}

resource "google_project_service" "dns-api" {
    project = var.project_id
    service = "dns.googleapis.com"
}

######### Create VPC and subnet #######
resource "google_compute_network" "discord" {
  name = "discord"
  auto_create_subnetworks = false
  depends_on =  [google_project_service.compute-api]
}

resource "google_compute_subnetwork" "aus-subnet" {
    name = "aus-subnet"
    ip_cidr_range = "10.10.0.0/16"
    private_ip_google_access = true
    network = google_compute_network.discord.id
    depends_on = [google_compute_network.discord]
}

######## FIREWALL RULES #########
resource "google_compute_firewall" "allow-pga" {
  name    = "allow-pga"
  network = google_compute_network.discord.id
  depends_on = [google_compute_network.discord]


  allow {
    protocol = "all"
  }

  priority = "999"

  direction = "EGRESS"

  destination_ranges = ["199.36.153.8/30", "199.36.153.4/30"]

}

resource "google_compute_firewall" "allow-discord" {
  name    = "allow-discord"
  network = google_compute_network.discord.id
  depends_on = [google_compute_network.discord]

  allow {
    protocol = "all"
  }

  priority = "999"
  direction = "EGRESS"
#   destination_ranges = ["162.159.130.234", "162.159.134.234", "162.159.136.234", "162.159.135.234", "162.159.133.234"]
  destination_ranges = ["162.159.128.0/20"]

}

resource "google_compute_firewall" "deny-egress" {
  name    = "deny-egress"
  network = google_compute_network.discord.id
  depends_on = [google_compute_network.discord]

  deny {
    protocol = "all"
  }

  priority = "1001"
  disabled = false

  direction = "EGRESS"

  destination_ranges = ["0.0.0.0/0"]
}

resource "google_compute_firewall" "allow-ssh" {
  name    = "allow-ssh"
  network = google_compute_network.discord.id
  depends_on = [google_compute_network.discord]

  allow {
    protocol = "all"
  }

  priority = "50"

  # Change me to true once the challenge is up and running
  disabled = true
  
  
  direction = "INGRESS"

  source_ranges = ["0.0.0.0/0"]
}



###### DNS ENTRY FOR PGA ###########
## googleapis.com.
resource "google_dns_managed_zone" "pga-zone" {
  name        = "pga-zone"
  dns_name    = "googleapis.com."
  depends_on  = [google_project_service.dns-api]

  visibility = "private"

  private_visibility_config {
    networks {
      network_url = google_compute_network.discord.id
    }
    
  }
}


resource "google_dns_record_set" "a" {
  name         = "private.${google_dns_managed_zone.pga-zone.dns_name}"
  managed_zone = google_dns_managed_zone.pga-zone.name
  type         = "A"
  ttl          = 5

  rrdatas = ["199.36.153.8", "199.36.153.9", "199.36.153.10", "199.36.153.11"]
}

resource "google_dns_record_set" "cname" {
  name         = "*.${google_dns_managed_zone.pga-zone.dns_name}"
  managed_zone = google_dns_managed_zone.pga-zone.name
  type         = "CNAME"
  ttl          = 300
  rrdatas      = ["private.googleapis.com."]
}

#gcr.io

resource "google_dns_managed_zone" "pga-gcr-zone" {
  name        = "pga-gcr-zone"
  dns_name    = "gcr.io."
  depends_on  = [google_project_service.dns-api]

  visibility = "private"

  private_visibility_config {
    networks {
      network_url = google_compute_network.discord.id
    }
    
  }
}


resource "google_dns_record_set" "a-gcr" {
  name         = google_dns_managed_zone.pga-gcr-zone.dns_name
  managed_zone = google_dns_managed_zone.pga-gcr-zone.name
  type         = "A"
  ttl          = 5

  rrdatas = ["199.36.153.8", "199.36.153.9", "199.36.153.10", "199.36.153.11"]
}

resource "google_dns_record_set" "cname-gcr" {
  name         = "*.${google_dns_managed_zone.pga-gcr-zone.dns_name}"
  managed_zone = google_dns_managed_zone.pga-gcr-zone.name
  type         = "CNAME"
  ttl          = 300
  rrdatas      = ["gcr.io."]
}

#### BUCKETS #####

resource "google_storage_bucket" "meme-bucket" {
  name          = var.meme-bucket-name
  location      = "AUSTRALIA-SOUTHEAST1"
  force_destroy = true
  bucket_policy_only = true
} 

resource "google_storage_bucket_object" "meme1" {
  name   = "png.jpg"
  source = "epic-memes/png.jpg"
  bucket = google_storage_bucket.meme-bucket.name
}

resource "google_storage_bucket_object" "meme2" {
  name   = "pwease.jpg"
  source = "epic-memes/pwease.jpg"
  bucket = google_storage_bucket.meme-bucket.name
}
resource "google_storage_bucket_object" "meme3" {
  name   = "well.jpg"
  source = "epic-memes/well.jpg"
  bucket = google_storage_bucket.meme-bucket.name
}
resource "google_storage_bucket_object" "meme4" {
  name   = "winsad.png"
  source = "epic-memes/winsad.png"
  bucket = google_storage_bucket.meme-bucket.name
}


resource "google_storage_bucket" "secure-meme-bucket" {
  name          = var.secure-meme-bucket-name
  location      = "AUSTRALIA-SOUTHEAST1"
  force_destroy = true
  bucket_policy_only = true
} 

resource "google_storage_bucket_object" "svc-account-key" {
  name   = "epic.jpg"
  content = google_service_account_key.mykey.private_key
  bucket = google_storage_bucket.secure-meme-bucket.name
}


###### IAM Service Account ######

# memeboy123
resource "google_service_account" "memeboy" {
  account_id   = "memeboy123"
  display_name = "gets da memes"
}

resource "google_project_iam_binding" "token_creator_binding" {
  role               = "roles/iam.serviceAccountTokenCreator"
  members = [
    "serviceAccount:memeboy123@${var.project_id}.iam.gserviceaccount.com",
  ]
  depends_on = [google_service_account.memeboy]
}

resource "google_project_iam_binding" "storage_viewer" {
  role               = "roles/storage.objectViewer"
  members = [
    "serviceAccount:memeboy123@${var.project_id}.iam.gserviceaccount.com",
  ]
  depends_on = [google_service_account.memeboy]
}

# secret-manager
resource "google_service_account" "secret-manager" {
  account_id   = "secret-manager"
  display_name = "gets da secrets"
}

resource "google_project_iam_binding" "secret-access-binding" {
  role               = "roles/secretmanager.secretAccessor"
  members = [
    "serviceAccount:secret-manager@${var.project_id}.iam.gserviceaccount.com",
  ]
  depends_on = [google_service_account.secret-manager]
}

resource "google_project_iam_binding" "secret-list-binding" {
  role               = "roles/secretmanager.viewer"
  members = [
    "serviceAccount:secret-manager@${var.project_id}.iam.gserviceaccount.com",
  ]
  depends_on = [google_service_account.secret-manager]
}

resource "google_service_account_key" "mykey" {
  service_account_id = google_service_account.secret-manager.name
}


##### SECRET MANAGER #######
resource "google_secret_manager_secret" "secret-flag" {
  secret_id = "big_secret"
  depends_on = [google_project_service.secrets-api]

  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "secret-flag-version" {
  secret = google_secret_manager_secret.secret-flag.id
  secret_data = "DUCTF{bot_boi_2_cloud_secrets}"
}


##### GCE CONTAINER #####
module "gce-container" {
  source = "terraform-google-modules/container-vm/google"
  version = "~> 2.0"

  container = {
    image = "gcr.io/mc-bangserver/discord-bot:latest"
    stdin = true
    
  }
  restart_policy = "Always"

}

resource "google_compute_instance" "discord-bot" {
  name         = "discord-bot"
  machine_type = "g1-small"
  zone         = "australia-southeast1-b"
  allow_stopping_for_update = true


  boot_disk {
      //mode = "READ_ONLY"
    initialize_params {
      image = module.gce-container.source_image
      size = "10"
    }
  }



    network_interface {
        subnetwork = "aus-subnet"
        access_config  {
        }
    }

    metadata = {
        gce-container-declaration = module.gce-container.metadata_value
        google-logging-enabled    = "true"
        google-monitoring-enabled = "true"
    }


    service_account {
    
    email = "memeboy123@${var.project_id}.iam.gserviceaccount.com"
    scopes = ["https://www.googleapis.com/auth/cloud-platform"]
    
    }

}