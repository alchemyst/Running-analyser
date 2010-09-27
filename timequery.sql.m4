define(garmintime,`datetime(strftime("%s", "2001-01-01 00:00") + $1, "unixepoch")')
select strftime('timefmt', garmintime(run.zstarttime3)) as starttime, sum(lap.zdistance) as distance 
from zcdtreeitem as run left join zcdtreeitem as lap on lap.zbelongstorun=run.z_pk 
where run.zactivity2=3 
group by starttime 
order by starttime;
