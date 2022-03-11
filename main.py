import requests
import json
apikey = 'YOUR_API_KEY'
payload={}
headers = {}
class Place:

    def __init__(self,link):
        self.link = link
        coord = link[link.find('@')+1:].split(',')
        self.lat = coord[0]
        self.lng = coord[1]

    
class Route:

    def __init__(self,places,origin):
        self.places = places
        self.origin = origin    

    def calculate_route_all(self):

        def calculate_route(origin,places):
            #calculate the route

            def calculate_places(place,place2):
                #calculate distance between two places
                url = f"https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={place.lat},{place.lng}&destinations={place2.lat},{place2.lng}&key={apikey}"
                response = requests.request("GET", url, headers=headers, data=payload)
                distance = response.json()['rows'][0]['elements'][0]['distance']['value']
                return distance

            nearest = -1
            for i in places:
                if nearest == -1:
                    nearest = calculate_places(origin,i)
                    nearest_i = i
                else:
                    aux = calculate_places(origin, i)
                    if (nearest > aux):
                        nearest = aux
                        nearest_i = i
            return nearest_i

        #calculate the route for all places
        #first route to calculate is the origin
        sorted_route =[calculate_route(self.origin,self.places)]
        self.places.remove(sorted_route[0])
        #now calculate the rest of the route
        for i in self.places:
            sorted_route.append(calculate_route(sorted_route[-1],self.places))
            self.places.remove(sorted_route[-1])

        self.places=sorted_route

    def generate_link(self):
        #generate the link for the route
        link = f'https://www.google.com/maps/dir/{self.origin.lat},{self.origin.lng}/'
        for i in self.places:
            link = link + i.lat + ',' + i.lng + '/'
        link = link[:-1]
        return link

place1= Place('https://www.google.com/maps/@-34.9517847,-57.9799734,20.79z')
place2 = Place('https://www.google.com/maps/@-34.8950067,-57.9312336,19z')
place3 = Place('https://www.google.com/maps/@-34.9464345,-57.9753363,18.5z')
place4 = Place('https://www.google.com.ar/maps/@-34.9232599,-57.9722255,20z')
place5 = Place('https://www.google.com.ar/maps/@-34.9254204,-57.9475397,19.58z')
place6 = Place('https://www.google.com.ar/maps/@-34.9060248,-57.9573246,19.04z')
place7 = Place('https://www.google.com.ar/maps/@-34.9391617,-57.9624341,18.21z')
place8 = Place('https://www.google.com.ar/maps/@-34.8965315,-57.9325349,19.67z')
place9 = Place('https://www.google.com.ar/maps/@-34.8659175,-57.9129162,21z')
place10 = Place('https://www.google.com.ar/maps/@-34.9006942,-57.9511314,19.92z')
route = Route([place2,place3,place4,place5,place6,place7,place8,place9,place10],place1)
route.calculate_route_all()
print(route.generate_link())