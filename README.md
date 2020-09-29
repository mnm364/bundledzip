# Bundled Zip

`bundledzip` is a simple script to zip many files into many zips of some specified size. Size can be defined by space or count, e.g, 3MB zips or zips with 10 files each.

## Installation

1. Install Python - [https://www.python.org/downloads/](https://www.python.org/downloads/)

    This script should work with any Python version 3.6 or higher.
    For posterity, this script was tested/developed on Python 3.8.6.

2. Install dependencies

We will also need [PIP](https://pypi.org/project/pip/) to install dependencies. You can follow tutorials to do so on: [MacOS/Linux](https://www.tecmint.com/install-pip-in-linux/) or [Windows](https://phoenixnap.com/kb/install-pip-windows). Then run the following within the `bundledzip` directory:

```
pip install -r requirements.txt
```

## Usage

Help can be found by running 

```
python bundledzip.py --help
```

For convenience, we paste the output here:

```
usage: bundledzip.py [-h] -d DIRECTORY -o OUTPUT [-e EXTENSION] -n BUNDLE_NAME -s BUNDLE_SIZE [-u {GB,MB,KB,None}]

Compresses a set of files into a set of bundles of some specified size.

optional arguments:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        The input directory that contains the files to bundle
  -o OUTPUT, --output OUTPUT
                        The directory to write the bundles; created if it does not exist
  -e EXTENSION, --extension EXTENSION
                        The extension of files to zip; unspecified will zip all files
  -n BUNDLE_NAME, --bundle-name BUNDLE_NAME
                        The name to give the bundled files
  -s BUNDLE_SIZE, --bundle-size BUNDLE_SIZE
                        The size of a bundle, whose unit is given by --bundle-unit
  -u {GB,MB,KB,None}, --bundle-unit {GB,MB,KB,None}
                        The unit of the bundle size. "None" will simply treat size as count, which is the default
```

## Example

This project contains an example in `example/`. In this example, we have a folder called `example/unbundled` that has a few uncompressed files. Using the below command, a directory is created called `example/bundled`, which will contain 3 zip files that each contain 2 `*.txt` documents.

```
python bundledzip.py -d example/unbundled -o example/bundled -e txt -n lorem -s 2
```

Another example may be to compress a directory containing 50GBs of files to send to a client, say Jack in the Box. However, there is a 100MB limit imposed on the size of zips sent - say over some FTP. For this scenario, a contrived `bundledzip` that may solve this problem may be:

```
python bundledzip.py -d manysmallfiles/ -o fewerlargezips/ -n jackinthebox -s 100 -u MB
```

This will roughly create 500 zip files under the `fewerlargezips` directory each of size close to 100MB. These zip files can then be sent to the client by whatever means is most convenient for you.
