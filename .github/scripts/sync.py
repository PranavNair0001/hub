import utilities
import os
import logging
import json

logging.getLogger().setLevel(logging.DEBUG)    # Enable logging in GitHub Workflow

central_bucket, regional_buckets = utilities.get_bucket_list()

jsonStr = ''
for bucket in regional_buckets:
    jsonStr += '{\"central_address\":\"%s\",\"regional_address\":\"%s\"},' %('gs://' + central_bucket, 'gs://project-step-pranav-hub-cdap-io-' + bucket)

output = '[' + jsonStr[:-1] + ']'
logging.debug('Output of list.py: ')
logging.debug(json.dumps(json.loads(output), indent=2))    # Pretty print JSON output

env_file = os.getenv('GITHUB_ENV')
with open(env_file, "a") as myfile:
    myfile.write("buckets=" + str(output))

utilities.run_shell_command('gsutil -m rsync -d -c -r packages/ gs://' + central_bucket + '/packages/')
utilities.run_shell_command('gsutil cp -n categories.json gs://' + central_bucket + '/categories.json')
utilities.run_shell_command('gsutil cp -n packages.json gs://' + central_bucket + '/packages.json')