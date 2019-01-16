import urllib
import urllib.request
import urllib.error

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
        for bizModelItem in Business.objects.all().order_by('name'):
            try:
                # TODO: See if lat and long already set
                # TODO: If so, continue
                latLongItem = BusinessLatLong.objects.filter(
                    business=bizModelItem).first()
                if (latLongItem is not None
                        and latLongItem.latitude is not None
                        and latLongItem.longitude is not None):
                    print("Already have geomap info for " + bizModelItem.name +
                          ", skipping")
                    continue

                # TODO: Generate a search url base on the template above
                #   Get the full address into one string like: "address, city state zip"
                fullAddr = bizModelItem.address + " " + bizModelItem.city + " " + \
                    bizModelItem.state + " " + bizModelItem.zipcode

                fullAddr = fullAddr.strip()
                print("Searching: [" + bizModelItem.name + "] [" + fullAddr +
                      "]")
                fullAddr = fullAddr.replace(" ", "%20")

                #   replace the "{ADDRESS}" in the url template with the urlencoded address
                requestUrl = self.forwardLookupUrl.replace(
                    "{ADDRESS}", fullAddr)

                #   Convert the url into urlencoded form
                # request = urllib.parse.urlparse(requestUrl)
                # request.timeout = 5000

                # TODO: send the request to mapbox

                try:
                    mapboxResponse = urllib.request.urlopen(requestUrl)

                    # TODO: get the results (as string?)
                    responseText = mapboxResponse.read().decode("utf-8")
                    # print("[Raw]")
                    # print(responseText)
                    # print()
                    # TODO: deserialize the result string into a JSON object
                    jsonObject = json.loads(responseText)

                except urllib.error.HTTPError:
                    print(
                        "An HTTP error occured fetching and/or parsing the Mapbox \
                        request")
                    continue

                except IOError:
                    print(
                        "An IO error occured fetching and/or parsing the Mapbox \
                        request")
                    continue

                except Exception:
                    print(
                        "An unspecified error occured fetching and/or parsing the \
                        Mapbox request")
                    continue

                # TODO: parse the JSON object for the lat/long entry for the best match
                queryPlace = " ".join(jsonObject['query'])

                entries = jsonObject['features']
                if (entries is None):
                    print("Mapbox did not return a lat/long for " +
                          bizModelItem.name)
                    continue

                if (len(entries) < 1):
                    print("Mapbox did not return a lat/long for " +
                          bizModelItem.name)
                    continue

                # TODO: get the highest ranked feature by "relevance" field (for now just get the first)
                bestEntry = entries[0]
                if (bestEntry is None):
                    print("Mapbox did not return a lat/long for " +
                          bizModelItem.name)
                    continue

                # TODO: update the bizModelItem with the lat/long
                if (latLongItem is None):
                    latLongItem = BusinessLatLong()
                    latLongItem.business = bizModelItem

                print("[" + bizModelItem.name + "]")
                print("   Query: " + queryPlace)

                latLongItem.location_name = bestEntry['place_name']
                print("   Actual: " + latLongItem.location_name)

                latLongItem.relevance = bestEntry['relevance']
                print("   Relevance: " + str(latLongItem.relevance))

                latLongItem.latitude = bestEntry['center'][1]
                print("   Latitude: " + str(latLongItem.latitude))

                latLongItem.longitude = bestEntry['center'][0]
                print("   Longitude: " + str(latLongItem.longitude))

                if (latLongItem.relevance < self.minRelevance):
                    print("WARNING: Low relevance!!!!")
                    continue

                if (latLongItem.latitude < self.minLatitude
                        or latLongItem.latitude > self.maxLatitude
                        or latLongItem.longitude < self.minLongitude
                        or latLongItem.longitude > self.maxLongitude):
                    print("WARNING: Out of bounds!")
                    continue

                # TODO: Save the bizModelItem
                print("Saving entry to database...")
                latLongItem.save()
                # Continue
            except Exception:
                print("An error occured... too bad, you loose!")
                continue
