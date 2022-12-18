# data-in-the-wild

### Team Members: 
Andreas Belsager (abel@itu.dk), Mads Høgenhaug (mkrh@itu.dk), Marcus Friis (mahf@itu.dk) & Mia Pugholm (mipu@itu.dk)

# Overview
This project is split up into 3 main parts:
1. Data collection
2. Data wrangling and processing
3. Data analysis

This readme documents which files are responsible for what parts, and how to replicate our results. For a full project 
overview, see [Project Overview](#project-overview)


## Data collection
If you don't want to collect data yourself, see the [data folder](data)
Data collection can be broken up into 2 parts:

### Scrape YouTube data
There are 2 different kinds of data that needs to be scraped from YouTube: trailer video data and comments.
These can both be collected with the [*youtube_api*](/tree/main/src/youtube_api) module. To start off, you first need one or more YouTube 
API key, which should be stored in the [*config.ini*](/blob/main/src/config.ini) file as such:

```
[DEFAULT]
key1=YOUR_API_KEY
key2=YOUR_API_KEY_2
        .
        .
        .
keyn=YOUR_API_KEY_n
```

It is recommended to have multiple keys, since searching for YouTube videos quickly use up the _____ credits?? \reference
Once [*config.ini*](/blob/main/src/config.ini) has keys, you can collect trailers and comments with [*main.py*](/blob/main/src/main.py) from the root as 
>python main.py

This will by default collect all YouTube videos listed with "trailer" from the official channels of Amazon, Disney, 
HBO and Netflix, and output each file in *[data/raw/trailers/](/tree/main/data/raw/trailers)* and [*data/raw/comments/*](/tree/main/data/raw/comments)

### Download IMDb data


# [Project Overview](#project-overview)
The following describes all files within this project, their purpose and their location.
```
│
├───data                                            <- Directory for all data used in the project
│   ├───external                                    <- Directory for all data from external sources
│   │   └───imdb                                    <- Directory for IMDb data, the contents should be downloaded
│   │       ├───IMDbREADME.md                       <- README detailing how to get the data and which files specifically 
│   │       ├───title.basics.tsv        
│   │       └───title.ratings.tsv       
│   │       
│   ├───interim                                     <- Directory for all files that aren't raw or fully processed
│   │   │   ├───annotated.csv                       <- All raw data annotations, outputted from Label-Studio
│   │   │   ├───annotated_aggregate.csv             <- Aggregate of annotated.csv, aggregates all annotations per comment into one
│   │   │   ├───match.csv                           <- File for joining IMDb data with YouTube trailer data, composite file of the files found in /match 
│   │   │   ├───release_dates.csv                   <- Release dates scraped from IMDb with imdbscraper
│   │   │   └───trailers.csv                        <- All collected trailers with non-trailers removed
│   │   │       
│   │   ├───match                                   <- Directory for all match.csv files needed for join IMDb and YouTube
│   │   │   ├───amazon_match.csv        
│   │   │   ├───disney_match.csv        
│   │   │   ├───hbo_match.csv       
│   │   │   └───netflix_match.csv       
│   │   │       
│   │   └───trailers                                <- Directory for all processed trailer files for each network, used to create trailers.csv
│   │       ├───amazon.csv      
│   │       ├───disney.csv      
│   │       ├───hbo.csv     
│   │       └───netflix.csv     
│   │       
│   ├───processed                                   <- Directory for final processed dataset
│   │   ├───ProcessedREADME.md                      <- README detailing how to get full dataset
│   │   └───data.csv                                <- File to download from README link
│   │       
│   └───raw                                         <- Directory for all unprocessed data
│       ├───returnyoutubedislikes.csv               <- Data collected with Return YouTube Dislikes API
│       ├───trailers.csv                            <- Trailers collected with youtubevideogetter.py for netflix, disney, amazon and hbo
│       │       
│       ├───comments                                <- Directory for all raw comment data
│       │   ├───amazon_comments.csv     
│       │   ├───disney_comments.csv     
│       │   ├───hbo_comments.csv        
│       │   └───netflix_comments.csv        
│       │       
│       └───trailers                                <- Directory for all composite trailer files, collected with youtubevideogetter.py
│           ├───amazon_trailers.csv      
│           ├───disney_trailers.csv      
│           ├───hbo_trailers.csv     
│           └───netflix_trailers.csv     
│       
├───notebooks                                       <- Directory for all Jupyter Notebooks
│   ├───drafts                                      <- Directory for notebooks used in the process of creating this project
│   │   ├───analysis.ipynb      
│   │   ├───annotation_analysis.ipynb       
│   │   ├───hbo_analysis.ipynb      
│   │   ├───imdb_scraper.ipynb      
│   │   ├───movie_trends.ipynb      
│   │   └───utubetest.ipynb     
│   │       
│   └───reports                                     <- Directory for all finished notebooks, some produce results used in the report
│       ├───data_cleaning.ipynb     
│       ├───data_merging.ipynb                      <- Notebook for putting all composite files together and joining all the data together to form the final data.csv
│       ├───EDA.ipynb                               <- Light exploratory data analysis
│       ├───ReturnYouTubeDislikesAnalysis.ipynb     <- Notebook for exploring Return YouTube Dislike data
│       ├───return_youtube_dislikes.ipynb           <- Notebook for collecting Return YouTube Dislike data
│       ├───scatter_relation.ipynb                  <- Notebook for creating one of the main plots
│       ├───stat_test.ipynb                         <- Notebook for testing the statistical significance of sentiment prerelease
│       └───timeseries_analysis.ipynb               <- Notebook for creatin main timeseries plot
│
├───reports                                         <- Directory for all things used for the paper
│   │   ├───annotation_guide.tex                    <- Annotation guide describing the guidelines for the annotation process
│   │   ├───main.tex                                <- Main LaTeX file for the paper
│   │   ├───paper.pdf                               <- Finalized paper in PDF format
│   │   └───references.bib                          <- References of the paper
│   │
│   └───figs                                        <- Directory for figures of the repo and paper
│       ├───aamatrix.svg                            <- Annotator agreement matrix
│       ├───discourse_time.svg                      <- Sentiment over time for "good" and "bad" trailers
│       ├───likedislike_sentiment_scatter.svg       <- Relationship between like-dislike-ratio and IMDb rating
│       ├───sentiment_rating_scatter.svg            <- Scatterplot of average sentiment and IMDb rating
│       ├───stat_hist.svg                           <- Histogram of ratings for statistical significance test
│       ├───trailer_comment_dist.svg                <- Plots for visualizing the number of comments per trailer
│       └───trailer_dist.svg                        <- Number of collected trailers per network   
│
└───src                                             <- Root directory for all code
    ├───config.ini                                  <- Config file for storing YouTube API keys
    ├───main.py                                     <- Collects YouTube trailers and comments
    ├───sentiment.py                                <- Code for classifying comments using Vader
    ├───visualizor.py                               <- Enforces styleguide used for visualizations
    ├───__init__.py
    │
    ├───imdb_api                                    <- Module for scraping IMDb release dates
    │       imdbscraper.py                          <- Code for getting release dates from IMDb
    │
    └───youtube_api                                 <- Module for collecting trailers, comments with utilities
            utilities.py                            <- Helper functions for the module
            youtubecommentgetter.py                 <- Gets comments for each video
            youtubegetter.py                        <- Parent class for YoutubeCommentGetter and YoutubeVideoGetter
            youtubevideogetter.py                   <- Gets videos from YouTube
```



