install.packages('yaml')
library(yaml)

job <- read_yaml('job.yaml')

head(job)
