library(RMySQL)
library(dplyr)

mysql_con <- dbConnect(MySQL(),    user='root',    password='password',   dbname='my_data', host='localhost')
my_fix <- dbSendQuery(mysql_con, " SET GLOBAL local_infile = true;")
dbHasCompleted(my_fix)

#create new data frame changing columns to character
full_df_2 <- data.frame(lapply(full_df, as.character), stringsAsFactors=FALSE)

#change encoding of the columns due to special characters
for (col in colnames(full_df_2))
  {
  Encoding(full_df_2[[col]]) <- "latin1"
}


#drop SQL table if it exists, then write the data frame to the SQL table
dbSendQuery(mysql_con, "drop table if exists tblJobs")
dbWriteTable(mysql_con, "tblJobs", full_df_2)


#load the data back from the SQL table
job_data <- tbl(mysql_con, sql("select * from tblJobs"))
job_data_df <- as.data.frame(job_data)

dim(job_data_df)
str(job_data_df)
head(job_data_df)

dbDisconnect(mysql_con)