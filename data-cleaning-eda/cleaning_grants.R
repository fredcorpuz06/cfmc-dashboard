library(magrittr)
library(readxl)
library(tidyverse)



setwd("./repos/cfmc-dashboard/data-cleaning-eda")



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
human_services <- c("Ambulance Service", "Basic Human Need", "Community Health (Health/Medical/Hospital Care)", "Dental", "Disaster Relief", "Disease/Disorder", "Essex", "Food/Nutrition", "General Health", "General Health", "Haiti", "Hospital", "Human Service", "Human Services", "Mental Health", "Shelter/Housing", "United Way")
public_social_ben <- c("Capacity Building", "Capital", "Capital", "Career", "Civil Rights", "Community Devel", "Community Development", "Economic Development", "Economic Security/Opportunity", "Economic Security/Opportunity", "Fire Service", "Government Department", "Government", "Human Rights", "Land Trust", "Legal", "Miscellaneous", "Neighborhood Enhancement", "Public Affairs", "Public Safety", "Public/Social Benefit (Civic Improve/Social Srvcs)", "Religion", "Safer Communities", "Transportation", "Volunteer", "Wkforce Development") 
educ_youth_dev <- c("Child Care", "Education (Community Wide/Schools)", "Educational", "Library Service", "Positive Youth Development", "Scholarship", "School", "Science", "Technical", "University/College", "Youth Organization", "Youth Service Bureau")
env <- c("Agricultural", "Environment")
arts_culture <- c("Arts Related", "Arts", "Community Enrichment (Arts/Culture/Heritage)", "Dance", "Heritage Enhancement", "Heritage", "Historical Society", "Museum", "Music", "Theater")
recreation <- c("Camp", "Recreation", "Sports/Leisure")
special_int <- c("Animal Related", "Boys & Young Men", "Church/Synagogue", "Diversity", "Veterans", "Women & Girls", "Women's Service")

## Region groupings
middletown <- c("Middletown")      
north_county <- c("Northern County", "Cromwell", "Middlefield", "East Hampton", "Haddam", "Portland", "Durham/Middlefie")
south_county <- c("Southern/Low Cty", "Essex", "Old Saybrook", "East Haddam", "Westbrook", "Clinton", "Chester/DR/Essex", "Chester", "Deep River", "Durham", "Haddam/Killingwo", "Killingworth", "Essex/Deep River", "CT River Valley", "Ivoryton")
all_county_plus <- c("All County", "All of CT", "CT/Out of County", "Out of State", "International", "Multiple Towns", "National-All US")


my_vars <- c("year", "Program_Name", "Alpha", "project_impact", "org_impact",
             "region", "Requested_DAmt", "Grant_DAmt", "lifetime_grant")

grants_sub <- grants %>% 
  mutate(project_impact = ifelse(Program_Area %in% human_services, "Human Services",
                                 ifelse(Program_Area %in% public_social_ben, "Public and Social Benefit",
                                        ifelse(Program_Area %in% educ_youth_dev, "Education and Youth Development",
                                               ifelse(Program_Area %in% env, "Environment",
                                                      ifelse(Program_Area %in% arts_culture, "Arts and Culture",
                                                             ifelse(Program_Area %in% recreation, "Recreation",
                                                                    ifelse(Program_Area %in% special_int, "Special Interests", 
                                                                           "Uncategorized"))))))),
         org_impact = ifelse(OrgType %in% human_services, "Human Services",
                             ifelse(OrgType %in% public_social_ben, "Public and Social Benefit",
                                    ifelse(OrgType %in% educ_youth_dev, "Education and Youth Development",
                                           ifelse(OrgType %in% env, "Environment",
                                                  ifelse(OrgType %in% arts_culture, "Arts and Culture",
                                                         ifelse(OrgType %in% recreation, "Recreation",
                                                                ifelse(OrgType %in% special_int, "Special Interests", 
                                                                       "Uncategorized"))))))),
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

write_csv(grants_sub, "../data/grants_clean2.csv")
