library(tidyverse)
library(readxl)

setwd("./repos/cfmc-dashboard/r-scripts")



##------------
## Data in
##------------
funds <- read_csv('../data/funds_clean.csv')


##-----------------
## Multivariate exploration
##------------------

## Over time, how much money goes into each category? 
  ## Gross: Money out increases, especially 2013
for_viz <- funds %>% 
  group_by(year) %>% 
  mutate(running_money = cumsum(Fund_DAmt)) %>% 
  group_by(year, impact_area) %>% 
  summarise(total_money = sum(Fund_DAmt),
            yearly_money = max(running_money)) %>% 
  ungroup() %>% 
  mutate(perc_money = total_money/yearly_money) 
  

ggplot(for_viz) +
  geom_area(aes(x = year, y = total_money, fill = impact_area))
  
  ## Perc: Most money started going to poverty alleviation since 2000
yearly <- funds %>%
  group_by(year) %>% 
  summarise(yearly_money = sum(Fund_DAmt))

for_viz2 <- for_viz %>% 
  left_join(yearly, by = "year") %>% 
  mutate(perc_money = total_money/yearly_money)

ggplot(for_viz2) +
  geom_bar(aes(x = year, y = perc_money, fill = impact_area), stat = 'identity')

## Every year, who are the top 5 places who receive the most money?


## What are the best indicators of receiving a large fund?