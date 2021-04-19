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


from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web import request, redirect, URL, Field, HTTP,action
from py4web.utils.form import Form, FormStyleBootstrap4
from . import settings
import os
from PIL import Image



@action("profiledetails/<pid>", method=['POST', 'GET'])
@action.uses(auth.user,session, db,  'profiledetails.html')
def profiledatails(pid=None):
    row = db(db.auth_user.id==pid).select(db.auth_user.ALL, db.profile.ALL,left=db.profile.on(db.auth_user.id == db.profile.user)).first()
    return dict(row=row)

@action("index", method=['POST', 'GET'])
@action.uses(auth.user,session, db,  'index.html')
def index():
    #rows = db(db.auth_user).select()
    #images=db(db.profile).select()
    rows = db().select(db.auth_user.ALL, db.profile.ALL,left=db.profile.on(db.auth_user.id == db.profile.user))
    return dict(rows=rows)
    
    
@action("profile", method=['POST', 'GET'])
@action.uses(auth.user,session, db,  'profile.html')
def profile():
    db.auth_user.username.readable = True
    db.auth_user.username.writable = False
    db.auth_user.avgrating.readable = False
    db.auth_user.avgrating.writable = False
    db.auth_user.location.readable = True
    db.auth_user.location.writable = True
    db.auth_user.portfolio.readable = True
    db.auth_user.portfolio.writable = True
    db.auth_user.id.readable = True
    db.auth_user.id.writable = False
    user = auth.get_user()
    profile = db.auth_user(auth.user_id).profile.select().first()
    username= db(db.auth_user==auth.user_id).select(db.auth_user.username).first()
    username_form=username.username

    icon = f"images/{profile.image}"
    # Append the user profile icon to the dict so it prepopulates it with current data
    user.update({"image": profile.image})

    # Get all the required fields out of the 2 tables to display them: Username, Email, First/Last name, and Profile Pic
    form_list = [field for field in db.auth_user if not field.type == "id" ] + [field for field in db.profile if not field.type == "id"]
    aform = Form(
        form_list,
        record=user,
        noncreate=True,
        csrf_session=session,
        deletable=False,
        hidden={"username":username_form},
        formstyle=FormStyleBootstrap4,
    )
    if aform.accepted:
        # Update the auth user
        db.auth_user[user["id"]].update_record(
            location=aform.vars["location"],
            portfolio=aform.vars["portfolio"],
            email=aform.vars["email"],
            first_name=aform.vars["first_name"],
            last_name=aform.vars["last_name"],
        )

        # The icon we want to update our profile will always have a default of default.jpg
        update_icon = "default.jpg"

        if not aform.vars["image"] and profile.image == update_icon:
            # We can't delete the default image so we just redirect back to the page.
            redirect(URL("profile"))

        if aform.vars["image"]:
            print (aform.vars["image"])
            # If we are setting it equal to a new icon, we set icon to that file name
            update_icon = aform.vars["image"]
        
        #if update_icon != profile.image:
            # If the new icon (which can be default.jpg) isn't the same icon as before, remove the old one and update
         #   if profile.image != "default.jpg":
            #cleanup_image(profile.image)
            #resize_image(update_icon)
            profile.update_record(image=update_icon)

        # Once done with everything (Or after doing nothing because the icons are the same), return to the profile page
        redirect(URL("profile"))
    return dict(icon=icon,form=aform)

def resize_image(image_path):
    total_path = os.path.join(settings.UPLOAD_FOLDER, image_path)

    img = Image.open(total_path)
    if img.height > 300 or img.width > 300:
        output_size = (300, 300)
        img.thumbnail(output_size)
        img.save(total_path)


def cleanup_image(image_path):
    total_path = os.path.join(settings.UPLOAD_FOLDER, image_path)
    os.remove(total_path, dir_fd=None)