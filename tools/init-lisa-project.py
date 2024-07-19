# Initialize LISA projects for annotating keyframes in fish-obstacle-avoidance project
#
# Abhishek Dutta
# 16-Nov-2021 (Updated on 12-Dec-2022)

import os
import argparse

from json import encoder
encoder.FLOAT_REPR = lambda o: format(o, '.3f') # save float with only 3 decimal places

from lisa import LISA

def is_image(filename):
    ext = filename.split('.')[-1].lower()
    if ext == 'jpg' or ext == 'jpeg' or ext == 'png':
        return True
    else:
        return False

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Initialise a LISA project based on images contained in a folder")
    parser.add_argument("--image-dir",
                      required=True,
                      type=str,
                      help="folder containing images")
    parser.add_argument("--object-name",
                      required=True,
                      type=str,
                      help="fish or obstacle_top")
    parser.add_argument("--offset",
                      required=True,
                      type=int,
                      help="to include all images, set value to 1")
    parser.add_argument("--file-src-prefix",
                      required=False,
                      type=str,
                      help="load files from this URL (e.g. http://...)")
    parser.add_argument("--outfn",
                      required=True,
                      type=str,
                      help="filename for saved LISA project")

    args = parser.parse_args()
    ## These attributes are specific for the fish-tank-obstacles projects
    ## For other projects, these can be modified by the users to suit their requirements

    object_type_aid = 'object_type'
    object_type_attribute = {
        'aname': 'Object Type',
        'atype': 'select',
        'options': {},
        'default_option_id': ''
    }

    outdir = os.path.dirname(args.outfn)
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    if args.object_name == 'fish':
        ## Export LISA project for manual annotation of fish
        lisa = LISA('training dataset for Picasso triggerfish')
        object_type_attribute['options'] = {'fish': 'Fish'}
        object_type_attribute['default_option_id'] = 'fish'
        lisa.add_attribute('region',
                           object_type_aid,
                           object_type_attribute)

        lisa_findex = 0
        for root, dirs, files in os.walk(args.image_dir):
            if len(files) == 0:
                continue
            if root == args.image_dir:
                prefix = ''
            else:
                prefix = os.path.relpath(root, args.image_dir)

            print('Processing ' + prefix)
            files_sorted = sorted(files)
            for findex in range(0, len(files_sorted), args.offset):
                filename = files_sorted[findex]
                if not is_image(filename):
                    continue
                file_relpath = os.path.join(prefix, filename)
                lisa_findex = lisa.add_file(file_relpath, -1, -1)
            if args.file_src_prefix is not None:
                lisa.config('file_src_prefix', args.file_src_prefix)
            lisa.config('navigation_to', lisa_findex)
            lisa.save_json(args.outfn)
        print('LISA projects saved to %s' % (args.outfn))
    if args.object_name == 'obstacle_top':
        lisa = LISA('training dataset for cylindrical obstacles (top part)')
        object_type_attribute['options'] = {'obstacle_top': 'Obstacle Top'}
        object_type_attribute['default_option_id'] = 'obstacle_top'
        lisa.add_attribute('region',
                           object_type_aid,
                           object_type_attribute)

        lisa_findex = 0
        for root, dirs, files in os.walk(args.image_dir):
            if len(files) == 0:
                continue
            if root == args.image_dir:
                prefix = ''
            else:
                prefix = os.path.relpath(root, args.image_dir)

            print('Processing ' + prefix)
            # for static obstacles, it is sufficient to annotation only the first frame
            files_sorted = sorted(files)
            filename = files_sorted[args.offset]
            if not is_image(filename):
                continue
            file_relpath = os.path.join(prefix, filename)
            lisa_findex = lisa.add_file(file_relpath, -1, -1)
        lisa.config('navigation_to', lisa_findex)
        if args.file_src_prefix is not None:
            lisa.config('file_src_prefix', args.file_src_prefix)
        lisa.save_json(args.outfn)
        print('LISA projects saved to %s' % (args.outfn))
