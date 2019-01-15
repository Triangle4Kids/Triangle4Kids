import urllib
import urllib.request
from bs4 import BeautifulSoup
from core.models import Event


class CParentEventScraper(object):
    eventDirectoryUrl = "http://www.carolinaparent.com/CP/Calendar/index.php/name/A-Year-of-Birding-at-Yates-Mill-Pond/event/34948/"
    pageIndex = 0  # Just a hint for debugging, not required
    listingIndex = 0  # Just a hint for debugging, not required

    # Main entry point to run the event scraper for CParent
    def Run(self):
        # Event model objects
        eventList = []

        classList = self.getEventBizList()
        for event in eventList:
            eventList.append(camp)

        # Get more biz entries from other directories if you have time...
        # sportList=self.getSportBizList()
        # for sportBiz in sportList:
        #     self.bizList.append(sportBiz)

        # Now just call Save to commit the changes to the database
        print("Don't save to db yet...")
        self.Save(eventList)

    def getEventBizList(self):
        eventBizList = []
        print("[Getting CParent Event Listings]")
        pageUrl = self.campDirectoryUrl

        while pageUrl != "":
            self.pageIndex = self.pageIndex + 1
            print("Requesting Page " + str(self.pageIndex))
            # get the full page source
            response = urllib.request.urlopen(pageUrl)
            pageHtml = response.read()

            if (pageHtml is None):
                print("Failed to retrieve page")
                return

            pageBizModelList = self.ParseCampPage(pageHtml)

            for pageCamp in pageBizModelList:
                campBizList.append(pageCamp)

            # TODO: check to see if this is the last page
            pageUrl = self.GetNextPageUrl(pageHtml)
            # END OF WHILE LOOP

        # Return the list of biz Names from all pages
        return campBizList

    def GetNextPageUrl(self, pageHtml):
        nextPageUrl = ""

        #Create a new parser for the page content that was passed to us
        soup = BeautifulSoup(pageHtml, "html.parser")

        #Find the listings element (use find, there should only be one!)
        # paginationTag = soup.find("div", {"class": "pagination"})
        nextPageLinkTag = soup.find("a", {"class": "afteractive"})
        if (nextPageLinkTag is None):
            print("No pagination tag found on page " + str(self.pageIndex))
        else:
            nextPageUrl = str(nextPageLinkTag['href'])
            # TODO: Parse the pageHtml for the next page url in the pagination div
            print("TODO: implement parsing of pagination for next page url")

        return nextPageUrl

    # Returns a list of biz on the Page
    def ParseCampPage(self, pageHtml):
        currentCampPageBizList = []

        contentLength = len(pageHtml)
        if (contentLength == 0):
            print("No content provided, skipping page")
            return currentCampPageBizList

        # Get a list of the biz entry HTML on the page
        pageCampListings = self.GetPageCampListings(pageHtml)
        self.listingIndex = 0
        # Loop through all the entries on the page
        # and parse each one to create a business model object
        for listingTag in pageCampListings:
            self.listingIndex = self.listingIndex + 1
            bizModel = self.ParseListing(listingTag)
            if (bizModel is not None):
                currentCampPageBizList.append(bizModel)

        # Return the list of biz Names from the current page
        return currentCampPageBizList

    # This should get the HTML for each "biz entry on the page"
    def GetPageCampListings(self, pageHtml):
        contentLength = len(pageHtml)
        if (contentLength == 0):
            print("No page content provided, skipping page")
            return []

        print("Parsing camp listings from page " + str(self.pageIndex) +
              " content: " + str(contentLength) + " bytes")

        #Create a new parser for the page content that was passed to us
        soup = BeautifulSoup(pageHtml, "html.parser")

        #Reset listing to 0 since we are starting a new page
        self.listingIndex = 0

        #Find the listings element (use find, there should only be one!)
        listingElement = soup.find("ul", {"class": "listings"})
        if (listingElement is None):
            print("Listings not found on page " + self.pageIndex)
            return []

        listingContent = listingElement.contents
        contentLength = len(listingContent)
        print("[Page listing: " + str(contentLength) + " bytes")

        listings = listingElement.find_all("li")
        listingCount = len(listings)
        if (listingCount == 0):
            print("No listings found in listing container on " +
                  self.EntryName())
            return []

        print("Found " + str(listingCount) + " listings...")
        return listings

    # Parse a listing entry and return either a new or updated database entry
    def ParseListing(self, listingTag):
        bizModel = None

        print("[Parsing Listing]")
        # First get the info from the element with the class "business-name":
        # <h4 class="business-name">
        #     <a
        #         href="http://www.carolinaparent.com/CP/Camp-Listings/index.php/name/Biomedicine-Bots-Computing-Engineering-STEM-for-Kids/listing/58765/"
        #         target="_top" class="geobaselink" onclick="geobase_tracker.track('58765','clickthrough')">
        #         Biomedicine, Bots, Computing &amp; Engineering - STEM for Kids
        #     </a>
        # </h4>

        #print(listingTag.contents)

        bizHeaderTag = listingTag.select(".business-name")[0]
        if (bizHeaderTag is None):
            print("Can't find business header for Listing ")
            return bizModel

        bizDataTag = listingTag.select(".data")[0]
        if (bizDataTag is None):
            print("Can't find business data for Listing ")
            return bizModel

        if (bizHeaderTag.a is None):
            print("Can't find business Link for Listing ")
            return bizModel

        listingName = bizHeaderTag.a.string
        print("BusinessName: " + listingName)

        # query the db to find an existing record with the current campName
        bizModel = Business.objects.filter(name=listingName).first()

        if (bizModel is None):
            print("No existing database entry found for: [" + listingName +
                  "], creating new item")
            bizModel = Business()
            bizModel.name = listingName

        cpLink = bizHeaderTag.a['href']
        bizLink = self.GetLinkFromDetailPage(cpLink)
        if (bizModel.link != bizLink):
            bizModel.link = bizLink

        addressLines = bizDataTag.select(".address1")

        address = ""
        if (addressLines is not None):
            for addrLine in addressLines:
                address = address + " " + str(addrLine.string)
            if (address != bizModel.address):
                bizModel.address = address

        cityLine = str(bizDataTag.select(".city")[0].string)
        if (cityLine is not None):
            # TODO: Parse city line:
            # City line may have zero, one or more of "city, state zip"
            # split out city, state and zip from this cityLine
            city = ""
            state = ""
            zipcode = ""

            if (city != bizModel.city):
                bizModel.city = city
            if (state != bizModel.state):
                bizModel.state = state
            if (zipcode != bizModel.zipcode):
                bizModel.zipcode = zipcode

        phone = bizDataTag.select(".phone")[0]
        if (phone is not None):
            phoneString = str(phone.string)
            if (phoneString != bizModel.phone):
                bizModel.phone = phoneString

        # # todo: add country to business model
        country = bizDataTag.select(".country")[0]
        if (country is not None):
            country = country.string
            if (country == ""):
                country = "USA"
            # TODO: Add country to Business Model
            # if (country != bizModel.country):
            #     bizModel.country=country

        categoryList = []
        categoriesDiv = bizDataTag.select(".categories")[0]
        if (categoriesDiv is not None):
            catSpan = categoriesDiv.select("span")[1]
            if (catSpan is not None):
                categoryText = str(catSpan.string).strip()
                categoryList = categoryText.split(",")
            else:
                print("No categories found for " + bizModel.name)
        bizModel.categories = ', '.join([str(x) for x in categoryList])

        bizModel.slug = bizModel.name.replace(" ", "_")
        print("[" + self.EntryName() + "]")
        print("   Name: " + bizModel.name)
        print("   Link: " + bizModel.link)
        print("   Phone: " + str(bizModel.phone))
        print("   Address: " + bizModel.address)
        print("   City: " + bizModel.city)
        print("   Slug: " + bizModel.slug)
        print("   Categories: " + bizModel.categories)
        print("")
        # We are done, just return the biz object
        return bizModel

    def GetLinkFromDetailPage(self, cpDetailLink):
        # Go get the html for the detail page
        # find the link and return it
        # <a href="http://www.trianglerockclub.com/morrisville/youth/track-out-camps/"
        # target="_new"
        # class="geobaselink"
        # onclick="geobase_tracker.track('58133','weblinkclick')">www.trianglerockclub.c...</a>
        response = urllib.request.urlopen(cpDetailLink)
        pageHtml = response.read()
        docTag = BeautifulSoup(pageHtml, "html.parser")
        linkElements = docTag.find_all("a", {"class": "geobaselink"})
        linkCount = len(linkElements)
        if (linkCount == 0):
            # linkElements = docTag.find_all([0].strong, {"href"})
            print("Can't find a public link for the biz")
            return cpDetailLink
        elif (linkCount > 1):
            print(
                "Got multiple elements to choose from, Norman, please compute..."
            )
            return cpDetailLink
        else:
            return str(linkElements[0]['href'])

    def Save(self, bizModelList):
        # Do duplicate
        savedNames = []
        newItems = 0
        updatedItems = 0
        skippedItems = 0

        for bizModel in bizModelList:
            if bizModel.name not in savedNames:
                if (bizModel.pk == 0):
                    newItems = newItems + 1
                else:
                    updatedItems = updatedItems + 1
                bizModel.save()
                savedNames.append(bizModel.name)
            else:
                print("Skipping previously saved biz: " + bizModel.name)
                skippedItems = skippedItems + 1

        print("New Listings: " + str(newItems))
        print("Updated Listings: " + str(updatedItems))
        print("Duplicate names skipped: " + str(skippedItems))

    def EntryName(self):
        return "Entry[" + str(self.pageIndex) + "][" + str(
            self.listingIndex) + "]"