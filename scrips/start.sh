echo "Starting localstack"
docker-compose up -d

echo "starting terraform"
cd infrastructure
terraform init
terraform apply -auto-approve

echo "starting tests"
cd ..
python3 -m pytest -v tests/test_*.py
