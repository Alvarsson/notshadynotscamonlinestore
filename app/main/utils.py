import requests
from flask import url_for



def is_url_image(image_url): 
        image_formats = ("image/png", "image/jpeg", "image/jpg")
        try:
            r = requests.head(image_url)
            if r.headers["content-type"] in image_formats:
                return image_url
        except:
            #return url_for('static', filename='img/noimage.png')
            pass
        return url_for('static', filename='img/noimage.png')

