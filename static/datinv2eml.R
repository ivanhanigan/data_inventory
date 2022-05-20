if(!require(EML)) {install.packages("EML"); library(EML)}
if(!require(cardatdbtools)) {remotes::install_github("cardat/cardatdbtools"); library(cardatdbtools)}
if(!require(data.table)) {install.packages("data.table"); library(data.table)}
if(!require(RSQLite)) {install.packages("RSQLite")}; library(RSQLite)
connect2pg <- FALSE
if(connect2pg){
db <- "data_inventory_car"
username <- "ivan_hanigan"
hostip <- "swish4.tern.org.au"
pwd <- getPassword()
ch <- connect2postgres(db = db, 
                       user = username, 
                       hostip = hostip,
                       p = pwd)
} else {
  
  sqlite <- dbDriver("SQLite")
  ch <- dbConnect(sqlite,"databases/storage.sqlite")
  
}

######################################################################################################S
datinv2eml <- function(
    ch = ch
    , 
    proj_name = "Biomass_Smoke_Validated_Events" 
    ,
    dset_shortname = "Biomass_Smoke_Validated_Events"
    ,
    entity_name = "storage.sqlite"
    
){
  ls_projs <- dbGetQuery(ch, "select title from project")
  ##ls_projs
  # retrieve project metadata
  meta_proj <- as.data.table(
    dbGetQuery(ch, sprintf(
      "select * from project 
    where title = '%s' ", proj_name))
  )
  
  ##meta_proj  

  
  # retrieve datasets metadata
  meta_dataset <- as.data.table(
    dbGetQuery(ch, sprintf(
      "select dataset.* 
      from dataset
      join project on 
      dataset.project_id = project.id
      where project.title = '%s' ", proj_name))
  )
  ##meta_dataset[,1:5]
  meta_dataset <- meta_dataset[shortname == dset_shortname,]
  ##meta_dataset$geographicdescription
  bbox1 <- strsplit(meta_dataset$boundingcoordinates,split = ",")
  bbox <- lapply(bbox1, strsplit, " = ")
  coverage <- set_coverage(geographicDescription = meta_dataset$geographicdescription,
                           north = unlist(bbox[[1]][1])[2], south = unlist(bbox[[1]][2])[2],
                           east = unlist(bbox[[1]][3])[2], west = unlist(bbox[[1]][4])[2])
  
  meta_rights <- as.data.table(
    dbGetQuery(ch, sprintf(
      "select intellectualright.* from intellectualright
    join dataset on intellectualright.dataset_id = dataset.id
    where dataset.id IN (%s) ", 
      meta_dataset$id
    ))
  )
  #meta_rights
  
  #### start metadata ####
  creator_dat <- strsplit(meta_dataset$creator," ")
  creator_info <- eml$creator(
    individualName = eml$individualName(
      givenName = creator_dat[[1]][1], 
      surName = creator_dat[[1]][2]),
    userId = eml$userId("ORCID")
  )
  
  orcid <- dbGetQuery(ch, paste0("select * from orcid where name_per_creator_tbl = '",creator_dat[[1]][1]," ",creator_dat[[1]][2],"'"))
  ##orcid
  creator_info$userId[[2]] <- paste0("https://orcid.org/", orcid$orcid)
  #creator_info
  
  contact_info <- eml$contact(positionName = meta_dataset$contact,
                              electronicMailAddress = meta_dataset$contact_email)
  #contact_info
  
  entity <- dbGetQuery(ch, paste0("select * from entity where dataset_id = ", meta_dataset$id))
  entity <- entity[entity$entityname == entity_name,]
  #t(entity)
  
  attributes <- dbGetQuery(
    ch,
    paste0(
      'select
variable_name as "attributeName",
variable_definition as "attributeDefinition"
from attr where entity_id = ',
      entity$id
    )
  )
  
  if(nrow(attributes) > 0){ 
  attributes$measurementScale <- "nominal"
  attributes$domain <- "textDomain"
  attributeList <-  set_attributes(attributes)
  my_eml <- eml$eml(
    packageId = uuid::UUIDgenerate(),  
    system = "uuid",
    dataset = eml$dataset(
      id = as.character(meta_dataset$id),
      shortName = meta_dataset$shortname,
      title = meta_dataset$title,
      creator = creator_info,
      contact = contact_info,
      pubDate = meta_dataset$pubdate,
      abstract = meta_dataset$abstract,
      coverage = coverage,
      intellectualRights = meta_rights$special_conditions,
      publisher = list(organizationName = meta_dataset$publisher),
      dataTable = eml$dataTable(
        entityName = entity$entityname,
        entityDescription = entity$entitydescription,
        attributeList = attributeList                                         
      )
      ,
      project = eml$project(id = as.character(meta_proj$id),
                            title = meta_proj$title,
                            personnel = eml$personnel(
                              individualName = list(givenName = strsplit(meta_proj$personnel_data_owner," ")[[1]][1]
                                                    ,
                                                    surName = strsplit(meta_proj$personnel_data_owner," ")[[1]][2]
                              ),
                              organizationName = "Curtin University",
                              role = "principalInvestigator"),
                            
                            abstract = meta_proj$project_abstract,
                            funding = meta_proj$funding
      )
      
    ),
    additionalMetadata = eml$additionalMetadata(metadata = list(unitList = meta_dataset$additional_metadata))
  )
  } else {
    my_eml <- eml$eml(
      packageId = uuid::UUIDgenerate(),  
      system = "uuid",
      dataset = eml$dataset(
        id = as.character(meta_dataset$id),
        shortName = meta_dataset$shortname,
        title = meta_dataset$title,
        creator = creator_info,
        contact = contact_info,
        pubDate = meta_dataset$pubdate,
        abstract = meta_dataset$abstract,
        coverage = coverage,
        intellectualRights = meta_rights$special_conditions,
        publisher = list(organizationName = meta_dataset$publisher)
        
        ,
        project = eml$project(id = as.character(meta_proj$id),
                              title = meta_proj$title,
                              personnel = eml$personnel(
                                individualName = list(givenName = strsplit(meta_proj$personnel_data_owner," ")[[1]][1]
                                                      ,
                                                      surName = strsplit(meta_proj$personnel_data_owner," ")[[1]][2]
                                ),
                                organizationName = "Curtin University",
                                role = "principalInvestigator"),
                              
                              abstract = meta_proj$project_abstract,
                              funding = meta_proj$funding
        )
        
      ),
      additionalMetadata = eml$additionalMetadata(metadata = list(unitList = meta_dataset$additional_metadata))
    )
  }
  emld::eml_version("eml-2.1.1")
  return(my_eml)
}

#########################################################################################3
my_eml <- datinv2eml(
    ch = ch
    , 
    proj_name = "Biomass_Smoke_Validated_Events" 
    ,
    dset_shortname = "Biomass_Smoke_Validated_Events"
    ,
    entity_name = "storage.sqlite")

my_eml

dir()
file_output <- paste0("foo",".xml")
write_eml(my_eml, file_output)

##dbDisconnect(ch)

eml_record <- as_emld(file_output)
cat(eml_record$dataset$coverage$geographicCoverage$geographicDescription)
eml_record$dataset$dataTable$attributeList

eml_record$dataset$dataTable$attributeList[[1]]$attributeName
eml_record$dataset$dataTable$attributeList[[1]]$attributeDefinition
