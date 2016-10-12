# -*- coding: utf-8 -*-
"""
Python client utils
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


IMAGE_TYPES = ['jpg', 'bmp', 'png']
FILE_SEPERATOR = '/'


def is_image(file_path):
    """return true if is image, false if not"""
    return (file_path.split('.')[-1] in IMAGE_TYPES)


def get_images_from_folder(folder):
    """return image file names from a folder"""
    from os import walk
    from shutil import abspath

    for (dirpath, dirnames, filenames) in walk(folder):
        for f in filenames:
            file_path = abspath(dirpath + FILE_SEPERATOR + f)
            if is_image(file_path):
                yield file_path
