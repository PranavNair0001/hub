import os
import utilities

utilities.gcs_sync_dir('gs://project-step-pranav-hub-cdap-io/packages/', './packages/')

toFetch = []
ids = []

