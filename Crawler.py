""" Async Web Crawler """

import asyncio
import html
import requests
from re import findall, compile
from requests_html import AsyncHTMLSession
from typing import List


async def get_html_content(url: str) -> AsyncHTMLSession.get:
    """
    Return an html content of a given url

    :param url: A web url.
    :return: Html content of a website.
    """

    session = AsyncHTMLSession()
    response = await session.get(url)
    return response


async def get_all_links(url: str) -> List[str]:
    """
    Find all links in a given url

    :param url: A web url.
    :return: A list of all links found.
    """

    response = await get_html_content(url)
    links = response.html.absolute_links
    return links


class web_crawler:
    """ A Web Crawler class consisting different methods that implement it """

    def __init__(self, url: str):
        """
        An initialise method which define the self variables

        :param url: A web url to crawl at.
        """

        self.url = url
        self.visited_urls = []

    def check_visited(self, url: str) -> bool:
        """
        Check if the given url was already visited by the web crawler

        :param url: A web url.
        :return: True if the given url was visited and False if not.
        """

        if url in self.visited_urls:
            return True
        else:
            return False

    async def crawl(self, url: str):
        """
        Crawl in a given url

        :param url: A url to crawl in.
        """

        for link in await get_all_links(url):
            if not self.check_visited(link):
                self.visited_urls.append(link)
                await self.crawl(link)

    async def start_crawling(self):
        """ Start crawling in the first url """

        await self.crawl(self.url)


async def main():
    """ Build a Web Crawler and start it """

    crawler = web_crawler("https://www.google.com")
    await crawler.start_crawling()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
