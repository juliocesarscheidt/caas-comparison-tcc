# GCP VM Instance to execute load tests

It's using by default the region southamerica-east1 (Sao Paulo - Brazil) with a Debian 10, and a burstable instance f1-micro with 0.2 CPUs and 0.60 GB of memory.

```bash
# terraform workflow
terraform init
terraform validate
terraform plan
terraform apply -auto-approve

# output from created resources
export INSTANCE_IP=$(terraform output -raw instance_ip)
terraform output -raw private_key > private_key.pem && chmod 400 private_key.pem

# copy load test template to the instance
scp -i private_key.pem ../../load-tests/load-test-template.yml google@$INSTANCE_IP:/home/google/load-test-template.yml
# access the instance
ssh -i private_key.pem google@$INSTANCE_IP

# execute load tests...

# clean up
terraform destroy -auto-approve
```
