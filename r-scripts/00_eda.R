library(tidyverse)
library(readxl)
library(magrittr)
library(ggalluvial)

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

##----------------------
## Feature Engineering
##---------------------
educ <- c("Education (Community Wide/Schools)", "Scholarship", "Science" , "Positive Youth Development")
env <- c("Animal Related","Environment")
poverty_alleviation <- c("Community Devel" , "Neighborhood Enhancement", "Human Services", "Public/Social Benefit (Civic Improve/Social Srvcs)", "Capacity Building" , "Economic Security/Opportunity" , "Economic Development", "Public Safety" , "Capital" , "Haiti" , "United Way", "Essex" , "Miscellaneous")
peace_and_human_rights <- c("Human Rights" , "Legal" , "Mental Health" , "Veterans", "Public Affairs", "Safer Communities" , "Religion", "Women & Girls" , "Boys & Young Men")
public_health <- c("Disaster Relief", "Community Health (Health/Medical/Hospital Care)" , "Basic Human Need", "Disease/Disorder", "Dental")
arts <- c("Arts", "Recreation", "Camp", "Sports/Leisure", "Music" , "Community Enrichment (Arts/Culture/Heritage)", "Heritage Enhancement")

fund1 %<>% 
  mutate(impact_area = ifelse(Program_Area %in% educ, "Education",
                              ifelse(Program_Area %in% env, "Environment and Climate Change",
                                     ifelse(Program_Area %in% poverty_alleviation, "Poverty Alleviation",
                                            ifelse(Program_Area %in% peace_and_human_rights, "Peace and Human Rights",
                                                   ifelse(Program_Area %in% public_health, "Public Health",
                                                          ifelse(Program_Area %in% arts, "Arts", "Uncategorized")))))))
fund1$year <- str_extract(fund1$Batch, "(?<=-)[0-9]{2}") %>% 
  as.factor

##-----------------------
## Multivariate exploration
##-----------------------

## How much money came from each fund? --> table [Count/DAmt]displaying top 5 results 
my_viz <- fund1 %>% 
  select(Fund_Alpha, Fund_DAmt) %>% 
  group_by(Fund_Alpha) %>% 
  summarise(total_DAmt = sum(Fund_DAmt),
            count = n(),
            avg_DAmt = total_DAmt/count) %>% 
  arrange(desc(total_DAmt))

cor(my_viz[2:4]) ##  bigger Funds tend to give bigger avg. funds

## What are my big areas of impact? --> Bar chart 6 columns
my_viz <- fund1 %>% 
  group_by(impact_area) %>% 
  summarise(impact_n = n()) ## Lots of funds toward poverty alleviation

ggplot(my_viz) +
  geom_bar(aes(x = impact_area, y = impact_n), stat = "identity") +
  labs(title = "# of Funds ~ Impact Area") + 
  theme(axis.text.x = element_text(angle = 10, hjust = 1))

## How much goes into each area of impact? --> Bar chart [by year] (raw $ + perc of that year)
my_viz <- fund1 %>% 
  group_by(year, impact_area) %>% 
  summarize(impact_DAmt = sum(Fund_DAmt)) ## gave out 1.2M in 2 years

ggplot(my_viz) +
  geom_bar(aes(x = impact_area, y = impact_DAmt, fill = year),
           stat = "identity", position = "dodge") +
  geom_text(aes(x = impact_area, y = impact_DAmt, label = round(impact_DAmt, 0))) +
  labs(title = "Total $ ~ Impact Area") + 
  theme(axis.text.x = element_text(angle = 10, hjust = 1)) ## roughly same amount goes into each category


## What category does the money come from?
my_viz <- fund1 %>% 
  group_by(year, Fdescript) %>% 
  summarize(total_DAmt = sum(Fund_DAmt),
         count = n(),
         avg_DAmt = total_DAmt/count)
ggplot(my_viz) +
  geom_bar(aes(x = Fdescript, y = total_DAmt), stat = 'identity') +
  facet_grid(~year) + 
  labs(title = "Total $ ~ Fund type") + 
  theme(axis.text.x = element_text(angle = 10, hjust = 1))


## Which fund type contributes to impact_area?
my_viz <- fund1 %>% 
  group_by(year, Fdescript, impact_area) %>% 
  summarize(total_DAmt = sum(Fund_DAmt),
            count = n(),
            avg_DAmt = total_DAmt/count) %>%
  # filter(Fdescript %in% c("Designated", "Donor Advised", "Field of Interst", "Unrestricted"))
filter(Fdescript %in% c("Designated", "Donor Advised", "Field of Interst", "Unrestricted"))
ggplot(my_viz, aes(y = total_DAmt, axis1 = Fdescript, axis2 = impact_area)) +
  geom_alluvium(aes(fill = Fdescript), width = 1/12) +
  geom_stratum() +
  geom_label(stat = 'stratum', label.strata = TRUE) +
  ggtitle("$ From Funds to Impact Area") + 
  facet_grid(~year)

## Same size flows but show connections with $ Amt
## think about how to use Secondary categories ==> another set of flows to secondary project category
  ## educate nonprofit into telling their stories better
## give the message to the board that we do it all! 


# my_viz2 <- fund1 %>% 
#   group_by(year, Fdescript, impact_area) %>% 
#   summarize(total_DAmt = sum(Fund_DAmt),
#             count = n(),
#             avg_DAmt = total_DAmt/count) %>% 
#   filter(!(Fdescript %in% c("Designated", "Donor Advised", "Field of Interst", "Unrestricted")))
# 
# ggplot(my_viz2, aes(y = total_DAmt, axis1 = Fdescript, axis2 = impact_area)) +
#   geom_alluvium(aes(fill = Fdescript), width = 1/12) +
#   geom_stratum() +
#   geom_label(stat = 'stratum', label.strata = TRUE)


## three words describing what the CFMC does
