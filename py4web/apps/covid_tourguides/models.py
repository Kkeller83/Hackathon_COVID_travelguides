"""
This file defines the database models
"""

from .common import db, Field, Auth
from py4web import URL
from pydal.validators import IS_NOT_EMPTY
import datetime
from . import settings

### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later


def get_time():
    return datetime.datetime.utcnow()


def get_download_url(picture):
    return f"images/{picture}"


def get_user():
    return auth.current_user.get("id") if auth.current_user else None


db.define_table(
    "profile",
    Field("user", "reference auth_user", readable=False, writable=False),
    Field(
        "image",
        "upload",
        default="default.jpg",
        uploadfolder=settings.UPLOAD_FOLDER,
        download_url=get_download_url, label="Profile Picture",
    )
)

db.profile.id.readable = False
db.profile.id.writable = False


#
db.commit()
#
