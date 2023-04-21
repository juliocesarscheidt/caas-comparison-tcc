# CaaS platforms comparison

This project will present a comparison between AWS ECS and Azure ACI, using the same container API and running it on each platform.

For the deployment it will be using Terraform and IaC.

## Deploy the API on ECS

Check here: [ECS](./terraform/ecs/README.md)

## Deploy the API on ACI

Check here: [ACI](./terraform/aci/README.md)

## Performance comparison using Artillery

There will be three sequences of tests, with 600 seconds of duration.

First and second sequences of tests with 30 RPS and total of 9.000 requests.

Third sequence of tests with 60 RPS and total of 18.000 requests.

```bash
export API_ENDPOINT="http://<LB_DNS_OR_IP>/api/v1"
API_ENDPOINT=$(echo "$API_ENDPOINT" | sed -r 's/\//\\\//gm')
export TEST_TYPE="<ecs|aci>" # aws ecs or azure aci

for I in 0 1; do
  echo "load testing - sequence $I"
  cp load-tests/load-test-template.yml load-tests/load-test.yml
  # first and second sequences of tests with 30 RPS and total of 9.000 requests
  sed -i "s/{{API_ENDPOINT}}/${API_ENDPOINT}/; s/{{REQUESTS_PER_SECOND}}/30/; s/{{REQUESTS_TOTAL}}/9000/" load-tests/load-test.yml
  # execute tests and generate the report
  artillery run load-tests/load-test.yml --output load-tests/$TEST_TYPE/$TEST_TYPE-$I.json
  artillery report load-tests/$TEST_TYPE/$TEST_TYPE-$I.json
  rm -f load-tests/load-test.yml
done

for I in 2; do
  echo "load testing - sequence $I"
  cp load-tests/load-test-template.yml load-tests/load-test.yml
  # third sequence of tests with 60 RPS and total of 18.000 requests
  sed -i "s/{{API_ENDPOINT}}/${API_ENDPOINT}/; s/{{REQUESTS_PER_SECOND}}/60/; s/{{REQUESTS_TOTAL}}/18000/" load-tests/load-test.yml
  # execute tests and generate the report
  artillery run load-tests/load-test.yml --output load-tests/$TEST_TYPE/$TEST_TYPE-$I.json
  artillery report load-tests/$TEST_TYPE/$TEST_TYPE-$I.json
  rm -f load-tests/load-test.yml
done
```
