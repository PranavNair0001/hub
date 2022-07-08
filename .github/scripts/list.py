import json
import os
import utilities
import logging

logging.getLogger().setLevel(logging.INFO)    # Enable logging in GitHub Workflow

toFetch, ids = utilities.get_missing_files()

logging.info('Missing files before retrieval are: ')
for file in toFetch:
  logging.info(file)

logging.info('Maven IDs of corresponding missing files are: ')
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
logging.info('Output of list.py: ')
logging.info(json.dumps(json.loads(output), indent=2))    # Pretty print JSON output
output = '[' + jsonStr[:-1] + ']'

# Set output as environment variable of GitHub workflow runner
env_file = os.getenv('GITHUB_ENV')

with open(env_file, "a") as myfile:
  myfile.write("output=" + str(output))


