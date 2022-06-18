import os
import utilities

utilities.gcs_sync_dir('gs://project-step-pranav-hub-cdap-io/packages/', './packages/', ignore=True)

toFetch, ids = utilities.get_missing_files()

print('Missing files before retrieval are: ')
for file in toFetch:
  print(file)

for id in ids:
  print(id)

jsonStr = ''
for i in range(len(toFetch)):
  extension = toFetch[i].split('.')[-1]
  jsonStr += '{\"path\":\"' + toFetch[i] + '\",\"target_path\":\"artifact/' + toFetch[i].split('/')[3] + '\",\"artifact\":\"' + toFetch[i].split('/')[3] + '\",\"repo\":{\"id\":\"' + ids[i] + '\",\"file_type\":\"' + extension + '\"}},'

output = '[' + jsonStr[:-1] + ']'
print('Output of fetch.py: ')
print(output)

env_file = os.getenv('GITHUB_ENV')

with open(env_file, "a") as myfile:
  myfile.write("output=" + str(output))