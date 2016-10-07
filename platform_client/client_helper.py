# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import base64


def sync_import_image(image_path, repoid, client):
    with open(image_path, 'rb') as f:
        picture_base64 = base64.b64encode(f.read())

        return client.sync_import_image(
            repository_id=repoid,
            picture_image_content_base64=picture_base64
        )


def sync_import_folder(folder_path, repoid, client):
    pass
