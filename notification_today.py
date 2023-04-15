import time

import date_type
import main
import config
import json
import windows_notify
import os
import util
from datetime import datetime

# FIX
url = config.URL
query = config.QUERY_NEXT_AIRING
var = main.TypesResponses().response_todays_anime
dir_project = os.path.dirname(os.path.realpath(__file__))


# RUNNING
def notification_windows_today():
    # RUN API
    animes = main.AnimesAiringsInfo()
    animes.post_api(url, query, var)
    animes.get_all()
    animes.union_all()

    # GET ALL ANIMES TODAY
    today_animes = animes.montado

    for animes in today_animes:
        # CONVERT TO JSON
        animes_dump = json.dumps(animes)
        animes_json = json.loads(animes_dump)

        # ANIMES INFO
        title = animes_json['title']
        next_episode = animes_json['next_episode']
        url_anilist = animes_json['site_anilist']
        url_image = animes_json['url_image']
        external_links = animes_json['external_links']
        file_name = url_image.split('/')[-1]

        # ADD EXTERNAL LINKS
        actions = windows_notify.create_actions(external_links)

        # ANIME DATE AIRING
        anime_timestamp_airing = animes['ts_date_airing']
        anime_date_airing = animes['f_date_airing']

        while True:
            time.sleep(1)
            # GET DATETIME IN TIMEZONE America/Sao_Paulo
            # COMMENT FOR TEST USING TIME OF WINDOWS
            # datetime_now = util.get_datetime_sao_paulo()
            # TIME OF WINDOWS
            datetime_now = datetime.now()

            # REMOVE SECONDS AND CONVERT TO TIMESTAMP
            pop_seconds = util.format_date(datetime_now, date_type.Datetime1)
            to_datetime = datetime.strptime(pop_seconds, date_type.Fdatetime1)
            now_timestamp = util.date_to_timestamp(str(to_datetime))

            if anime_timestamp_airing <= now_timestamp:

                if anime_timestamp_airing < now_timestamp:
                    print(f' - Anime: {title}\n - Aired on: {anime_date_airing}\n')
                    break

                # DOWNLOAD IMAGE ANIME
                path_image = util.download_image(url_image, f'{dir_project}\\img', file_name)

                windows_notify.new_ep_notification(
                    title=title,
                    episode=next_episode,
                    image_anime=path_image[1],
                    url_anilist=url_anilist,
                    action_sites=actions
                )

                # NOT REMOVE IF IMAGE IS DEFAULT
                if path_image[0]:
                    time.sleep(3)
                    os.remove(path_image[1])

                break

            print(f' - Current time:   {datetime_now}')
            print(f' - Next release:   {anime_date_airing}\n')
            time.sleep(2)


notification_windows_today()
