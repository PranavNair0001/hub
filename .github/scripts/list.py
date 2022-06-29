import os
import utilities
import logging
import json
import time

logging.getLogger().setLevel(logging.INFO)
# utilities.gcs_sync_dir('gs://project-step-pranav-hub-cdap-io/packages/', './packages/', ignore=True)

toFetch, ids = utilities.get_missing_files()

logging.info('Missing files before retrieval are: ')
for file in toFetch:
  logging.info(file)
  time.sleep(5)

for id in ids:
  logging.info(id)

jsonStr = ''
for i in range(len(toFetch)):
  #example obj : packages/hydrator-plugin-gcp-plugins/0.17.4/google-cloud-0.17.4.jar
  obj = toFetch[i]
  extension = obj.split('.')[-1]
  file_name = obj.split('/')[3]
  jsonStr += '{' + \
             '"path":\"' + obj + \
             '\","target_path":\"artifact/' + file_name + \
             '\","artifact":\"' + file_name + \
             '\","repo": {"id":\"' + ids[i] + \
             '\","file_type":\"' + extension + \
             '\"}},'

output = '{"output":[' + jsonStr[:-1] + ']}'
print('Output of list.py: ')
json_object = json.loads(output)
json_formatted_str = json.dumps(json_object, indent=2)
print(json_formatted_str)

env_file = os.getenv('GITHUB_ENV')

with open(env_file, "a") as myfile:
  myfile.write("output=" + str(output))