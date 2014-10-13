
# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Welcome to web2py!")
    return dict(message=T('Hello World'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())

def entry_datasets():
    """returns a form where the can entry a post"""
    form = crud.create(db.data_inventory)
    return dict(form=form)

#def search_dogs():
#    form, records = crud.search(db.datainventory)
#    return dict(form=form, records=records)

def search_dogs():
    return dict(form=SQLFORM.grid(db.data_inventory, user_signature=False, maxtextlength =200,
                                  fields = [db.data_inventory.id, db.data_inventory.plot_network_study_name, db.data_inventory.pn_group, db.data_inventory.data_type, db.data_inventory.eda_status_date]))


def search_datasets():
    return dict(form=SQLFORM.grid(db.dataset.id==db.data_inventory.id2, user_signature=False, maxtextlength =200,
                                  fields = [db.dataset.id, db.dataset.plot_network_study_name, db.dataset.pn_code, db.dataset.dataset, db.dataset.tern_type, db.data_inventory.notes_issues]))



def manage_projects():
    grid = SQLFORM.smartgrid(db.project,linked_tables=['dataset', 'attribute'],
                             user_signature=False)
    return dict(grid=grid)
