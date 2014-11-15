
response.menu = [['Manage Projects', False, URL('manage_projects')],
                 ['Register Accessor', False, URL('register_accessor')],
                 ['Access Dataset', False, URL('access_dataset')]]

def register_accessor():
    # create an insert form from the table
    form = SQLFORM(db.accessor).process()

    # if form correct perform the insert
    if form.accepted:
        response.flash = 'new record inserted'

    # and get a list of all persons
    records = SQLTABLE(db().select(db.accessor.ALL),headers='fieldname:capitalize')

    return dict(form=form, records=records)
def access_dataset():
    form = SQLFORM.factory(
        Field('accessor_id',requires=IS_IN_DB(db,db.accessor.id,'%(email)s')),
        Field('dataset_id',requires=IS_IN_DB(db,db.dataset.id,'%(title)s')),
        Field('title','string',requires=IS_NOT_EMPTY())).process()
    
    if form.accepted:
        # get previous access for same dataset
        access = db((db.accessrequest.accessor_id == form.vars.accessor_id)&
            (db.accessrequest.dataset_id==form.vars.dataset_id)).select().first()

        db.accessrequest.insert(accessor_id=form.vars.accessor_id,
                         dataset_id=form.vars.dataset_id,
                         title=form.vars.title)

        response.flash = 'dataset accessed!'
    elif form.errors:
        response.flash = 'invalid values in form!'

    
    # now get a list of all purchases
    accessing = (db.accessor.id==db.accessrequest.accessor_id)&(db.dataset.id==db.accessrequest.dataset_id)
    records = SQLTABLE(db(accessing).select(),headers='fieldname:capitalize')
    return dict(form=form, records=records)
def manage_projects():
    grid = SQLFORM.smartgrid(db.project,linked_tables=['dataset', 'datatable', 'attributelist','accessrequest'],
                             fields = [db.project.title,
                                       db.dataset.title, db.dataset.creator,
                                       db.datatable.entityname,
                                       db.attributelist.name, db.attributelist.definition,
                                       db.accessrequest.accessor_id, db.accessrequest.dataset_id, db.accessrequest.title],
                             user_signature=False,maxtextlength =200)
    return dict(grid=grid)
