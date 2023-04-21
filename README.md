# CaaS platforms comparison

## Deploy the API on ECS

Check here: [ECS](./terraform/ecs/README.md)

## Deploy the API on ACI

Check here: [ACI](./terraform/aci/README.md)

## Performance comparison using Artillery

First and second sequences of tests with 30 RPS and total of 9.000 requests.

Third sequence of tests with 60 RPS and total of 18.000 requests.

```bash
export API_ENDPOINT="http://<LB_DNS_OR_IP>/api/v1/message"
API_ENDPOINT=$(echo "$API_ENDPOINT" | sed -r 's/\//\\\//gm')

for I in 0 1; do
  echo "load testing - sequence $I"
  cp load-tests/load-test-template.yml load-tests/load-test.yml
  # first and second sequences of tests with 30 RPS and total of 9.000 requests
  sed -i "s/{{API_ENDPOINT}}/${API_ENDPOINT}/; s/{{REQUESTS_PER_SECOND}}/30/; s/{{REQUESTS_TOTAL}}/9000/" load-tests/load-test.yml
  # execute tests and generate the report
  artillery run load-tests/load-test.yml --output load-tests/ecs/ecs-$I.json
  artillery report load-tests/ecs/ecs-$I.json
  rm -f load-tests/load-test.yml
done

for I in 2; do
  echo "load testing - sequence $I"
  cp load-tests/load-test-template.yml load-tests/load-test.yml
  # third sequence of tests with 60 RPS and total of 18.000 requests
  sed -i "s/{{API_ENDPOINT}}/${API_ENDPOINT}/; s/{{REQUESTS_PER_SECOND}}/60/; s/{{REQUESTS_TOTAL}}/18000/" load-tests/load-test.yml
  # execute tests and generate the report
  artillery run load-tests/load-test.yml --output load-tests/ecs/ecs-$I.json
  artillery report load-tests/ecs/ecs-$I.json
  rm -f load-tests/load-test.yml
done
```
