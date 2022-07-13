import os
import subprocess
import json
import yaml
import re
import logging

logging.getLogger().setLevel(logging.INFO)    # Enable logging in GitHub Workflow and enable printing of info level logs

class LazyDecoder(json.JSONDecoder):
  def decode(self, s, **kwargs):
    regex_replacements = [
        (re.compile(r'([^\\])\\([^\\])'), r'\1\\\\\2'),
        (re.compile(r',(\s*])'), r'\1'),
    ]
    for regex, replacement in regex_replacements:
      s = regex.sub(replacement, s)
    return super().decode(s, **kwargs)

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
      logging.info('Checking artifact: ' + artifact)
      for version in os.listdir(artifactDir):
        artifactVersionDir = os.path.join(artifactDir, version)
        if(os.path.isdir(artifactVersionDir)):
          logging.info('Checking missing files in ' + artifactVersionDir)
          if(os.path.isfile(os.path.join(artifactVersionDir, 'spec.json'))):
            logging.info('Inspecting spec.json for necessary files')
            specFile = open(os.path.join(artifactVersionDir, 'spec.json'))
            specData = json.load(specFile, cls=LazyDecoder)
            jarFiles = []
            configFiles = []

            for object in specData['actions']:
              for property in object['arguments']:
                if(property['name'] == 'jar'):
                  jarFiles.append(property['value'])
                if(property['name'] == 'config'):
                  configFiles.append(property['value'])
            logging.info('Required files: ')
            logging.info(jarFiles)
            logging.info(configFiles)
            for jarFile in jarFiles:
              if(not os.path.isfile(os.path.join(artifactVersionDir, jarFile))):
                if(os.path.isfile(os.path.join(artifactDir, 'build.yaml'))):
                  buildFile = open(os.path.join(artifactDir, 'build.yaml'))
                  buildData = yaml.load(buildFile, Loader=yaml.FullLoader)
                  groupId = buildData['maven-central']['groupId']
                  artifactId = buildData['maven-central']['artifactId']
                  files.append(os.path.join(artifactVersionDir, jarFile))
                  ids.append('%s:%s:%s' %(groupId, artifactId, version))
                  logging.info('Missing file: ' + jarFile)
                else:
                  logging.info('WARNING: build.yaml file does not exist for ' + artifactDir)
                  files.append(os.path.join(artifactVersionDir, jarFile))
                  ids.append('::%s' %(version))
            for configFile in configFiles:
              if(not os.path.isfile(os.path.join(artifactVersionDir, configFile))):
                if(os.path.isfile(os.path.join(artifactDir, 'build.yaml'))):
                  buildFile = open(os.path.join(artifactDir, 'build.yaml'))
                  buildData = yaml.load(buildFile, Loader=yaml.FullLoader)
                  groupId = buildData['maven-central']['groupId']
                  artifactId = buildData['maven-central']['artifactId']
                  files.append(os.path.join(artifactVersionDir, configFile))
                  ids.append('%s:%s:%s' %(groupId, artifactId, version))
                  logging.info('Missing file: ' + configFile)
                else:
                  logging.info('WARNING: build.yaml file does not exist for ' + artifactDir)
                  files.append(os.path.join(artifactVersionDir, jarFile))
                  ids.append('::%s' %(version))
          else:
            logging.info('ERROR: spec.json does not exist for ' + artifactVersionDir)
            exit(1)
  return files, ids

def gcs_sync_dir(source, destination, ignore=False):
  logging.info('Syncing directory using gsutil. Source: ' + source + ' Destination: ' + destination)
  if ignore:
    run_shell_command('gsutil -m rsync -i -r %s %s' %(source, destination))
  else:
    run_shell_command('gsutil -m rsync -r %s %s' %(source, destination))

def gcs_copy(source, destination, overwrite=False):
  logging.info('Copying file using gsutil. Source: ' + source + ' Destination: ' + destination)
  if overwrite:
    run_shell_command('gsutil cp %s %s' %(source, destination))
  else:
    run_shell_command('gsutil cp -n %s %s' %(source, destination))