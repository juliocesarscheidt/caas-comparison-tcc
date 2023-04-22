import glob
import json
import pandas as pd

def replace_dot_with_comma_for_csv(value) -> str:
  rounded_value = float('%.4f' % value)
  return str(rounded_value).replace('.', ',')

if __name__ == '__main__':
  result_dataset = []

  for filename in glob.glob('load-tests/**/result-*.json'):
    print(f'filename :: {filename}')
    test_type = str(filename.split('/')[1]).upper()
    print(f'test_type :: {test_type}')
    result_index = int(filename.split('-')[-1].replace('.json', '')) + 1

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
      # append all to dataset
      result_dataset.append({
        'test_type': test_type,
        'result_index': str(result_index) + 'ª Sequência',
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

  # create a pandas dataset from the processed data
  df = pd.DataFrame(data=result_dataset)
  df.sort_values(by=["result_index"], inplace=True)
  df = df.rename(columns={
    "test_type": "Provedor",
    "result_index": "Sequencia de Testes",
    "total_requests": "Total Requests",
    "requests_success": "Requests Sucesso",
    "requests_failure": "Requests Falha",
    "error_rate": "Taxa de Erro %",
    "latency_min": "Latência Mínima (ms)",
    "latency_max": "Latência Máxima (ms)",
    "latency_median": "Latência Mediana (ms)",
    "p90": "p90 (ms)",
    "p95": "p95 (ms)",
    "p99": "p99 (ms)",
  })
  print(df.head(10))
  # generate a csv from dataset
  df.to_csv(
    f"tests_summary.csv",
    index=False,
    sep=",",
    encoding="utf-8",
  )
