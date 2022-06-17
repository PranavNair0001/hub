import os
import subprocess
import json
import yaml

def run_shell_command(cmd):
  process = subprocess.run(cmd, stderr=subprocess.PIPE, shell=True)
  if(process.returncode != 0):
    print('Process completed with error: ', process.stderr)
  assert process.returncode == 0

def get_missing_files():
  files = []
  ids = []
  packagesDir = 'packages/'
  for artifact in os.listdir(packagesDir):
    artifactDir = os.path.join(packagesDir, artifact)
    if(os.path.isdir(artifactDir)):
      for version in os.listdir(artifactDir):
        artifactVersionDir = os.path.join(artifactDir, version)
        if(os.path.isdir(artifactVersionDir)):
          if(os.path.isfile(os.path.join(artifactVersionDir, 'spec.json'))):
            specFile = open(os.path.join(artifactVersionDir, 'spec.json'))
            specData = json.load(specFile)
            jarFiles = []
            configFiles = []
            for object in specData['actions']:
              if(object['type'] == 'one_step_deploy_plugin'):
                for property in object['arguments']:
                  if(property['name'] == 'jar'):
                    jarFiles.append(property['value'])
                  if(property['name'] == 'config'):
                    configFiles.append(property['value'])
            for jarFile in jarFiles:
              if(not os.path.isfile(os.path.join(artifactVersionDir, jarFile))):
                if(os.path.isfile(os.path.join(artifactDir, 'build.yaml'))):
                  buildFile = open(os.path.join(artifactDir, 'build.yaml'))
                  buildData = yaml.load(buildFile, Loader=yaml.FullLoader)
                  groupId = buildData['maven-central']['groupId']
                  artifactId = buildData['maven-central']['artifactId']
                  files.append(os.path.join(artifactVersionDir, jarFile))
                  ids.append('%s:%s:%s' %(groupId, artifactId, version))
                else:
                  print('Error: build.yaml file does not exist for ' + artifactDir)
            for configFile in configFiles:
              if(not os.path.isfile(os.path.join(artifactVersionDir, configFile))):
                if(os.path.isfile(os.path.join(artifactDir, 'build.yaml'))):
                  buildFile = open(os.path.join(artifactDir, 'build.yaml'))
                  buildData = yaml.load(buildFile, Loader=yaml.FullLoader)
                  groupId = buildData['maven-central']['groupId']
                  artifactId = buildData['maven-central']['artifactId']
                  files.append(os.path.join(artifactVersionDir, configFile))
                  ids.append('%s:%s:%s' %(groupId, artifactId, version))
                else:
                  print('Error: build.yaml file does not exist for ' + artifactDir)
          else:
            print('Error: spec.json does not exist for ' + artifactVersionDir)
            exit(1)
  return files, ids

def gcs_sync_dir(source, destination, ignore=False):
  if ignore:
    run_shell_command('gsutil -m rsync -i -r %s %s' %(source, destination))
  else:
    run_shell_command('gsutil -m rsync -r %s %s' %(source, destination))
