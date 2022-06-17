import os
import utilities

utilities.gcs_sync_dir('gs://project-step-pranav-hub-cdap-io/packages/', './packages/')

toFetch, ids = utilities.get_missing_files()

print('Missing files before retrieval are: ')
for file in toFetch:
  print(file)

for id in ids:
  print(id)

jsonStr = ''
for i in range(len(toFetch)):
  filename = utilities.run_shell_command('basename -- ' + toFetch[i])
  extension = utilities.run_shell_command('filename=' + filename + ' && ${filename##*.}')
  jsonStr += '{"path":"' + toFetch[i] + '","target_path":"artifact/' + toFetch[i].split('/')[3] + '","artifact":"' + toFetch[i].split('/')[3] + '","repo":{"id":"' + ids[i] + '","file_type":"' + extension + '"}},'

output = '[' + jsonStr[:-1] + ']'
print('Output of fetch.py: ')
print(output)

utilities.run_shell_command('output=' + output + ' && export output && echo "output=${output}" >> $GITHUB_ENV')