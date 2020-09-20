Setup guide 

Set up the challenge

1. Create a new project on GCP and note down the `project_id` 
2. Download the [gcloud sdk](https://cloud.google.com/sdk/install) on your machine and run `gcloud auth application-default login`
3. Update terraform/terraform.tfvars with the `project_id` from step 1 and give two bucket names that haven't been used yet
4. Update bot-src/index.js and update line 25 and 26 with the bucket names from step 3

Running the terraform

5. Move into the terraform folder and run `./terraform init`
6. Run `./terraform plan` and verify everything is ok
7. Run `./terraform apply` and type yes to create the infrastructure
8. If some fail wait a few minutes and run `./terraform apply` again to wait for the API's to be enabled properly

These steps are so the token isn't leaked (best effort)

9. SSH into the machine with `gcloud compute ssh discord-bot`
10. Run `docker ps` and note the name of the container
11. Run `docker attach <container_name>` and then paste the Discord Bot Token in and hit enter
12.  CTRL+P, CTRL+Q to detach and then you can exit

Disable SSH on the machine

13. Change line 107 in `terraform.tf` to true and run `./terraform apply` to disallow ssh on the machine (DO THIS ONLY ONCE YOU HAVE CONFIRMED THE CHALLENGE IS UP AND RUNNING GOODLY)