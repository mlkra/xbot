# Copyright (C) 2022  Michał Krasoń
import re

import requests
from bs4 import BeautifulSoup
from typing_extensions import Self
from xbot.settings import settings
from xbot.xkom_api_client.schemas import Product

CHROME_UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
)


class XKomAPIClient:
    def __init__(self):
        self.session = None
        self.xkom_url = settings.xkom_url
        self.xkom_api_url = settings.xkom_api_url

    def __enter__(self) -> Self:
        self.session = requests.Session()

        self.session.headers.update({"User-Agent": CHROME_UA})

        api_key = self._get_api_key()
        self.session.headers.update({"X-API-KEY": api_key})

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session = None

    def get_product(self, product_id: str) -> Product | None:
        response = self.session.get(
            f"{self.xkom_api_url}/api/v1/xkom/products/{product_id}"
        )
        if response.status_code != 200:
            return None
        return response.json()

    def _get_api_key(self) -> str:
        response = self.session.get(self.xkom_url)
        soup = BeautifulSoup(response.text, "html.parser")
        tag = soup.head.find("script", type="module", src=re.compile("chunk-app"))
        js_script = self.session.get(f'http:{tag["src"]}').text

        m = re.search(r'{path:"/api/v1/xkom",key:"(\w+)"}', js_script)

        return m.group(1)
