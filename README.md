# douyu_cli

### Broken At this Moment ###

## USAGE
```
./douyu_api.py [-q quality] [-r room_id] [-p | -s output_filename] DOUYU_URL

-r, --room_id   use room id instead of url
-q, --quality   0 for high, 1 for low and 2 for medium
-p, --mpv       play with mpv
-s, --record fn record with ffmpeg, fn is the output filename

-p and -s are mutually exclusive

example:
./douyu_api.py -q 1 -r 3484 -s out
```

```
./douyu_notify.py [-t time_interval] [-i input_file] DOUYU_URL

-t, --interval   After checking all rooms the process will sleep for t secs
-i, --input      input file containing room IDs or URLs, seperated by new lines

example:
./douyu_api.py -t 60 -i watch_list.txt
./douyu_api.py -t 120 -i watch_list_2.txt http://douyu.com/3484
```
