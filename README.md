# douyu_cli

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
