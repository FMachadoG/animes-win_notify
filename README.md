## Windows Notify - Animes
Project for personal study, create in `Python`, 
with request in [Anilist GraphQL API](https://github.com/AniList/ApiV2-GraphQL-Docs)
and notofication using [Microsoft Toast notification](https://learn.microsoft.com/en-us/windows/apps/design/shell/tiles-and-notifications/toast-ux-guidance)

## About
When running the project, it will request the animes that will be released today. 
Depending on the time, it will inform in the terminal that the anime has already aired and will wait until the time of the next release.
When the time "hits", it will notify on Windows.
<br><br>
When the available streaming button is clicked, you will be redirect to the anime streaming site. 
The button site AniList will always be informad, redirect to anime AniList site.

## Example
```bash
(venv) ~> python notification_today.py
```
#### Images
<div style="align-items: center; float: left;">
  <img src="/img/doc/terminal_info.png" alt="Terminal informations." style="float: left; padding: 5px; height: 250px;"/>
  <img src="/img/doc/notify_dr_stone_ep2.png" alt="Windows notification Dr. Stone Ep 2" style="float: left; padding: 5px; height: 250px;"/>
  <img src="/img/doc/notify_bojji_ep1.png" alt="Windows notification Ousama Ranking Ep 1" style="float: left; padding: 5px; height: 250px;"/>
</div>

#### Video
https://vimeo.com/817997238
