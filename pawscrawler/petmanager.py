from lxml import html
from pawscrawler.models import Pet
import requests
import re

def get_pet_urls():
    page = requests.get("http://www.pawschicago.org/our-work/pet-adoption/pets-available/#dogsResults")
    tree = html.fromstring(page.content)

    nodes = tree.xpath("//div[@class='adopt-pet']/a")
    urls = set()

    for node in nodes:
        url = node.attrib['href']

        if "showcat" in url:
            continue

        if url in urls:
            continue

        urls.add(url)

    return urls

def parse_pet(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)

    name = tree.xpath("//li[@class='current']")[0].text
    breed = tree.xpath("//div[@class='floating-tabs breed-dog']/p")[0].text.replace(",","-")
    gender = tree.xpath("//div[@class='floating-tabs gender grey-bg']/p")[0].text

    age = tree.xpath("//div[@class='floating-tabs age']/p")[0].text #deal with this
    age_stripped = float(re.sub(r'[^\d.]+', "", age))
    if "Month" in age:
        age_stripped = age_stripped / 12

    weight = tree.xpath("//div[@class='floating-tabs weight grey-bg']/p")[0].text #deal with this
    weight_stripped = float(re.sub(r'[^\d.]+', "", weight))

    location_xpath = "//div[@class='floating-tabs location']/p"
    location = tree.xpath(location_xpath)[0].text
    if location == None:
        location_xpath += "/a"
        location = tree.xpath(location_xpath)[0].text

    return Pet(name=name, breed=breed, gender=gender, age=age_stripped, weight=weight_stripped, location=location, url=url)