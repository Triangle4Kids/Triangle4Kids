import urllib
import urllib.request
import json
from core.models import Business, BusinessLatLong


class BizLatLong(object):
    forwardLookupUrl = "https://api.mapbox.com/geocoding/v5/mapbox.places/{ADDRESS}.json?access_token=pk.eyJ1IjoidHJpYW5nbGU0a2lkcyIsImEiOiJjanFubWRwMGw3a2hjNGFtc3RrMWQ4OXl5In0.eZj0i5qyOBlmeY2oH6LWow"
    # e.g. https://api.mapbox.com/geocoding/v5/mapbox.places/1515%205th%20Ave%20Nashville%20TN%2037208.json?access_token=pk.eyJ1IjoidHJpYW5nbGU0a2lkcyIsImEiOiJjanFubWRwMGw3a2hjNGFtc3RrMWQ4OXl5In0.eZj0i5qyOBlmeY2oH6LWow
    maxLatitude = 36.3
    minLatitude = 35.5
    maxLongitude = -78.3
    minLongitude = -79.1
    minRelevance = .8

    #Raleigh: -78.6391,35.7804
    pageIndex = 0  # Just a hint for debugging, not required
    listingIndex = 0  # Just a hint for debugging, not required

    # Main entry point to run the LatLog Updater
    def Run(self):
        testRunCount = 1
        i = 0
        for bizModelItem in Business.objects.all().order_by('name'):
            i = i + 1
            if (i > testRunCount):
                return

            # TODO: See if lat and long already set
            # TODO: If so, next
            latLongItem = BusinessLatLong.objects.filter(
                business=bizModelItem).first()
            if (latLongItem is not None and latLongItem.latitude is not None
                    and latLongItem.longitude is not None):
                next

            # TODO: Generate a search url base on the template above
            #   Get the full address into one string like: "address, city state zip"
            fullAddr = bizModelItem.address + " " + bizModelItem.city + " " + \
                bizModelItem.state + " " + bizModelItem.zipcode

            fullAddr = fullAddr.strip().replace(" ", "%20")
            print("Searching: [" + fullAddr + "]")

            #   replace the "{ADDRESS}" in the url template with the urlencoded address
            requestUrl = self.forwardLookupUrl.replace("{ADDRESS}", fullAddr)

            #   Convert the url into urlencoded form
            # request = urllib.parse.urlparse(requestUrl)
            # request.timeout = 5000

            # TODO: send the request to mapbox

            mapboxResponse = urllib.request.urlopen(requestUrl)

            # TODO: get the results (as string?)
            responseText = mapboxResponse.read().decode("utf-8")
            # print("[Raw]")
            # print(responseText)
            # print()
            # TODO: deserialize the result string into a JSON object
            jsonObject = json.loads(responseText)
            # tmp = json.dumps(jsonObject)
            # print("[Dump]")
            # print(tmp)

            # TODO: parse the JSON object for the lat/long entry for the best match
            # TODO: get the highest ranked feature by "relevance" field (for now just get the first)
            #
            queryPlace = " ".join(jsonObject['query'])

            bestEntry = jsonObject['features'][0]
            if (bestEntry is None):
                print("Mapbox did not return a lat/long for " +
                      bizModelItem.name)
                next

            print("[" + bizModelItem.name + "]")
            print("   Query: " + queryPlace)

            actualPlace = bestEntry['place_name']
            print("   Actual: " + actualPlace)

            relevance = bestEntry['relevance']
            print("   Relevance: " + str(relevance))

            latitude = bestEntry['center'][1]
            print("   Latitude: " + str(latitude))

            longitude = bestEntry['center'][0]
            print("   Longitude: " + str(longitude))

            if (relevance < self.minRelevance):
                print("WARNING: Low relevance!!!!")
                next

            if (latitude < self.minLatitude or latitude > self.maxLatitude
                    or longitude < self.minLongitude
                    or longitude > self.maxLongitude):
                print("WARNING: Out of bounds!")
                next

            # TODO: update the bizModelItem with the lat/long
            if (latLongItem is None):
                latLongItem = BusinessLatLong()
                latLongItem.business = bizModelItem

            latLongItem.latitude = latitude
            latLongItem.longitude = longitude

            return
            # TODO: Save the bizModelItem
            latLongItem.save()
            # Next
