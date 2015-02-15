
response.menu = [['Inventory Home', False, URL('data_inventory','default','index')],
                 ['Manage Projects', False, URL('manage_projects')],
                 ['Manage Datasets', False, URL('manage_datasets')],
                 ['Manage Accessors or Groups', False, URL('manage_accessors_or_groups')],
                 ['Set Access to a Dataset', False, URL('access_dataset')],
                 ['Documentation', False, XML(URL('static','index.html', scheme=True, host=True))]]
def access_dataset():
    form = SQLFORM.factory(
        Field('accessdataset_id',requires=IS_IN_DB(db,db.accessdataset.id,'%(name)s')),
        Field('dataset_id',requires=IS_IN_DB(db,db.dataset.id,'%(title)s')),
        Field('title','string',requires=IS_NOT_EMPTY())).process()
    
    if form.accepted:
        # get previous access for same dataset
        access = db((db.accessrequest.accessdataset_id == form.vars.accessdataset_id)&
            (db.accessrequest.dataset_id==form.vars.dataset_id)).select().first()

        db.accessrequest.insert(accessdataset_id=form.vars.accessdataset_id,
                         dataset_id=form.vars.dataset_id,
                         title=form.vars.title)

        response.flash = 'dataset accessed!'
    elif form.errors:
        response.flash = 'invalid values in form!'

    
    # now get a list of all purchases
    accessing = (db.accessor.id==db.accessrequest.accessdataset_id)&(db.dataset.id==db.accessrequest.dataset_id)
    records = SQLTABLE(db(accessing).select(),headers='fieldname:capitalize')
    return dict(form=form, records=records)
def manage_projects():
    grid = SQLFORM.smartgrid(db.project,linked_tables=['dataset', 'entity','intellectualright', 'attr','accessrequest', 
                                                      'checklist', 'error'],
                             fields = [db.project.title,db.project.id,
                                       db.dataset.shortname,
                                       db.dataset.id,
                                       db.dataset.additionalinfo,
                                       db.dataset.alternateidentifier,
                                       db.entity.entityname,
                                       db.attr.name, db.attr.definition,
                                       db.accessrequest.accessdataset_id, 
                                       db.accessrequest.dataset_id,
                                       db.accessrequest.title, 
                                       db.error.logged_by, db.error.date_logged,
                                       db.checklist.checked_by, db.checklist.check_date, 
                                       db.checklist.draft_publication_checklist_passed, db.checklist.reporting_checklist_passed, 
                                       db.intellectualright.data_owner],
                                       orderby = dict(project=db.project.id, dataset=db.dataset.title),
                             user_signature=True,maxtextlength =200)
    return dict(grid=grid)
def manage_datasets():
    grid = SQLFORM.smartgrid(db.dataset,linked_tables=['project', 'entity','intellectualright', 'attr','accessrequest', 
                                                       'checklist',  'error'],
                             fields = [db.dataset.project_id,
                                       db.dataset.title, db.dataset.ltern_id,db.dataset.tern_contract_type,
                                       db.entity.entityname,
                                       db.attr.name, db.attr.definition,
                                       db.accessrequest.accessdataset_id, db.accessrequest.dataset_id,
                                       db.accessrequest.title, 
                                       db.error.logged_by, db.error.date_logged,
                                       db.checklist.checked_by, db.checklist.check_date, 
                                       db.checklist.draft_publication_checklist_passed, db.checklist.reporting_checklist_passed, 
                                       db.intellectualright.data_owner],
                                       orderby = dict(dataset=[db.dataset.project_id,db.dataset.title]),
                             user_signature=True,maxtextlength =200)
    return dict(grid=grid)
def manage_accessors_or_groups():
    grid = SQLFORM.smartgrid(db.accessdataset,linked_tables=['accessor'],
                             fields = [
                                       db.accessdataset.name,
                                       db.accessdataset.email,
                                       db.accessor.name, db.accessor.email],
                                       orderby = dict(accessdataset=[db.accessdataset.name]),
                             user_signature=True,maxtextlength =200)

    return dict(grid=grid)
    # db.accessor.email.requires = [IS_IN_DB(db,db.accessor.id,'%(email)s')]
