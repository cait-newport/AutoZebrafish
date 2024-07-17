# Description: Create a shared project from an existing LISA project
# Example: python push-as-shared-project.py --lisa-fn /path/to/lisa.json
# Dependencies: None
# Notes: This script is intended to be run from the terminal command line.
#
# Abhishek Dutta
# 2023-01-13

import csv
import time
import json
import os
import numpy as np
import random
import http.client
import argparse

from json import encoder
encoder.FLOAT_REPR = lambda o: format(o, '.3f') # save float with only 3 decimal places

def create_shared_project(project_data):
	project_data_str = json.dumps(project_data, indent=None, separators=(',',':'))
	conn = http.client.HTTPSConnection('meru.robots.ox.ac.uk', 443)
	conn.request('POST', '/store/', project_data_str)
	response = conn.getresponse()
	shared_project_info = ''
	if response.status == 200:
		shared_project_info = response.read().decode('utf-8')
	else:
		via_project_id = 'ERROR:' + response.reason
	conn.close()
	return shared_project_info

if __name__ == "__main__":
	parser = argparse.ArgumentParser('push-as-shared-project', 'Create a shared project from an existing LISA project')
	parser.add_argument('--lisa-fn', required=True, type=str, help='LISA project filename')
	args = parser.parse_args()

	print('Pushing as shared project: %s' % (args.lisa_fn))
	with open(args.lisa_fn, 'r') as f:
		lisa = json.load(f)
		lisa['shared_fid'] = '__FILE_ID__'
		lisa['shared_rev'] = '__FILE_REV_ID__'
		lisa['shared_rev_timestamp'] = '__FILE_REV_TIMESTAMP__'
		lisa['project_id'] = ''
		shared_pinfo_str = create_shared_project(lisa)
		print(shared_pinfo_str)
		shared_pinfo = json.loads(shared_pinfo_str)
		print(json.dumps(shared_pinfo, indent=True))
	print('Done')