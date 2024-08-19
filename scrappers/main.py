import csv
import json
import sys
import time
from dataclasses import asdict, dataclass

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
    # url = "https://www.mandchomedepot.com/ecommerce/products/products-m-c?department=builders-hardware&page=2"
    print("getting html...")
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
    }

    resp = httpx.get(
        base_url + str(page), headers=headers, timeout=None, follow_redirects=True
    )
    html = HTMLParser(resp.text)
    return html


# def parse_product(html):
#     site_base_url = "https://www.mandchomedepot.com"
#     new_products = Product(
#         name=extract_data(html, "a div").text(),
#         price=extract_data(html, ".price").text(),
#         brand=extract_data(html, ".tagline-4.product-brand").text(),
#         url=site_base_url + extract_data(html, "a").attributes["href"],
#         image=site_base_url + extract_data(html, "img").attributes["src"],
#     )


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
    products = html.css("div.product-display")

    for product in products:
        site_base_url = "https://www.mandchomedepot.com"
        new_item = Product(
            name=extract_text(product, "a div"),
            price=extract_text(product, ".price"),
            brand=extract_text(product, ".tagline-4.product-brand"),
            image=site_base_url + extract_attribute(product, "img", "src"),
            url=site_base_url + extract_attribute(product, "a", "href"),
        )
        # print(product.css_first("a div").text())
        # print(product.css_first(".price").text())
        # print(product.css_first(".tagline-4.product-brand").text())
        yield asdict(new_item)


def export_to_json(data):
    print("exporting to json...")
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def append_to_csv(data):
    print("exporting to csv...")
    with open("lumber-plywood.csv", "a") as f:
        writer = csv.DictWriter(f, ["name", "price", "brand", "url", "image"])
        writer.writeheader()
        writer.writerows(data)


def main():
    product_list = []
    base_url = "https://www.mandchomedepot.com/ecommerce/products/products-m-c?department=lumber-plywood&page="
    for i in range(1, 6):
        data = parse_page(get_html(base_url, i))
        for item in data:
            product_list.append(item)
            print("added", item["name"], "...")
    # for product in product_list:
    # print(asdict(product))
    # export_to_json(product_list)
    append_to_csv(product_list)
    # print("exported to data.json")
    # print(product_list)


if __name__ == "__main__":
    main()

# url = "https://www.mandchomedepot.com/ecommerce/products/products-m-c?department=builders-hardware&page=1"

# headers = {
#     "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
# }

# resp = httpx.get(
#     url, headers=headers, timeout=None, follow_redirects=True
# )
# html = HTMLParser(resp.text)
# products = html.css("div.product-display")
# print(products)

# for product in products:
#     url =product.css_first("img").attributes["src"]

#     img_base_url = 'https://www.mandchomedepot.com'
#     print(img_base_url + url)
