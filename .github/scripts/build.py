import os
import logging
import utilities

logging.getLogger().setLevel(logging.INFO)    # Enable logging in GitHub Workflow and enable printing of info level logs

#Initial environment and version check logs
logging.info('Starting Setup and Build of Packager, packages.json  ....')
logging.info('Checking environment ....\n')

logging.info('Java version: ')
utilities.run_shell_command('java -version')

logging.info('Java compile version: ')
utilities.run_shell_command('javac -version')

logging.info('Maven version: ')
utilities.run_shell_command('mvn -version')

#Building packager and packages
logging.info('Building packager ....\n')
os.chdir('./packager/')
utilities.run_shell_command('mvn clean package')
os.chdir('../')

logging.info('Building packages.json ....\n')
utilities.run_shell_command('java -cp "packager/target/lib/*:packager/target/*" io.cdap.hub.Tool build')

#Listing all files
logging.info('ls:\n', os.listdir())
