library(tidyverse)
library(readxl)
# library(magrittr)

setwd("./repos/cfmc-dashboard/r-scripts")



##------------
## Data in
##------------
read_fund <- function(n, fp = '../data/grants-apps-funds.xlsx') {
  return(read_xlsx(fp, skip = 1, sheet = n))
}

funds <- lapply(2:6, read_fund)

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


my_vars <- c("Batch", "Program_Area", "Fund_DAmt", "Fdescript")
funds_sub <- lapply(funds, my_polisher, my_vars) %>% 
  bind_rows()

##-----------------
## Feature Engineering
##-----------------
educ <- c("Education (Community Wide/Schools)", "Scholarship", "Science" , "Positive Youth Development")
env <- c("Animal Related","Environment")
poverty_alleviation <- c("Community Devel" , "Neighborhood Enhancement", "Human Services", "Public/Social Benefit (Civic Improve/Social Srvcs)", "Capacity Building" , "Economic Security/Opportunity" , "Economic Development", "Public Safety" , "Capital" , "Haiti" , "United Way", "Essex" , "Miscellaneous")
peace_and_human_rights <- c("Human Rights" , "Legal" , "Mental Health" , "Veterans", "Public Affairs", "Safer Communities" , "Religion", "Women & Girls" , "Boys & Young Men")
public_health <- c("Disaster Relief", "Community Health (Health/Medical/Hospital Care)" , "Basic Human Need", "Disease/Disorder", "Dental")
arts <- c("Arts", "Recreation", "Camp", "Sports/Leisure", "Music" , "Community Enrichment (Arts/Culture/Heritage)", "Heritage Enhancement")

funds_sub <- funds_sub %>% 
  mutate(impact_area = ifelse(Program_Area %in% educ, "Education",
                              ifelse(Program_Area %in% env, "Environment and Climate Change",
                                     ifelse(Program_Area %in% poverty_alleviation, "Poverty Alleviation",
                                            ifelse(Program_Area %in% peace_and_human_rights, "Peace and Human Rights",
                                                   ifelse(Program_Area %in% public_health, "Public Health",
                                                          ifelse(Program_Area %in% arts, "Arts", "Uncategorized")))))),
         year = as.numeric(str_extract(Batch, "(?<=-)[0-9]{2}")) %>%
           {ifelse(. > 90, . + 1900, . + 2000)} %>% 
           as.factor) %>% 
  select(year, impact_area, Fdescript, Fund_DAmt)


write_csv(funds_sub, "../data/funds_clean.csv")


##0