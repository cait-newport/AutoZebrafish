# List Annotator (LISA) application uses JSON to store a manual annotation
# project. This python class corresponds to the JSON file data structure
# of LISA.
#
# Author : Abhishek Dutta <adutta@robots.ox.ac.uk>
# Date   : 2022-08-22

import json
import uuid
import time
from datetime import datetime

class LISA():
    """List Annotator (LISA) project, see https://gitlab.com/vgg/lisa"""
    def __init__(self, project_name=None):
        self._fid_to_findex = {}
        self._filename_to_fid = {}
        self._lisa = {}
        project_id = str(uuid.uuid4())
        now_timestamp = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z'))
        self._lisa['project'] = {
            'shared_fid':'__FILE_ID__',
            'shared_rev':'__FILE_REV_ID__',
            'shared_rev_timestamp':'__FILE_REV_TIMESTAMP__',
            'project_name':project_name,
            'project_id': project_id,
            'creator':'List Annotator - LISA (https://gitlab.com/vgg/lisa)',
            'editor':'List Annotator - LISA (https://gitlab.com/vgg/lisa)',
            'file_format_version':'0.0.3',
            'created_timestamp':now_timestamp,
        }
        self._lisa['config'] = {
            "file_src_prefix": "",
            "navigation_from": 0,
            "navigation_to": 256,
            "item_per_page": 256,
            "float_precision": 4,
            "item_height_in_pixel": 300,
            'show_attributes': { 'file':[], 'region':[] }
        }

        self._lisa['attributes'] = {}
        self._lisa['attributes']['file'] = {
            'width': {'aname':'Width', 'atype':'text'},
            'height': {'aname':'Height', 'atype':'text'},
        }

        self._lisa['attributes']['region'] = {}
        self._lisa['files'] = []

    def config(self, key, value):
        self._lisa['config'][key] = value

    def set_project_editor(self):
        self._lisa['project']['editor'] = ''

    def add_attribute(self, atype, attribute_id, attribute_def):
        if atype != 'file' and atype != 'region':
            print('attribute atype must be {file, region}')
            return
        if attribute_id in self._lisa['attributes'][atype]:
            print('attribute %s already exists' % (attribute_id))
            return
        self._lisa['attributes'][atype][attribute_id] = attribute_def
        self._lisa['config']['show_attributes'][atype].append(attribute_id)

    def add_file(self, filename, width, height):
        findex = len(self._lisa['files'])
        self._lisa['files'].append( {
            'fid':findex,
            'src':filename,
            'regions':[],
            'rdata':[],
            'fdata': {
                'width':width,
                'height':height,
            }
        })
        self._filename_to_fid[filename] = findex
        return findex

    def add_region(self, findex, region, rdata):
        rindex = len(self._lisa['files'][findex]['regions'])
        self._lisa['files'][findex]['regions'].append(region)
        self._lisa['files'][findex]['rdata'].append(rdata)
        return rindex

    def load_json(self, fn):
        with open(fn, 'r') as f:
            self._lisa = json.load(f)
            print('Loaded LISA project from %s' % (fn))

    def save_json(self, fn):
        with open(fn, 'w') as f:
            json.dump(self._lisa, f)
