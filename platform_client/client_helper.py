# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import base64
from .utils import get_images_from_folder


def sync_import_image(image_path, repoid, client):
    with open(image_path, 'rb') as f:
        picture_base64 = base64.b64encode(f.read())

        return client.sync_import_image(
            repository_id=repoid,
            picture_image_content_base64=picture_base64
        )


def async_import_image(image_path, repoid, client):
    with open(image_path, 'rb') as f:
        picture_base64 = base64.b64decode(f.read())

        return client.async_import_image(
            repository_id=repoid,
            picture_image_content_base64=picture_base64
        )


def sync_import_folder(folder_path, repoid, client):
    for f in get_images_from_folder(folder_path):
        sync_import_image(f, repoid, client)


def async_import_folder(folder_path, repoid, client):
    for f in get_images_from_folder(folder_path):
        async_import_image(f, repoid, client)
