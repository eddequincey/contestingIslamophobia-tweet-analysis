import pandas as pd
import os
from lib import tools
import heapq
import xlsxwriter
from datetime import datetime, time
import random
from matplotlib import pyplot
import numpy as np
from wordcloud import WordCloud
from emoji import demojize
import requests
from bs4 import BeautifulSoup
from queue import Queue
from collections import Counter
import copy

pd.set_option('display.max_columns', None)

def write_linegraph(file, title, file_name, to_dir):
    df = pd.read_csv(to_dir + file, header=0, index_col=0, parse_dates=True)
    df.squeeze('columns')
    df.drop(columns='Timestamp_ms', inplace=True)
    plt = df.plot(
        kind='line',
        figsize=(30, 15),
        fontsize=20,
        legend=None
    )
    plt.set_title(title, fontsize=32, pad=30)
    pyplot.xlabel('Date & Time', fontsize=32, labelpad=30)
    pyplot.ylabel('Num of Tweets', fontsize=32, labelpad=30)

    frequency = int(len(df['Timestamp'])/30)
    frequency = 1 if frequency is 0 else frequency

    pyplot.xticks(
        np.arange(0, len(df['Timestamp']), frequency),
        rotation=45,
        va="top",
        ha="right"
    )
    plt.set_xticklabels(df['Timestamp'][::frequency])
    pyplot.tight_layout()

    final = plt.get_figure()
    final.savefig(to_dir + file_name + '.pdf')

def write_to_csv(data, name, to_dir):
    df = pd.DataFrame(data)
    df.to_csv(to_dir + name + '.csv')

def write_to_xlsx(data, name, to_dir):

    def get_col_widths(dataframe):
        # First we find the maximum length of the index column   
        idx_max = max([len(str(s)) for s in dataframe.index.values] + [len(str(dataframe.index.name))])
        # Then, we concatenate this to the max of the lengths of column name and its values for each column, left to right
        return [idx_max] + [max([len(str(s)) for s in dataframe[col].values] + [len(col)]) for col in dataframe.columns]

    df = pd.DataFrame(data)
    ### create a Pandas Excel writer using XlsxWriter as the engine.
    # writer = pd.ExcelWriter(to_dir + name + '.xlsx', engine='xlsxwriter', options={'link to profile': True})
    
    writer = pd.ExcelWriter(to_dir + name + '.xlsx', engine='xlsxwriter')
    ### convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name=name)

    workbook  = writer.book
    worksheet = writer.sheets[name]
    ### auto resize columns
    for i, width in enumerate(get_col_widths(df)):
        worksheet.set_column(i, i, width)

    ### close the Pandas Excel writer and output the Excel file.
    writer.close()

def write_to_file(buffer, dir, filename):
    try:
        file_num = len([name for name in os.listdir(dir) if os.path.isfile(os.path.join(dir, name))])
    except OSError as e:
        file_num = 0
    write_to_xlsx(buffer,  'allTweets_' + filename + '_' + str(file_num), dir)
    buffer.clear()

def write_counters_file(file_name, data, columns, to_dir):
    df = pd.DataFrame(data.most_common())
    df.columns = columns
    df.to_csv(to_dir + file_name)

def write_timeline(file_name, timestamp_list, to_dir, time_chunks=3600000):

    def convert_to_milliseconds(time):
        dt_obj = datetime.strptime(time,'%Y-%m-%d %H:%M:%S')
        millisec = dt_obj.timestamp() * 1000
        return int(millisec)
    
    def convert_to_datetime(time):
        return datetime.fromtimestamp(time/1000.0)

    timestamps = timestamp_list.copy()
    result = []
    smallest_time = convert_to_milliseconds(convert_to_datetime(int(min(timestamps))).replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d %H:%M:%S'))
    largest_time = convert_to_milliseconds(convert_to_datetime(int(max(timestamps))).replace(hour=23, minute=59, second=59, microsecond=59).strftime('%Y-%m-%d %H:%M:%S'))
    for start_time in range(smallest_time, largest_time, time_chunks):
        end_time = (start_time+time_chunks)
        to_remove = []
        count = 0
        for i,t in enumerate(timestamps):
            if start_time <= int(t) < end_time:
                count += 1
                to_remove.append(i)
        for r in reversed(to_remove):
            del timestamps[r]
        result.append(
            {
                'Timestamp_ms': end_time,
                'Timestamp': convert_to_datetime(end_time).strftime('%Y-%m-%d %H:%M:%S'),
                'Tweet Count': count
            }
        )
    write_to_csv(result, file_name, to_dir)

def write_media_links(filename, media_dict, media_count, list_size, to_dir):
    result = []
    id_filter = media_count.most_common()[:list_size]
    for _iter in id_filter:
        _id    = _iter[0]
        _count = _iter[1]
        url = media_dict[_id]
        obj = {
            'media link': tools.return_clickable_link(_id),
            'count': _count,
            'context tweet': tools.return_clickable_link(url)
        }
        result.append(obj)
    write_to_xlsx(result , filename, to_dir)

def write_retweet_tweets(filename, text_list, id_counter, mapping, timestamp_tweets, user_info, list_size, to_dir):
    result = []
    id_filter = id_counter.most_common()[:list_size]
    for _iter in id_filter:
        _id    =_iter[0]
        _count = _iter[1]
        user_id = mapping[_id]
        info = user_info[user_id]
        obj = {
            'tweet id': str(_id),
            'count': str(_count),
            'text': text_list[_id],
            'link to tweet': tools.return_tweet_link(_id),
            'name': info['name'],
            'screen_name': info['screen_name'],
            'verified': info['verified'],
            'link to profile': tools.return_twitter_profile_link(info['screen_name'])
        }
        result.append(obj)
    if len(id_filter) < list_size:
        remainder = list_size - len(id_filter)
        random.shuffle(timestamp_tweets)
        timestamp_filter = timestamp_tweets[:remainder]
        for _iter in timestamp_filter:
            _id  =  _iter['tweet id']
            user_id = _iter['user_id']
            info = user_info[user_id]
            obj = {
                'tweet id': _id,
                'count': 0,
                'text': _iter['text'],
                'link to tweet': tools.return_tweet_link(_id),
                'name': info['name'],
                'screen_name': info['screen_name'],
                'verified': info['verified'],
                'link to profile': tools.return_twitter_profile_link(info['screen_name'])
            }
            result.append(obj)
    # write_to_csv(result ,'retweet', to_dir)
    write_to_xlsx(result, filename, to_dir)

def write_retweet_users(filename, id_counter, user_info, list_size, to_dir):
    result = []
    id_filter = id_counter.most_common()[:list_size]
    for _iter in id_filter:
        _id    =_iter[0]
        _count = _iter[1]
        info = user_info[_id]
        obj = {
            'user id': str(_id),
            'count': str(_count),
            'name': info['name'],
            'screen_name': info['screen_name'],
            'verified': info['verified'],
            'link to profile': tools.return_twitter_profile_link(info['screen_name'])
        }
        result.append(obj)
    # write_to_csv(result ,'retweet', to_dir)
    write_to_xlsx(result, filename, to_dir)

def write_top_users_tweet_count(filename, text_list, id_counter, list_size, to_dir):
    result = []
    id_filter = id_counter.most_common()[:list_size]
    for _iter in id_filter:
        _id    = _iter[0]
        _count = _iter[1]
        obj = text_list[_id]
        obj = {
            'user id': _id,
            'tweet count': _count,
            'name': obj['name'],
            'verified': obj['verified'],
            'link': tools.return_twitter_profile_link(obj['screen_name'])
        }
        result.append(obj)
    # write_to_csv(result ,'user_frequency', to_dir)
    write_to_xlsx(result , filename, to_dir)

def write_top_user_followers(filename, text_list, followers_counter, to_dir):
    result = []
    for i in heapq.nlargest(len(followers_counter), followers_counter):
        _id    = i[1]
        _followers = i[0]
        obj = text_list[_id]
        obj = {
            'user id': _id,
            'followers': _followers,
            'name': obj['name'],
            'screen_name': obj['screen_name'],
            'verified': obj['verified'],
            'link': tools.return_twitter_profile_link(obj['screen_name'])
        }
        result.append(obj)
    # write_to_csv(result ,'top_users_followers', to_dir)
    write_to_xlsx(result, filename, to_dir)

def write_word_frequency_in_tweet(filename, total, unique, word_counter, tweet_counter, to_dir):
    result = []
    total_list = total.most_common()
    for (key, value) in total_list:
        _word  = key
        ## remove the text for retweet
        if _word == 'rt': continue
        _count = value
        _unique_count = unique[key]
        obj = {
            'word':_word,
            'total count': _count,
            'use per tweet': _unique_count,
            'proportion of all words': _count/word_counter,
            'proportion of tweets': _unique_count/tweet_counter,
            'colour': 'N/A'
        }
        result.append(obj)
    write_to_csv(result , filename, to_dir)

def write_emoji_frequencies(filename, total, list_size, to_dir):
    result = []
    total_list = total.most_common()[:list_size]
    for (key, value) in total_list:
        _emoji  = key
        _count = value
        obj = {
            'emoji':_emoji,
            'frequency': _count,
            'description':demojize(_emoji)
        }
        result.append(obj)
    write_to_csv(result, filename, to_dir)

def write_URL_frequencies(filename, total, list_size, to_dir):
    result = []
    total_list = total.most_common()[:list_size]
    for (key, value) in total_list:
        _URL  = key
        _count = value
        try:
            response = requests.get(_URL)
            soup = BeautifulSoup(response.text)
            metas = soup.find_all('meta')
            _description = [ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'description' ]
        except requests.exceptions.MissingSchema:
            _description = ''
        except requests.exceptions.ConnectionError:
            _description = ''
        except requests.exceptions.ContentDecodingError:
            _description = ''
        except KeyError:
            _description = ''
        obj = {
            'URL':_URL,
            'frequency': _count,
            'description': _description
        }
        result.append(obj)
    write_to_csv(result, filename, to_dir)

def write_word_frequency_in_bio(filename, total, tweet_users, to_dir):
    result = []
    total_list = total.most_common()
    for (key, value) in total_list:
        _word  = key
        _count = value
        obj = {
            'word':_word,
            'frequency': _count,
            'proportionate to unique users': _count/tweet_users
        }
        result.append(obj)
    write_to_csv(result, filename, to_dir)

def write_contextual_collocated(filename, collocated_words, to_dir):
    result = []
    words_list = collocated_words.most_common()
    for (key, value) in words_list:
        _1word  = key[0]
        _2word  = key[1]
        _3word  = key[2]
        _count = value
        obj = {
            '1st word':_1word,
            '2nd word':_2word,
            '3rd word':_3word,
            'frequency': _count,
        }
        result.append(obj)
    write_to_csv(result , filename, to_dir)

def write_tweet_count(file_name, numOfTweets, retweets, quote_retweets, original_tweets, tweet_media, tweet_URLS, to_dir):
    f = open(to_dir + file_name, "w")
    f.write('Total Tweets: ' + str(numOfTweets))
    f.write('\n')
    f.write('Total Retweets: ' + str(retweets))
    f.write('\n')
    f.write('Total Quote Retweets: ' + str(quote_retweets))
    f.write('\n')
    f.write('Total Original Tweets: ' + str(original_tweets))
    f.write('\n')
    f.write('Tweets with URL: ' + str(tweet_URLS))
    f.write('\n')
    f.write('Tweets with media: ' + str(tweet_media))
    f.write('\n')
    f.close()

noneInfo = {
    'name': 'Unavailable',
    'screen_name': 'Unavailable',
    'verified': False,
    'link_to_profile': 'Unavailable'
}

def write_tweet_nodes(filename, nodesArray, count, user_info, to_dir):
    result = []
    for nodes in nodesArray:
        for _idTuple in nodes.items():
            _id = _idTuple[0]
            info = user_info[_idTuple[1]] if _idTuple[1] != None else noneInfo
            value = 1 + count[_id]
            obj = {
                'id': str(_id),
                'val': value,
                'name': info['name'],
                'screen_name': info['screen_name'],
                'verified': info['verified'],
                'link_to_profile': info['link_to_profile'],
                'link_to_tweet': "https://twitter.com/i/web/status/" + str(_id)
            }
            result.append(obj)
    write_to_csv(result, filename, to_dir)

def write_users_nodes(filename, nodes, vals, to_dir):
    result = []

    ### add retweet value to 'val'
    ### then convert dict to array
    for node in nodes.values():
        if node['screen_name'] == 'undefined':
            continue
        if node['screen_name'] in vals:
            node['val'] += vals[node['screen_name']]
        result.append(node)

    write_to_csv(result, filename, to_dir)

def write_network_edges(filename, edges, to_dir):
    result = edges
    write_to_csv(result, filename, to_dir)

def write_optimised_network(filename, nodes, edges, vals, to_dir):
    influencer_to_add = []
    ### ideal size for optimal network
    network_size = 150000
    ### maximum limit for influencers
    max_influencers_limit = 20000

    ### get influencers
    top_threshold = int(len(vals)*0.10)
    top_threshold = top_threshold if top_threshold < max_influencers_limit else max_influencers_limit
    influencer = dict(vals.most_common()[:top_threshold])
    influencer_size = network_size - top_threshold

    ### add retweet value to 'val'
    for node in nodes.values():
        if node['screen_name'] == 'undefined':
            continue
        if node['screen_name'] in vals:
            node['val'] += vals[node['screen_name']]
    
    neighbours = {
        'quote': Counter(),
        'retweet': Counter()
    }
    edges_dict = {
        'quote': {},
        'retweet': {}
    }

    ### needed to calaute how many edges were chosen
    edge_size = len(edges)

    ### add neighbouring nodes to influencer in a hashmap
    for key in influencer.keys():
        influencer_to_add.append(nodes[key])
        ### start from the back so edges can be removed each iteration
        for i in range(len(edges)-1, 0, -1):
                edge = edges[i]
                target = edge['target']
                ### influencer should always be the target
                if (target == key):
                    source = edge['source']
                    group = edge['group']
                    ### add edge to dict for use later
                    edges_dict[group][(source,target)] = edge
                    if target not in neighbours[group]:
                        neighbours[group][target] = Counter()
                    ### increase counter by source's value
                    neighbours[group][target][source] = nodes[source]['val']
                    ### if target has been found then it is
                    ### not needed for each influencer loop
                    del edges[i]
    
    ### calc new edge size
    edge_size = edge_size - len(edges)
    ### assuming that each edge required a new node
    ### not accurate but close enough
    network_size = edge_size + (edge_size * 0.5)
    ### a percentage of neighbours to keep
    try:
        percentage_to_keep = min((influencer_size/network_size),1)
    except ZeroDivisionError:
        percentage_to_keep = 1
    ### create a buffer on either side in case method fails
    buffer_percentages = [0.7,0.8,0.9,1.0,1.1,1.2] if percentage_to_keep < 0.83 else [0.5,0.6,0.7,0.8,0.9,1.0]
    percentages_to_keep = []
    for buffer in buffer_percentages:
        percentages_to_keep.append(percentage_to_keep * buffer)
    
    ### need sub-directory to old files
    to_dir = to_dir + "optimised_nodes/"
    try:
        os.mkdir(to_dir)
    except OSError:
        print ("Creation of the directory %s failed" % to_dir)
    else:
        print ("Successfully created the directory %s " % to_dir)

    ### 
    for percentage in percentages_to_keep:
        nodes_to_add = copy.deepcopy(influencer_to_add)
        edges_to_add = []
        for group in ['quote','retweet']:
            for target in neighbours[group]:
                size_thershold = int(len(neighbours[group][target]) * percentage)
                neighbours_to_keep = neighbours[group][target].most_common()[:size_thershold]
                for (source, value) in neighbours_to_keep:
                    nodes_to_add.append(nodes[source])
                    edges_to_add.append(edges_dict[group][(source,target)])

        write_to_csv(nodes_to_add, str(percentage) + '_' + filename + '_nodes', to_dir)
        write_to_csv(edges_to_add, str(percentage) + '_' + filename + '_edges', to_dir)


def write_word_cloud(file, file_name, to_dir):    
    df = pd.read_csv(to_dir + file, header=0, index_col=0, parse_dates=True)
    df.squeeze('columns')
    df.drop(columns='use per tweet', inplace=True)
    df.drop(columns='proportion of all words', inplace=True)
    df.drop(columns='proportion of tweets', inplace=True)
    df.drop(columns='colour', inplace=True)
    wordsToAdd = ''

    ### convert list of words into a single string
    for (word, count) in df.values.tolist():
        ### only allow words passed two counts
        for i in range(1,count):
            wordsToAdd += str(word) + ' '

    ### no word cloud could be generated
    if wordsToAdd is '':
        return None
    
    wc = WordCloud(width=5000,height=5000,collocations=False).generate(wordsToAdd.lower())
    pyplot.figure()
    pyplot.imshow(wc, interpolation="bilinear")
    pyplot.axis('off')
    pyplot.savefig(to_dir + file_name, dpi=500, bbox_inches='tight', pad_inches = 0)

def write_analytics_files(analytics, to_dir, retweet_size, top_users_size):
    write_tweet_count(
        'tweet_stats.txt',
        analytics['counter']['tweets'],
        analytics['counter']['retweets'],
        analytics['counter']['quote_retweets'],
        analytics['counter']['original_tweets'],
        analytics['counter']['with_media'],
        analytics['counter']['with_url'],
        to_dir
    )

    if (len(analytics['coloc_bio_frequency']['unique'])):
        write_counters_file(
            'frequency_collocations_via_bio.csv',
            analytics['coloc_bio_frequency']['unique'],
            ['Word', 'Total_Count'],
            to_dir
        )
    
    if (len(analytics['coloc_text_frequency']['unique'])):
        write_counters_file(
            'frequency_collocations_via_tweets.csv',
            analytics['coloc_text_frequency']['unique'],
            ['Word', 'Total_Count'],
            to_dir
        ) 
    
    write_counters_file(
        'frequency_hashtag.csv',
        analytics['hashtag_frequencies'],
        ['Hashtags', 'Frequency'],
        to_dir
    )
    write_counters_file(
        'frequency_language.csv',
        tools.return_human_language(analytics['language_frequencies']),
        ['Language', 'Frequency'],
        to_dir
    ) 
    write_counters_file(
        'frequency_location.csv',
        analytics['location_frequencies'],
        ['Location', 'Frequency'],
        to_dir
    )
    write_timeline(
        'timeline-hourly',
        analytics['timeline_frequencies'],
        to_dir
    )

    write_linegraph(
        'timeline-hourly.csv',
        'Timeline Hourly',
        'timeline-hourly-graph',
        to_dir
    )

    write_timeline(
        'timeline-daily',
        analytics['timeline_frequencies'],
        to_dir,
        86400000
    )

    write_linegraph(
        'timeline-daily.csv',
        'Timeline Daily',
        'timeline-daily-graph',
        to_dir
    )

    ### Retweet - tweets
    write_retweet_tweets(
        'top_retweets',
        analytics['tweet_retweet_frequencies']['retweet_text'],
        analytics['tweet_retweet_frequencies']['retweet_count'],
        analytics['tweet_retweet_frequencies']['tweet_to_user_mapping'],
        analytics['priority_tweets_from_timestamps'],
        analytics['user_info'],
        retweet_size,
        to_dir
    )
    ### Retweet - users
    write_retweet_users(
        'top_users_via_retweets',
        analytics['tweet_retweet_frequencies']['retweet_user_count'],
        analytics['user_info'],
        retweet_size,
        to_dir
    ) 
    ### top users based on unique tweets
    write_top_users_tweet_count(
        'top_users_via_tweet_count',
        analytics['user_info'],
        analytics['user_frequencies']['user_unique_tweet_count'],
        top_users_size,
        to_dir
    ) 
    ### top users based on followers
    write_top_user_followers(
        'top_users_via_followers',
        analytics['user_info'],
        analytics['user_frequencies']['top_users_via_followers'],
        to_dir
    ) 
    ###
    write_word_frequency_in_tweet(
        'word_frequency_in_tweet',
        analytics['word_frequency']['total'],
        analytics['word_frequency']['unique'],
        analytics['counter']['words'],
        analytics['counter']['tweets'],
        to_dir
    )
    write_word_cloud(
        'word_frequency_in_tweet.csv',
        'word_cloud.png',
        to_dir
    )
    ###
    write_word_frequency_in_bio(
        'word_frequency_in_bio',
        analytics['bio_word_frequency'],
        len(analytics['user_info']),
        to_dir
    ) 
    ###
    write_contextual_collocated(
        'contextual_collocated_bio_text',
        analytics['coloc_bio_frequency']['contextual'],
        to_dir
    ) 
    ###
    write_contextual_collocated(
        'contextual_collocated_tweet_text',
        analytics['coloc_text_frequency']['contextual'],
        to_dir
    )
    ### 
    write_users_nodes(
        'network_nodes',
        analytics['network']['nodes'],
        analytics['network']['vals'],
        to_dir
    )
    ###
    write_network_edges(
        'network_edges',
        analytics['network']['edges'],
        to_dir
    )
    ##
    write_optimised_network(
        'network_optimised',
        analytics['network']['nodes'],
        analytics['network']['edges'],
        analytics['network']['vals'],
        to_dir,
    )
    ##
    write_emoji_frequencies(
        'frequency_emoji_tweet_text',
        analytics['emoji_frequency']['text_total'],
        retweet_size,
        to_dir
    )
    ##
    write_emoji_frequencies(
        'frequency_emoji_bio_text',
        analytics['emoji_frequency']['bio_total'],
        retweet_size,
        to_dir
    )
    ##
    write_emoji_frequencies(
        'frequency_emoji_name_text',
        analytics['emoji_frequency']['name_total'],
        retweet_size,
        to_dir
    )
    ##
    write_media_links(
        'frequency_media_links',
        analytics['media']['link'],
        analytics['media']['count'],
        retweet_size,
        to_dir
    )
    ##
    write_URL_frequencies(
        'frequency_URLs_unqiue',
        analytics['URLS']['unqiue'],
        retweet_size,
        to_dir
    )
    ##
    write_URL_frequencies(
        'frequency_URLs_domain',
        analytics['URLS']['domain'],
        retweet_size,
        to_dir
    )