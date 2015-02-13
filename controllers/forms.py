
response.menu = [['Manage Projects', False, URL('manage_projects')],
                 ['Manage Datasets', False, URL('manage_datasets')],
                 ['Manage Access Groups', False, URL('manage_accessgroups')],
                 ['Register Accessor', False, URL('register_accessor')],
                 ['Access Dataset', False, URL('access_dataset')],
                 ['Documentation', False, XML(URL('static','index.html', scheme=True, host=True))]]
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
        Field('accessgroup_id',requires=IS_IN_DB(db,db.accessor.id,'%(name)s')),
        Field('dataset_id',requires=IS_IN_DB(db,db.dataset.id,'%(title)s')),
        Field('title','string',requires=IS_NOT_EMPTY())).process()
    
    if form.accepted:
        # get previous access for same dataset
        access = db((db.accessrequest.accessgroup_id == form.vars.accessgroup_id)&
            (db.accessrequest.dataset_id==form.vars.dataset_id)).select().first()

        db.accessrequest.insert(accessgroup_id=form.vars.accessgroup_id,
                         dataset_id=form.vars.dataset_id,
                         title=form.vars.title)

        response.flash = 'dataset accessed!'
    elif form.errors:
        response.flash = 'invalid values in form!'

    
    # now get a list of all purchases
    accessing = (db.accessor.id==db.accessrequest.accessgroup_id)&(db.dataset.id==db.accessrequest.dataset_id)
    records = SQLTABLE(db(accessing).select(),headers='fieldname:capitalize')
    return dict(form=form, records=records)
def manage_projects():
    grid = SQLFORM.smartgrid(db.project,linked_tables=['dataset', 'entity','deed', 'attribute','accessrequest', 
                                                      'checklist', 'error'],
                             fields = [db.project.title,db.project.id,
                                       db.dataset.title, db.dataset.ltern_id,db.dataset.tern_contract_type,
                                       db.entity.entityname,
                                       db.attribute.name, db.attribute.definition,
                                       db.accessrequest.accessgroup_id, db.accessrequest.dataset_id,
                                       db.accessrequest.title, 
                                       db.error.logged_by, db.error.date_logged,
                                       db.checklist.checked_by, db.checklist.check_date, 
                                       db.checklist.draft_publication_checklist_passed, db.checklist.reporting_checklist_passed, 
                                       db.deed.data_owner],
                                       orderby = dict(project=db.project.id, dataset=db.dataset.title),
                             user_signature=True,maxtextlength =200)
    return dict(grid=grid)
def manage_datasets():
    grid = SQLFORM.smartgrid(db.dataset,linked_tables=['project', 'entity','deed', 'attribute','accessrequest', 
                                                       'checklist',  'error'],
                             fields = [db.dataset.project_id,
                                       db.dataset.title, db.dataset.ltern_id,db.dataset.tern_contract_type,
                                       db.entity.entityname,
                                       db.attribute.name, db.attribute.definition,
                                       db.accessrequest.accessgroup_id, db.accessrequest.dataset_id,
                                       db.accessrequest.title, 
                                       db.error.logged_by, db.error.date_logged,
                                       db.checklist.checked_by, db.checklist.check_date, 
                                       db.checklist.draft_publication_checklist_passed, db.checklist.reporting_checklist_passed, 
                                       db.deed.data_owner],
                                       orderby = dict(dataset=[db.dataset.project_id,db.dataset.title]),
                             user_signature=True,maxtextlength =200)
    return dict(grid=grid)
def manage_accessgroups():
    grid = SQLFORM.smartgrid(db.accessgroup,linked_tables=['accessor'],
                             fields = [
                                       db.accessgroup.name,
                                       db.accessgroup.email,
                                       db.accessor.name, db.accessor.email],
                                       orderby = dict(accessgroup=[db.accessgroup.name]),
                             user_signature=True,maxtextlength =200)

    return dict(grid=grid)
    # db.accessor.email.requires = [IS_IN_DB(db,db.accessor.id,'%(email)s')]
