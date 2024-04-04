#!/usr/bin/python3
"""Distributes an archive to web servers"""
from fabric.api import env, put, run
import os

env.hosts = ['54.208.71.151', '100.25.34.99']
env.user = 'ubuntu'


def upload(file):
    """Uploads a file to the web servers

    Args:
        file (str): path to the archive file

    """
    return put(file, '/tmp')


def decompress_path(file):
    """Returns the extraction path for an archive.
    This path will be:
    `/data/web_static/releases/<archive filename without extension>`

    Args:
        file (_type_): archive name
    """
    releases = '/data/web_static/releases'
    basename = os.path.basename(file)
    filename = os.path.splitext(basename)[0]
    return os.path.join(releases, filename, '')


def decompress(file_path, save_path):
    """Decompresses an archive saved in `/tmp` to releases
    and then deletes the archive

    Args:
        file (str): archive name
        save_path (str): location to decompress to

    Returns:
        bool: False if any step fails, True otherwise
    """

    if run(f"mkdir -p {save_path}").failed:
        return False
    if run(f"tar -xzf {file_path} -C {save_path}").failed:
        return False

    static = os.path.join(save_path, 'web_static')
    if run(f"mv {static}/* {save_path}").failed:
        return False
    if run(f"rm -rf {file_path} {static}").failed:
        return False
    return True


def update_link(target):
    """Creates a new symbolic link, linked to the extracted code

    Args:
        target (str): path to extracted code in `releases`
    """
    current = '/data/web_static/current'

    if run(f"rm -rf {current}").failed:
        return False
    return run(f"ln -s {target} {current}")


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

    upload_res = upload(archive_path)
    if upload_res.failed:
        return False

    save_path = decompress_path(archive_path)
    upload_path = upload_res[0]

    if not decompress(upload_path, save_path):
        return False

    if update_link(save_path).failed:
        return False

    print("New version deployed!")
    return True
