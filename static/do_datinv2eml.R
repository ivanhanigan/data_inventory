# do_datinv2EML
if(!require(EML)) {install.packages("EML"); library(EML)}
if(!require(cardatdbtools)) {remotes::install_github("cardat/cardatdbtools"); library(cardatdbtools)}
if(!require(data.table)) {install.packages("data.table"); library(data.table)}
if(!require(RSQLite)) {install.packages("RSQLite")}; library(RSQLite)

source("static/R/datinv2eml.R")

connect2pg <- T#FALSE
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

## do
my_eml <- datinv2eml(
  ch = ch
  , 
  proj_name = "AWAP_GRIDS" #Biomass_Smoke_Validated_Events" 
  ,
  dset_shortname = "AWAP_GRIDS_1900_2015" #"Biomass_Smoke_Validated_Events"
  ,
  entity_name = "GTif_{variable}_{daterange}.tif" #"storage.sqlite"
  ,
  show_data_table = T
  ,
  datinv_source = "datinv"
  )

my_eml

dir()

file_output <- paste0("static/AWAP_GRIDS_1900_2015",".xml")

write_eml(my_eml, file_output)
eml_validate(file_output)
##dbDisconnect(ch)

eml_record <- as_emld(file_output)
cat(eml_record$dataset$coverage$geographicCoverage$geographicDescription)
eml_record$dataset$dataTable$attributeList

eml_record$dataset$dataTable$attributeList$attribute[[1]]$attributeName
eml_record$dataset$dataTable$attributeList$attribute[[1]]$attributeDefinition
