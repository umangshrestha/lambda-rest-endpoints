echo "Starting localstack"
docker-compose up -d

echo "starting terraform"
cd infrastructure
terraform init
terraform plan -out plan.out
terraform apply -auto-approve plan.out

echo "starting tests"
cd ..
python3 -m pytest -v tests/test_*.py
