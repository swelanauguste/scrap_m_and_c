import csv
import sys
import time
from dataclasses import asdict, dataclass
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup
from playwright.sync_api import Playwright, sync_playwright
from selectolax.parser import HTMLParser


@dataclass
class Product:
    name: str | None
    price: str | None
    category: str | None
    url: str | None
    image: str | None


def append_to_csv(data):
    print("exporting to csv...")
    with open("massy_pharmaceutical.csv", "a") as f:
        writer = csv.DictWriter(f, ["name", "price", "category", "url", "image"])
        # writer.writeheader()
        writer.writerows(data)


def get_products(products):
    for product in products:
        new_item = Product(
            name=product.css_first("h2").text(),
            price=product.css_first("p.offer-price.mb-0").text(),
            category=category_url.replace(
                "https://www.shopmassystoresslu.com/product-category/", ""
            ).replace("/", ""),
            url=product.css_first("a").attributes["href"],
            image=product.css_first("img").attributes["src"],
        )
        yield (asdict(new_item))
        # print(asdict(new_item))


with sync_playwright() as p:
    base_url = "https://www.shopmassystoresslu.com"
    # def main(playwright: Playwright):
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(base_url)
    # page.wait_for_selector("div#popmake-377265")
    page.click("button.pum-close")
    page.locator("[name=wcmlim_change_lc_to]").select_option("Gourmet")
    html = page.inner_html("#slider_76188")
    html = HTMLParser(html)

    categories = html.css("div.owl-item.active")
    categories_links = []
    for category in categories:
        category_link = category.css_first("a").attributes["href"]
        categories_links.append(
            category_link.replace("https://www.shopmassystoresslu.com", "")
        )

    for category_link in categories_links[7:8]:
        category_url = base_url + category_link
        print("-----", category_url, "------")

        # for i in range(24, 25):
        #     print(f"loading page {i}...")

        #     page.goto(f"{category_url}page/{i}/" )
        #     page.locator("[name=wcmlim_change_lc_to]").select_option("Gourmet")
        #     page.wait_for_selector("div.row.products")
        #     html = page.inner_html("div.row.products")
        #     html = HTMLParser(html)
        #     products = html.css("div.col-md-4.col-xs-6.pmb-3")
        #     print("page", i, "contents", len(products))
            
        #     append_to_csv(get_products(products))
        #     print("page", i, "done")
        #     time.sleep(3)

    #             break
    # append_to_csv(get_products(category_url))

    #     try:
    #         page.locator("[name=wcmlim_change_lc_to]").select_option("Gourmet")
    #         loading_more_button = page.locator("a.lmp_button")
    #         while loading_more_button.is_visible():
    #             page.click("a.lmp_button")
    #             page.wait_for_selector("div.row.products")
    #             html = page.inner_html("div.row.products")
    #             html = HTMLParser(html)
    #             get_products(html, category_url)
    #             break
    #     except:
    #         page.wait_for_selector("div.row.products")
    #         loading_more_button = page.locator("a.lmp_button")
    #         while loading_more_button.is_visible():
    #             # print("loading more...")
    #             # if loading_more_button.is_visible():
    #             page.click("a.lmp_button")
    #             page.wait_for_selector("div.row.products")
    #             html = page.inner_html("div.row.products")
    #             html = HTMLParser(html)
    #             get_products(html, category_url)
    #             break
