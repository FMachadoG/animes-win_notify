import winsdk.windows.ui.notifications as notifications
import winsdk.windows.data.xml.dom as dom
import os

# notification as string
tString = r"""
<toast scenario="incomingCall">
	<visual>
		<binding template="ToastGeneric" >
			<text hint-callScenarioCenterAlign="true">{title}</text>
			<text hint-callScenarioCenterAlign="true">Episode {episode} aired.</text>
			<image src="{image_anime}"/>
			<group>
                <subgroup>
                    <text hint-style="captionSubtle">By: fmachadog | AniList.co</text>
                </subgroup>
			</group>
		</binding>
	</visual>
	<actions>
        {action_sites}
		<action 
			content="AniList" 
			imageUri="D:\Filipe\Projetos\test\img\anilist_logo_icon_247617.png" 
			activationType="protocol" 
			arguments="{url_anilist}"/>
		<action 
			content="Cancel" 
			arguments=""/>
	</actions>
</toast>
"""

dir_project = os.path.dirname(os.path.realpath(__file__))


def insert_action(name_site, logo_site, url_site):
    string = r'<action ' \
             r'content="{name_site}" ' \
             r'imageUri="{logo_site}" ' \
             r'activationType="protocol" ' \
             r'arguments="{url_site}"' \
             r'/>'
    action = string.format(
        name_site=name_site,
        logo_site=logo_site,
        url_site=url_site
    )

    return action


def new_ep_notification(
        title: str,
        episode: int,
        image_anime: str,
        url_anilist: str,
        action_sites: list = None):
    app = '{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\\WindowsPowerShell\\v1.0\\powershell.exe'

    actions = ''
    if action_sites is not None:
        for action in action_sites:
            actions += action

    # create notifier
    nManager = notifications.ToastNotificationManager
    notifier = nManager.create_toast_notifier(app)

    # convert notification to an XmlDocument
    tString2 = tString.format(
        title=title,
        episode=episode,
        image_anime=image_anime,
        url_anilist=url_anilist,
        action_sites=actions
    )
    xDoc = dom.XmlDocument()
    xDoc.load_xml(tString2)

    # display notification
    notifier.show(notifications.ToastNotification(xDoc))


def create_actions(external_links: list) -> list[str]:
    """ Create actions buttons for streaming using metod insert_action

    :type external_links: object
    :return list[str]
    """
    # CREATE ACTION STREAMER
    dir_images_sites = f'{dir_project}\\img\\streaming-logo'

    streaming = ['Crunchyroll', 'Netflix', 'Bilibili TV']
    actions = []
    anime_streaming = [li for li in external_links if li['site'] in streaming]

    for site in anime_streaming:
        name_image = site["site"].lower().replace(' ', '_')
        image_streaming = f'{dir_images_sites}\\{name_image}_logo_icon.png'

        if len(anime_streaming) == 3 and site['site'] == streaming[0]:
            short_cruchy_action = insert_action(
                'Crunch', image_streaming, site['url'])

            actions.append(short_cruchy_action)

        else:
            site_action = insert_action(
                site['site'], image_streaming, site['url'])

            actions.append(site_action)

    return actions
