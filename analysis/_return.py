### string - identifying punctuation in sentences
from string import punctuation

### TO-DO: Explain
import string

### re - basic regular expressions used in text functions
import re
import regex

# from nltk.stem import WordNetLemmatizer
# lemmatizer = WordNetLemmatizer()

from emoji import UNICODE_EMOJI


with open('../nltk_data/StopWords_GenericLong.txt', 'r') as stop:
	StopWords = [line.strip() for line in stop]

def return_emoji_list(string):
    if string is None: return []
    emoji_list = []
    data = regex.findall(r'\X', string)
    for word in data:
        if any(char in UNICODE_EMOJI['en'] for char in word):
            emoji_list.append(word)
    # print(emoji_list)
    return emoji_list

def return_tweet_type(json_buffer):
    ### https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet
    ### define tweet type
    original_tweet, retweet, quote_retweet = False, False, False

    ### 'is_quote_status' does not always work; 'quoted_status_id' does
    if 'retweeted_status' in json_buffer: 
        retweet = True
    if 'quoted_status_id' in json_buffer: 
        quote_retweet = True
    if not retweet:
        original_tweet = True
    
    return original_tweet, retweet, quote_retweet

def return_tweet_text(json_buffer, retweet=False):
    # if is a retweet, the 'retweeted_status' needs to be used
    if not retweet:
        if json_buffer['truncated']:
            return json_buffer['extended_tweet']['full_text']
        return json_buffer['text'] 
    else:
        rt_screen_name = json_buffer['retweeted_status']['user']['screen_name']
        return 'RT @'+ rt_screen_name + ': \"' + return_tweet_text(json_buffer['retweeted_status']) + '\"'

def return_hashtag_text(json_buffer, retweet=False):
    # if is a retweet, the 'retweeted_status' needs to be used
    if not retweet:
        if json_buffer['truncated']:
            return [x['text'].lower() for x in json_buffer['extended_tweet']['entities']['hashtags']]
        return [x['text'].lower() for x in json_buffer['entities']['hashtags']]
    else:
        return return_hashtag_text(json_buffer['retweeted_status'])

def return_quote_data(buffer, primary_text):
    analysis_text, main_text, secondary_text, hashtags = '', '', '', []
    # needed for formatting
    if 'quoted_status' in buffer:
        qt_screen_name = buffer['quoted_status']['user']['screen_name']
        secondary_text = return_tweet_text(buffer['quoted_status'])
        hashtags       = return_hashtag_text(buffer['quoted_status'])

        # need the pure text for analysis
        analysis_text = primary_text + ' ' + secondary_text
    else:
        qt_screen_name = 'undefined'
        secondary_text = 'This Tweet is unavailable.'

    # need the pure text for analysis
    analysis_text = primary_text + ' ' + secondary_text

    # set values
    main_text = 'QT @' + qt_screen_name + ': \"' + secondary_text + '\" \n\n' + primary_text
    return analysis_text, main_text, secondary_text, hashtags

### followers can change throughout the data so the ID
### needs to be checked in the 2nd tuple element
def return_duplicate_check(top_users_via_followers, _id):
    ans = [i for i in top_users_via_followers if _id in i[1]]
    return (len(ans) > 0)

def return_clean_text(text, stopWords=True):
    if text is None: return []
    # tokenize
    word_tokenizer = lambda x: re.findall(r"\w+(?:[-']\w+)*|'|[-.(]+|\S\w*", x, flags = re.IGNORECASE)
    # lower case
    text = text.lower()
    text = text.translate(str.maketrans('','',string.punctuation))
    text = text.replace('\n', ' ')
    text = [x for x in word_tokenizer(text) if not x in punctuation]
    # remove stopwords
    if stopWords:
        text = [i for i in text if i not in StopWords]
    text = [x for x in text if x.isalpha()]
    return text

def return_collocation_list(text, search):

    def valid_index(length_of_list, index):
        return 0 < index < length_of_list

    if text is None: return []
    try:
        # get list of collocation words 
        clean_text = return_clean_text(text)
        list_len = len(clean_text)
        if list_len <= 1: return []
        # create temporary variable
        collocation_list = []
        # for the index, and element in the list of words
        for idx, ele in enumerate(clean_text):
            # if the root version of the word in the list is in search terms
            if ele in search:
                first_word  = clean_text[idx-1] if valid_index(list_len, idx-1) else 'NA'
                middle_word = clean_text[idx]
                last_word   = clean_text[idx+1] if valid_index(list_len, idx+1) else 'NA'
                collocation_list.append((first_word, middle_word, last_word))

    except IndexError:
        print (text)
    return collocation_list