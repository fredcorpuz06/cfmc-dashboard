library(magrittr)
library(readxl)
library(tidyverse)



setwd("./repos/cfmc-dashboard/r-scripts")



##------------
## Data in
##------------
read_data <- function(n, fp = '../data/grants-apps-funds.xlsx') {
  return(read_xlsx(fp, skip = 1, sheet = n))
}

grants <- read_data(1)

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

grants <- clean_colnames(grants)



##----------------------
## Check vars
##----------------------
see_unique <- function(df, x) {
  x <- enquo(x)
  count(df, !!x, sort = TRUE)
}


# How am I helping?
see_unique(grants, OrgType)  
see_unique(grants, Organization) ## redundant
see_unique(grants, Program_Area) 
see_unique(grants, Second_Program_Area) ## almost half missing


# Where am i helping?
see_unique(grants, Region)
see_unique(grants, Region__1) # redundant
see_unique(grants, OrgProgramArea) # confusing: location + purpose

# Where does the money come from?
see_unique(grants, Grant_Typ) 

## Names
see_unique(grants, Alpha)




##----------------
##----------------

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


my_vars <- c("year", "Program_Name", "Alpha", "project_impact", "org_impact",
             "region", "Requested_DAmt", "Grant_DAmt", "lifetime_grant")

grants_sub <- grants %>% 
  mutate(project_impact = ifelse(Program_Area %in% educ, "Education",
                                 ifelse(Program_Area %in% env, "Environment and Climate Change",
                                        ifelse(Program_Area %in% poverty_alleviation, "Poverty Alleviation",
                                               ifelse(Program_Area %in% peace_and_human_rights, "Peace and Human Rights",
                                                      ifelse(Program_Area %in% public_health, "Public Health",
                                                             ifelse(Program_Area %in% arts, "Arts", "Uncategorized")))))),
         # secondary_impact = ifelse(Second_Program_Area %in% educ, "Education",
         #                           ifelse(Second_Program_Area %in% env, "Environment and Climate Change",
         #                                  ifelse(Second_Program_Area %in% poverty_alleviation, "Poverty Alleviation",
         #                                         ifelse(Second_Program_Area %in% peace_and_human_rights, "Peace and Human Rights",
         #                                                ifelse(Second_Program_Area %in% public_health, "Public Health",
         #                                                       ifelse(Second_Program_Area %in% arts, "Arts", "Uncategorized")))))),
         org_impact = ifelse(OrgType %in% educ, "Education",
                             ifelse(OrgType %in% env, "Environment and Climate Change",
                                    ifelse(OrgType %in% poverty_alleviation, "Poverty Alleviation",
                                           ifelse(OrgType %in% peace_and_human_rights, "Peace and Human Rights",
                                                  ifelse(OrgType %in% public_health, "Public Health",
                                                         ifelse(OrgType %in% arts, "Arts", "Uncategorized")))))),
         year = as.numeric(str_extract(Batch, "(?<=-)[0-9]{2}")) %>%
          {ifelse(. > 90, . + 1900, . + 2000)} %>% 
          as.factor,
         region = ifelse(Region %in% all_county_plus, "Middlesex and beyond",
                         ifelse(Region %in% north_county, "North County", 
                                ifelse(Region %in% south_county, "South County",
                                       ifelse(Region %in% middletown, "Middletown", "Uncategorized"))))
         ) %>% 
  group_by(Alpha) %>% 
  mutate(lifetime_grant = cumsum(Grant_DAmt)) %>% 
  ungroup %>% 
  select(my_vars) %>% 
  rename(org_name = Alpha)

colnames(grants_sub) %<>%  tolower

a <- grants_sub %>% 
  filter(org_name == "Buttonwood Tree/NEAR")
a

write_csv(grants_sub, "../data/grants_clean.csv")
