"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""




from py4web import action, URL
from py4web.utils.grid import Grid
from py4web.utils.form import Form, FormStyleBootstrap4
from .common import *
from PIL import Image



@unauthenticated()
def index():
    form = Form(db.cat,"1")
    cat=db(db.cat.id=="1").select(db.cat.image).first()
    icon = f"/cats/download/{cat.image}"
    db.cat.image.download_url
    return dict(icon=icon,form=form)