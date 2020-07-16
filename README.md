# teletext-twitter
Display Twitter timelines or searches for tweets and turns them into teletext pages for your Raspberry Pi

![Screenshot](https://i.imgur.com/yPKagm8.jpg "Screenshot 1")

## What is this?
Useless, for a start.. But if you've ever had the desire to read your tweets by pushing the teletext button on your remote and keying a page number then this is the package for you! Retro chic for the social media generation!

## Installation
After cloning the repository you'll need to install the Python-Twitter wrapper with pip:
`pip install python-twitter`

Before you get this up and running there are two other things you need to do first:

1) Connect your Raspberry Pi to a TV over composite using a cable with the correct pin-out. I bought mine from The Pi Hut: https://thepihut.com/products/adafruit-a-v-and-rca-composite-video-audio-cable-for-raspberry-pi
2) Install the VBIT2 and raspi-teletext apps and make sure they are outputting teletext data to your TV

* raspi-teletext (Alistair Buxton): https://github.com/ali1234/raspi-teletext - Only PAL is supported by raspi-teletext
* VBIT2 (Peter Kwan): https://github.com/peterkvt80/vbit2

## Setup
After getting everything installed there's one more setup task to do. Rename config.py-default to config.py and open the file in a text editor.

Now add your Twitter access tokens to the top section. You can find a good guide for doing this here - https://iag.me/socialmedia/how-to-create-a-twitter-app-in-8-easy-steps/ You will need to pick a unique name for the app. Which is annoying. Pick anything you want that isn't taken. Maybe add your name at the end.

## Usage

When you've setup your config.py you can run the script like this example that grabs your home timeline:

`python3 teletext-twitter -m home` (add -h to show options - also listed below)

The script will constantly update your chosen page number (default is 153 - chosen because it used to be used for this purpose on Teefax in the past) in the main teletext folder (which defaults in VBIT2 to /home/pi/teletext/).

All of the files in that folder are sent across to the TV every so often, therefore the script constantly overwrites it with new tweets so that it will update on your screen. Up to 99 subpages of tweets will be displayed - any further tweets will be dropped. Tweets are truncated for space reasons. You kinda have to, really...

## Config options

As well as your Twitter access tokens the following things can be changed in be config.py file:

### Theme support
In the config.py file you can see a theme section. The teletext level I am using supports 7 colours:
* Red 
* Green
* Yellow
* Blue
* Magenta
* Cyan
* White

You can change the colours of:
- the main header bar
- the thin separator bar
- the page title
- tweeter's usernames
- tweet timestamps
- the text of the tweet itself
- the highlight used on search queries

The title text string and colour at the top can be changed, although there is a 30 character limit or things look wonky.

Finally, you can set the fastext link page numbers, and the contents of row 24 (using .tti format 7-bit escaping for control codes).

### Level 2.5 teletext options
These options require appropriate downloading pages and a magazine organisation table to be present in the teletext service. Example files are included for a teletext-twitter page on P153 in the enhancement directory.
- packet_28: if present write value to enhancement packet 28 (string is tti OL,28 row encoding)
- emoji_support: use global dynamic redefineable character set to display certain emoji
- logo_object_triplet: if present this is added to the enhancement packets on each subpage to invoke an object at the location of the twitter logo.

### Miscellaneous options

- tti_path: (default: "/home/pi/teletext/") - the path your pages will be saved to
- page_number: (default: 153) - the page number to use
- cycle_time: (default: 20) - approximate time in seconds between subpages

## Notes
* New tweets are grabbed every 60 seconds by default. This is configurable with the -d option, but you do have be aware of the Twitter API limits. 60 seconds is the minimum
* Up to 99 subpages are written.
* Emoji stripping is now included. Mostly.
* URLs are stripped and replaced with the placeholder [LINK]
* Level 1.5 teletext is supported - meaning more characters are now supported! There you go, Europeans!

Apart from those notes, things should work ok. Have fun, turn back the clock, and if you genuinely use this for anything please let me know (also you're mental/cool).

### -h/--help output

<pre>
usage: teletext-twitter [-h] [-m MODE] [-q QUERY] [-c COUNT] [-d DELAY] [-n]
                        [-v] [-Q]

Reads your Twitter timeline and turns it into teletext pages for your
Raspberry Pi.

optional arguments:
  -h, --help            show this help message and exit
  -m MODE, --mode MODE  choose between different modes - home, user or search
  -q QUERY, --query QUERY
                        a search query, either a search term or a username.
                        hashtags supported if you put quotes around the string
  -c COUNT, --count COUNT
                        number of tweets to download (default is 5, capped at
                        200)
  -d DELAY, --delay DELAY
                        seconds between timeline scrapes (default is 60
                        seconds - lower values have no effect)
  -n, --no-repeat       only download tweets once - overrules -d switch
  -v, --version         show program's version number and exit
  -Q, --quiet           suppresses all output to the terminal except warnings
                        and errors
</pre>
