import logging
from fake_useragent import UserAgent as ua
from scraper_api import ScraperAPIClient


logging.getLogger("urllib3").setLevel(logging.WARNING)

class Client:
    client = ScraperAPIClient("4da56c39f7acf50aeb8e1f62ace21731")
    proxies = {
        "http": "http://scraperapi:4da56c39f7acf50aeb8e1f62ace21731@proxy-server.scraperapi.com:8001"
    }

    user_agent = ua()
    accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,'
    accept += 'image/avif,image/webp,image/apng,*/*;q=0.8,application'
    accept += '/signed-exchange;v=b3;q=0.9'

    headers = {
        'User-Agent': user_agent.random,
        'Accept': accept,
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Cookie': "disclaimer=Y",
        'Host': '',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Referer': "",
        'Upgrade-Insecure-Requests': '1',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Linux'
    }
