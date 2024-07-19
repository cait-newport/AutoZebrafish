# Description: Export annotations for shared projects created using List Annotator (LISA)
#
# Author: Abhishek Dutta (4 Oct 2020)
# Updated by Cait Newport to add error handling (19 July 2024)
# This script requires that you have a text file made that lists your project IDs (one per line) (pid)
# Example: python export-annotations.py --shared-pid-file /path/to/shared-pid-list.txt > annotations.csv

import json
import os
import http.client
import sys
import csv
import argparse

SHARED_PROJECT_SERVER = 'meru.robots.ox.ac.uk'

def fetch_shared_project(project_id):
    conn = http.client.HTTPSConnection(SHARED_PROJECT_SERVER)
    endpoint = '/store/' + project_id
    conn.request('GET', endpoint)
    response = conn.getresponse()
    if response.status != 200:
        print('Failed to fetch annotations from http://%s%s' % (SHARED_PROJECT_SERVER, endpoint))
        print('HTTP Error: %d %s' % (response.status, response.reason))
        sys.exit(0)

    project_data = response.read().decode('utf-8')
    conn.close()
    return project_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='export-annotations.py',
                                     description='Export annotations contained in a shared LISA project')
    parser.add_argument('--shared-pid-file',
                        required=True,
                        type=str,
                        help='a text file containing list of shared project id (one per line)')
    args = parser.parse_args()

    if not os.path.exists(args.shared_pid_file):
        print('Cannot open file containing shared pid list: %s' % (args.shared_pid_file))
        sys.exit(0)

    print('shared_pid,filename,x,y,width,height,class') # csv header
    with open(args.shared_pid_file) as f:
        pid_reader = csv.reader(f)
        for row in pid_reader:
            shared_pid = row[0]
            shared_project_str = fetch_shared_project(shared_pid)
            shared_project = json.loads(shared_project_str)
            for file_index, file in enumerate(shared_project['files']):
                for rindex, region in enumerate(file['regions']):
                    try:
                        # Check if the region has at least 4 elements
                        if len(region) < 4:
                            print(f'Skipping region with insufficient elements in file {file_index}:', region)
                            continue

                        # Check for None values
                        if None in region[:4]:
                            print(f'Skipping region with None values in file {file_index}:', region)
                            continue

                        # Check for class information
                        class_info = ''
                        if 'rdata' in file and len(file['rdata']) > rindex and 'class' in file['rdata'][rindex]:
                            class_info = file['rdata'][rindex]['class']

                        print('%s,%s,%d,%d,%d,%d,%s' % (shared_pid, file['src'], region[0], region[1], region[2], region[3], class_info))
                    except TypeError as e:
                        print(f'TypeError for file {file_index} region {rindex}: {e}')
                    except IndexError as e:
                        print(f'IndexError for file {file_index} region {rindex}: {e}')
                    except Exception as e:
                        print(f'Unexpected error for file {file_index} region {rindex}: {e}')
