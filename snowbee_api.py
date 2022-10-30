from typing import List

import requests

API_URL = "http://api.snowbee.byakuren.pw"


class Product:
    def __init__(self, name: str, vendor_id: str, price: float, product_page: str, preview_url: str):
        self.name = name
        self.vendor_id = vendor_id
        self.price = price
        self.product_page = product_page
        self.preview_url = preview_url


class Vendor:
    def __init__(self, id: str, name: str, url: str, favicon: str):
        self.id = id
        self.name = name
        self.url = url
        self.favicon = favicon


def _json_to_product(json_obj: dict) -> Product:
    return Product(json_obj["name"], json_obj["vendor"], json_obj["price"], json_obj["product_page"],
                   json_obj["preview_url"])


def _json_to_vendor(json_obj: dict) -> Vendor:
    return Vendor(json_obj["id"], json_obj["name"], json_obj["url"], json_obj["favicon"])


def fetch_vendors() -> "List[Vendor]":
    response = requests.get(f"{API_URL}/vendors")
    if response.status_code == 200:
        return list(map(_json_to_vendor, response.json()["vendors"]))
    elif response.status_code == 404:
        return list()
    else:
        raise RuntimeError(f"api returned {response.status_code}")


def fetch_products(query: str) -> "List[Product]":
    response = requests.post(
        f"{API_URL}/query", json={
            "query": query,
            "filters": []
        }
    )
    if response.status_code == 200:
        return list(map(_json_to_product, response.json()["products"]))
    elif response.status_code == 404:
        return list()
    else:
        raise RuntimeError(f"api returned {response.status_code}")
