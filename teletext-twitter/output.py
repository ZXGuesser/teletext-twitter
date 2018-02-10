# teletext-twitter - creates pages for vbit2 teletext system
# (c) Mark Pentler 2018 (https://github.com/mpentler)
# see README.md for details on getting it running or run with -h
# output module

from processor import *
import time

# define our control codes here for easy use later
ESCAPE = chr(27)
DOUBLE_HEIGHT = ESCAPE + chr(77)
SET_BACKGROUND = ESCAPE + chr(93)
TWITTER_BIRD = chr(41) + chr(108) + chr(39)
text_colours = {"red" : 65, "green" : 66, "yellow" : 67 , "blue" : 68, "magenta" : 69, "cyan" : 70, "white" : 71}
mosaic_colours = {"red" : 81, "green" : 82, "yellow" : 83, "blue" : 84, "magenta" : 85, "cyan" : 86, "white" : 87}

def write_tweet_info(file, line_num, username, timestamp, config):
    string = "OL," + str(line_num) + ","
    string += "`" * (35-len(timestamp)-len(username))
    string += ESCAPE + chr(text_colours[config["username_colour"]]) +"@" + username
    string += ESCAPE + chr(text_colours["white"]) + "|"
    string += ESCAPE + chr(text_colours[config["timestamp_colour"]]) + timestamp
    string += "\r\n"
    file.write(string)

def write_tweet_line(file, line_num, line, config):
    string = "OL," + str(line_num) + ","
    string += ESCAPE + chr(text_colours[config["tweet_colour"]]) + line
    string += "\r\n"
    file.write(string)

def write_header(file, subpage, max_subpages, config): # write a header for the page and pop a nice banner at the top
    page_title = config["page_title"] + " " + "{:02d}/{:02d}".format(subpage, max_subpages)
    logo_spacer = " " * (39 - (4 + len(page_title) + 5))
    if subpage == 1: # we only want these lines once
        file.write("DE,Autogenerated by Teletext-Twitter\r\n")
        file.write("SC,0000\r\n")
        file.write("PS,8000\r\n")
        file.write("CT," + str(config["cycle_time"]) + ",T\r\n")
    file.write("PN," + str(config["page_number"]) + "{:02}\r\n".format(subpage))
    file.write("OL,1," + ESCAPE + chr(text_colours[config["header_colour"]]) + SET_BACKGROUND +
               DOUBLE_HEIGHT + ESCAPE + chr(text_colours[config["page_title_colour"]]) + page_title +
               logo_spacer + ESCAPE + chr(mosaic_colours["cyan"]) + TWITTER_BIRD + "\r\n")
    file.write("OL,3," + ESCAPE + chr(mosaic_colours[config["header_separator"]]) + (chr(35) * 39) + "\r\n")

def write_tweets(twitter_object, mode, count, config, query=None): # grab the latest timeline
    if mode == "home":
        statuses = twitter_object.GetHomeTimeline(count=count)
    elif mode == "search":
        statuses = twitter_object.GetSearch(term=query, result_type="recent", count=count)
    elif mode == "user":
        statuses = twitter_object.GetUserTimeline(screen_name=query, count=count)

    filename = config["tti_path"] + "P" + str(config["page_number"]) + ".tti"
    subpage = 1

    # pre-calculate how many subpages we're going to
    # write - is there a better way of doing this?
    line_position = 4
    for status in statuses:
        tweet_text = tweet_remove_emojis(status.text)
        tweet_text = tweet_remove_urls(tweet_text)
        tweet_text = charsub(tweet_text)
        tweet_text = textwrap.wrap(tweet_text, 38)
        post_length = len(tweet_text) + 1
        if (line_position + post_length) > 25:
            subpage += 1
            if subpage > 99:
                break # reached subpage limit - no point checking the rest
            line_position = 4
        line_position += post_length
    max_subpages = min(subpage, 99)

    # reset everything for the actual writing
    subpage = 1
    with open(filename, "w+") as file:
        write_header(file, subpage, max_subpages, config)
    line_position = 4

    for status in statuses: # iterate through our responses
        tweet_text = tweet_remove_emojis(status.text)
        tweet_text = tweet_remove_urls(tweet_text)
        tweet_text = charsub(tweet_text)
        tweet_text = textwrap.wrap(tweet_text, 38) # make sure our lines fit on the screen
        tweet_time = time.strptime(status.created_at,"%a %b %d %H:%M:%S +0000 %Y")
        tweet_human_time = time.strftime("%d-%b-%Y %H:%M", tweet_time) # reformat time/date output
        tweet_username = charsub(status.user.screen_name)

        with open(filename, "a") as file:
            post_length = len(tweet_text) + 1 # how long is our next tweet? (including info line)
            if (line_position + post_length) > 25: # are we about to go over the page?
                for blankline_position in range(line_position, 25): # how many blank lines do we need?
                    file.write("OL,{},\r\n".format(blankline_position))
                subpage += 1 # start a new page
                if subpage > 99:
                    break # reached subpage limit - dump the rest
                write_header(file, subpage, max_subpages, config)
                line_position = 4 # and reset our cursor
            write_tweet_info(file, line_position, tweet_username, tweet_human_time, config)
            line_position += 1
            for line in tweet_text:
                write_tweet_line(file, line_position, line, config)
                line_position += 1
