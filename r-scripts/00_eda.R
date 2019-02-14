library(tidyverse)
library(readxl)

setwd("./repos/cfmc-dashboard/r-scripts")



##------------
## Data in
##------------
read_fund <- function(n, fp = '../data/grants-apps-funds.xlsx') {
  return(read_xlsx(fp, skip = 1, sheet = n))
}

funds <- lapply(2:6, read_fund)

fund1 <- funds[[5]]

my_cols <- colnames(fund1)
colnames(fund1) <- my_cols %>% 
  str_replace_all('\\s', '_') %>%
  str_replace('^\\$', 'DAmt_') %>% 
  str_replace('(?<!_)\\$$', '_DAmt') %>% 
  str_replace('Fund_\\$', 'Fund_DAmt') %>% 
  str_replace('1st', 'First') %>% 
  str_replace('2nd', 'Second') %>% 
  str_replace('#', 'N')

##-----------------------
## Univariate exploration
##------------------------
  
see_unique <- function(df, x) {
  x <- enquo(x)
  count(df, !!x, sort = TRUE)
}

unused_vars <- c("Ftype", "Program", "School", "Scholar", "X__1")
date_vars <- c("DateFirstGrant", "DateLastGrant", "DateLargestGrant")

## Quant
plot(density(fund1$Grant_DAmt))
plot(density(fund1$Requested_DAmt))  ## only for competitve grants
plot(density(fund1$Fund_DAmt)) ## amount received from each Fund
plot(density(fund1$DAmt_FirstGrant))
plot(density(fund1$DAmt_LastGrant))
plot(density(fund1$DAmt_LargestGrant))
plot(density(fund1$LifetimeGrant_DAmt))

## How am I actually helping?
see_unique(fund1, Program_Area) ## 40 different areas --> can make bigger groups
see_unique(fund1, OrgProgramArea) ## (34) --> cam make bigger groups
see_unique(fund1, Second_Program_Area)## "None" --> NA, (38) --> can make bigger groups
see_unique(fund1, OrgType) ## (38) --> can make bigger groups
see_unique(fund1, Effect_Code)  ## (NAs) (8 different effects)

## Names
see_unique(fund1, Program_Name) ## "general support" is a catch-all
see_unique(fund1, Organization)  ## names of places

## how CFMC classifies/processes this money
see_unique(fund1, Batch) # 8 committees        
see_unique(fund1, Fdescript) ## 7 types of money flow 
see_unique(fund1, Cmte)  ## "None" --> NA
see_unique(fund1, Grant_Typ) ## refer to flowchart  

## Geo Impact
see_unique(fund1, Region) ## ask Thayer to group stuff
see_unique(fund1, Region__1) ## don't know what the difference is
see_unique(fund1, County_Served)## (NAs) 

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
