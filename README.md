# data-in-the-wild

### Team Members: 
Andreas Belsager (abel@itu.dk), Mads Høgenhaug (mkrh@itu.dk), Marcus Friis (mahf@itu.dk) & Mia Pugholm (mipu@itu.dk)

### Introduction
Many TV-shows go on for many seasons.  Meanwhile, other shows are canceled almost immediately. This begs the question: what is the relationship between a tv show getting more seasons, its ratings over time and its initial reception. 

### Motivation
We’ve probably all had a well-liked TV show that has been canceled, while other TV shows are able to continue on to the 20th season. We want to investigate why this happens to shows, based on the general consensus surrounding these series, as well as looking to which degree the number of years a series has run affects the likeliness of the show continuing or being canceled. Additionally, we investigate the relationship between the initial reaction to a series and its following rating.

### Methodology
We consider a TV-show to be “successful” when a TV-show makes it to the final season and unsuccessful when it gets canceled. To figure out when shows are canceled or make it to the final season, we will scrape data from “Etonline”, which composes lists of canceled & final-season tv-shows.
We’ll scrape rating counts from IMDb, using their API. Furthermore, we collect reactions to the official trailer of shows from YouTube to estimate the public reaction to the announcement. We do this by looking at likes, views, dislikes from “ReturnYoutubeDislike”, ratios, comments, comment sentiments and more. This requires sentiment analysis of YouTube comments. We’ll also collect data from “ReturnYoutubeDislike”, which estimates the number of dislikes on a Youtube video. 

Overall, we limit ourselves to shows from 2018 and forward, to restrain the scope of the project and since “etonline” does not contain older data.  

### Data sources
To do this project, we pull data from:
IMDb → Ratings, number of seasons
YouTube → Initial reaction, views, likes, comments, sentiments
Etonline → List of renewed/canceled/final season tv-shows. 
ReturnYoutubeDislike → Estimated dislikes for Youtube videos. 


### Potential challenges (both technical and societal/ethical)
One of the biggest challenges will be to map each show to their official announcement trailer. This is easy to do manually, but to automate the process will be challenging. Plan b is to use data from Twitter instead, sorting for tweets that were written before the show aired. This can function similarly. 

Another challenge will be mapping the renewal status of a show to the appropriate season. We might need to find a new data source for renewal status. Fin.
