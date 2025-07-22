# AHRC Twitter Documentation

# General

## Purpose of this document?

The document will cover specifics of how the analysis files are collected and created. Where applicable implications of the researchers choice will be explained and expanded upon.

## How is the data retrieved and how is it analyzed?

The pipeline to produce the analysis has been split up into three sections”

Retrieve:
Two methods are used for retrieving tweets.
Tweet JSON data in this project is split between direct Data URLs from Twitter that provide the flat-files. The ‘download_job.py’ is the file used to download this data and is in Twitter API 1.1 format.
The second is using Twitter API 2.0 with the file ‘get-tweets.IPYNB’. This method relies on the search_tweets.py library. To create queries read through the documentation link and look at the previously used config files.

Split:
The raw data is searched through to find tweets that match a certain criteria and separates them into a new JSON file/s.
These criteria include: hashtags, search phrases, search terms, time range and language.
During the splitting process, the code can recognise when the data being input is API 1.1 or 2.0. This code will reconstruct 2.0 back to the 1.1 format so that it can plug into the analysis code.

Analyse:
This takes the splitted tweet data and generates all the analysis files.
How those files are generated is expanded upon throughout this document.


## What is Twitter API 1.1 vs 2.0?

Data in this project is split between Twitter API 1.1 and 2.0 but what does that mean? In layman's terms, Twitter data in 1.1 and 2.0 in theory can provide the same data, but they are structured in their own unique way.

WARNING: If you are to create more analysis on the Twitter data, look back at the splitter code in how the code converts 2.0 to 1.1. Some data may be dropped as is not essential, but may be needed for future analysis.
## Which data used API 1.1 and which data used API 2.0?






## What are ‘combined tweets ’?

If a tweet is a quote tweet, there will always be two sets of data to anaylse (hashtags, tweets, media) etc. A search criteria treats both these sets as a single set.

Example: when looking into the tweet text both the new tweet text and the orignal quote tweet text will be combined and anaylsed as a single string.

## What is ‘Clean Text’?

Clean text splits a string into a list for easy analysis.
Text is converted to lowercase
Punctuation is removed
Line breaks are replaced with a space
Stop words are removed (Stop words from the )


# Split

## Why does raw data need splitting?

In general, when requesting data from Twitter the original query to retrieve the data already has the search terms and in the correct time frame. However, because of the mix of API, the splitting step is necessary to convert to a common format that the analysis code is always excepting.

## How to read the tables in this section?

Each covers hashtags, search phrases and search terms.
Hashtags look for a match in the hashtags only.
Phrases look for multiple words which match the phrase in the tweet text.
Terms look for a single word in the tweet text.

If any one of the conditions are found the data is added to the split.

If there are multiple tables then BOTH tables need one condition.

## Where is the search criteria looking in the data?

Hashtags are provided by twitter in their own list and are scanned from there.

Phrases and Terms look at tweet text, if a quote tweet is found both tweet and quoted tweet will be scanned for the phrases; as this is how the Twitter API retrieves that data.

# Analysis

## How is tweet_stats calculated?

This file has six data points:

Total Tweets: Each time a tweet is come across, whether that be an original tweet, retweet or quote tweet, it will be counted.

Total Retweets: Each time a user has retweeted another original tweet, it will be counted.

Total Quote Retweets: Each time a user has quote-tweeted another original tweet, it will be counted.

Total Original Tweets: All unique tweets and quote tweets are considered ‘Original Tweets’ as they provide new content.

Tweets with URL: Tweets that contain a url (or multiple) will be counted.

Tweets with media: Tweets that contain the ‘media’ object will be counted.


## How is frequency_collocations_via_bio calculated?

For the bio, a collocation list is created by taking the bio text (as clean text) and looking for positive and negative terms; these terms are decided by the library .

When a term is found the previous word and proceeding word are collected and added to a list.

The program only allows one unique string per bio. For example, A bio that says
“The magical country and country is mind-blowing”

After clean text, would reduce to:
“magical country country mind-blowing”

Country would be before and after a positive word but country will only be counted once in the frequency_collocations_via_bio file.

## How is contextual_collocated_bio_text calculated?

How collocated bio text is collected is the same as ‘frequency_collocations_via_bio’ (above). Each time a unique combination of three words are together the collection is incremented.

## How is frequency_collocations_via_tweets calculated?

For the tweet, a collocation list is created by taking the tweet text (as clean text) and looking for search terms; these terms are decided by the user.



When a term is found the previous word and proceeding word are collected and added to a list.

The program only allows one unique string per bio. See frequency_collocations_via_bio for example of this (above).

## How is contextual_collocated_tweet_text calculated?

How collocated tweet text is collected is the same as ‘frequency_collocations_via_tweets’ (above). Each time a unique combination of three words are together the collection is incremented.

## How is frequency_hashtag calculated?

Hashtags are provided in Twitter’s data via a pre-allocated list. Each hashtag in the list gets incremented by one in ‘frequency_hashtag’ data.

## How is frequency_language calculated?

Languages are provided in Twitter’s data. The language for each tweet is incremented in the ‘frequency_language’ data.

## How is frequency_location calculated?

Locations are provided in Twitter’s data. The location for each tweet is incremented in the ‘frequency_location’ data.

## How is the timeline-hourly calculated?

The smallest and largest dates and times are found in the date ranges. The smallest is reverted back to the previous day and largest is converted to the start of the proceeding day.

From there, the smallest time is the starting value and the end value is the start + an hour. Each cycle the previous end value becomes the starting value.

If there is a tweet within the range of the starting value and end value then the count for the end value is incremented. Before the next cycle, the end value with the counter is saved in the data structure.

NOTE: The x-axis labels for the graph state how many tweets happening WITHIN the hour

## How is timeline-daily calculated?

Functions the same as ‘timeline-hourly’ (see above) except the increment goes up via a day.

## How is top_retweets calculated?

Each time a tweet is found in the data and it is a retweet, the tweet that is being retweeted will get an increment of 1; this will not happen if it is a quote tweet.

Once all the tweets are seen, the list is sorted and the top 1100 are kept and printed to a file.

## How is top_users_via_retweets calculated?

Each time a tweet is found in the data and it is a retweet, the author of the tweet that is being retweeted will get an increment of 1; this will not happen if it is a quote tweet.

Once all the tweets are seen, the list is sorted and the top 1100 are kept and printed to a file.

## How is top_users_via_tweet_count calculated?

Each time an original or quote tweet is found in the data,  the author of the tweet will get an increment of 1.

Once all the tweets are seen, the list is sorted and the top 1100 are kept and printed to a file.

## How is top_users_via_followers calculated?

A heap of 1100 is present during the analysis stage. Each time a user has not been seen before comes up in the data it is compared to those in the heap. If the heap is not full then the user goes into the data. If the heap is full the user’s followers are compared against every other user in the heap and replace the lowest if it is larger than the user in the heap.

Followers are captured when the tweet was created. Therefore, users can gain or lose followers in that time. The drawback of this approach is that the first instance of the followers are captured and no acknowledgement of future gains or losses.

## How is word_frequency_in_tweet calculated?

This file has six columns:

Word: Each word in this column is taken from the clean text of each tweet text. If it is a quote tweet, the original tweet and quoted tweet will be included in the clean text.

total count: Each word from the clean text is incremented. If two words pop up in a single tweet they are both counted.

use per tweet: Each unique word from the clean text is incremented. If two words pop up in a single tweet only one is counted.

proportion of all words: total count/total number of words. Total number of words is calculated by adding all clean text for each tweet text.

proportion of tweets: use per tweet/total tweets. Total tweets are calculated by incrementing a value each tweet; this includes retweets.

Colour: this column can be used in conjunction with ‘word-cloud-coloured.py’ to provide the colours of each word in the word cloud.

## How is word_frequency_in_bio calculated?

The words are incremented by getting unique text on clean bio text.

## How is network_nodes created?

Each time a unique user is seen their screen name is added to the nodes data.

This does not account for changes in ‘screen_name’ at a later point.

## How is network_edges created?

Whenever a retweet or quote tweet comes up in the data a new edge will be created. The source of the edge is the original (unique) tweet and the target is the tweet being retweeted or quoted.

## What is network_optimised nodes & edges and how is it created?

The library used to visualize the retweet network is called  running on a  server. Force-graph can support networks of up to 1+ million elements, but through testing the sweet spot for these networks seems to be around 150k elements (nodes and links combined). With large datasets, nodes and edges have to be smartly compressed to create a usable visualisation while retaining the same narrative; this is the purpose of optimised network files.

Each user has a value, this is their retweet & quote tweet values combined.

The top percentage of users are selected, which are called influencers.
Influencer's size cannot exceed 20k and can only be a maximum of 10% of the data.

For each influencer, their neighbours are found. A neighbour is a user node that is connected directly to the influencer whether that be a retweet or a quote tweet.

Each neighbour goes into separate lists of ‘retweet neighbours’ and ‘quote tweet neighbours.

A percentage value is calculated of how many neighbours stay in the network to reduce the value to 150k elements.

As this percentage value is proportional, the size of retweets one influencer achieves will still be in proportion to other influencers.

Each list is sorted so that the highest value neighbours (those with the most retweets and quote tweets) are more likely to stay in the network. This is because they are likely to be influential on a smaller scale and will connect influencers together via connecting links; allowing clustering of similar influencers to take place.

The ‘retweet neighbours’ and ‘quote tweet neighbours’ are then reduced by the percentage value and added to the optimised files.

This is taxing from a time complexity point of view. It is the 20’000 to the power of the number of edges. So, expect this to be a lengthy step in the ‘twitter-analysis.py’ file.

## How are emojis found in text?

All text is analysed for emojis using the library , specifically looking for the unicode emoji range.

The string of the text splits any emoji that may be connected to another word or emoji without a space. This ensures all emojis in the text are found and accounted for.

## How is frequency_emoji_tweet_text calculated?

For each tweet, an emoji analysis takes place on the text and each time an emoji is found it is incremented by one.

So, multiple emojis in one tweet would allow multiple increments.

## How is frequency_emoji_bio_text calculated?

For each tweet an emoji analysis takes place on the user’s bio and each time an emoji is found it is incremented by one.

If the same user tweets multiple times, the bio will be analyzed each time and emojis will be incremented.

## How is frequency_emoji_name_text calculated?

For each tweet an emoji analysis takes place on the user’s screen name and each time an emoji is found it is incremented by one.

If the same user tweets multiple times, the screen name will be analyzed each time and emojis will be incremented.

## How is frequency_URLs_unqiue calculated?

Twitter provides an ‘entities’ list with additional information regarding the tweet such as URLs and media. If this data contains ‘expanded_url’ the domain is taken and incremented by one.

When all URLs are collected, a HTTP request is sent out and  is used as an attempt to find some description of the article/web page without having the click on the link. Not all pages provide this information however.

## How is frequency_URLs_domain calculated?

Twitter provides an ‘entities’ list with additional information regarding the tweet such as URLs and media. If this data contains ‘expanded_url’ the python method is used to leave only the domain. Each domain is incremented by one.

## How is frequency_media_links calculated?

Twitter provides an ‘entities’ list with additional information regarding the tweet such as URLs and media. If this data contains ‘media’ then each ‘media_url_https’ is extracted and incremented.

Note: URLs will change if the same media is reuploaded so the count for this file will specifically show highly retweeted or highly quoted media. The data also does not state the format, and for videos the provided link will be for a still frame from the video. This is why ‘context tweet’ was added to show the origin of the media.
