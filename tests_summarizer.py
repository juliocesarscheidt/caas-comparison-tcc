import os
import glob
import json
import pandas as pd

TEST_TYPE = os.environ.get('TEST_TYPE')

def replace_dot_with_comma_for_csv(value) -> str:
  rounded_value = float('%.4f' % value)
  return str(rounded_value).replace('.', ',')

if __name__ == '__main__':
  result_dataset = []

  for filename in glob.glob(f'load-tests/{TEST_TYPE}/result-*.json'):
    print(f'filename :: {filename}')
    result_index = filename.split('-')[-1].replace('.json', '')
    print(f'result_index :: {result_index}')

    with open(filename, 'r') as f:
      result = json.loads(str(f.read()))
      aggregate = result['aggregate']
      counters = aggregate['counters']
      response_time = aggregate['summaries']['http.response_time']
      # requests
      total_requests = counters['http.requests']
      requests_success = counters['vusers.completed']
      requests_failure = counters['vusers.failed']
      error_rate = (requests_failure / total_requests)
      # latency
      latency_min = response_time['min']
      latency_max = response_time['max']
      latency_median = response_time['median']
      # percentis
      p90 = response_time['p90']
      p95 = response_time['p95']
      p99 = response_time['p99']

      result_dataset.append({
        'result_index': result_index,
        'total_requests': total_requests,
        'requests_success': requests_success,
        'requests_failure': requests_failure,
        'error_rate': replace_dot_with_comma_for_csv(error_rate * 100),
        'latency_min': replace_dot_with_comma_for_csv(latency_min),
        'latency_max': replace_dot_with_comma_for_csv(latency_max),
        'latency_median': replace_dot_with_comma_for_csv(latency_median),
        'p90': replace_dot_with_comma_for_csv(p90),
        'p95': replace_dot_with_comma_for_csv(p95),
        'p99': replace_dot_with_comma_for_csv(p99),
      })

  print(result_dataset)
  # generate a csv from dataset
  df = pd.DataFrame(data=result_dataset)
  df.sort_values(by=["result_index"], inplace=True)
  df.to_csv(
    f"tests_results_{TEST_TYPE}.csv",
    index=False,
    sep=",",
    encoding="utf-8",
  )
