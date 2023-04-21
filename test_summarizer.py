import os
import glob
import sys
import csv
import json

TEST_TYPE = os.environ.get('TEST_TYPE')

if __name__ == '__main__':
  for filename in glob.glob(f'load-tests/{TEST_TYPE}/result-*.json'):
    with open(filename, 'r') as f:
      result = json.loads(str(f.read()))
      try:
        print(result)
      except Exception as e:
        print(e)
