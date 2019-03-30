
library(readxl)
library(magrittr)
library(tidyverse)

setwd("./repos/cfmc-dashboard/data-cleaning-eda")



##------------
## Data in
##------------
read_data <- function(n, fp = '../data/grants-apps-funds.xlsx') {
  return(read_xlsx(fp, skip = 1, sheet = n))
}

funds <- lapply(2:6, read_data)

fund1 <- funds[[1]] ## no PrevGrant
fund2 <- funds[[2]] ## no PrevGrant
fund3 <- funds[[3]] ## no PrevGrant
fund4 <- funds[[4]]
fund5 <- funds[[5]]



clean_colnames <- function(df) {
  my_cols <- colnames(df)
  colnames(df) <- my_cols %>% 
    str_replace_all('\\s', '_') %>%
    str_replace('^\\$', 'DAmt_') %>% 
    str_replace('(?<!_)\\$$', '_DAmt') %>% 
    str_replace('Fund_\\$', 'Fund_DAmt') %>% 
    str_replace('1st', 'First') %>% 
    str_replace('2nd', 'Second') %>% 
    str_replace('#', 'N')
  return(df)
}

handpick_cols <- function(df, cnames) {
  return(df[cnames])
}


my_polisher <- function(df, cnames) {
  df <- clean_colnames(df)
  return(handpick_cols(df, cnames))
}


colnames(clean_colnames(fund5))



my_vars <- c("Batch", "Program_Area", "OrgProgramArea", "Second_Program_Area" ,"Fund_DAmt", "Fdescript",
             "Region", "Alpha", "Grant_DAmt", "Fund_Alpha", "Program_Name")
funds_sub <- lapply(funds, my_polisher, my_vars) %>% 
  bind_rows()






##-------------
## 
##------------
see_unique <- function(df, x) {
  x <- enquo(x)
  count(df, !!x, sort = TRUE)
}

## How am I actually helping?
see_unique(fund1, Program_Area) ## 40 different areas --> can make bigger groups
see_unique(fund1, OrgProgramArea) ## (34) --> cam make bigger groups
see_unique(fund1, Second_Program_Area)## "None" --> NA, (38) --> can make bigger groups
see_unique(fund1, OrgType) ## (38) --> can make bigger groups
see_unique(fund1, Effect_Code)  ## (NAs) (8 different effects)

## Names
see_unique(fund1, Program_Name) ## "general support" is a catch-all
see_unique(fund1, Organization)  ## names of places ==> top 5 places who receive

## how CFMC classifies/processes this money
see_unique(fund1, Batch) # 8 committees        
see_unique(fund1, Fdescript) ## 7 types of money flow 
  ## geographic affiliate --> affiliate
  ## remove agency funds

see_unique(fund1, Cmte)  ## "None" --> NA
see_unique(fund1, Grant_Typ) ## refer to flowchart  

## Geo Impact
see_unique(fund1, Region) ## ask Thayer to group stuff
see_unique(fund1, Region__1) ## don't know what the difference is
see_unique(fund1, County_Served)## (NAs) 

## all of county: north county, south county, all county

## Things to take into account when awarding grants
see_unique(fund1, Request_Type) ## mostly operations/program development (23) --> can make bigger groups    
see_unique(fund1, PrevGrant) ## "None" --> NA only (hasApplied, hasReceived, no)
see_unique(fund1, Anonymous_Fund)  # missing

## Source of the money
see_unique(fund1, Fund_ID) # code name of fund who gave the grant
see_unique(fund1, Fund_Alpha) # full name of fund
see_unique(fund1, FirstFundID)           
see_unique(fund1, LastFundID)         

## Who did we impact? Demographics
see_unique(fund1, Pop_Age) ## (NAs) overlapping age groups + catchalls
see_unique(fund1, Disability) ## (NAs) (7) not sure how to collapse groups (maybe just binary)
see_unique(fund1, Economic) ## (NAs) (2 - low income, homeless)     
see_unique(fund1, Ethnic) ## (NAs) (2) no idea what these are ****  
see_unique(fund1, Gender) ## (NAs) (2)


##-----------------
## Feature Engineering
##-----------------
## Impact categories
educ <- c("Education (Community Wide/Schools)", "Scholarship", "Science" , "Positive Youth Development", "Technical")
env <- c("Animal Related","Environment")
poverty_alleviation <- c("Community Devel" , "Neighborhood Enhancement", "Human Services", "Public/Social Benefit (Civic Improve/Social Srvcs)", "Capacity Building" , "Economic Security/Opportunity" , "Economic Development", "Public Safety" , "Capital" , "Haiti" , "United Way", "Essex" , "Miscellaneous", "Transportation", "Shelter/Housing", "Volunteer", "Wkforce Development")
peace_and_human_rights <- c("Human Rights" , "Legal" , "Mental Health" , "Veterans", "Public Affairs", "Safer Communities" , "Religion", "Women & Girls" , "Boys & Young Men", "Civil Rights")
public_health <- c("Disaster Relief", "Community Health (Health/Medical/Hospital Care)" , "Basic Human Need", "Disease/Disorder", "Dental", "General Health", "Food/Nutrition")
arts <- c("Arts", "Recreation", "Camp", "Sports/Leisure", "Music" , "Community Enrichment (Arts/Culture/Heritage)", "Heritage Enhancement", "Theater", "Dance" )


## Region groupings
middletown <- c("Middletown")      
north_county <- c("Northern County", "Cromwell", "Middlefield", "East Hampton", "Haddam", "Portland", "Durham/Middlefie")
south_county <- c("Southern/Low Cty", "Essex", "Old Saybrook", "East Haddam", "Westbrook", "Clinton", "Chester/DR/Essex", "Chester", "Deep River", "Durham", "Haddam/Killingwo", "Killingworth", "Essex/Deep River", "CT River Valley", "Ivoryton")
all_county_plus <- c("All County", "All of CT", "CT/Out of County", "Out of State", "International", "Multiple Towns", "National-All US")

my_vars <- c("year", "Fund_Alpha", "Fdescript", "Fund_DAmt", "Program_Name", "Alpha", "project_impact", "org_impact",
             "region", "Grant_DAmt")

funds_sub <- funds_sub %>% 
  mutate(project_impact = ifelse(Program_Area %in% educ, "Education",
                              ifelse(Program_Area %in% env, "Environment and Climate Change",
                                     ifelse(Program_Area %in% poverty_alleviation, "Poverty Alleviation",
                                            ifelse(Program_Area %in% peace_and_human_rights, "Peace and Human Rights",
                                                   ifelse(Program_Area %in% public_health, "Public Health",
                                                          ifelse(Program_Area %in% arts, "Arts", "Uncategorized")))))),
         # secondary_impact = ifelse(Second_Program_Area %in% educ, "Education",
         #                      ifelse(Second_Program_Area %in% env, "Environment and Climate Change",
         #                             ifelse(Second_Program_Area %in% poverty_alleviation, "Poverty Alleviation",
         #                                    ifelse(Second_Program_Area %in% peace_and_human_rights, "Peace and Human Rights",
         #                                           ifelse(Second_Program_Area %in% public_health, "Public Health",
         #                                                  ifelse(Second_Program_Area %in% arts, "Arts", "Uncategorized")))))),
         org_impact = ifelse(OrgProgramArea %in% educ, "Education",
                              ifelse(OrgProgramArea %in% env, "Environment and Climate Change",
                                     ifelse(OrgProgramArea %in% poverty_alleviation, "Poverty Alleviation",
                                            ifelse(OrgProgramArea %in% peace_and_human_rights, "Peace and Human Rights",
                                                   ifelse(OrgProgramArea %in% public_health, "Public Health",
                                                          ifelse(OrgProgramArea %in% arts, "Arts", "Uncategorized")))))),
         year = as.numeric(str_extract(Batch, "(?<=-)[0-9]{2}")) %>%
           {ifelse(. > 90, . + 1900, . + 2000)} %>% 
           as.factor(),
         region = ifelse(Region %in% all_county_plus, "Middlesex and beyond",
                         ifelse(Region %in% north_county, "North County", 
                                ifelse(Region %in% south_county, "South County",
                                       ifelse(Region %in% middletown, "Middletown", "Uncategorized"))))
         ) %>% 
  select(my_vars) %>% 
  rename(org_name = Alpha,
         fund_name = Fund_Alpha,
         fund_type = Fdescript)

colnames(funds_sub) %<>% tolower


write_csv(funds_sub, "../data/funds_clean.csv")


##

