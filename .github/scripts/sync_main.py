import utilities
utilities.run_shell_command('gsutil -m rsync -d -r packages/ gs://project-step-pranav-hub-cdap-io/packages/')
utilities.run_shell_command('gsutil cp categories.json gs://project-step-pranav-hub-cdap-io/categories.json')
utilities.run_shell_command('gsutil cp packages.json gs://project-step-pranav-hub-cdap-io/packages.json')
utilities.run_shell_command('gsutil -m rsync -d -r gs://project-step-pranav-hub-cdap-io/ gs://project-step-pranav-hub-cdap-io-master/')