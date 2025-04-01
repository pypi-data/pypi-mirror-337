from __future__ import annotations

import asyncio
import logging
import os
import warnings
from datetime import datetime, timezone
from functools import cached_property
from itertools import cycle
from random import shuffle
from time import time
from types import TracebackType
from typing import Any, Literal, Optional

import aiohttp
from lxml.etree import _Element
from lxml.html import HTMLParser as LHTMLParser
from lxml.html import document_fromstring

from .exceptions import (
    DuckDuckGoSearchException,
    RatelimitException,
    TimeoutException,
    ValueValidationError,
)

from .utils import (
    _expand_proxy_tb_alias,
    _extract_vqd,
    _normalize,
    _normalize_url,
    json_loads,
)

logger = logging.getLogger("duckduckgo_search.aDDGS")

class aDDGS:
    """DuckDuckGo search class for asynchronous searches on duckduckgo.com.

    This class provides methods to perform various types of searches (text, images, videos, news)
    on DuckDuckGo using asynchronous HTTP requests, optimizing performance for concurrent operations.

    Attributes:
        headers (dict[str, str]): Custom headers for HTTP requests.
        proxy (str | None): Proxy URL for HTTP requests.
        timeout (int): Timeout in seconds for each HTTP request.
        verify (bool): Whether to verify SSL certificates.
        enable_rate_limit (bool): Whether rate limiting is enabled.
        min_request_interval (float): Minimum time between requests for rate limiting.
        delay_if_needed (float): Delay to apply if rate limit conditions are met.
        client (aiohttp.ClientSession | None): The HTTP client session.
        sleep_timestamp (float): Timestamp of the last request for rate limiting.
    """

    _impersonates = (
        "chrome_100", "chrome_101", "chrome_104", "chrome_105", "chrome_106", "chrome_107",
        "chrome_108", "chrome_109", "chrome_114", "chrome_116", "chrome_117", "chrome_118",
        "chrome_119", "chrome_120", "chrome_123", "chrome_124", "chrome_126", "chrome_127",
        "chrome_128", "chrome_129", "chrome_130", "chrome_131", "chrome_133",
        "safari_ios_16.5", "safari_ios_17.2", "safari_ios_17.4.1", "safari_ios_18.1.1",
        "safari_15.3", "safari_15.5", "safari_15.6.1", "safari_16", "safari_16.5",
        "safari_17.0", "safari_17.2.1", "safari_17.4.1", "safari_17.5",
        "safari_18", "safari_18.2",
        "safari_ipad_18",
        "edge_101", "edge_122", "edge_127", "edge_131",
        "firefox_109", "firefox_117", "firefox_128", "firefox_133", "firefox_135",
    )  # fmt: skip
    _impersonates_os = ("android", "ios", "linux", "macos", "windows")

    def __init__(
        self,
        headers: dict[str, str] | None = None,
        proxy: str | None = None,
        proxies: dict[str, str] | str | None = None,  # deprecated
        timeout: int | None = 10,
        verify: bool = True,
        enable_rate_limit: bool = True,
        min_request_interval: float = 20.0,
        delay_if_needed: float = 0.75,
    ) -> None:
        """Initialize the aDDGS object with customizable HTTP and rate limiting settings.

        Args:
            headers (dict[str, str] | None, optional): Custom headers for HTTP requests, e.g., {"Accept": "application/json"}.
                Useful for mimicking specific browsers or passing additional metadata. Defaults to None, using a default User-Agent.
            proxy (str | None, optional): Proxy URL for HTTP requests, e.g., "http://user:pass@example.com:3128".
                Supports HTTP, HTTPS, and SOCKS5 proxies. Overrides environment variable "aDDGS_PROXY" if set. Defaults to None.
            proxies (dict[str, str] | str | None, optional): Deprecated. Use 'proxy' instead. Maintained for backward compatibility.
            timeout (int | None, optional): Total timeout in seconds for each HTTP request. Applies to connection and read time.
                Defaults to 10 seconds.
            verify (bool, optional): Whether to verify SSL certificates. Set to False for self-signed certificates or certain proxies,
                but this reduces security by skipping certificate validation. Defaults to True.
            enable_rate_limit (bool, optional): Enables rate limiting to prevent hitting DuckDuckGo's request limits.
                If False, no delays are applied between requests. Defaults to True.
            min_request_interval (float, optional): Minimum interval in seconds between consecutive requests when rate limiting
                is enabled. If the time since the last request is less than this, a delay is applied. Defaults to 20.0 seconds.
            delay_if_needed (float, optional): Delay in seconds to sleep if the time since the last request is less than
                `min_request_interval`. Set to 0 to effectively disable delays while keeping rate limit logic. Defaults to 0.75 seconds.
        """
        aDDGS_proxy: str | None = os.environ.get("aDDGS_PROXY")
        self.proxy: str | None = aDDGS_proxy if aDDGS_proxy else _expand_proxy_tb_alias(proxy)
        assert self.proxy is None or isinstance(self.proxy, str), "proxy must be a str"
        if not proxy and proxies:
            warnings.warn("'proxies' is deprecated, use 'proxy' instead.", stacklevel=1)
            self.proxy = proxies.get("http") or proxies.get("https") if isinstance(proxies, dict) else proxies
        self.headers = headers if headers else {}
        self.headers["User-Agent"] = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
        )
        self.headers["Referer"] = "https://duckduckgo.com/"
        self.timeout = timeout
        self.verify = verify
        self.enable_rate_limit = enable_rate_limit
        self.min_request_interval = min_request_interval
        self.delay_if_needed = delay_if_needed
        self.client: Optional[aiohttp.ClientSession] = None
        self.sleep_timestamp = 0.0

    async def __aenter__(self) -> "aDDGS":
        """Asynchronous context manager entry to initialize the HTTP client session.

        Returns:
            aDDGS: The initialized instance.
        """
        connector = aiohttp.TCPConnector(ssl=self.verify)
        self.client = aiohttp.ClientSession(
            headers=self.headers,
            connector=connector,
            timeout=aiohttp.ClientTimeout(total=self.timeout),
        )
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]] = None,
        exc_val: Optional[BaseException] = None,
        exc_tb: Optional[TracebackType] = None,
    ) -> None:
        """Asynchronous context manager exit to close the HTTP client session."""
        if self.client:
            await self.client.close()

    @cached_property
    def parser(self) -> LHTMLParser:
        """Get a cached HTML parser for efficient parsing of responses.

        Returns:
            LHTMLParser: Configured parser with optimizations (e.g., removing blank text, comments).
        """
        return LHTMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True, collect_ids=False)

    async def _sleep(self) -> None:
        """Asynchronously sleep between API requests if rate limiting is enabled and necessary.

        This method checks the time since the last request against `min_request_interval`. If less time has passed
        and rate limiting is enabled, it sleeps for `delay_if_needed` seconds to enforce the interval.
        """
        if self.enable_rate_limit:
            now = time()
            if self.sleep_timestamp and now - self.sleep_timestamp < self.min_request_interval:
                await asyncio.sleep(self.delay_if_needed)
            self.sleep_timestamp = now

    async def _get_url(
        self,
        method: Literal["GET", "HEAD", "OPTIONS", "DELETE", "POST", "PUT", "PATCH"],
        url: str,
        params: dict[str, str] | None = None,
        content: bytes | None = None,
        data: dict[str, str] | None = None,
        headers: dict[str, str] | None = None,
        cookies: dict[str, str] | None = None,
        json: Any = None,
        timeout: float | None = None,
    ) -> aiohttp.ClientResponse:
        """Asynchronously fetch a URL with the specified HTTP method and parameters.

        This method sends an HTTP request to the specified URL using the given method and parameters.
        **It returns the response object regardless of the status code, allowing the caller to handle
        the response appropriately.**

        Args:
            method (Literal): HTTP method to use (e.g., "GET", "POST").
            url (str): The URL to fetch.
            params (dict[str, str] | None, optional): Query parameters. Defaults to None.
            content (bytes | None, optional): Raw content for the request body. Defaults to None.
            data (dict[str, str] | None, optional): Form data for the request. Defaults to None.
            headers (dict[str, str] | None, optional): Additional headers. Defaults to None.
            cookies (dict[str, str] | None, optional): Cookies to send. Defaults to None.
            json (Any, optional): JSON data to send. Defaults to None.
            timeout (float | None, optional): Override timeout for this request. Defaults to instance timeout.

        Returns:
            aiohttp.ClientResponse: The HTTP response object.

        Raises:
            DuckDuckGoSearchException: If the client session is not initialized or a generic error occurs.
            TimeoutException: If the request times out.
        """
        if not self.client:
            raise DuckDuckGoSearchException("Client session not initialized. Use 'async with aDDGS()'.")
        await self._sleep()
        try:
            resp = await self.client.request(
                method,
                url,
                params=params,
                data=data if content is None else content,
                json=json,
                headers=headers,
                cookies=cookies,
                timeout=aiohttp.ClientTimeout(total=timeout or self.timeout),
                proxy=self.proxy,
                allow_redirects=False,
            )
            return resp
        except asyncio.TimeoutError as ex:
            raise TimeoutException(f"{url} timeout") from ex
        except aiohttp.ClientError as ex:
            raise DuckDuckGoSearchException(f"{url} {type(ex).__name__}: {ex}") from ex

    async def _get_vqd(self, keywords: str) -> str:
        """Get the 'vqd' value required for certain DuckDuckGo searches asynchronously.

        Args:
            keywords (str): The search query.

        Returns:
            str: The 'vqd' token extracted from the response.

        Raises:
            ValueValidationError: If keywords is empty or None.
        """
        if not keywords or not keywords.strip():
            raise ValueValidationError("keywords must not be empty or None")
        async with (await self._get_url("GET", "https://duckduckgo.com", params={"q": keywords})) as resp:
            resp_content = await resp.read()
        return _extract_vqd(resp_content, keywords)

    async def text(
        self,
        keywords: str,
        region: str = "wt-wt",
        safesearch: str = "moderate",
        timelimit: str | None = None,
        backend: str = "auto",
        max_results: int | None = None,
        max_pages: int = 5,
    ) -> list[dict[str, str]]:
        """Perform an asynchronous text search on DuckDuckGo.

        Args:
            keywords (str): The search query (required, must not be empty or None).
            region (str, optional): Region code for search localization (e.g., "us-en", "uk-en"). Defaults to "wt-wt" (worldwide).
            safesearch (str, optional): Safe search level ("on", "moderate", "off"). Defaults to "moderate".
            timelimit (str | None, optional): Time filter for results (e.g., "d" for day, "w" for week, "m" for month, "y" for year).
                Defaults to None (no filter).
            backend (str, optional): Backend to use ("auto", "html", "lite"). "auto" tries both html and lite randomly.
                Defaults to "auto".
            max_results (int | None, optional): Maximum number of results to return. If None, returns first page only.
                Defaults to None.
            max_pages (int, optional): Maximum number of pages to fetch. Each page requires an HTTP request, subject to rate limiting.
                Defaults to 5.

        Returns:
            list[dict[str, str]]: List of results with keys 'title', 'href', and 'body'.

        Raises:
            ValueValidationError: If keywords is empty or None.
            DuckDuckGoSearchException: If both backends fail to retrieve results.
        """
        if not keywords or not keywords.strip():
            raise ValueValidationError("keywords must not be empty or None")
        if backend in ("api", "ecosia"):
            warnings.warn(f"{backend=} is deprecated, using backend='auto'", stacklevel=2)
            backend = "auto"
        backends = ["html", "lite"] if backend == "auto" else [backend]
        shuffle(backends)

        results, err = [], None
        for b in backends:
            try:
                if b == "html":
                    results = await self._text_html(keywords, region, timelimit, max_results, max_pages)
                elif b == "lite":
                    results = await self._text_lite(keywords, region, timelimit, max_results, max_pages)
                return results
            except Exception as ex:
                logger.info(f"Error to search using {b} backend: {ex}")
                err = ex

        raise DuckDuckGoSearchException(err)

    async def _text_html(
        self,
        keywords: str,
        region: str = "wt-wt",
        timelimit: str | None = None,
        max_results: int | None = None,
        max_pages: int = 5,
    ) -> list[dict[str, str]]:
        """Internal method to fetch text search results using the HTML backend.

        Args:
            keywords (str): The search query (required, must not be empty or None).
            region (str, optional): Region code. Defaults to "wt-wt".
            timelimit (str | None, optional): Time filter. Defaults to None.
            max_results (int | None, optional): Max results. Defaults to None.
            max_pages (int, optional): Max pages to fetch. Defaults to 5.

        Returns:
            list[dict[str, str]]: Search results.
        """
        # Validation moved to parent method 'text'
        payload = {"q": keywords, "b": "", "kl": region}
        if timelimit:
            payload["df"] = timelimit

        cache = set()
        results: list[dict[str, str]] = []

        for _ in range(max_pages):
            async with (
                await self._get_url("POST", "https://html.duckduckgo.com/html", data=payload)
            ) as resp:
                resp_content = await resp.read()
            if b"No  results." in resp_content:
                return results

            tree = document_fromstring(resp_content, self.parser)
            elements = tree.xpath("//div[h2]")
            if not isinstance(elements, list):
                return results

            for e in elements:
                if isinstance(e, _Element):
                    hrefxpath = e.xpath("./a/@href")
                    href = str(hrefxpath[0]) if hrefxpath and isinstance(hrefxpath, list) else None
                    if (
                        href
                        and href not in cache
                        and not href.startswith(
                            ("http://www.google.com/search?q=", "https://duckduckgo.com/y.js?ad_domain")
                        )
                    ):
                        cache.add(href)
                        titlexpath = e.xpath("./h2/a/text()")
                        title = str(titlexpath[0]) if titlexpath and isinstance(titlexpath, list) else ""
                        bodyxpath = e.xpath("./a//text()")
                        body = "".join(str(x) for x in bodyxpath) if bodyxpath and isinstance(bodyxpath, list) else ""
                        results.append(
                            {
                                "title": _normalize(title),
                                "href": _normalize_url(href),
                                "body": _normalize(body),
                            }
                        )
                        if max_results and len(results) >= max_results:
                            return results

            npx = tree.xpath('.//div[@class="nav-link"]')
            if not npx or not max_results:
                return results
            next_page = npx[-1] if isinstance(npx, list) else None
            if isinstance(next_page, _Element):
                names = next_page.xpath('.//input[@type="hidden"]/@name')
                values = next_page.xpath('.//input[@type="hidden"]/@value')
                if isinstance(names, list) and isinstance(values, list):
                    payload = {str(n): str(v) for n, v in zip(names, values)}

        return results

    async def _text_lite(
        self,
        keywords: str,
        region: str = "wt-wt",
        timelimit: str | None = None,
        max_results: int | None = None,
        max_pages: int = 5,
    ) -> list[dict[str, str]]:
        """Internal method to fetch text search results using the lite backend.

        Args:
            keywords (str): The search query (required, must not be empty or None).
            region (str, optional): Region code. Defaults to "wt-wt".
            timelimit (str | None, optional): Time filter. Defaults to None.
            max_results (int | None, optional): Max results. Defaults to None.
            max_pages (int, optional): Max pages to fetch. Defaults to 5.

        Returns:
            list[dict[str, str]]: Search results.
        """
        # Validation moved to parent method 'text'
        payload = {"q": keywords, "kl": region}
        if timelimit:
            payload["df"] = timelimit

        cache = set()
        results: list[dict[str, str]] = []

        for _ in range(max_pages):
            async with (
                await self._get_url("POST", "https://lite.duckduckgo.com/lite/", data=payload)
            ) as resp:
                resp_content = await resp.read()
            if b"No more results." in resp_content:
                return results

            tree = document_fromstring(resp_content, self.parser)
            elements = tree.xpath("//table[last()]//tr")
            if not isinstance(elements, list):
                return results

            data = zip(cycle(range(1, 5)), elements)
            for i, e in data:
                if isinstance(e, _Element):
                    if i == 1:
                        hrefxpath = e.xpath(".//a//@href")
                        href = str(hrefxpath[0]) if hrefxpath and isinstance(hrefxpath, list) else None
                        if (
                            href is None
                            or href in cache
                            or href.startswith(
                                ("http://www.google.com/search?q=", "https://duckduckgo.com/y.js?ad_domain")
                            )
                        ):
                            [next(data, None) for _ in range(3)]
                        else:
                            cache.add(href)
                            titlexpath = e.xpath(".//a//text()")
                            title = str(titlexpath[0]) if titlexpath and isinstance(titlexpath, list) else ""
                    elif i == 2:
                        bodyxpath = e.xpath(".//td[@class='result-snippet']//text()")
                        body = (
                            "".join(str(x) for x in bodyxpath).strip()
                            if bodyxpath and isinstance(bodyxpath, list)
                            else ""
                        )
                        if href:
                            results.append(
                                {
                                    "title": _normalize(title),
                                    "href": _normalize_url(href),
                                    "body": _normalize(body),
                                }
                            )
                            if max_results and len(results) >= max_results:
                                return results

            npx = tree.xpath("//form[./input[contains(@value, 'ext')]]")
            if not npx or not max_results:
                return results
            next_page = npx[-1] if isinstance(npx, list) else None
            if isinstance(next_page, _Element):
                names = next_page.xpath('.//input[@type="hidden"]/@name')
                values = next_page.xpath('.//input[@type="hidden"]/@value')
                if isinstance(names, list) and isinstance(values, list):
                    payload = {str(n): str(v) for n, v in zip(names, values)}

        return results

    async def images(
        self,
        keywords: str,
        region: str = "wt-wt",
        safesearch: str = "moderate",
        timelimit: str | None = None,
        size: str | None = None,
        color: str | None = None,
        type_image: str | None = None,
        layout: str | None = None,
        license_image: str | None = None,
        max_results: int | None = None,
        max_pages: int = 5,
    ) -> list[dict[str, str]]:
        """Perform an asynchronous image search on DuckDuckGo.

        Args:
            keywords (str): The search query (required, must not be empty or None).
            region (str, optional): Region code. Defaults to "wt-wt".
            safesearch (str, optional): Safe search level ("on", "moderate", "off"). Defaults to "moderate".
            timelimit (str | None, optional): Time filter (e.g., "d", "w", "m", "y"). Defaults to None.
            size (str | None, optional): Image size filter (e.g., "Small", "Medium", "Large"). Defaults to None.
            color (str | None, optional): Color filter (e.g., "color", "Monochrome"). Defaults to None.
            type_image (str | None, optional): Image type (e.g., "photo", "clipart"). Defaults to None.
            layout (str | None, optional): Layout filter (e.g., "Square", "Wide"). Defaults to None.
            license_image (str | None, optional): License filter (e.g., "Public"). Defaults to None.
            max_results (int | None, optional): Max results. If None, returns first page. Defaults to None.
            max_pages (int, optional): Max pages to fetch. Defaults to 5.

        Returns:
            list[dict[str, str]]: List of image results with keys 'title', 'image', 'thumbnail', 'url', 'height', 'width', 'source'.

        Raises:
            ValueValidationError: If keywords is empty or None.
            DuckDuckGoSearchException: If the search fails due to network issues or invalid response.
        """
        if not keywords or not keywords.strip():
            raise ValueValidationError("keywords must not be empty or None")
        vqd = await self._get_vqd(keywords)

        safesearch_base = {"on": "1", "moderate": "1", "off": "-1"}
        timelimit = f"time:{timelimit}" if timelimit else ""
        size = f"size:{size}" if size else ""
        color = f"color:{color}" if color else ""
        type_image = f"type:{type_image}" if type_image else ""
        layout = f"layout:{layout}" if layout else ""
        license_image = f"license:{license_image}" if license_image else ""
        payload = {
            "l": region,
            "o": "json",
            "q": keywords,
            "vqd": vqd,
            "f": f"{timelimit},{size},{color},{type_image},{layout},{license_image}",
            "p": safesearch_base[safesearch.lower()],
        }

        cache = set()
        results: list[dict[str, str]] = []

        for _ in range(max_pages):
            async with (
                await self._get_url(
                    "GET", "https://duckduckgo.com/i.js", params=payload, headers={"Referer": "https://duckduckgo.com/"}
                )
            ) as resp:
                resp_content = await resp.read()
            resp_json = json_loads(resp_content)
            page_data = resp_json.get("results", [])

            for row in page_data:
                image_url = row.get("image")
                if image_url and image_url not in cache:
                    cache.add(image_url)
                    result = {
                        "title": row["title"],
                        "image": _normalize_url(image_url),
                        "thumbnail": _normalize_url(row["thumbnail"]),
                        "url": _normalize_url(row["url"]),
                        "height": row["height"],
                        "width": row["width"],
                        "source": row["source"],
                    }
                    results.append(result)
                    if max_results and len(results) >= max_results:
                        return results
            next = resp_json.get("next")
            if next is None or not max_results:
                return results
            payload["s"] = next.split("s=")[-1].split("&")[0]

        return results

    async def videos(
        self,
        keywords: str,
        region: str = "wt-wt",
        safesearch: str = "moderate",
        timelimit: str | None = None,
        resolution: str | None = None,
        duration: str | None = None,
        license_videos: str | None = None,
        max_results: int | None = None,
        max_pages: int = 8,
    ) -> list[dict[str, str]]:
        """Perform an asynchronous video search on DuckDuckGo.

        Args:
            keywords (str): The search query (required, must not be empty or None).
            region (str, optional): Region code. Defaults to "wt-wt".
            safesearch (str, optional): Safe search level ("on", "moderate", "off"). Defaults to "moderate".
            timelimit (str | None, optional): Time filter (e.g., "d", "w", "m", "y"). Defaults to None.
            resolution (str | None, optional): Resolution filter (e.g., "high", "standard"). Defaults to None.
            duration (str | None, optional): Duration filter (e.g., "short", "medium", "long"). Defaults to None.
            license_videos (str | None, optional): License filter (e.g., "creativeCommon"). Defaults to None.
            max_results (int | None, optional): Max results. If None, returns first page. Defaults to None.
            max_pages (int, optional): Max pages to fetch. Defaults to 8 (videos often have more pages).

        Returns:
            list[dict[str, str]]: List of video results with keys 'content', 'title', and additional fields from DuckDuckGo.

        Raises:
            ValueValidationError: If keywords is empty or None.
            DuckDuckGoSearchException: If the search fails due to network issues or invalid response.
        """
        if not keywords or not keywords.strip():
            raise ValueValidationError("keywords must not be empty or None")
        vqd = await self._get_vqd(keywords)

        safesearch_base = {"on": "1", "moderate": "-1", "off": "-2"}
        timelimit = f"publishedAfter:{timelimit}" if timelimit else ""
        resolution = f"videoDefinition:{resolution}" if resolution else ""
        duration = f"videoDuration:{duration}" if duration else ""
        license_videos = f"videoLicense:{license_videos}" if license_videos else ""
        payload = {
            "l": region,
            "o": "json",
            "q": keywords,
            "vqd": vqd,
            "f": f"{timelimit},{resolution},{duration},{license_videos}",
            "p": safesearch_base[safesearch.lower()],
        }

        cache = set()
        results: list[dict[str, str]] = []

        for _ in range(max_pages):
            async with (await self._get_url("GET", "https://duckduckgo.com/v.js", params=payload)) as resp:
                resp_content = await resp.read()
            resp_json = json_loads(resp_content)
            page_data = resp_json.get("results", [])

            for row in page_data:
                if row["content"] not in cache:
                    cache.add(row["content"])
                    results.append(row)
                    if max_results and len(results) >= max_results:
                        return results
            next = resp_json.get("next")
            if next is None or not max_results:
                return results
            payload["s"] = next.split("s=")[-1].split("&")[0]

        return results

    async def news(
        self,
        keywords: str,
        region: str = "wt-wt",
        safesearch: str = "moderate",
        timelimit: str | None = None,
        max_results: int | None = None,
        max_pages: int = 5,
    ) -> list[dict[str, str]]:
        """Perform an asynchronous news search on DuckDuckGo.

        Args:
            keywords (str): The search query (required, must not be empty or None).
            region (str, optional): Region code. Defaults to "wt-wt".
            safesearch (str, optional): Safe search level ("on", "moderate", "off"). Defaults to "moderate".
            timelimit (str | None, optional): Time filter (e.g., "d", "w", "m", "y"). Defaults to None.
            max_results (int | None, optional): Max results. If None, returns first page. Defaults to None.
            max_pages (int, optional): Max pages to fetch. Defaults to 5.

        Returns:
            list[dict[str, str]]: List of news results with keys 'date', 'title', 'body', 'url', 'image' (optional), 'source'.

        Raises:
            ValueValidationError: If keywords is empty or None.
            DuckDuckGoSearchException: If the search fails due to network issues or invalid response.
        """
        if not keywords or not keywords.strip():
            raise ValueValidationError("keywords must not be empty or None")
        vqd = await self._get_vqd(keywords)

        safesearch_base = {"on": "1", "moderate": "-1", "off": "-2"}
        payload = {
            "l": region,
            "o": "json",
            "noamp": "1",
            "q": keywords,
            "vqd": vqd,
            "p": safesearch_base[safesearch.lower()],
        }
        if timelimit:
            payload["df"] = timelimit

        cache = set()
        results: list[dict[str, str]] = []

        for _ in range(max_pages):
            async with (await self._get_url("GET", "https://duckduckgo.com/news.js", params=payload)) as resp:
                resp_content = await resp.read()
            resp_json = json_loads(resp_content)
            page_data = resp_json.get("results", [])

            for row in page_data:
                if row["url"] not in cache:
                    cache.add(row["url"])
                    image_url = row.get("image", None)
                    result = {
                        "date": datetime.fromtimestamp(row["date"], timezone.utc).isoformat(),
                        "title": row["title"],
                        "body": _normalize(row["excerpt"]),
                        "url": _normalize_url(row["url"]),
                        "image": _normalize_url(image_url) if image_url else None,
                        "source": row["source"],
                    }
                    results.append(result)
                    if max_results and len(results) >= max_results:
                        return results

            next = resp_json.get("next")
            if next is None or not max_results:
                return results
            payload["s"] = next.split("s=")[-1].split("&")[0]

        return results