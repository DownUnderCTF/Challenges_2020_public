variable "project_id" {
  description = "GCP Project id"
  type        = string
}

variable "meme-bucket-name" {
  description = "Name of the meme bucket"
  type        = string
}

variable "secure-meme-bucket-name" {
  description = "Name of the secure meme bucket which has the key"
  type        = string
}