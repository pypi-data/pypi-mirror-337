#!/usr/local/bin/python3.7

import hashlib, sys

filename = "dist/PyIRCIoT-0.0.233.tar.gz"
with open(filename, "rb") as f:
    file_data = f.read()
blake2_hash = hashlib.blake2b(file_data, digest_size=32).hexdigest()
print("BLAKE2-256-Digest: {}".format(blake2_hash))

sys.exit(0)

