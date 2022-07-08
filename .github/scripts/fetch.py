##not in use: using shell script in main workflow itself
import os
import logging
import utilities

logging.getLogger().setLevel(logging.INFO)    # Enable logging in GitHub Workflow and enable printing of info level logs

#Creating artifact directory
logging.info('Creating temporary \'artifact/\' directory')
os.mkdir('./artifact')

#Initial sync
logging.info('Syncing with gs://project-step-pranav-hub-cdap-io/' + os.getenv('DIR'))
utilities.gcs_sync_dir(source='gs://project-step-pranav-hub-cdap-io/' + os.getenv('DIR'), destination='./artifact')

if (os.path.isfile(os.path.join('./artifact', os.getenv('FILENAME')))):
  logging.info(os.getenv('FILENAME') + ' : Found in GCS Bucket')
else:
  logging.info(os.getenv('FILENAME') + ' : Not found in GCS Bucket. Fetching from Maven Central')
  utilities.run_shell_command('mvn org.apache.maven.plugins:maven-dependency-plugin:2.8:copy -Dartifact=${ID}:${VERSION}:${EXTENSION} -DoutputDirectory=./artifact/')