from collections import Counter
from iso639 import languages

def return_empty_JSON():
    return {
        'user_id': '',
        'tweet_id': '',
        'name': '',
        'screen name': '',
        'timestamp': '',
        'text': '',
        'bio': '',
        'hashtags': '',
        'link to tweet': '',
        'follower count': '',
        'friends count': '',
        'listed count': '',
        'location': '',
        'language_twitter': '',
        'status count': '',
        'collocations_text': [],
        'collocations_bio': [],
        'verified': ''
    }

def return_empty_analytics():
    return {
        'counter': {
            'words': 0,
            'tweets': 0,
            'retweets': 0,
            'quote_retweets': 0,
            'original_tweets': 0,
            'with_media': 0,
            'with_url': 0
        },
        'media': {
            'link': {},
            'count': Counter()
        },
        'hashtag_frequencies': Counter(),
        'location_frequencies': Counter(),
        'language_frequencies': Counter(),
        'timeline_frequencies': [],
        'coloc_text_frequency': {
            'contextual': Counter(),
            'unique': Counter()
        },
        'coloc_bio_frequency': {
            'contextual': Counter(),
            'unique': Counter()
        },
        'emoji_frequency': {
            'text_total': Counter(),
            'text_unique': Counter(),
            'bio_total': Counter(),
            'bio_unique': Counter(),
            'name_total': Counter(),
            'name_unique': Counter(),
        },
        'URLS': {
            'unqiue': Counter(),
            'domain': Counter(),
        },
        'user_info': {},
        'word_frequency': {
            'total': Counter(),
            'unique': Counter()
        },
        'bio_word_frequency': Counter(),
        'user_frequencies': {
            'top_users_via_followers': [],
            'user_unique_tweet_count': Counter()
        },
        'tweet_retweet_frequencies': { 
            'retweet_count': Counter(),
            'retweet_user_count': Counter(),
            'retweet_text': {},
            'tweet_to_user_mapping': {}
        },
        'tweet_quote_frequencies': { 
            'quote_count': Counter(),
        },
        'priority_tweets_from_timestamps': [],
        'network': { 
            'nodes': {},
            'edges': [],
            'vals': Counter()
        }
    }

def return_human_language(lang_list):
    result = Counter()
    for lang in lang_list.keys():
        try:
            hr_lang = languages.get(alpha2=lang).name
        except KeyError:
            hr_lang = "Undetermined"
        result.update([hr_lang])
        result[hr_lang] += (lang_list[lang]-1)
    return result

def return_clickable_link(url):
    return '=HYPERLINK(\"{}\",\"{}\")'.format(url, 'Link')

def return_tweet_link(id):
    url = 'https://twitter.com/i/web/status/' + str(id)
    return return_clickable_link(url)

def return_twitter_profile_link(screen_name):
    url = 'https://twitter.com/' + str(screen_name)
    return return_clickable_link(url)