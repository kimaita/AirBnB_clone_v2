#!/usr/bin/python3
"""Compresses and distributes a static website to web servers
and does some cleanup"""
from datetime import datetime
from fabric.api import local, env, put, run, runs_once
import os

env.hosts = ['52.207.207.213', '54.242.186.218']
env.user = 'ubuntu'

RELEASES = '/data/web_static/releases'
VERSIONS = 'versions'


@runs_once
def do_pack():
    """Archives `web_static` into a tarball, saving it in `versions`

    Returns:
        str or None: path to archive or None if archiving failed
    """
    os.makedirs(VERSIONS, exist_ok=True)
    timestmp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"web_static_{timestmp}.tgz"
    filepath = os.path.join(VERSIONS, filename)

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
    file = archive_name.rsplit('.', maxsplit=1)[0]
    save_path = os.path.join(RELEASES, file, '')

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
    """_summary_
    """
    archive_path = do_pack()
    if archive_path is None:
        return False

    return do_deploy(archive_path)


@runs_once
def clean_local(cmd):
    local(cmd)


def clean_remote(cmd):
    run(cmd)


def do_clean(number=0):
    """Deletes out-of-date archives, retaining `number` most-recent versions.

    0 or 1 keeps only the most recent version.
    Args:
        number (int, optional): Number of files to keep. Defaults to 0.
    """
    number = int(number) or 1
    cmd = "cd {0} && ls | sort | head -n -{1} | xargs -r rm"
    clean_local(cmd.format(VERSIONS, number))
    clean_remote(cmd.format(RELEASES, number))
