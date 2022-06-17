import os
import subprocess

def run_shell_command(cmd):
    process = subprocess.run(cmd, stderr=subprocess.PIPE, shell=True)
    if(process.returncode != 0):
        print('Process completed with error: ', process.stderr)
    assert process.returncode == 0

print('Starting Setup and Build of Packager, packages.json  ....')
print('Checking environment ....\n')

print('Java version: ')
run_shell_command('java -version')

print('Java compile version: ')
run_shell_command('javac -version')

print('Maven version: ')
run_shell_command('mvn -version')

print('Building packager ....\n')
os.chdir('./packager/')
run_shell_command('mvn clean package')
os.chdir('../')

print('Building packages.json ....\n')
run_shell_command('java -cp "packager/target/lib/*:packager/target/*" io.cdap.hub.Tool build')

print('ls:\n', os.listdir())
