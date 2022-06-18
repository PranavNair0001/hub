import os
import utilities
import shutil

utilities.gcs_sync_dir('gs://project-step-pranav-hub-cdap-io/packages/', './packages/', ignore=True)

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

utilities.gcs_sync_dir('packages', 'gs://project-step-pranav-hub-cdap-io/packages/')
utilities.gcs_sync('packages.json', 'gs://project-step-pranav-hub-cdap-io/packages.json')
utilities.gcs_sync('categories.json', 'gs://project-step-pranav-hub-cdap-io/categores.json')