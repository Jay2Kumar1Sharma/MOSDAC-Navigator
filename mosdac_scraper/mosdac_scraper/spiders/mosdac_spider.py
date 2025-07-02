import scrapy
import fitz  # PyMuPDF
from mosdac_scraper.items import MosdacItem
from urllib.parse import urlparse

class MosdacSpider(scrapy.Spider):
    name = "mosdac"
    allowed_domains = ["mosdac.gov.in"]
    start_urls = ["https://www.mosdac.gov.in/"]

    def parse(self, response):
        """
        Parses HTML pages, extracts content, and follows links to other pages and PDFs.
        This version is improved to avoid boilerplate content.
        """
        # --- Handle HTML Pages ---
        if response.headers.get('Content-Type', b'').decode('utf-8').startswith('text/html'):
            item = MosdacItem()
            item['url'] = response.url
            item['title'] = response.css('title::text').get(default='').strip()
            item['content_type'] = 'html'

            # --- IMPROVEMENT: More specific content selection ---
            # Try to find the most specific content container first.
            # The order matters: from most specific (like an 'article' tag) to most general.
            content_selectors = [
                'main',
                'article',
                'div.page-content',
                'div.main-content',
                'div.content_area',
                '#accordion'  # For the MOSDAC FAQ page
            ]
            
            main_content = None
            for selector in content_selectors:
                main_content = response.css(selector)
                if main_content:
                    self.logger.info(f"Found content in specific selector '{selector}' for URL: {response.url}")
                    break  # Stop when we find the first, most specific container

            # If no specific container is found, fall back to the whole body
            if not main_content:
                self.logger.warning(f"No specific content selector found for URL: {response.url}. Falling back to 'body'.")
                main_content = response.css('body')

            # --- IMPROVEMENT: Exclude boilerplate selectors ---
            # Remove common headers, footers, navs, sidebars, and script/style tags
            # from the selected content before extracting text.
            main_content.css('header, footer, nav, script, style, .sidebar, .menu, .navbar').remove()
            
            # Extract text ONLY from the cleaned content block
            text_nodes = main_content.css('::text').getall()
            content = " ".join(text.strip() for text in text_nodes if text.strip())
            item['content'] = content
            
            # Yield the item only if we successfully extracted content
            if item['content']:
                yield item

        # --- Find and follow all links on the page ---
        for a_tag in response.css('a::attr(href)').getall():
            link = response.urljoin(a_tag)
            
            # Only follow links that are within the allowed domain
            if urlparse(link).netloc == self.allowed_domains[0]:
                if link.lower().endswith('.pdf'):
                    # If it's a PDF, send it to the PDF parser
                    yield scrapy.Request(link, callback=self.parse_pdf)
                else:
                    # If it's another HTML page, follow it recursively
                    yield scrapy.Request(link, callback=self.parse)

    def parse_pdf(self, response):
        """
        This function handles PDF responses, extracts text using PyMuPDF.
        """
        # This function remains the same as before, as it already extracts pure text.
        item = MosdacItem()
        item['url'] = response.url
        item['content_type'] = 'pdf'
        item['title'] = urlparse(response.url).path.split('/')[-1]

        try:
            with fitz.open(stream=response.body, filetype="pdf") as doc:
                text = "".join(page.get_text() for page in doc)
                item['content'] = " ".join(text.split())
                if doc.metadata and doc.metadata.get('title'):
                    item['title'] = doc.metadata['title']
        except Exception as e:
            self.logger.error(f"Failed to parse PDF {response.url}: {e}")
            item['content'] = ""

        if item['content']:
            yield item