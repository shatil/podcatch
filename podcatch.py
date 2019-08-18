#!/usr/bin/env python3
"""PodCatch downloads episodes linked from a podcast's RSS feed."""

import argparse
import datetime
import logging
import re
import typing
import urllib.request
import xml.etree.ElementTree


EPISODE_GENERATOR = typing.Generator[typing.Tuple[str, str, str, str], None, None]


def get_xml(link: str) -> xml.etree.ElementTree.Element:
    """Download XML from URL.

    Arguments
    =========
    link
        RSS feed or some other link to an XML document.
    """
    logging.info("Getting XML from %s", link)
    response = urllib.request.urlopen(link)
    return xml.etree.ElementTree.fromstring(response.read())


def get_episodes(tree: xml.etree.ElementTree.Element) -> EPISODE_GENERATOR:
    """Find episodes within XML tree.

    Arguments
    =========
    tree
        Parsed XML from link.

    Yields
    ======
    Tuples of (
        filesystem-safe episode name,
        date,
        description,
        link to download episode's MP3
    ).
    """
    for item in tree.iter("item"):
        title = item.find("title").text
        logging.info("Found episode: %s", title)
        name = re.sub(r"[^\w]", "-", title)  # Non-word characters to dash.
        name = re.sub(r"-+", "-", name).strip("-").lower()
        pub_date = item.find("pubDate").text
        # `pubDate` looks like `Mon, 21 May 2018 00:01:33 -0400`
        date = datetime.datetime.strptime(
            pub_date, "%a, %d %b %Y %H:%M:%S %z"
        ).strftime("%Y-%m-%d")
        yield name, date, item.find("description").text, item.find("enclosure").attrib[
            "url"
        ]


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("link", help="Link to podcast RSS feed.")
    parser.add_argument(
        "--exclude",
        default="originally aired",
        help="Exclude episodes where description includes this.",
    )
    args = parser.parse_args()

    for name, date, description, link in get_episodes(get_xml(args.link)):
        if args.exclude and args.exclude.lower() in description.lower():
            logging.info("Skipping %s", name)
            continue
        print(f"curl -LSfo {date}-{name}.mp3 '{link}'")
