"""
This file defines the database models
"""

from .common import db, Field
from py4web import action, URL
from pydal.validators import *
from .import settings

### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later
db.define_table('cat', Field('name', required=True), Field('image','upload'))
db.cat.image.upload_path = settings.UPLOAD_FOLDER
db.cat.image.download_url = lambda filename: URL('download/%s' % filename)
db.commit()
#
