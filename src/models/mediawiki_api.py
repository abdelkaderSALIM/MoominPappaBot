"""This module represente the Wikimedia API class."""

import requests

from config import APP_NAME
from config import DATE
from config import MEDIAWIKI_API_URL


class MediawikiApi:
    """Respresents the WikiMedia API."""

    def __init__(self, latitude, longitude):
        self.api_url = MEDIAWIKI_API_URL
        self.latitude = latitude
        self.longitude = longitude
        self.content = self.get_data()

    @property
    def title(self):
        """Import data from API and give title."""
        if self.content is not None:
            return self.content.get("title")

    @property
    def description(self):
        """Import data from API and give description."""
        if self.content is not None:
            return self.content.get("extract")

    @property
    def url(self):
        """Import data from API and give url."""
        if self.content is not None:
            return self.content.get("fullurl")

    def get_data(self):
        """Import data from WikiMediaApi and return them as dictionnary."""

        parameters = {
            "action": "query",
            "prop": "extracts|info",
            "inprop": "url",
            "explaintext": True,
            "exsentences": 2,
            "exlimit": 1,
            "generator": "geosearch",
            "ggsradius": 10000,
            "ggscoord": f"{self.latitude}|{self.longitude}",
            "format": "json",
        }

        headers = {"date": DATE, "user-agent": APP_NAME}
        response = requests.get(
            self.api_url, params=parameters, headers=headers, timeout=3
        )

        if response.status_code == 200:
            content = response.json()
            if content.get("query", "") != "":
                if content.get("query").get("pages", "") != "":
                    places = content.get("query").get("pages")
                    places_list = []

                    # select the nearest place
                    for place in places:
                        # select the smallest index
                        places_list.append(
                            (
                                places.get(place).get("index"),
                                places.get(place).get("pageid"),
                            )
                        )

                    place_selected = min(places_list)
                    pageid_selected = str(place_selected[1])

                    return {
                        "title": content.get("query")
                        .get("pages")
                        .get(pageid_selected)
                        .get("title", ""),
                        "extract": content.get("query")
                        .get("pages")
                        .get(pageid_selected)
                        .get("extract", ""),
                        "fullurl": content.get("query")
                        .get("pages")
                        .get(pageid_selected)
                        .get("fullurl", ""),
                    }

        else:
            err = f"Mediawiki API : '{response.status_code}' error occurred"
            print(err)
