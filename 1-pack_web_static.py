#!/usr/bin/python3
"""generates a .tgz archive from the contents of the web_static folder"""
from datetime import datetime
from fabric.api import local
import os


def get_timestamp():
    """Returns the current datetime as a formatted string

    Returns:
        str: current datetime as YYYYMMDDHHMMSS
    """
    return datetime.now().strftime('%Y%m%d%H%M%S')


def do_pack():
    """Archives `web_static` into a tarball, saving it in `versions`


    Returns:
        str or None: path to archive or None if archiving failed
    """
    os.makedirs('versions', exist_ok=True)
    filename = f"web_static_{get_timestamp()}.tgz"
    filepath = os.path.join('versions', filename)

    res = local(f"tar -cvzf {filepath} web_static")
    if res.succeeded:
        tarsize = os.path.getsize(filepath)
        print(f'web_static packed: {filepath} -> {tarsize}Bytes')
        return filepath

    return None
