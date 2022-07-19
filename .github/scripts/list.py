# Copyright © 2022 Cask Data, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

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
    jsonStr += '{\"path\":\"' + toFetch[i] + '\",\"target_path\":\"artifact/' + toFetch[i].split('/')[3] + '\",\"artifact\":\"' + toFetch[i].split('/')[3] + '\",\"artifactDir\":\"' + toFetch[i].rsplit('/', 1)[0] + '\",\"repo\":{\"id\":\"' + ids[i] + '\",\"file_type\":\"' + extension + '\"}},'

output = '[' + jsonStr[:-1] + ']'
logging.info('Output of list.py: ')
logging.info(json.dumps(json.loads(output), indent=2))    # Pretty print JSON output

# Set output as environment variable of GitHub workflow runner
env_file = os.getenv('GITHUB_ENV')
with open(env_file, "a") as myfile:
    myfile.write("output=" + str(output))