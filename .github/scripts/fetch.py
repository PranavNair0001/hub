import utilities
import os

os.mkdir('./artifact')

utilities.gcs_sync_dir(source='gs://project-step-pranav-hub-cdap-io/' + os.getenv('DIR'), destination='./artifact')

if (os.path.isfile(os.path.join('./artifact', os.getenv('FILENAME')))):
  print(os.getenv('FILENAME') + ' : Found in GCS Bucket')
else:
  print(os.getenv('FILENAME') + ' : Not found in GCS Bucket')
  utilities.run_shell_command('mvn org.apache.maven.plugins:maven-dependency-plugin:2.8:copy -Dartifact=${ID}:${VERSION}:${EXTENSION} -DoutputDirectory=./artifact/')