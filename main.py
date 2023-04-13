from datetime import datetime
import requests
import json

import config
import date_type
import util


class TypesResponses:
    def __init__(self):
        self.variable = {}

    @property
    def response_todays_anime(self):
        # GET DATE TODAY AND SUM 1
        datetime_now = datetime.now()
        datetime_plus1 = util.datetime_now_sum_days(datetime_now, 1)

        # CONVERT TO DATE
        date_now = datetime_now.date()
        date_plus1 = datetime_plus1.date()

        # CONVERT TO DATETIME
        datetime_now = datetime.combine(date_now, datetime.min.time())
        datetime_plus1 = datetime.combine(date_plus1, datetime.min.time())

        # GET TIMESTEMP
        airingat_greater = util.date_to_timestamp(str(datetime_now))
        airingat_lesser = util.date_to_timestamp(str(datetime_plus1))

        # GET CONFIG
        # url = config.URL
        # query = config.QUERY_NEXT_AIRING
        # var = config.VARIABLES_NEXT_AIRING

        # CHANGING VARIABLES
        self.variable |= {
            "airingAt_greater": airingat_greater,
            "airingAt_lesser": airingat_lesser
        }

        return self.variable


class AnimesAiringsInfo:
    def __init__(self):
        self.response = None
        self.base = None
        self.titles = []
        self.episode = []
        self.date_airing_formatted = []
        self.date_airing_timestamp = []
        self.site_anilist = []
        self.external_links = []
        self.url_image = []
        self.montado = []

    def post_api(self, al_url, al_query, al_variables: TypesResponses):
        self.response = requests.post(
            al_url,
            json={'query': al_query, 'variables': al_variables}
        )

        if not self.response.status_code == 200:
            error = self.response.json()
            return False, error

        # response_json = json.dumps(response_todays_anime.json())

        return self.response

    @property
    def _base_return_json(self):
        response = json.dumps(self.response.json())
        response = json.loads(response)

        self.base = response['data']['Page']['airingSchedules']

        return self.base

    def get_titles(self):
        base = self._base_return_json

        for titles in base:
            self.titles.append(titles['media']['title']['romaji'])

    def get_episodes(self):
        base = self._base_return_json

        for episode in base:
            self.episode.append(episode['episode'])

    def get_date_airing_formatted(self):
        base = self._base_return_json

        for date_airing_formatted in base:
            time_stamp = date_airing_formatted['airingAt']

            date = util.timesmap_to_date(time_stamp,
                                         config.TIME_ZONE)
            datenow_formated = datetime.strftime(date, date_type.Fdatetime2)

            self.date_airing_formatted.append(datenow_formated)

    def get_date_airing_timestamp(self):
        base = self._base_return_json

        for date_airing_timestamp in base:
            time_stamp = date_airing_timestamp['airingAt']

            self.date_airing_timestamp.append(time_stamp)

    def get_site_anilist(self):
        base = self._base_return_json

        for site_anilist in base:
            path_site_anilist = site_anilist[
                'media']['siteUrl']

            self.site_anilist.append(path_site_anilist)

    def get_url_image(self):
        base = self._base_return_json

        for url_image in base:
            path_url_image = url_image[
                'media']['coverImage']['extraLarge']

            self.url_image.append(path_url_image)

    def get_external_links(self):
        base = self._base_return_json

        for links in base:
            self.external_links.append(links['media']['externalLinks'])

    def get_all(self):
        self.get_titles()
        self.get_episodes()
        self.get_date_airing_formatted()
        self.get_date_airing_timestamp()
        self.get_site_anilist()
        self.get_url_image()
        self.get_external_links()

    def union_all(self):
        animes_airing = [
            self.titles,
            self.episode,
            self.date_airing_formatted,
            self.date_airing_timestamp,
            self.site_anilist,
            self.url_image,
            self.external_links
        ]

        for enum, (ti, ep, fdt, tsdt, snl, uimg, el) in enumerate(
                zip(*animes_airing), start=0):

            self.montado.append(
                {
                    "enum": enum,
                    "title": ti,
                    "next_episode": ep,
                    "f_date_airing": fdt,
                    "ts_date_airing": tsdt,
                    "site_anilist": snl,
                    "url_image": uimg,
                    "external_links": el
                }
            )
