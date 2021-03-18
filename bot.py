#IMPORTS
import tweepy
import os
import shutil
from google_images_search import GoogleImagesSearch

#CONSTANTES(
CONSUMER_KEY = str(os.environ.get('PEIXESFODAS_CONSUMER_KEY'))
CONSUMER_SECRET = str(os.environ.get('PEIXESFODAS_CONSUMER_SECRET'))
ACCESS_KEY = str(os.environ.get('PEIXESFODAS_ACCESS_KEY'))
ACCESS_SECRET = str(os.environ.get('PEIXESFODAS_ACCESS_SECRET'))
GOOGLE_API_KEY= str(os.environ.get('GOOGLE_API_KEY'))
GOOGLE_PROJECT_KEY= str(os.environ.get('GOOGLE_PROJECT_KEY'))


#AUTENTICAÇÃO
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

with open("files/fishes.txt","r",encoding="utf8") as f:
    fish_r = f.readlines()
f.close()

with open("files/cont.txt","r",encoding="utf8") as f:
    num = f.readlines()
    num = [int(s) for s in num[0].split() if s.isdigit()]
f.close()

with open("files/cont.txt","w",encoding="utf8") as f:
    f.write(str(num[0]+1))
f.close()

with open("files/cont_real.txt","r",encoding="utf8") as f:
    num_real = f.readlines()
    num_real = [int(s) for s in num_real[0].split() if s.isdigit()]
f.close()

query = fish_r[num[0]]
query = query[0:len(query)-1] + " peixe"
print(query)

gis = GoogleImagesSearch('AIzaSyCEW9Rimxwv5QU4Fu6HoUbtwGeYVdrVtL8', 'e13ca726c4a88dc1e')

_search_params = {
    'q': query,
    'num': 10,
    'searchType': 'image',
    'safe': 'off',
    'imgType': 'photo',
    'fileType': 'jpg',
    'orTerms': 'peixe|fish|pesca|pescaria|rio|isca|nadando|nadar|água|mar|anzol'
}

try:
    gis.search(search_params=_search_params, path_to_dir='images/' + str(num))
except:
    print('f')

path = 'images/' + str(num)+'/'
max_bytes = 50000
sec_max_bytes = 80000

if os.path.exists('images/' + str(num)):
    for filename in os.listdir('images/' + str(num)):
        print(filename)
        file = open(path + filename)
        file.seek(0, os.SEEK_END)
        print("Size of file is :", file.tell(), "bytes")
        if file.tell() > max_bytes:
            max_bytes = file.tell()
            os.rename(path + filename,path + '1.jpg')
        elif file.tell() > sec_max_bytes:
            os.rename(path + filename,path + '2.jpg')
            sec_max_bytes = file.tell()
        else:
            os.remove(path + filename)

images = []

if os.path.exists(path+'2.jpg'):
    images.append(path + '2.jpg')

if os.path.exists(path+'1.jpg'):
    images.append(path + '1.jpg')
    media_ids = [api.media_upload(i).media_id_string for i in images]
    #api.update_status(status="Peixe foda #" + str(num_real[0]) + " - " +fish_r[num[0]], media_ids=media_ids)

    with open("files/cont_real.txt","w",encoding="utf8") as f:
        f.write(str(num_real[0]+1))
    f.close()

if os.path.exists(path+'2.jpg'):
    os.remove(path + '2.jpg')

if os.path.exists(path+'1.jpg'):
    os.remove(path + '1.jpg')

if os.path.exists('images/'):
    shutil.rmtree('/images')