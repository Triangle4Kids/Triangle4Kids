import requests
from bs4 import BeautifulSoup
from core.models import Business


class CParentBizScraper(object):
    campDirectoryUrl = 'http://www.carolinaparent.com/CP/Camp-Listings/index.php?'
    sportDirectoryUrl = 'http://www.carolinaparent.com/CP/Sports-Fitness/'

    # Main entry point to run the scraper for CParent
    def Run(self):
        # Business model objects
        bizList = [
            'name',
            'address',
            'city',
            'phone',
            'link',
        ]

        campList = self.getCampBizList()
        for camp in campList:
            bizList.append(camp)

        # Get more biz entries from other categories if you have time...
        # sportList=self.getSportBizList()
        # for sportBiz in sportList:
        #     self.bizList.append(sportBiz)

        # Now just call Save to commit the changes to the database
        self.Save(bizList)

    def getCampBizList(self):
        campBizList = []

        pageUrl = self.campDirectoryUrl

        while pageUrl != "":
            #get the full page source
            pageHtml = requests.get(pageUrl).text

            pageCamps = self.ParseCampPage(pageHtml)

            for pageCamp in pageCamps:
                campBizList.append(pageCamp)

                # TODO: check to see if this is the last page
                pageUrl = self.GetNextPageUrl(pageHtml)

            # END OF WHILE LOOP

        # Return the list of biz Names from all pages
        return campBizList

    def GetNextPageUrl(self, pageHtml):
        nextPageUrl = ""

        # TODO: Parse the pageHtml for the next page url in the pagination div
        # ...

        return nextPageUrl

    # Returns a list of biz on the Page
    def ParseCampPage(self, pageHtml):
        currentCampPageBizList = []

        # Get a list of the biz entry HTML on the page
        pageEntrySourceList = self.GetPageCampEntrySources(pageHtml)

        # Loop through all the entries on the page
        # and parse each one to create a business model object
        for entrySource in pageEntrySourceList:
            bizModel = self.ParseCampEntry(entrySource)
            if (bizModel is not None):
                currentCampPageBizList.append(bizModel)

        # Return the list of biz Names from the current page
        return currentCampPageBizList

    # This should get the HTML for each "biz entry on the page"
    def GetPageCampEntrySources(self, pageSource):
        pageEntrySources = []
        # soup = BeautifulSoup(pageSource, 'lxml')
        # listing = soup.find(id="listing0")

        # TODO: Parse the page source and for each biz you find, append
        # TODO: it to pageEntrySources

        return pageEntrySources

    # This should get the HTML for each "biz entry on the page"
    # It will populate a Business model object with the information
    # and return it.
    # If the parsing fails, return a "None" (empty) Business
    def ParseCampEntry(self, entrySource):

        campName = ""
        # TODO: Parse the HTML source for the name of the camp and update campName
        #
        #
        # campName="What I found"

        if campName == "":
            return None

        # query the db to find an existing record with the current campName
        bizModel = Business.objects.filter(Name=campName).First()
        if (bizModel is None):
            bizModel = Business()
            bizModel.name = campName

        # Now get other biz info and add it to the bizModel
        # TODO: Get the current address for the biz
        # Set the address info you found
        bizModel.address = "the address"
        bizModel.city = "the city"

        # TODO: Get phone
        bizModel.phone = ""

        # TODO: Get link
        bizModel.link = ""

        # ...

        # We are done, just return the biz object
        return bizModel

    def Save(self, bizList):
        for biz in bizList:
            biz.Save()
