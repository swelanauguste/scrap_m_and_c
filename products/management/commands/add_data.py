import csv
import decimal

from django.core.management.base import BaseCommand

from ...models import Product


class Command(BaseCommand):
    help = "Import products from a CSV file"

    def handle(self, *args, **kwargs):
        with open("/home/cworks/Developer/scrap_m_and_c/scrappers/data/mc_drugstore.csv", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                product, created = Product.objects.get_or_create(
                    name=row["name"].strip(),
                    price=row["price"]
                    .replace('"', "")
                    .replace("$", "")
                    .replace(",", "")
                    .replace("\n", "").strip(),
                    brand=row["category"].strip(),
                    url=row["url"].strip(),
                    image=row["img_url"].strip(),
                    supplier='m&c drugstore',
                    # supplier=row["supplier"].strip(),
                    # price=row['price'].replace('"', '').replace('$',''),
                    # defaults={
                    #     'price': decimal.Decimal(price),
                    #     'brand': row['brand'],
                    #     'url': row['url'],
                    #     'image': row['image']
                    # }
                )
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Product '{product.name}' created successfully."
                        )
                    )
                else:
                    self.stdout.write(f"Product '{product.name}' already exists.")
