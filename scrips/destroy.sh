# echo "destroying terraform"
cd infrastructure
terraform destroy -auto-approve

# echo "stopping localstack"
cd ..
docker-compose down