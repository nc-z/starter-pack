"""Zip the built pack and create thread posts."""
# TODO:  calculate, save, and post checksums and timestamp.

import os
import shutil
import zipfile

import yaml

from . import paths


def zip_pack():
    """Compress the build dir to a zipped pack."""
    if not os.path.isdir(paths.dist()):
        os.makedirs(paths.dist())
    with zipfile.ZipFile(paths.zipped(), 'w', zipfile.ZIP_DEFLATED) as zf:
        for dirname, _, files in os.walk(paths.build()):
            zf.write(dirname, os.path.relpath(dirname, paths.build()))
            for filename in files:
                fname = os.path.join(dirname, filename)
                zf.write(fname, os.path.relpath(fname, paths.build()))


def release_docs():
    """Document the file checksum and create a forum post."""
    shutil.copy(paths.lnp('about', 'contents.txt'), paths.dist())
    with open(paths.lnp('about', 'changelog.txt')) as f:
        dffd_id = yaml.load(paths.base('PyLNP-json.yml'))['updates']['dffdID']
        changes = f.read().split('\n\n')[0]
        s = ('The Starter Pack has updated to {}!  As usual, [url=http://dffd'
             '.bay12games.com/file.php?id={}]you can get it here.[/url]\n\n'
             '\n\n{}').format(paths.PACK_VERSION, dffd_id, changes)
    with open(paths.dist('forum_post.txt'), 'w') as f:
        f.write(s)


def make():
    """Make the dist folder."""
    print('\nCompressing pack...')
    zip_pack()
    release_docs()
    print('Pack zipped in ./dist/ and ready to inspect.')
