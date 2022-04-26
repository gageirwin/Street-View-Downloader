# street_view-dl
A downloader tool for google street view 360 images.

## How to use
1.  Install python 3
2.  Install PIL with  `pip install pillow`
    - If the command doesn't run try adding `python -m`, `python3 -m`, or `py -m` to the front
3.  Run `python street_view-dl.py --urls URL`
    - If the script doesn't run try replacing `python` with `python3` or `py`

# Command Line Options 

`--urls URLS`  
Takes in a url or list of urls separated by a comma.  
`--street-view-ids`  
Takes in a street view id or list of street view ids separated by a comma.  
`--from-file FILE`  
Reads in a file with urls separated by new lines. Lines starting with # will not be read in.  
`--output-path`  
The output path where images are downloaded.  
`--zoom`  
The zoom level of the street view image. (default: 4)  
`--retry`  
The amount of times to retry downloading. (default: 5)  
`--overwrite`  
Overwrite any previously created files.  

# Notes
-   Valid zoom levels are 1-4.
-   Files will not be overwritten by default.
-   Default output path is the current working directory.
-   If using the get_links.py method of getting street view links I would not recommend using `--overwrite` as some times there are duplicate urls. 

# Examples
```bash
python street_view-dl.py --from-file "gmaps.txt" --output-path "images" --zoom 4

python street_view-dl.py --urls "URLS,URL,URL" --zoom 5

python street_view-dl.py --street-view-ids ID --zoom 2 --overwrite
```

