import vk
import time
import requests
import re
from PIL import Image, ImageDraw, ImageFont
_imaging = Image.core


class Banner:
    def __init__(self, k):
        self.key = k
        self.api = vk.API(vk.Session(access_token = self.key))

    def Run(self):
        mn = str(time.gmtime()[4])
        hr = str((time.gmtime()[3] + 3) % 24)
        self.Generate(hr, mn)
        self.Upload()
        while True:
            tmp = str(time.gmtime()[4])
            if tmp != mn:
                hr = str((time.gmtime()[3] + 3) % 24)
                self.Generate(hr, tmp)
                self.Upload()
                mn = tmp

    def Generate(self, hr, mn):
        if len(mn) == 1:
            mn = '0' + mn
        img = Image.open('VKover.jpg')
        imgDrawer = ImageDraw.Draw(img)
        imgDrawer.text((1100, 100), hr, fill='Black', font=ImageFont.truetype("SourceSansPro-ExtraLight.otf", 120))
        imgDrawer.text((1100, 230), mn, fill='Black', font=ImageFont.truetype("SourceSansPro-ExtraLight.otf", 120))
        img.save('s.jpg')

    def Upload(self):
        u = self.api.photos.getOwnerCoverPhotoUploadServer(group_id=149556739, crop_x=0, crop_y=0, crop_x2=1590,
                                                           crop_y2=400)['upload_url']
        files = {'photo': open('s.jpg', 'rb')}
        try:
            r = requests.post(u, files=files)
        except:
            time.sleep(10)
            r = requests.post(u, files=files)
        r = str(r.text)
        hsh = r[r.find('hash') + 7:r.find('photo') - 3]
        photo = r[r.find('photo') + 8:len(r) - 2]
        self.api.photos.saveOwnerCoverPhoto(hash=hsh, photo=photo)