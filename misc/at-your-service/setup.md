# How to set up this challenge

This challenge requires a bit of set up from terraform and it probs could be done better but here it is.

## Set up Project and gcloud
1. Sign into your Google Cloud Platform account and create a new project with what ever name
2. Once it has been created note the `project id` 
3. In gcloud make sure you are logged in with the same account with `gcloud auth login`


## Set up infra with terraform
1. Download the right terraform binary to the `challenge/terraform` folder and run `./terraform init`
2. Update `challenge/terraform/terraform.tfvars` with the variables, the first is your project ID from above and then a globally unique bucket name ( no one in the world can have the same bucket name)
3. Run `./terraform plan` check the output make sure it looks all good
4. Run `./terraform apply` to apply the infrastructuyre set up

## Set up Cloud Function and App Engine
*I know you can do this with terraform but I couldn't be bothered to find a way to deploy src code to a bucket*
1. Navigate to the `challenge/app-src` directory and run `gcloud app deploy --project <Your Project ID>`
2. Navigate to the `challenge/cf-src` directory and run `gcloud functions deploy professional-signer --region australia-southeast1 --trigger-http --runtime nodejs12 --entry-point signURL --service-account tracy-worker@<your_project_id>.iam.gserviceaccount.com` and make sure you say `N` to any unauthenticated invocations

## Create Key and get App Engine URL for chal
1. To get the IAM key for svc account cory use the command `gcloud iam service-accounts keys create cory.json --iam-account cory-worthington@<your_project_ID_here>.iam.gserviceaccount.com` provide this to the competitors
2. Run `gcloud app describe --project <your_project_idhere>` and get the `default_hostname` this is the URL to the app engine instance, provide this also to the competitors. 

DONE!

