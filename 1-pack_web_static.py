#!/usr/bin/python3
"""generates a .tgz archive from the contents of the web_static folder"""
from datetime import datetime
from fabric.api import local
import os


def do_pack():
    """Archives `web_static` into a tarball, saving it in `versions`

    Returns:
        str or None: path to archive or None if archiving failed
    """
    os.makedirs('versions', exist_ok=True)
    timestmp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"web_static_{timestmp}.tgz"
    filepath = os.path.join('versions', filename)

    try:
        print(f'Packing web_static to {filepath}')
        local(f"tar -cvzf {filepath} web_static")
        tarsize = os.path.getsize(filepath)
        print(f'web_static packed: {filepath} -> {tarsize}Bytes')
        return filepath
    except Exception:
        return None
