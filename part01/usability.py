import os
import requests
import time
import urllib3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from requests.adapters import HTTPAdapter

session = requests.Session()
adapter = HTTPAdapter(max_retries=3)
session.mount("http://", adapter)
session.mount("https://", adapter)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

urllib3.disable_warnings()


os.environ["WDM_LOCAL"] = "1"

URLS = [
    (
        "https://nrega.nic.in/MGNREGA_new/Nrega_home.aspx",
        ["https://nrega.nic.in/MGNREGA_new/NREGA_home_hi.aspx"],
    ),  # "https://nrega.nic.in/Nregahome/MGNREGA_new/Nrega_home.aspx" is broken
    ("https://www.usa.gov/", ["https://www.usa.gov/es/"]),
    ("https://www.bits-pilani.ac.in/", []),
    ("https://www.isro.gov.in/", ["https://www.isro.gov.in/ISRO_HINDI/"]),
    ("https://medium.com/", []),
    (
        "https://www.education.gov.in/",
        ["https://www.education.gov.in/hi"],
    ),  # "https://www.education.gov.in/en" is broken
]
SKIP_TO_CONTENT_XPATH = '//*[@title="Skip to main content"]'
RANDOM_ROUTE_TEXT = "t"

edge_options = EdgeOptions()
edge_options.binary_location = "/usr/bin/microsoft-edge-dev"


driver = webdriver.Edge(
    service=EdgeService(EdgeChromiumDriverManager().install()), options=edge_options
)


def count_alt_image_tags():
    img_elements = driver.find_elements(By.TAG_NAME, "img")
    img_with_alt_text_count = 0
    for img in img_elements:
        alt_text = img.get_attribute("alt")
        if alt_text is not None and (alt_text.strip() != "" and alt_text != "icon"):
            img_with_alt_text_count += 1

    print(f"Out of {len(img_elements)} images, {img_with_alt_text_count} have alt text")


def find_broken_links():
    links = driver.find_elements(By.TAG_NAME, "a")
    broken_links = []
    print(len(links))
    i = 0
    session = requests.Session()
    adapter = HTTPAdapter(max_retries=10)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    for link in links:
        time.sleep(1)
        i += 1
        href = link.get_attribute("href")
        if href and (href.startswith("http") or href.startswith("https")):
            try:
                response = session.head(href, headers=headers, verify=False)
                if response.status_code < 200 and response.status_code >= 400:
                    print(f"{href} is broken {response.status_code}")
                    broken_links.append((href, response.status_code))
            except Exception as e:
                broken_links.append((href, e))

    print(f"Out of {len(links)} links, {len(broken_links)} are broken")


def skip_to_content_button_check():
    try:
        driver.find_element(By.XPATH, SKIP_TO_CONTENT_XPATH)
        print("Skip to main content button found")
    except Exception:
        print("No skip to content button")


def check_random_route_handle(url: str):
    response = session.get(url + RANDOM_ROUTE_TEXT)
    if response.status_code != 404:
        print("Does not handle not found errors well")


def check_lang_switch(l10n_urls: list):
    for url in l10n_urls:
        driver.get(url)
        html = driver.find_element(By.XPATH, "/html")
        lang_attr = html.get_attribute("lang")
        if lang_attr is not None and lang_attr == "en":
            print("Language switch not reflecting for screen readers")
        else:
            print("Language switch is reflecting")


def calculate_average_load_time(url: str, number_of_times: int) -> float:
    sum = 0
    for _ in range(0, number_of_times):
        start_time = time.time()
        driver.get(url)
        sum += time.time() - start_time

    return sum / number_of_times


def test_usability():
    for url, l10n_urls in URLS:
        load_time = calculate_average_load_time(url, 3)
        print(f"{url} took a average of {load_time:.2f} seconds to load")
        time.sleep(10)
        skip_to_content_button_check()
        count_alt_image_tags()
        check_random_route_handle(url)
        find_broken_links()
        check_lang_switch(l10n_urls)
        print()


test_usability()
print()
driver.quit()
