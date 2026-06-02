<!-- mcp-name: io.github.D4Vinci/Scrapling -->

# Scrapling — Adaptive Web Scraping for the Modern Web

Scrapling is an adaptive web scraping framework that handles everything from a single request to a full-scale crawl.

Its parser learns from website changes and automatically relocates your elements when pages update. Its fetchers bypass anti-bot systems like Cloudflare Turnstile out of the box. And its spider framework lets you scale up to concurrent, multi-session crawls with pause/resume and automatic proxy rotation, all in a few lines of Python.

```python
from scrapling.fetchers import Fetcher, AsyncFetcher, StealthyFetcher, DynamicFetcher
StealthyFetcher.adaptive = True
p = StealthyFetcher.fetch('https://example.com', headless=True, network_idle=True)  # Fetch website under the radar!
products = p.css('.product', auto_save=True)                                        # Scrape data that survives website design changes!
products = p.css('.product', adaptive=True)                                         # Later, if the website structure changes, pass `adaptive=True` to find them!
```
Or scale up to full crawls
```python
from scrapling.spiders import Spider, Response

class MySpider(Spider):
  name = "demo"
  start_urls = ["https://example.com/"]

  async def parse(self, response: Response):
      for item in response.css('.product'):
          yield {"title": item.css('h2::text').get()}

MySpider().start()
```

---

## Avalara GTM Engineering Use Case

Scrapling is the **live signal-research layer** for Avalara's GTM engineering stack. Before any outreach is drafted, the AI sales agent uses Scrapling to gather the public "Why Now" triggers that make a message relevant.

| GTM need | How Scrapling delivers | Business result |
|---|---|---|
| Find buying triggers (new state expansion, M&A, ERP migration, new compliance hires) | Adaptive fetchers pull press releases, job postings, and newsroom pages | Outreach references a real, current event instead of a generic pitch |
| Keep research running when sites change layout | Parser relocates elements via similarity scoring, so scrapers don't break | Near-zero maintenance, signal pipeline keeps running unattended |
| Let the AI agent research without writing code | Built-in MCP server exposes scraping tools directly to Claude/Cursor/ChatGPT | Reps' agents enrich accounts on demand, no engineering ticket needed |
| Research dozens of accounts quickly | Concurrent spider framework with pause/resume | An agent researches 10+ accounts in the time a human checks 2 |

**Net impact for Avalara:** faster, evidence-backed prospecting that lifts reply rates and shortens the time from "cold account" to "qualified conversation." This is the engine that feeds specific public signals into the cold-email formula in the GTM sales system.

---

## Key Features

### Spiders - A Full Crawling Framework
- **Scrapy-like Spider API**: Define spiders with `start_urls`, async `parse` callbacks, and `Request`/`Response` objects.
- **Concurrent Crawling**: Configurable concurrency limits, per-domain throttling, and download delays.
- **Multi-Session Support**: Unified interface for HTTP requests and stealthy headless browsers in a single spider, route requests to different sessions by ID.
- **Pause & Resume**: Checkpoint-based crawl persistence. Press Ctrl+C for a graceful shutdown; restart to resume from where you left off.
- **Streaming Mode**: Stream scraped items as they arrive via `async for item in spider.stream()` with real-time stats.
- **Blocked Request Detection**: Automatic detection and retry of blocked requests with customizable logic.
- **Robots.txt Compliance**: Optional `robots_txt_obey` flag that respects `Disallow`, `Crawl-delay`, and `Request-rate` directives with per-domain caching.
- **Development Mode**: Cache responses to disk on the first run and replay them on subsequent runs.
- **Built-in Export**: Export results through hooks and your own pipeline or the built-in JSON/JSONL with `result.items.to_json()` / `result.items.to_jsonl()`.

### Advanced Websites Fetching with Session Support
- **HTTP Requests**: Fast and stealthy HTTP requests with the `Fetcher` class. Can impersonate browsers' TLS fingerprint, headers, and use HTTP/3.
- **Dynamic Loading**: Fetch dynamic websites with full browser automation through the `DynamicFetcher` class supporting Playwright's Chromium and Google's Chrome.
- **Anti-bot Bypass**: Advanced stealth capabilities with `StealthyFetcher` and fingerprint spoofing. Can bypass all types of Cloudflare's Turnstile/Interstitial with automation.
- **Session Management**: Persistent session support with `FetcherSession`, `StealthySession`, and `DynamicSession` classes for cookie and state management across requests.
- **Proxy Rotation**: Built-in `ProxyRotator` with cyclic or custom rotation strategies across all session types, plus per-request proxy overrides.
- **Domain & Ad Blocking**: Block requests to specific domains (and their subdomains) or enable built-in ad blocking in browser-based fetchers.
- **DNS Leak Prevention**: Optional DNS-over-HTTPS support.
- **Async Support**: Complete async support across all fetchers and dedicated async session classes.

### Adaptive Scraping & AI Integration
- **Smart Element Tracking**: Relocate elements after website changes using intelligent similarity algorithms.
- **Smart Flexible Selection**: CSS selectors, XPath selectors, filter-based search, text search, regex search, and more.
- **Find Similar Elements**: Automatically locate elements similar to found elements.
- **MCP Server for AI**: Built-in MCP server for AI-assisted web scraping and data extraction. The MCP server extracts targeted content before passing it to the AI (Claude/Cursor/etc), speeding up operations and reducing costs by minimizing token usage.

### High-Performance & Battle-Tested Architecture
- **Lightning Fast**: Optimized performance outperforming most Python scraping libraries.
- **Memory Efficient**: Optimized data structures and lazy loading for a minimal memory footprint.
- **Fast JSON Serialization**: 10x faster than the standard library.
- **Battle tested**: 92% test coverage and full type hints coverage.

### Developer-Friendly Experience
- **Interactive Web Scraping Shell**: Optional built-in IPython shell with Scrapling integration and shortcuts.
- **Use it directly from the Terminal**: Scrape a URL without writing a single line of code.
- **Rich Navigation API**: Advanced DOM traversal with parent, sibling, and child navigation methods.
- **Enhanced Text Processing**: Built-in regex, cleaning methods, and optimized string operations.
- **Auto Selector Generation**: Generate robust CSS/XPath selectors for any element.
- **Familiar API**: Similar to Scrapy/BeautifulSoup with the same pseudo-elements used in Scrapy/Parsel.
- **Complete Type Coverage**: Full type hints for excellent IDE support.
- **Ready Docker image**: With each release, a Docker image containing all browsers is automatically built.

## Getting Started

### Basic Usage
HTTP requests with session support
```python
from scrapling.fetchers import Fetcher, FetcherSession

with FetcherSession(impersonate='chrome') as session:  # Use latest version of Chrome's TLS fingerprint
    page = session.get('https://quotes.toscrape.com/', stealthy_headers=True)
    quotes = page.css('.quote .text::text').getall()

# Or use one-off requests
page = Fetcher.get('https://quotes.toscrape.com/')
quotes = page.css('.quote .text::text').getall()
```
Advanced stealth mode
```python
from scrapling.fetchers import StealthyFetcher, StealthySession

with StealthySession(headless=True, solve_cloudflare=True) as session:  # Keep the browser open until you finish
    page = session.fetch('https://nopecha.com/demo/cloudflare', google_search=False)
    data = page.css('#padded_content a').getall()

# Or use one-off request style, it opens the browser for this request, then closes it after finishing
page = StealthyFetcher.fetch('https://nopecha.com/demo/cloudflare')
data = page.css('#padded_content a').getall()
```
Full browser automation
```python
from scrapling.fetchers import DynamicFetcher, DynamicSession

with DynamicSession(headless=True, disable_resources=False, network_idle=True) as session:  # Keep the browser open until you finish
    page = session.fetch('https://quotes.toscrape.com/', load_dom=False)
    data = page.xpath('//span[@class="text"]/text()').getall()  # XPath selector if you prefer it

# Or use one-off request style, it opens the browser for this request, then closes it after finishing
page = DynamicFetcher.fetch('https://quotes.toscrape.com/')
data = page.css('.quote .text::text').getall()
```

### Spiders
Build full crawlers with concurrent requests, multiple session types, and pause/resume:
```python
from scrapling.spiders import Spider, Request, Response

class QuotesSpider(Spider):
    name = "quotes"
    start_urls = ["https://quotes.toscrape.com/"]
    concurrent_requests = 10
    
    async def parse(self, response: Response):
        for quote in response.css('.quote'):
            yield {
                "text": quote.css('.text::text').get(),
                "author": quote.css('.author::text').get(),
            }
            
        next_page = response.css('.next a')
        if next_page:
            yield response.follow(next_page[0].attrib['href'])

result = QuotesSpider().start()
print(f"Scraped {len(result.items)} quotes")
result.items.to_json("quotes.json")
```
Use multiple session types in a single spider:
```python
from scrapling.spiders import Spider, Request, Response
from scrapling.fetchers import FetcherSession, AsyncStealthySession

class MultiSessionSpider(Spider):
    name = "multi"
    start_urls = ["https://example.com/"]
    
    def configure_sessions(self, manager):
        manager.add("fast", FetcherSession(impersonate="chrome"))
        manager.add("stealth", AsyncStealthySession(headless=True), lazy=True)
    
    async def parse(self, response: Response):
        for link in response.css('a::attr(href)').getall():
            # Route protected pages through the stealth session
            if "protected" in link:
                yield Request(link, sid="stealth")
            else:
                yield Request(link, sid="fast", callback=self.parse)  # explicit callback
```
Pause and resume long crawls with checkpoints by running the spider like this:
```python
QuotesSpider(crawldir="./crawl_data").start()
```
Press Ctrl+C to pause gracefully, progress is saved automatically. Later, when you start the spider again, pass the same `crawldir`, and it will resume from where it stopped.

### Advanced Parsing & Navigation
```python
from scrapling.fetchers import Fetcher

# Rich element selection and navigation
page = Fetcher.get('https://quotes.toscrape.com/')

# Get quotes with multiple selection methods
quotes = page.css('.quote')  # CSS selector
quotes = page.xpath('//div[@class="quote"]')  # XPath
quotes = page.find_all('div', {'class': 'quote'})  # BeautifulSoup-style
# Same as
quotes = page.find_all('div', class_='quote')
quotes = page.find_all(['div'], class_='quote')
quotes = page.find_all(class_='quote')  # and so on...
# Find element by text content
quotes = page.find_by_text('quote', tag='div')

# Advanced navigation
quote_text = page.css('.quote')[0].css('.text::text').get()
quote_text = page.css('.quote').css('.text::text').getall()  # Chained selectors
first_quote = page.css('.quote')[0]
author = first_quote.next_sibling.css('.author::text')
parent_container = first_quote.parent

# Element relationships and similarity
similar_elements = first_quote.find_similar()
below_elements = first_quote.below_elements()
```
You can use the parser right away if you don't want to fetch websites like below:
```python
from scrapling.parser import Selector

page = Selector("<html>...</html>")
```
And it works precisely the same way!

### Async Session Management Examples
```python
import asyncio
from scrapling.fetchers import FetcherSession, AsyncStealthySession, AsyncDynamicSession

async with FetcherSession(http3=True) as session:  # `FetcherSession` is context-aware and can work in both sync/async patterns
    page1 = session.get('https://quotes.toscrape.com/')
    page2 = session.get('https://quotes.toscrape.com/', impersonate='firefox135')

# Async session usage
async with AsyncStealthySession(max_pages=2) as session:
    tasks = []
    urls = ['https://example.com/page1', 'https://example.com/page2']
    
    for url in urls:
        task = session.fetch(url)
        tasks.append(task)
    
    print(session.get_pool_stats())  # Optional - The status of the browser tabs pool (busy/free/error)
    results = await asyncio.gather(*tasks)
    print(session.get_pool_stats())
```

## CLI & Interactive Shell

Scrapling includes a powerful command-line interface.

Launch the interactive Web Scraping shell
```bash
scrapling shell
```
Extract pages to a file directly without programming (extracts the content inside the `body` tag by default). If the output file ends with `.txt`, the text content is extracted. If it ends in `.md`, it will be a Markdown representation of the HTML content; if it ends in `.html`, it will be the HTML content itself.
```bash
scrapling extract get 'https://example.com' content.md
scrapling extract get 'https://example.com' content.txt --css-selector '#fromSkipToProducts' --impersonate 'chrome'  # All elements matching the CSS selector
scrapling extract fetch 'https://example.com' content.md --css-selector '#fromSkipToProducts' --no-headless
scrapling extract stealthy-fetch 'https://nopecha.com/demo/cloudflare' captchas.html --css-selector '#padded_content a' --solve-cloudflare
```

## Performance Benchmarks

### Text Extraction Speed Test (5000 nested elements)

| # |      Library      | Time (ms) | vs Scrapling | 
|---|:-----------------:|:---------:|:------------:|
| 1 |     Scrapling     |   2.02    |     1.0x     |
| 2 |   Parsel/Scrapy   |   2.04    |     1.01     |
| 3 |     Raw Lxml      |   2.54    |    1.257     |
| 4 |      PyQuery      |   24.17   |     ~12x     |
| 5 |    Selectolax     |   82.63   |     ~41x     |
| 6 |  MechanicalSoup   |  1549.71  |   ~767.1x    |
| 7 |   BS4 with Lxml   |  1584.31  |   ~784.3x    |
| 8 | BS4 with html5lib |  3391.91  |   ~1679.1x   |

### Element Similarity & Text Search Performance

| Library     | Time (ms) | vs Scrapling |
|-------------|:---------:|:------------:|
| Scrapling   |   2.39    |     1.0x     |
| AutoScraper |   12.45   |    5.209x    |

> All benchmarks represent averages of 100+ runs. See `benchmarks.py` for methodology.

## Installation

Scrapling requires Python 3.10 or higher:

```bash
pip install scrapling
```

This installation only includes the parser engine and its dependencies, without any fetchers or commandline dependencies.

### Optional Dependencies

1. If you are going to use any of the extra features below, the fetchers, or their classes, you will need to install fetchers' dependencies and their browser dependencies as follows:
    ```bash
    pip install "scrapling[fetchers]"
    
    scrapling install           # normal install
    scrapling install  --force  # force reinstall
    ```

    This downloads all browsers, along with their system dependencies and fingerprint manipulation dependencies.

    Or you can install them from the code instead of running a command like this:
    ```python
    from scrapling.cli import install
    
    install([], standalone_mode=False)          # normal install
    install(["--force"], standalone_mode=False) # force reinstall
    ```

2. Extra features:
   - Install the MCP server feature:
       ```bash
       pip install "scrapling[ai]"
       ```
   - Install shell features (Web Scraping shell and the `extract` command): 
       ```bash
       pip install "scrapling[shell]"
       ```
   - Install everything: 
       ```bash
       pip install "scrapling[all]"
       ```
   Remember that you need to install the browser dependencies with `scrapling install` after any of these extras (if you didn't already)

### Docker
You can also build/run a Docker image with all extras and browsers. The image is automatically built and pushed using GitHub Actions and the repository's main branch.

## Contributing

Internal Avalara contributions are welcome. Please follow the repository's contributing guidelines before getting started.

## Disclaimer

> [!CAUTION]
> This library is provided for educational and research purposes only. By using this library, you agree to comply with local and international data scraping and privacy laws. Always respect the terms of service of websites and robots.txt files.

## License

This work is licensed under the BSD-3-Clause License. See `LICENSE` for full terms.
