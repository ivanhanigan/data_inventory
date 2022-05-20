## add tables that I don't want to use models/db.py to do for pragmatic reasons
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

dbSendQuery(ch, "CREATE TABLE orcid (
	email varchar NULL,
	orcid varchar NOT NULL,
	name_per_creator_tbl varchar NULL,
	organization_name varchar NULL,
	CONSTRAINT orcid_pk PRIMARY KEY (orcid)
)")

dbSendQuery(ch,"INSERT INTO orcid
(email, orcid, name_per_creator_tbl, organization_name)
VALUES('timothy.chaston@sydney.edu.au', '0000-0003-3767-153X', 'Timothy Chaston', 'The University of Sydney')")

##VALUES('ivan.hanigan@curtin.edu.au', '0000-0002-6360-6793', 'Ivan Hanigan', 'Curtin University')")


