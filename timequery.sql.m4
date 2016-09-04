define(garmintime,`datetime(strftime("%s", "2001-01-01 00:00") + $1, "unixepoch")')
define(timefield,`strftime($1, garmintime($2))')
select timefield('groupfmt', run.zstarttime3) as grouptime, timefield('timefmt', max(run.zstarttime3)) as starttime, sum(lap.zdistance) as distance, sum(lap.zdisplayedascent) as ascent
from zcdtreeitem as run left join zcdtreeitem as lap on lap.zbelongstorun=run.z_pk 
where run.zactivity2 in (select known.value from known_runvalues as known where known.type='run') 
group by grouptime 
order by starttime;
