library(tidyverse)
library(readxl)

setwd("./repos/cfmc-dashboard/r-scripts")



##------------
## Data in
##------------
grants <- read_xlsx('../data/grants-apps-funds.xlsx', skip = 1, sheet = 1)


my_cols <- colnames(grants)
my_cols


##-----------------
## Multivariate exploration
##------------------

## Ave. $ of grants in each category