library(tidyverse)
library(readxl)

setwd("./repos/cfmc-dashboard/r-scripts")


##------------
## Data in
##------------
grants_sub <- read_csv('../data/grants_clean.csv')




##-------------------------------------
## Graphs
##------------------------------------
## Over time, how much money goes into each category? 
  ## Gross: Money out increases, especially 2013
for_viz <- grants_sub %>% 
  group_by(year, primary_impact) %>% 
  summarize(total_money = sum(Grant_DAmt))


ggplot(grants_sub) + 
  geom_bar(aes(x = year, y = Grant_DAmt, fill = primary_impact), stat = 'sum') +
  labs(title = 'Per year, how much money goes into each primary category?')
ggsave("../sample-graphs/totalMoney~year.png", width = 10, height = 4)

ggplot(grants_sub) + 
  geom_bar(aes(x = year, y = Grant_DAmt, fill = org_impact), stat = 'sum') +
  labs(title = 'Per year, how muc money goes into each secondary category?')
ggsave("../sample-graphs/totalMoney~year2.png", width = 10, height = 4)

  ## Perc: Most money started going to poverty alleviation since 2000


## Where does the money go? (no of grants, ave. grant amt, total amount of money)
ggplot(grants_sub) + 
  geom_bar(aes(x = region, y = Grant_DAmt), stat = 'sum')

## Who is the top 4 receiver of money per year, (group of years)?
## Who is 
  
