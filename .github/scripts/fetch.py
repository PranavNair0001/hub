import os
import utilities

utilities.gcs_sync_dir('gs://project-step-pranav-hub-cdap-io/packages/', './packages/')

toFetch, ids = utilities.get_missing_files()

print('Missing files before retrieval are: ')
for file in toFetch:
  print(file)

for id in ids:
  print(id)

for i in range(len(toFetch)):
  filename = utilities.run_shell_command('basename -- ' + toFetch[i])
  extension = utilities.run_shell_command('filename=' + filename + ' && ${filename##*.}')

