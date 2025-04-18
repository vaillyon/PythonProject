import sys
import tempfile  # create audio files
import webbrowser  # open podcast file
import feedparser  # parse RSS to URL
import requests  # fetch files
import argparse  # parse command line


def parse_args():

    # command line arguments listed


    parser = argparse.ArgumentParser(description="Simple command line podcast application.")
    parser.add_argument("feeds", nargs="+", help="RSS feed URLs")

    parser.add_argument("-s", action="store_true", help="Omit each item’s summary.")
    parser.add_argument("-n", type=int, help="Display at most x podcast items.")
    parser.add_argument("-p", type=int, help="Play the xth podcast from the feed.")
    return parser.parse_args( )


def fetch_feed(url):

   # parse RSS for URL

    try:
        feed = feedparser.parse(url)
        if not feed.entries:

            print(f"Warning: No valid entries found for feed: {url}", file=sys.stderr)
        return feed
    except Exception as e:
        print(f"Error fetching feed {url}: {e}", file=sys.stderr)
        return None


def display_feed(feed, omit_summary, max_items):

   # shows title, author, date, and link

    if "title" in feed.feed:
        print(f"\nFeed: {feed.feed.title}\n" + "=" * 40)

    count = 0
    for entry in feed.entries[:max_items]:
        print(f"Title: {entry.get('title', 'No title')}")
        print(f"Author: {entry.get('author', 'Unknown')}")
        print(f"Date: {entry.get('published', 'No date')}")
        print(f"Link: {entry.get('link', 'No link')}")
        if not omit_summary:
            print(f"Summary: {entry.get('summary', 'No summary')}")
        print("-" * 40)
        count += 1

    if count == 0:
        print("No items found.")


def play_podcast(feed, podcast_index):

    # play a podcast by getting audio file and open in browser

    try:
        #  podcast entry, this will go through if statments and check each one
        entry = feed.entries[podcast_index - 1]

        #  first audio link
        audio_url = next((link.href for link in entry.links if link.type.startswith("audio")), None)
        if not audio_url:
            print("No audio link found for the selected podcast.", file=sys.stderr)
            return

        #  podcast entry
        entry = feed.entries[podcast_index - 1]

        #  first audio link
        audio_url = next((link.href for link in entry.links if link.type.startswith("audio")), None)
        if not audio_url:
            print("No audio link found for the selected podcast.", file=sys.stderr)
            return

        # Download  audio
        response = requests.get(audio_url, stream=True)
        if response.status_code != 200:
            print("Failed to download podcast.", file=sys.stderr)
            return

        # stores
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:

                    temp_audio.write(chunk)
            temp_audio_path = temp_audio.name

        # pen audio
        print(f"Playing: {entry.title}" )
        webbrowser.open(temp_audio_path)
    except IndexError:
        print("Invalid podcast index.", file=sys.stderr)
    except Exception as e:
        print(f"Error playing podcast: {e}", file=sys.stderr)


def main( ):

    # give details

    args = parse_args()

    for feed_url in  args.feeds:
        feed = fetch_feed(feed_url)
        if not feed:
            continue

        if args.p:
            play_podcast (feed, args.p)
        else:
            display_feed(feed, args.s, args.n if args.n else len(feed.entries))


if __name__ == "__main__":
    main()




