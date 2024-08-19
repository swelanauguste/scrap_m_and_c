import csv
import json
import sys
import time
from dataclasses import asdict, dataclass
from bs4 import BeautifulSoup
import httpx
from selectolax.parser import HTMLParser

@dataclass
class Product:
    name: str | None
    price: str | None
    brand: str | None
    url: str | None
    image: str | None


def get_html(base_url, page):
    print("getting html...")
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
    }

    resp = httpx.get(
        base_url + str(page), headers=headers, timeout=None, follow_redirects=True
    )
    html = HTMLParser(resp.text)
    return html


def extract_text(html, sel):
    try:
        return html.css_first(sel).text()
    except AttributeError:
        return None


def extract_attribute(html, sel, attr):
    try:
        return html.css_first(sel).attributes[attr]
    except AttributeError:
        return None


def parse_page(html):
    products = html.css("div.product-small.box")
    # print(products)

    for product in products:
        site_base_url = "https://www.mandchomedepot.com"
        new_item = Product(
            name=extract_text(product, "a.woocommerce-LoopProduct-link"), # print(product.css_first("a.woocommerce-LoopProduct-link").text()) name
            price=extract_text(product, "div.price-wrapper"), # print(product.css_first("div.price-wrapper").text()) price
            brand=extract_text(product, "p.category"), # print(product.css_first("p.category").text()) brand/category
            image=extract_attribute(product, "img", "data-src"), # image = product.css_first("img").attributes["src"] image
            url=extract_attribute(product, "a", "href"), # url = product.css_first("a").attributes["href"] link
        )
        # print(product.css_first("a div").text())
        # print(product.css_first(".price").text())
        # print(product.css_first(".tagline-4.product-brand").text())
        yield asdict(new_item)


def append_to_csv(data):
    print("exporting to csv...")
    with open("computer_world2.csv", "a") as f:
        writer = csv.DictWriter(f, ["name", "price", "brand", "url", "image"])
        writer.writeheader()
        writer.writerows(data)


def main():
    product_list = []
    base_url = "https://computerworldslu.com/shop/page/"
    for i in range(1, 2):
        data = parse_page(get_html(base_url, i))
        for item in data:
            product_list.append(item)
    append_to_csv(product_list)


if __name__ == "__main__":
    main()

# base_url = "https://computerworldslu.com/shop/page/"
# headers = {
#     "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
# }

# resp = httpx.get(
#     base_url + str(1), headers=headers, timeout=None, follow_redirects=True
# )

# html = HTMLParser(resp.text)

# products = html.css("div.product-small.box")

# for product in products:
    # url = product.css_first("a").attributes["href"] link
    # image = product.css_first("img").attributes["src"] image
    # print(product.css_first("p.category").text()) brand/category
    # print(product.css_first("a.woocommerce-LoopProduct-link").text()) name
    # print(product.css_first("div.price-wrapper").text()) price
    