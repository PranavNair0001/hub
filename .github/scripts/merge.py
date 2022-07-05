import os
import shutil
import logging
import utilities

logging.getLogger().setLevel(logging.INFO)    # Enable logging in GitHub Workflow

toFetch, ids = utilities.get_missing_files()

for file in toFetch:
  fileName = file.split('/')[3]
  logging.info('Merging missing file: ' + fileName)
  if(os.path.isfile(os.path.join('artifacts', fileName, fileName))):
    shutil.move(os.path.join('artifacts', fileName, fileName), file)
  else:
    logging.info(file + ' : not retrieved')

shutil.move(os.path.join('artifacts', 'packages.json', 'packages.json'), 'packages.json')

toFetch, ids = utilities.get_missing_files()

logging.info('Missing files after retrieval: ')
for file in toFetch:
  logging.info(file)

if(len(toFetch) != 0):
  logging.info('Above file(s) yet to be fetched')
  exit(1)

if(os.path.isdir('artifacts')):
  shutil.rmtree('artifacts')

utilities.run_shell_command('gsutil -m rsync -d -r packages/ gs://project-step-pranav-hub-cdap-io/packages/')
utilities.run_shell_command('gsutil cp categories.json gs://project-step-pranav-hub-cdap-io/categories.json')
utilities.run_shell_command('gsutil cp packages.json gs://project-step-pranav-hub-cdap-io/packages.json')
utilities.run_shell_command('gsutil -m rsync -d -r gs://project-step-pranav-hub-cdap-io/ gs://project-step-pranav-hub-cdap-io-master/')