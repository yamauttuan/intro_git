import requests
import json
import time
from PIL import Image

#gittestコメント
#編集1
#編集2

class GooglePlaces(object):
    def __init__(self, apiKey):
        super(GooglePlaces, self).__init__()
        self.apiKey = apiKey
 
    def search_places_by_coordinate(self, location, radius, types):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        places = []
        params = {
            'keyword' : 'ネロ',
            'location': location,
            'radius': radius,
            'types': types,
            'key': self.apiKey
        }
        res = requests.get(endpoint_url, params = params)
        results =  json.loads(res.content)
        places.extend(results['results'])
        time.sleep(2)
        while "next_page_token" in results:
            params['pagetoken'] = results['next_page_token'],
            res = requests.get(endpoint_url, params = params)
            results = json.loads(res.content)
            places.extend(results['results'])
            time.sleep(2)
        return places
 
    def get_place_details(self, place_id, fields):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            'placeid': place_id,
            'fields': ",".join(fields),
            'language':'ja',
            'key': self.apiKey
        }
        res = requests.get(endpoint_url, params = params)
        place_details =  json.loads(res.content)
        return place_details

    def get_place_img(self, html_attributions, height, width, photo_reference):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/photo"
        params = {
            'html_attributions': html_attributions,
            'height': height,
            'width':width,
            'photo_reference': photo_reference,
            'key': self.apiKey
        }
        res = requests.get(endpoint_url, params = params)
        return res

    #移動距離/時間を取得
    def get_place_distance_time(self, origins, destinations):
        endpoint_url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        params = {
            'origins' : origins,
            'destinations': "place_id:" + destinations,
            'mode':'walking',
            'key': self.apiKey
        }
        res = requests.get(endpoint_url, params = params)
        distance_time = json.loads(res.content)
        return distance_time
    

if __name__ == '__main__':
    api = GooglePlaces("AIzaSyBQ_HzKvpdKet-T7W5o45Ozsry4clhz-6w")
    places = api.search_places_by_coordinate("35.291490, 136.799220", "300", "restaurant")
    fields = ['name', 'formatted_address', 'international_phone_number', 'website', 'rating', 'review', 'photos', 'opening_hours', 'rating']
    for place in places:
        details = api.get_place_details(place['place_id'], fields)
        try:
            website = details['result']['website']
        except KeyError:
            website = ""
 
        try:
            name = details['result']['name']
        except KeyError:
            name = ""
 
        try:
            address = details['result']['formatted_address']
        except KeyError:
            address = ""
 
        try:
            phone_number = details['result']['international_phone_number']
        except KeyError:
            phone_number = ""
 
        try:
            reviews = details['result']['reviews']
        except KeyError:
            reviews = []

        try:
            photos = details['result']['photos']
        except KeyError:
            photos = []
        try:
            opening_hours = details['result']['opening_hours']
        except KeyError:
            opening_hours = []

        try:
            rating = float(details['result']['rating'])
        except KeyError:
            rating = []

        try:
            distance_time = api.get_place_distance_time("35.291490, 136.799220", place['place_id'])
        except KeyError:
            distance_time = []
        """
        if not 'photos' in details['result']:
            photo = get_place_img(details['result']['photos'])
        except KeyError:
            photos = []
        """
        print("===================PLACE===================")
        print("Name:", name)
        print("Website:", website)
        print("Address:", address)
        print("Phone Number", phone_number)
        if opening_hours['open_now'] == True and rating > 4.0:
            print("Open now!")
        elif opening_hours['open_now'] == False:
            print("close")
        print(type(opening_hours))
        print("rating", rating)
        print("-------distance_time-------")
        #type(distance_time["rows"][0]['elements'][0]['distance']['text'])
        print("距離：{}".format(distance_time["rows"][0]['elements'][0]['distance']['text']))
        print("時間：{}".format(distance_time["rows"][0]['elements'][0]['duration']['text']))
        #print("距離：{}, 時間:{}".format(distance_time["rows"]["distance"]["text"], distance_time["rows"]["duration"]["text"]))
        #print("photos", photos)
        """
        print("==================REWIEVS==================")
        for review in reviews:
            author_name = review['author_name']
            rating = review['rating']
            text = review['text']
            time = review['relative_time_description']
            profile_photo = review['profile_photo_url']
            print("Author Name:", author_name)
            print("Rating:", rating)
            print("Text:", text)
            print("Time:", time)
            print("Profile photo:", profile_photo)
            print("-----------------------------------------")
        img = []
        """
        """
        for photo in photos:
            
            img = get_place_img(photo["html_attributions"], photo["height"], photo["width"], photo["photo_reference"])
            im = Imag.open(img)
            im.show()
            
            img.append("https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={}&key=AIzaSyBQ_HzKvpdKet-T7W5o45Ozsry4clhz-6w".format(photo["photo_reference"]))
        """
        #print(img)
        print("-----------------------------------------")