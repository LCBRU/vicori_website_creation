#!/usr/bin/env python3

import wget
import shutil
import zipfile
import tempfile
import os
import subprocess
from pathlib import Path


WWW_DIR='/local/www/'
HTTP_DIR=os.path.join(WWW_DIR, 'htdocs')


def get_automad():
    pwd = os.path.realpath('.')

    with tempfile.TemporaryDirectory() as tmpdirname:
        os.chdir(tmpdirname)

        automad_zip = wget.download('https://automad.org/download', bar=None)

        with zipfile.ZipFile(automad_zip,"r") as zip_ref:
            zip_ref.extractall(tmpdirname)

        extracted_dir = next(x for x in Path(tmpdirname).iterdir() if x.is_dir())

        os.unlink(os.path.join(HTTP_DIR, 'cache'))
        os.unlink(os.path.join(HTTP_DIR, 'pages'))
        os.unlink(os.path.join(HTTP_DIR, 'config'))
        shutil.rmtree(HTTP_DIR)
        shutil.copytree(extracted_dir.name, HTTP_DIR)

    shutil.rmtree(os.path.join(HTTP_DIR, 'cache'))
    shutil.rmtree(os.path.join(HTTP_DIR, 'pages'))
    shutil.rmtree(os.path.join(HTTP_DIR, 'config'))
    shutil.rmtree(os.path.join(HTTP_DIR, 'shared'))

    os.symlink(os.path.join(WWW_DIR, 'cache'), os.path.join(HTTP_DIR, 'cache'))
    os.symlink(os.path.join(WWW_DIR, 'pages'), os.path.join(HTTP_DIR, 'pages'))
    os.symlink(os.path.join(WWW_DIR, 'config'), os.path.join(HTTP_DIR, 'config'))
    os.symlink(os.path.join(WWW_DIR, 'shared'), os.path.join(HTTP_DIR, 'shared'))

    shutil.rmtree(os.path.join(HTTP_DIR, 'packages'))
    os.mkdir(os.path.join(HTTP_DIR, 'packages'))

    with tempfile.TemporaryDirectory() as tmpdirname:
        os.chdir(tmpdirname)

        theme_zip = wget.download('https://github.com/LCBRU/vicori_theme/archive/master.zip', bar=None)

        with zipfile.ZipFile(theme_zip,"r") as zip_ref:
            zip_ref.extractall(tmpdirname)

        extracted_dir = next(x for x in Path(tmpdirname).iterdir() if x.is_dir())
        shutil.copytree(extracted_dir.name, os.path.join(HTTP_DIR, 'packages/vicori_theme'))


get_automad()