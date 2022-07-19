import json
import os
import logging
import utilities

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
  extension = toFetch[i].split('.')[-1]
  jsonStr += '{\"path\":\"%s\",\"target_path\":\"artifact/%s\",\"artifact\":\"%s\",\"artifactDir\":\"%s\",\"repo\":{\"id\":\"%s\",\"file_type\":\"%s\"}},' %(toFetch[i], toFetch[i].split('/')[3], toFetch[i].split('/')[3], toFetch[i].rsplit('/', 1)[0], ids[i], extension)

output = '[' + jsonStr[:-1] + ']'
logging.info('Output of list.py: ')
logging.info(json.dumps(json.loads(output), indent=2))    # Pretty print JSON output

# Set output as environment variable of GitHub workflow runner
env_file = os.getenv('GITHUB_ENV')
with open(env_file, "a") as myfile:
  myfile.write("output=" + str(output))