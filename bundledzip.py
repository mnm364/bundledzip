import argparse
import binpacking
import os
import time
import zipfile

from datetime import datetime
from tqdm import tqdm

# The units that can be given to describe the size of a bundle
UNITS = {'GB': 1e9, 'MB': 1e6, 'KB': 1e3, None: 1}

# Setup the command line interface.
parser = argparse.ArgumentParser(description='Compresses a set of files into a set of bundles of some specified size.')
parser.add_argument('-d', '--directory', required=True, help='The input directory that contains the files to bundle')
parser.add_argument('-o', '--output', required=True, help='The directory to write the bundles; created if it does not exist')
parser.add_argument('-e', '--extension', help='The extension of files to zip; unspecified will zip all files')
parser.add_argument('-n', '--bundle-name', required=True, help='The name to give the bundled files')
parser.add_argument('-s', '--bundle-size', type=int, required=True, help='The size of a bundle, whose unit is given by --bundle-unit')
parser.add_argument('-u', '--bundle-unit', type=str, choices=UNITS.keys(), default=None, help='The unit of the bundle size. "None" will simply treat size as count, which is the default')
args = parser.parse_args()

# Load variables from the command line.
directory = args.directory
output = args.output
extension = args.extension
bundlename = args.bundle_name
bundlesize = args.bundle_size
bundleunit = args.bundle_unit

# Timestamp of this run as a Unix epoch.
seconds = time.time()

# Aggregate a mapping from filename to file size.
filesizes = {}
for entry in os.scandir(directory):
    filename = entry.name

    if not entry.is_file:
        continue
    if extension and not filename.endswith('.' + extension):
        continue

    filesize = entry.stat().st_size if bundleunit else 1
    filesizes[filename] = filesize

# Find an efficient packing of files into bundles of the requested size.
multiplier = UNITS[bundleunit]
bundles = binpacking.to_constant_volume(filesizes, bundlesize * multiplier)

# Create the output directory if it does not exist
if not os.path.exists(output):
    os.mkdir(output)

# Make and write zip to file
for index, bundle in enumerate(tqdm(bundles)):
    unique = datetime.fromtimestamp(seconds + index).strftime('%Y%m%d%H%M%S') 
    with zipfile.ZipFile(f'{output}/{bundlename}-{unique}.zip', 'w') as z:
        for filename in bundle.keys():
            filepath = os.path.join(directory, filename)
            z.write(os.path.abspath(filepath), filename)
