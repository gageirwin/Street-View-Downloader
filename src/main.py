import requests
import os
from PIL import Image
from io import BytesIO
import time

from .args import get_args

# helper functions in increase image down and right
def increase_right(img, pixels):
    width, height = img.size
    new_width = width + pixels
    result = Image.new(img.mode, (new_width, height), (250,250,250))
    result.paste(img, (0, 0))
    return result

def increase_down(img, pixels):
    width, height = img.size
    new_height = height + pixels
    result = Image.new(img.mode, (width, new_height), (250,250,250))
    result.paste(img, (0, 0))
    return result

class GMAP360:

    def __init__(self, SV_IDs:list = None, download_path:str = None, ZOOM:int = 4, retry:int = 5, overwrite:bool = False):
        self.location_ids = SV_IDs
        if not os.path.exists(download_path):
            raise Exception(f"File path does not exist: {download_path}")
        self.download_path = download_path
        self.retry = retry
        # only zoom levels from 1-5 are allowed
        if 5 < ZOOM < 0:
            raise Exception(f"Incorrect zoom size: {ZOOM}, only sizes 1-5 are allowed.")
        self.ZOOM = ZOOM
        self.overwrite = overwrite
        self.start()

    def download_street_view(self, location_id:str):
        # Street view 360 images are loaded in chunks.
        # The chunks are layed out in a 2D plane with an X and Y cordinate.
        # The number of chunks is based on the resolution of the full image.
        # You can not get the resolution of the the full image so we loop over X and Y till we reach a 400 status code.

        # to try to prevent throttling by using a browser user agent
        headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'}
        # start from 0,0
        X = Y = 0
        # variable to know when the column ends so we don't have to check when each column ends.
        end_column = 0
        # the zoom level determines the size of each chunk
        # zoom level 1-4 are 512 and 5 is 256
        block_size = 512 if self.ZOOM <= 4 else 256
        # loop over X positions of chunks
        while True:
            # loop over Y positions of chunks
            while True:
                # if the current Y position is at the end don't waste a GET requests
                if Y == end_column and Y != 0:
                    break
                # build url for chunk
                response = requests.get(f"https://streetviewpixels-pa.googleapis.com/v1/tile?cb_client=maps_sv.tactile&panoid={location_id}&x={X}&y={Y}&zoom={self.ZOOM}&nbt=1&fover=2",
                                        headers=headers)
                if response.status_code == 400:
                    end_column = Y
                    break
                # load image from responce
                image = Image.open(BytesIO(response.content))
                # if first chunk create new image
                if X == 0 and Y == 0:
                    # create empty panorama image of size block_size by block_size
                    panorama = Image.new('RGB',(block_size,block_size), (250,250,250))
                elif end_column == 0 and Y != 0:
                    # increase panorama image down by block_size amount
                    panorama = increase_down(panorama, block_size)
                # paste loaded image into panorama image
                panorama.paste(image,(X*block_size,Y*block_size))
                # move to next Y position
                Y += 1
                time.sleep(0.1)
            # reset Y position
            Y = 0
            # move to next X position
            X += 1
            response = requests.get(f"https://streetviewpixels-pa.googleapis.com/v1/tile?cb_client=maps_sv.tactile&panoid={location_id}&x={X}&y={Y}&zoom={self.ZOOM}&nbt=1&fover=2",
                                    headers=headers)
            # if no more X positions then we are done
            if response.status_code == 400:
                break
            # load image from responce
            image = Image.open(BytesIO(response.content))
            # increase panorama image right by block_size amount
            panorama = increase_right(panorama, block_size)
            # paste loaded image into panorama image
            panorama.paste(image,(X*block_size,Y*block_size))
        # save panorama image
        panorama.save(os.path.join(self.download_path, f"{location_id}.jpg"), format="JPEG")

    def download(self, location_id:str, retry:int):
        # wrapper function for self.download_street_view() to allow retrying
        try:
            self.download_street_view(location_id)
        except:
            print('Download Failed!')
            if retry > 0:
                print('Retrying...')
                self.download(location_id, retry-1)

    def start(self):
        for index, location_id in enumerate(self.location_ids):
            if not self.overwrite and os.path.exists(os.path.join(self.download_path, f"{location_id}.jpg")):
                print(f"Skipping download | Image {location_id}.jpg already exists")
                continue
            print(f"Downloading image {location_id}.jpg {index}/{len(self.location_ids)}")
            self.download(location_id, self.retry)

def main():
    args = get_args()
    GMAP360(
        SV_IDs=args['street-view-ids'],
        download_path=args['output_path'],
        ZOOM=args['zoom'], retry=args['retry'],
        overwrite=args['overwrite']
    )
    print('Done!')