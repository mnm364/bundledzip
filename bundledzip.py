import argparse
import binpacking
import datetime
import os
import subprocess
import time
import zipfile

from datetime import datetime

GIGABYTE_MULTIPLIER = 1E9

# Setup the command line interface.
parser = argparse.ArgumentParser(description='Compresses a set of files into a set of bundles of restricted size')
parser.add_argument('-d', '--directory', required=True, help='The input directory that contains the files to bundle')
parser.add_argument('-o', '--output', required=True, help='The directory to write the bundles; created if it does not exist')
parser.add_argument('-e', '--extension', default='pdf', help='The extension of files to zip')
parser.add_argument('-n', '--bundle-name', required=True, help='The name to give the bundled files')
parser.add_argument('-s', '--bundle-size', type=int, required=True, help='The max size a bundle can be in Gigabytes (Gb)')
args = parser.parse_args()

# Load variables from the command line.
directory = args.directory
output = args.output
extension = args.extension
bundlename = args.bundle_name
bundlesize = args.bundle_size

# Timestamp of this run as a Unix epoch.
seconds = time.time()

# Aggregate a mapping from filename to file size.
filesizes = {}
for entry in os.scandir(directory):
    filename = entry.name

    if not entry.is_file:
        continue
    if not filename.endswith('.' + extension):
        continue

    filesize = entry.stat().st_size
    filesizes[filename] = filesize

# Find an efficient packing of files into bundles of the requested size.
bundles = binpacking.to_constant_volume(filesizes, bundlesize * GIGABYTE_MULTIPLIER)

# Create the output directory if it does not exist
if not os.path.exists(output):
    os.mkdir(output)

# Make and write zip to file
for index, bundle in enumerate(bundles):
    unique = datetime.fromtimestamp(seconds + index).strftime('%Y%m%d%H%M%S') 
    with zipfile.ZipFile(f'{output}/{bundlename}-{unique}.zip', 'w') as z:
        for filename in bundle.keys():
            z.write(f'{directory}/{filename}')

