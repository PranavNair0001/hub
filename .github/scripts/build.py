import os
import utilities

print('Starting Setup and Build of Packager, packages.json  ....')
print('Checking environment ....\n')

print('Java version: ')
utilities.run_shell_command('java -version')

print('Java compile version: ')
utilities.run_shell_command('javac -version')

print('Maven version: ')
utilities.run_shell_command('mvn -version')

print('Building packager ....\n')
os.chdir('./packager/')
utilities.run_shell_command('mvn clean package')
os.chdir('../')

print('Building packages.json ....\n')
utilities.run_shell_command('java -cp "packager/target/lib/*:packager/target/*" io.cdap.hub.Tool build')

print('ls:\n', os.listdir())
