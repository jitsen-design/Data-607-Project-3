-- modify collation of job_desxcription column so it is case-sensitive
-- reference of how to do this https://stackoverflow.com/questions/4879846/how-to-configure-mysql-to-be-case-sensitive
ALTER TABLE tbljobs MODIFY job_description TEXT CHARACTER SET  utf8mb4 COLLATE  utf8mb4_0900_as_cs;

drop table if exists tblrpython;

create table tblRPython as
SELECT
	case when locate(' R,', job_description) = 0 and locate(' R ', job_description) = 0 then 0
		 when locate(' R,', job_description) = 0 and locate(' R ', job_description) <> 0 then locate(' R ', job_description) 
         when locate(' R,', job_description) <> 0 and locate(' R ', job_description) = 0 then locate(' R,', job_description) 
         else least(locate(' R,', job_description), locate(' R ', job_description))
         end as locR,
    case when locate('Python', job_description) = 0 and locate('python', job_description) = 0 then 0
		 when locate('Python', job_description) = 0 and locate('python', job_description) <> 0 then locate('python', job_description)
         when locate('Python', job_description) <> 0 and locate('python', job_description) = 0 then locate('Python', job_description) 
         else least(locate('Python', job_description), locate('python', job_description))
         end  as locPython,
    count(*) as jobs
FROM my_data.tbljobs
group by 	
    case when locate('Python', job_description) = 0 and locate('python', job_description) = 0 then 0
		 when locate('Python', job_description) = 0 and locate('python', job_description) <> 0 then locate('python', job_description)
         when locate('Python', job_description) <> 0 and locate('python', job_description) = 0 then locate('Python', job_description) 
         else least(locate('Python', job_description), locate('python', job_description))
         end  ,
    case when locate(' R,', job_description) = 0 and locate(' R ', job_description) = 0 then 0
		 when locate(' R,', job_description) = 0 and locate(' R ', job_description) <> 0 then locate(' R ', job_description) 
         when locate(' R,', job_description) <> 0 and locate(' R ', job_description) = 0 then locate(' R,', job_description) 
         else least(locate(' R,', job_description), locate(' R ', job_description))
         end 
  ;
  
  SELECT case when locR = 0 and locPython = 0 then 'Neither'
		 when locR = 0 and locPython <> 0 then 'Python' 
         when locR <> 0 and locPython = 0 then 'R'
         when locR < locPython then 'R'
         else 'Python'
         end as 'winner',
      sum(jobs) as jobs
FROM my_data.tblRpython
group by 	
    case when locR = 0 and locPython = 0 then 'Neither'
		 when locR = 0 and locPython <> 0 then 'Python' 
         when locR <> 0 and locPython = 0 then 'R'
         when locR < locPython then 'R'
         else 'Python'
         end
  ;
 