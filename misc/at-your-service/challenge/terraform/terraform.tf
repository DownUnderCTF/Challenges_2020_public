provider "google" {
  project = var.project_id
  region  = "australia-southeast1"
  zone    = "australia-southeast1-b"
}

resource "google_project_service" "iam-cred-api" {
  project = var.project_id
  service = "iamcredentials.googleapis.com"
}

resource "google_project_service" "cloudbuild-api" {
  project = var.project_id
  service = "cloudbuild.googleapis.com"
}

resource "google_project_service" "cloudfunctions-api" {
  project = var.project_id
  service = "cloudfunctions.googleapis.com"
}

## CUSTOM ROLES

resource "google_project_iam_custom_role" "storage_lister" {
  role_id = "storageLister"
  title = "Storage Lister"
  permissions = ["storage.buckets.list", "storage.objects.list"]
}

resource "google_project_iam_custom_role" "cloud_function_worker" {
  role_id = "functionWorker"
  title = "Function Worker"
  permissions = [
    "cloudfunctions.functions.get", 
    "cloudfunctions.functions.list", 
    "cloudfunctions.functions.sourceCodeGet",
    "cloudfunctions.locations.list",
    "cloudfunctions.functions.invoke"
    ]
}


###### IAM Service Account ######

# cory-worthington
resource "google_service_account" "cory" {
  account_id   = "cory-worthington"
  display_name = "nah not gonna take off my sunnies"
}

# CF-Runner
resource "google_service_account" "tracy" {
  account_id   = "tracy-worker"
  display_name = "u wanna take off your sunnies?"
}

### IAM ROLE BINDINGS

# cory-worthington
resource "google_project_iam_binding" "storage_lister_binding" {
  role = google_project_iam_custom_role.storage_lister.id
  members = [
    "serviceAccount:${google_service_account.cory.email}",
  ]
  depends_on = [google_service_account.cory]
}

resource "google_project_iam_binding" "function_worker_binding" {
  role = google_project_iam_custom_role.cloud_function_worker.id
  members = [
    "serviceAccount:${google_service_account.cory.email}",
  ]
  depends_on = [google_service_account.cory]
}

# CF RUNNER
resource "google_project_iam_binding" "token_creator_binding" {
  role = "roles/iam.serviceAccountTokenCreator"
  members = [
    "serviceAccount:${google_service_account.tracy.email}",
  ]
  depends_on = [google_service_account.tracy]
}


### CF config

# resource "google_cloudfunctions_function" "professional-signer" {
#   name        = "professional-signer"
#   runtime     = "nodejs12"

#   available_memory_mb   = 128
#   trigger_http          = true
#   timeout               = 60
#   entry_point           = "signURL"
#   depends_on =  [google_project_service.cloudbuild-api]
# }


### App Engine Config
resource "google_app_engine_application" "app" {
  project     = var.project_id
  location_id = "australia-southeast1"
}

# resource "google_app_engine_standard_app_version" "app" {
#   version_id = "v1"
#   service = "default"
#   runtime = "nodejs12"

#   deployment {
#     zip {
#       source_url = "app.zip"
#     }
#   }

#   env_variables = {
#     FLAG = "DUCTF{and_thats_the_way_its_gonna_be_little_darling_we'll_be_riding_on_the_horses_YEAAAAAAAAAAAAAAAAAAAAYEAAAAAAAAAAAAAAAAAAAAH}"
#   }
#   depends_on = [google_app_engine_application.app]
# }

### Bucket Config

resource "google_storage_bucket" "app-engine-bucket" {
  name          = var.app-engine-bucket
  location      = "australia-southeast1"
  force_destroy = true
  uniform_bucket_level_access = true
} 

# Bucket Access
resource "google_storage_bucket_iam_binding" "binding" {
  bucket = google_storage_bucket.app-engine-bucket.name
  role = "roles/storage.objectViewer"
  members = [
    "serviceAccount:${google_service_account.tracy.email}",
  ]
}

# Bucket objects
resource "google_storage_bucket_object" "index-js" {
  name   = "index.js"
  source = "../app-src/index.js"
  bucket = google_storage_bucket.app-engine-bucket.name
}

resource "google_storage_bucket_object" "package-json" {
  name   = "package.json"
  source = "../app-src/package.json"
  bucket = google_storage_bucket.app-engine-bucket.name
}
resource "google_storage_bucket_object" "package-lock-json" {
  name   = "package-lock.json"
  source = "../app-src/package-lock.json"
  bucket = google_storage_bucket.app-engine-bucket.name
}

resource "google_storage_bucket_object" "index-html" {
  name   = "static/index.html"
  source = "../app-src/static/index.html"
  bucket = google_storage_bucket.app-engine-bucket.name
}

