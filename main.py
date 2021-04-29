#IMPORTS
import os
import requests
import fishManager
import tweepy

#CONSTANTES
IAE_API_KEY = str(os.environ.get('IAE_PEIXESFODAS_APIKEY'))
IAE_API_SECRET = str(os.environ.get('IAE_PEIXESFODAS_APISECRET'))

TWIITER_ACCESS_KEY = str(os.environ.get('TWITTER_PEIXESFODAS_ACCESSKEY'))
TWIITER_ACCESS_SECRET = str(os.environ.get('TWITTER_PEIXESFODAS_ACCESSSECRET'))

TWITTER_CONSUMER_KEY = str(os.environ.get('TWITTER_PEIXESFODAS_CONSUMERKEY'))
TWITTER_CONSUMER_SECRET = str(os.environ.get('TWITTER_PEIXESFODAS_CONSUMERSECRET'))

GOOGLE_API_KEY = str(os.environ.get('GOOGLE_APIKEY'))
GOOGLE_PROJECT_KEY = str(os.environ.get('GOOLE_PROJECTKEY'))

#IaePost
def iaePost(image, conts, fish, API_KEY, API_SECRET):
    if image != []:
        url = 'https://api.iaebots.com/api/v1/posts'
        #url = 'http://localhost:3001/api/v1/posts'
        files = {'media': open(image[0], 'rb')}
        data = {'body': "Peixe foda #" + str(conts[1]) + " - " + fish}
        response = requests.post(url, headers = {'Authorization': 'Token api_key='+API_KEY+' api_secret='+API_SECRET}, files=files, data=data)
        return response

#twitterPost
def twitterPost(image, conts, fish, ACCESS_KEY, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET):
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

    media_ids = [api.media_upload(i).media_id_string for i in image]
    response = api.update_status(status="Peixe foda #" + str(conts[1]) + " - " +fish, media_ids=media_ids)
    return response
    
#Finding Nemo
def main():
    fm = fishManager.fishManager
    conts = fm.numFishSelector()
    fish = fm.fishSelector(conts[0])
    image = fm.fishImage(fish, GOOGLE_API_KEY, GOOGLE_PROJECT_KEY)

    responseT = twitterPost(image, conts, fish, TWIITER_ACCESS_KEY, TWIITER_ACCESS_SECRET, TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    responseI = iaePost(image, conts, fish, IAE_API_KEY, IAE_API_SECRET)

    print(responseI)
    print(responseT)
    fm.fishUpdate(conts, responseI.ok)


if __name__ == "__main__":
    main()
