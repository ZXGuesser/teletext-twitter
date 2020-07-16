# teletext-twitter - creates pages for vbit2 teletext system
# (c) Mark Pentler 2018 (https://github.com/mpentler)
# see README.md for details on getting it running or run with -h
# text processor module

import textwrap
import re

ESCAPE = chr(27)
text_colours = {"red" : 65, "green" : 66, "yellow" : 67 , "blue" : 68, "magenta" : 69, "cyan" : 70, "white" : 71}

def tweet_remove_emojis(tweet, config):
    # remove pesky emoji characters
    
    if config["emoji_support"] == True:
        # leave supported emoji
        emoji_pattern = re.compile("[" # our unicode ranges go here. this will need frequent tweaking
                                  u"\U00002300-\U000023FF" # misc technical
                                  u"\U0001F680-\U0001F9FF" # transport & map symbols
                                  u"\U0001F1E6-\U0001F1FF" # regional indicator symbols
                                   "]+", flags=re.UNICODE)
    else:
        emoji_pattern = re.compile("[" # our unicode ranges go here. this will need frequent tweaking
                                  u"\U00002300-\U000023FF" # misc technical
                                  u"\U000024C2-\U0001F251" # enclosed characters including flags
                                  u"\U0001F300-\U0001F5FF" # symbols & pictographs
                                  u"\U0001F600-\U0001F67F" # emoticons
                                  u"\U0001F680-\U0001F9FF" # transport & map symbols
                                  u"\U0001F1E6-\U0001F1FF" # regional indicator symbols
                                   "]+", flags=re.UNICODE)
    tweet = emoji_pattern.sub(r'', tweet)
    return tweet

def tweet_remove_urls(tweet):
    # all tweets are https t.co links, so this is all we need
    url_pattern = re.compile("https://\S+")
    tweet = url_pattern.sub('<LINK>', tweet)
    return tweet

def tweet_highlight_query(tweet, query, config):
    tweet = tweet.replace((" " + query + " "),
                          (ESCAPE + chr(text_colours[config["search_highlight"]]) + query + ESCAPE + chr(text_colours[config["tweet_colour"]])))
    return tweet

def charsub(text):
    # do any substitutitons that will change the length of the text
    text = text.replace("…", "...")
    text = text.replace("Ǆ", "DŽ")
    text = text.replace("ǅ", "Dž")
    text = text.replace("ǆ", "dž")
    text = text.replace("&lt;", "<")
    text = text.replace("&gt;", ">")
    text = text.replace("&amp;", "&")

    # map similar characters to one canonical unicode point
    text = text.replace("€", "₠")
    text = re.sub("[··᛫‧∙⋅⋅⸱⸳・ꞏ]","·",text,flags=re.UNICODE)
    text = text.replace("•", "●")
    text = text.replace("Ș", "Ş")
    text = text.replace("ș", "ş")
    text = text.replace("Å", "Å")
    text = text.replace("„", "”")
    text = text.replace("‟", "“")
    text = re.sub("[‒–—]","―",text,flags=re.UNICODE) # dashes to horizontal bar
    
    # emoji stuff
    text = re.sub("[😊☺]","🙂",text,flags=re.UNICODE) # like slightly smiling face
    text = re.sub("[😁😃😄😆]","😀",text,flags=re.UNICODE) # like grinning face
    text = text.replace("😝", "😛") # face with tongue
    text = text.replace("🤣", "😂") # rofl -> face with tears of joy
    text = text.replace("🤓", "😎") # nerd -> sunglasses
    text = re.sub("[☹😦]","🙁",text,flags=re.UNICODE) # like slightly frowning face
    text = re.sub("[😭😥]", "😢",text,flags=re.UNICODE) # like crying face
    text = re.sub("[🤚👋🖐]","✋",text,flags=re.UNICODE) # like raised hand
    text = re.sub("["u"\U0000FE00-\U0000FE0F]","",text,flags=re.UNICODE) # strip variation selectors
    
    return text

enhancementmapping = {
    # map to L1 replacement character, enhancement mode, enhancement data
    # these can be mapped to level 1 characters provided we are using the English language (which we always are right now)
    
    "£":[0x23,0,0],
    "←":[0x5b,0,0],
    "½":[0x5c,0,0],
    "→":[0x5d,0,0],
    "↑":[0x5e,0,0],
    "#":[0x5F,0,0],
    "―":[0x60,0,0],
    "¼":[0x7b,0,0],
    "‖":[0x7c,0,0],
    "¾":[0x7d,0,0],
    "÷":[0x7e,0,0],
    
    # no diacritic - i.e. the Latin G0 character set
    # 0x23 character already present in English NOS
    "¤":[0x7f,0x10,0x24],
    "[":[0x28,0x10,0x5b],
    "\\":[0x2f,0x10,0x5c],
    "]":[0x29,0x10,0x5d],
    "^":[0x20,0x10,0x5e], # don't map this to the English ↑ because of bug in Philips TVs
    "_":[0x20,0x10,0x5f], # don't map this to the English ― because of bug in Philips TVs
    "`":[0x27,0x10,0x60],
    "{":[0x28,0x10,0x7b],
    "|":[0x20,0x10,0x7c], # don't map this to the English ‖ because of bug in Philips TVs
    "}":[0x29,0x10,0x7d],
    "~":[0x7f,0x10,0x7e],

    # grave AEIOUaeiou
    "À":[0x41,0x11,0x41],"È":[0x45,0x11,0x45],"Ì":[0x49,0x11,0x49],"Ò":[0x4F,0x11,0x4F],"Ù":[0x55,0x11,0x55],
    "à":[0x61,0x11,0x61],"è":[0x65,0x11,0x65],"ì":[0x69,0x11,0x69],"ò":[0x6F,0x11,0x6F],"ù":[0x75,0x11,0x75],

    # acute ACEILNORSUYZacegilnorsuyz
    "Á":[0x41,0x12,0x41],"Ć":[0x43,0x12,0x43],"É":[0x45,0x12,0x45],"Í":[0x49,0x12,0x49],"Ĺ":[0x4c,0x12,0x4c],"Ń":[0x4e,0x12,0x4e],"Ó":[0x4f,0x12,0x4f],"Ŕ":[0x52,0x12,0x52],"Ś":[0x53,0x12,0x53],"Ú":[0x55,0x12,0x55],"Ý":[0x59,0x12,0x59],"Ź":[0x5a,0x12,0x5a],
    "á":[0x61,0x12,0x61],"ć":[0x63,0x12,0x63],"é":[0x65,0x12,0x65],"í":[0x69,0x12,0x69],"ĺ":[0x6c,0x12,0x6c],"ń":[0x6e,0x12,0x6e],"ó":[0x6f,0x12,0x6f],"ŕ":[0x72,0x12,0x72],"ś":[0x73,0x12,0x73],"ú":[0x75,0x12,0x75],"ý":[0x79,0x12,0x79],"ź":[0x7a,0x12,0x7a],

    # circumflex ACEGHIJOSUWYaceghijosuwy
    "Â":[0x41,0x13,0x41],"Ĉ":[0x43,0x13,0x43],"Ê":[0x45,0x13,0x45],"Ĝ":[0x47,0x13,0x47],"Ĥ":[0x48,0x13,0x48],"Î":[0x49,0x13,0x49],"Ĵ":[0x4a,0x13,0x4a],"Ô":[0x4f,0x13,0x4f],"Ŝ":[0x53,0x13,0x53],"Û":[0x55,0x13,0x55],"Ŵ":[0x57,0x13,0x57],"Ý":[0x59,0x13,0x59],
    "â":[0x61,0x13,0x61],"ĉ":[0x63,0x13,0x63],"ê":[0x65,0x13,0x65],"ĝ":[0x67,0x13,0x67],"ĥ":[0x68,0x13,0x68],"î":[0x69,0x13,0x69],"ĵ":[0x6a,0x13,0x6a],"ô":[0x6f,0x13,0x6f],"ŝ":[0x73,0x13,0x73],"û":[0x75,0x13,0x75],"ŵ":[0x77,0x13,0x77],"ý":[0x79,0x13,0x79],

    # tilde AINOUainou
    "Ã":[0x41,0x14,0x41],"Ĩ":[0x49,0x14,0x49],"Ñ":[0x4e,0x14,0x4e],"Õ":[0x4f,0x14,0x4f],"Ũ":[0x55,0x14,0x55],
    "ã":[0x61,0x14,0x61],"ĩ":[0x69,0x14,0x69],"ñ":[0x6e,0x14,0x6e],"õ":[0x6f,0x14,0x6f],"ũ":[0x75,0x14,0x75],

    # macron AEIOUaeiou
    "Ā":[0x41,0x15,0x41],"Ē":[0x45,0x15,0x45],"Ī":[0x49,0x15,0x49],"Ō":[0x4f,0x15,0x4f],"Ū":[0x55,0x15,0x55],
    "ā":[0x61,0x15,0x61],"ē":[0x65,0x15,0x65],"ī":[0x69,0x15,0x69],"ō":[0x6f,0x15,0x6f],"ū":[0x75,0x15,0x75],

    # breve AGUagu
    "Ă":[0x41,0x16,0x41],"Ğ":[0x47,0x16,0x47],"Ŭ":[0x55,0x16,0x55],
    "ă":[0x61,0x16,0x61],"ğ":[0x67,0x16,0x67],"ŭ":[0x75,0x16,0x75],

    # dot CEGIZcegz
    "Ċ":[0x43,0x17,0x43],"Ė":[0x45,0x17,0x45],"Ġ":[0x47,0x17,0x47],"İ":[0x49,0x17,0x49],"Ż":[0x5a,0x17,0x5a],
    "ċ":[0x63,0x17,0x63],"ė":[0x65,0x17,0x65],"ġ":[0x67,0x17,0x67],"ż":[0x7a,0x17,0x7a],

    # diaeresis/umlaut AEIOUYaeiouy
    "Ä":[0x41,0x18,0x41],"Ë":[0x45,0x18,0x45],"Ï":[0x49,0x18,0x49],"Ö":[0x4f,0x18,0x4f],"Ü":[0x55,0x18,0x55],"Ÿ":[0x59,0x18,0x59],
    "ä":[0x61,0x18,0x61],"ë":[0x65,0x18,0x65],"ï":[0x69,0x18,0x69],"ö":[0x6f,0x18,0x6f],"ü":[0x75,0x18,0x75],"ÿ":[0x79,0x18,0x79],

    # ring AUau
    "Å":[0x41,0x1a,0x41],"Ů":[0x55,0x1a,0x55],
    "å":[0x61,0x1a,0x61],"ů":[0x75,0x1a,0x75],

    # cedilla CGKLNRSTcklnrst
    "Ç":[0x43,0x1b,0x43],"Ģ":[0x47,0x1b,0x47],"Ķ":[0x4b,0x1b,0x4b],"Ļ":[0x4c,0x1b,0x4c],"Ņ":[0x4e,0x1b,0x4e],"Ŗ":[0x52,0x1b,0x52],"Ş":[0x53,0x1b,0x53],"Ț":[0x54,0x1b,0x54],
    "ç":[0x63,0x1b,0x63],"ķ":[0x6b,0x1b,0x6b],"ļ":[0x6c,0x1b,0x6c],"ņ":[0x6e,0x1b,0x6e],"ŗ":[0x72,0x1b,0x72],"ş":[0x73,0x1b,0x73],"ț":[0x74,0x1b,0x74],

    # double acute OUou
    "Ő":[0x4f,0x1d,0x4f],"Ű":[0x55,0x1d,0x55],
    "ő":[0x6f,0x1d,0x6f],"ű":[0x75,0x1d,0x75],

    # ogonek AEIUaeiu
    "Ą":[0x41,0x1e,0x41],"Ę":[0x45,0x1e,0x45],"Į":[0x49,0x1e,0x49],"Ų":[0x55,0x1e,0x55],
    "ą":[0x61,0x1e,0x61],"ę":[0x65,0x1e,0x65],"į":[0x69,0x1e,0x69],"ų":[0x75,0x1e,0x75],

    # caron/háček CDELNRSTZcdelnrstz
    "Č":[0x43,0x1f,0x43],"Ď":[0x44,0x1f,0x44],"Ě":[0x45,0x1f,0x45],"Ľ":[0x4c,0x1f,0x4c],"Ň":[0x4e,0x1f,0x4e],"Ř":[0x52,0x1f,0x52],"Š":[0x53,0x1f,0x53],"Ť":[0x54,0x1f,0x54],"Ž":[0x5a,0x1f,0x5a],
    "č":[0x63,0x1f,0x63],"ď":[0x64,0x1f,0x64],"ě":[0x65,0x1f,0x65],"ľ":[0x6c,0x1f,0x6c],"ň":[0x6e,0x1f,0x6e],"ř":[0x72,0x1f,0x72],"š":[0x73,0x1f,0x73],"ť":[0x74,0x1f,0x74],"ž":[0x7a,0x1f,0x7a],
    # symbols from the Latin G2 supplementary set
    "¡":[0x21,0x0F,0x21],
    "¢":[0x63,0x0F,0x22],
    # 0x23 character already present in English NOS
    # 0x24 character already present in English NOS
    "¥":[0x59,0x0F,0x25],
    # 0x26 character already present in English NOS
    "§":[0x53,0x0F,0x27],
    # 0x28 already mapped from G0 set
    "‘":[0x27,0x0F,0x29],
    "“":[0x22,0x0F,0x2a],
    "«":[0x3c,0x0F,0x2b],
    # 0x2c character already present in English NOS
    # 0x2d character already present in English NOS
    # 0x2e character already present in English NOS
    "↓":[0x7f,0x0F,0x2f],
    "°":[0x7f,0x0F,0x30],
    "±":[0x7f,0x0F,0x31],
    "²":[0x7f,0x0F,0x32],
    "³":[0x7f,0x0F,0x33],
    "×":[0x7f,0x0F,0x34],
    "µ":[0x7f,0x0F,0x35],
    "¶":[0x7f,0x0F,0x36],
    "·":[0x7f,0x0F,0x37],
    # 0x38 characeter already present in English NOS
    "’":[0x27,0x0F,0x39],
    "”":[0x22,0x0F,0x3a],
    "»":[0x3e,0x0F,0x3b],
    # 0x3c character already present in English NOS
    # 0x3d character already present in English NOS
    # 0x3e character already present in English NOS
    "¿":[0x3F,0x0F,0x3f],
    # 0x40-0x4f are the diacritic characters
    # 0x50 character already present in English NOS
    "¹":[0x7f,0x0F,0x51],
    "®":[0x7f,0x0F,0x52],
    "©":[0x7f,0x0F,0x53],
    "™":[0x7f,0x0F,0x54],
    "♪":[0x7f,0x0F,0x55],
    "₠":[0x45,0x0F,0x56],
    "‰":[0x7f,0x0F,0x57],
    "∝":[0x7f,0x0F,0x58],
    # 0x59-0x5b are reserved
    "⅛":[0x7f,0x0F,0x5c],
    "⅜":[0x7f,0x0F,0x5d],
    "⅝":[0x7f,0x0F,0x5e],
    "⅞":[0x7f,0x0F,0x5f],
    "Ω":[0x7f,0x0F,0x60],
    "Æ":[0x7f,0x0F,0x61],
    "Đ":[0x44,0x0F,0x62],
    "ª":[0x61,0x0F,0x63],
    "Ħ":[0x48,0x0F,0x64],
    # 0x65 is reserved
    "Ĳ":[0x7f,0x0F,0x66],
    "Ŀ":[0x4C,0x0F,0x67],
    "Ł":[0x4C,0x0F,0x68],
    "Ø":[0x4f,0x0F,0x69],
    "Œ":[0x7f,0x0F,0x6a],
    "º":[0x6f,0x0F,0x6b],
    "Þ":[0x7f,0x0F,0x6c],
    "Ŧ":[0x4f,0x0F,0x6d],
    "Ŋ":[0x7f,0x0F,0x6e],
    "ŉ":[0x6e,0x0F,0x6f],
    "ĸ":[0x71,0x0F,0x70],
    "æ":[0x7f,0x0F,0x71],
    "đ":[0x64,0x0F,0x72],
    "ð":[0x64,0x0F,0x73],
    "ħ":[0x68,0x0F,0x74],
    "ı":[0x69,0x0F,0x75],
    "ĳ":[0x7f,0x0F,0x76],
    "ŀ":[0x6C,0x0F,0x77],
    "ł":[0x6C,0x0F,0x78],
    "ø":[0x6f,0x0F,0x79],
    "œ":[0x7f,0x0F,0x7a],
    "ß":[0x73,0x0F,0x7b],
    "þ":[0x7f,0x0F,0x7c],
    "ŧ":[0x4f,0x0F,0x7d],
    "ŋ":[0x7f,0x0F,0x7e],
    
    # G1 mosaics
    "▌":[0x7f,0x01,0x35],
    "▐":[0x7f,0x01,0x6a],
    "█":[0x7f,0x01,0x7f],
    
    # G3 smooth mosaics and line drawing set
    "▒":[0x7f,0x02,0x2f],
    "●":[0x7f,0x02,0x4D],
    "⬤":[0x7f,0x02,0x4E],
    "◯":[0x4f,0x02,0x4F],
    
    # emojis from custom gdrcs
    "🙂":[0x20,0x0D,0x00], # slightly smiling face
    "😀":[0x20,0x0D,0x01], # grinning face
    "😛":[0x20,0x0D,0x02], # face with tongue
    "😉":[0x20,0x0D,0x03], # winking face
    "😂":[0x20,0x0D,0x04], # face with tears of joy
    "😎":[0x20,0x0D,0x05], # smiling face with sunglasses
    "😜":[0x20,0x0D,0x06], # winking face with tongue
    "😮":[0x20,0x0D,0x07], # face with open mouth
    "😵":[0x20,0x0D,0x08], # dizzy face
    "🙁":[0x20,0x0D,0x09], # slightly frowning face
    "😢":[0x20,0x0D,0x0A], # crying face
    "💯":[0x20,0x0D,0x0B], # hundred points
    "👍":[0x20,0x0D,0x0C], # thumbs up
    "👎":[0x20,0x0D,0x0D], # thumbs down
    "👌":[0x20,0x0D,0x0E], # OK hand
    "✋":[0x20,0x0D,0x0F], # raised hand
    "❤":[0x20,0x0D,0x10], # heavy black heart
    "💔":[0x20,0x0D,0x11], # broken heart
    
    #todo: more mappings
}

def charenhance(text,offset):
    # replace characters in text string for the level 1 page, and return a list of enhancement triplets
    newtext = ""
    enhancements = []
    for index, char in enumerate(text):
        newchar = enhancementmapping.get(char, [ord(char),0,0])
        if newchar[0] > 127:
            newchar = [0x7F,0,0] # blank unknown unicode characters
        newtext += chr(newchar[0])
        if (newchar[1]):
            enhancements.append([index+offset,newchar[1],newchar[2]])
    return newtext,enhancements
