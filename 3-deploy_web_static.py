#!/usr/bin/python3
"""Compresses and distributes a static website to web servers"""
from datetime import datetime
from fabric.api import local, env, put, run, runs_once
import os

env.hosts = ['54.242.186.218', '52.207.207.213']
env.user = 'ubuntu'


@runs_once
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


def upload(file):
    """Uploads a file to the web servers

    Args:
        file (str): path to the archive file
    """
    try:
        put(file, '/tmp')
        return True
    except Exception:
        return False


def decompress(archive_name):
    """Decompresses an archive saved in `/tmp` to `releases`
    and then deletes the archive

    Args:
        file (str): archive name
        save_path (str): location to decompress to

    Returns:
        bool: False if any step fails, True otherwise
    """
    current = '/data/web_static/current'
    releases = '/data/web_static/releases'
    file = archive_name.rsplit('.', maxsplit=1)[0]
    save_path = os.path.join(releases, file, '')

    try:
        run(f"mkdir -p {save_path}")
        run(f"tar -xzf /tmp/{archive_name} -C {save_path}")
        run(f"rm /tmp/{archive_name}")
        run(f"mv {save_path}/web_static/* {save_path}")
        run(f"rm -rf {save_path}/web_static")
        run(f"rm -rf {current}")
        run(f"ln -s {save_path} {current}")
        return True
    except Exception:
        return False


def do_deploy(archive_path):
    """Distributes an archive to the web servers
    and updates the `current` link

    Args:
        archive_path (str): path to archive file to upload

    Returns:
        bool: True if all steps execute correctly, False otherwise
    """
    if not os.path.isfile(archive_path):
        return False

    if not upload(archive_path):
        return False

    filename = archive_path.rsplit('/', maxsplit=1)[1]
    if not decompress(filename):
        return False

    print("New version deployed!")
    return True


def deploy():
    """Compresses, uploads and extracts static website content"""
    archive_path = do_pack()
    if archive_path is None:
        return False

    return do_deploy(archive_path)
