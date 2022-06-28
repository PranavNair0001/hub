import os
import utilities
import shutil

toFetch, ids = utilities.get_missing_files()

for file in toFetch:
  fileName = file.split('/')[3]
  if(os.path.isfile(os.path.join('artifacts', fileName, fileName))):
    shutil.move(os.path.join('artifacts', fileName, fileName), file)
  else:
    print(file + ' : not retrieved')

shutil.move(os.path.join('artifacts', 'packages.json', 'packages.json'), 'packages.json')

toFetch, ids = utilities.get_missing_files()

print('Missing files after retrieval: ')
for file in toFetch:
  print(file)

if(len(toFetch) != 0):
  print('Above file(s) yet to be fetched')
  exit(1)

if(os.path.isdir('artifacts')):
  shutil.rmtree('artifacts')

utilities.run_shell_command('gsutil -m rsync -d -r packages/ gs://project-step-pranav-hub-cdap-io/packages/')
utilities.run_shell_command('gsutil cp categories.json gs://project-step-pranav-hub-cdap-io/categories.json')
utilities.run_shell_command('gsutil cp packages.json gs://project-step-pranav-hub-cdap-io/packages.json')
utilities.run_shell_command('gsutil -m rsync -d -r gs://project-step-pranav-hub-cdap-io/ gs://project-step-pranav-hub-cdap-io-master/')