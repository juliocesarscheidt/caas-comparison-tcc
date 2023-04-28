# CaaS platforms comparison

This project will present a comparison between AWS ECS and Azure ACI, using the same container API and running it on each platform.

For the deployment it will be using Terraform and IaC.

## Deploy the API on ECS

Check here: [ECS](./terraform/ecs/README.md)

## Deploy the API on ACI

Check here: [ACI](./terraform/aci/README.md)

## Performance comparison using Artillery

There will be three sequences of tests, with 600 seconds of duration.

- First, second and third sequences of tests with 100 RPS and total of 30.000 requests each.

- Fourth and fifth sequence of tests with 500 RPS and total of 150.000 requests each.

```bash
export API_ENDPOINT=$(echo "http://<LB_DNS_OR_IP>/api/v1" | sed -r 's/\//\\\//gm')
export TEST_TYPE="<ecs|aci>" # for aws ecs or azure aci

for I in 0 1 2; do
  echo "load testing - sequence $I"
  cp load-test-template.yml load-test-$TEST_TYPE.yml
  # first and second sequences of tests with 100 RPS and total of 30.000 requests
  sed -i "s/{{API_ENDPOINT}}/${API_ENDPOINT}/; s/{{REQUESTS_PER_SECOND}}/100/; s/{{REQUESTS_TOTAL}}/30000/" load-test-$TEST_TYPE.yml
  # execute tests and generate HTML report
  mkdir -p $TEST_TYPE/
  artillery run load-test-$TEST_TYPE.yml --output $TEST_TYPE/result-$I.json
  artillery report $TEST_TYPE/result-$I.json
  rm -f load-test-$TEST_TYPE.yml
done

for I in 3 4; do
  echo "load testing - sequence $I"
  cp load-test-template.yml load-test-$TEST_TYPE.yml
  # third sequence of tests with 500 RPS and total of 150.000 requests
  sed -i "s/{{API_ENDPOINT}}/${API_ENDPOINT}/; s/{{REQUESTS_PER_SECOND}}/500/; s/{{REQUESTS_TOTAL}}/150000/" load-test-$TEST_TYPE.yml
  # execute tests and generate HTML report
  mkdir -p $TEST_TYPE/
  artillery run load-test-$TEST_TYPE.yml --output $TEST_TYPE/result-$I.json
  artillery report $TEST_TYPE/result-$I.json
  rm -f load-test-$TEST_TYPE.yml
done
```

## Generate tests summary in a CSV file

```bash
python tests_summarizer.py
```
