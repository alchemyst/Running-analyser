define(garmintime,`datetime(strftime("%s", "2001-01-01 00:00") + $1, "unixepoch")')
define(timefield,`strftime($1, garmintime($2))')
select timefield('groupfmt', run.zstarttime3) as grouptime, timefield('timefmt', max(run.zstarttime3)) as starttime, sum(lap.zdistance) as distance 
from zcdtreeitem as run left join zcdtreeitem as lap on lap.zbelongstorun=run.z_pk 
where run.zactivity2=3 or run.zactivity2=7
group by grouptime 
order by starttime;
