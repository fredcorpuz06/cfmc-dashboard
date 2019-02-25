library(tidyverse)

setwd("./repos/cfmc-dashboard/r-scripts")

df <- read_csv("../data/funds_clean.csv")

## How much money goes into each impact area?
impact_money <- df %>% 
  group_by(year, impact_area, Fdescript) %>% 
  summarise(total_DAmt = sum(Fund_DAmt),
            count = n(),
            avg_DAmt = total_DAmt/count)

write.csv(impact_money, "../data/impact_total_money.csv", row.names = FALSE)

fund_yearly_money <- df %>% 
  group_by(year, Fdescript) %>% 
  summarize(total_DAmt = sum(Fund_DAmt),
            count = n(),
            avg_DAmt = total_DAmt/count)

write.csv(fund_yearly_money, "../data/fund_yearly_money.csv", row.names = FALSE)
  