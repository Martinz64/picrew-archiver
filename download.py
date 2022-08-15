import os
import re
from sys import argv

import requests

pattern = re.compile("DL: \[(.*)\] -> \[(.*)\]")


def download(url: str, dest_folder: str):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist

    # be careful with file names
    filename = url.split('/')[-1].replace(" ", "_")
    file_path = os.path.join(dest_folder, filename)

    if os.path.exists(file_path):
        print("already saved", file_path)
        return

    r = requests.get(url, stream=True)
    if r.ok:
        print("saving to", os.path.abspath(file_path))
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))


with open(argv[1], "r", encoding="utf-8") as f: # To avoid encoding error, this happens when OS is not using utf-8
    data = f.readlines()
    for line in data:
        matches = pattern.findall(line)
        for match in matches:
            download(match[0], dest_folder=match[1])
