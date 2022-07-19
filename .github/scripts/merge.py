import os
import shutil
import logging
import utilities

logging.getLogger().setLevel(logging.DEBUG)    # Enable logging in GitHub Workflow

toFetch, ids = utilities.get_missing_files()

for file in toFetch:
  fileName = file.split('/')[3]
  logging.info('Merging missing file: ' + fileName)
  if(os.path.isfile(os.path.join('artifacts', fileName, fileName))):
    shutil.move(os.path.join('artifacts', fileName, fileName), file)
  else:
    logging.info('WARNING: ' + file + ' : not retrieved')

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
