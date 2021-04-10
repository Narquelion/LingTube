import re
from bs4 import BeautifulSoup
from requests import get
from time import sleep

def scrape_channel_info(channel, channel_set, depth, max_depth):

    sleep(1)

    print("Channel: {0}".format(channel))
    print("Depth: {0}".format(depth))

    if depth == max_depth:
          return channel_set

    channels_page = get("https://www.youtube.com/c/" + channel + "/channels")
    channels_html = BeautifulSoup(channels_page.content, "html.parser")

    listed_channels = set(re.findall('\"/user/([a-zA-Z0-9]+)\"', str(channels_html)))
    print("Listed channels: {0}".format(listed_channels))

    if not listed_channels:
        return channel_set

    for new_channel in listed_channels:
        #if new_channel in channel_set:
        #        continue

        channel_set.update(scrape_channel_info(new_channel, listed_channels, depth + 1, max_depth))
        print("Channel set: {0}".format(channel_set))
        print("Listed channels: {0}".format(listed_channels))

    return channel_set

def main():
    max_depth = 5
    channel_set_seed = set(["sophiachang"])
    channel_set = set()
    for channel in channel_set_seed:
        channel_set.update(scrape_channel_info(channel, set(), 1, max_depth))
    print(channel_set)

if __name__ == '__main__':
    main()