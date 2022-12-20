locals {
  data_lake_bucket = "dtc_data_lake"
}

variable "project" {
  description = "GCP project ID"
}

variable "region" {
  default = "europe-west6"
  type = string 
}

variable "storage_class" {
  default = "STANDARD"
}

variable "BQ_dataset" {
  type = string
  default = "trips_data_all"
}