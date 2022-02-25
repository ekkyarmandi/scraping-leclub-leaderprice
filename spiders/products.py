from bs4 import BeautifulSoup
import scrapy
import json
import re

class ProductsSpider(scrapy.Spider):
    name = 'products'
    allowed_domains = ['leclubleaderprice.fr']
    products = json.load(open("./output/product-links.json"))
    start_urls = [p['product_link'] for p in products]

    def parse(self, response):

        # parser the response
        page = BeautifulSoup(response.text,"html.parser")
        
        # define the output dictionary variable
        result = {
            "code" : None,
            "image_url" : None,
            "small_image_url" : None,
            "product_name" : None,
            "brand" : None,
            "nutriscore" : None,
            "categories" : None,
            "ingredients_text" : None,
            "calories" : None,
            "ingredients": None
        }

        # extract product details
        for script in page.find_all("script",{"type":"application/ld+json"}):
    
            try:

                # find product details
                product = json.loads(script.text)
                _type = product['@type']
                if _type == "Product":
                    output = {
                        "code" : product['gtin13'],
                        "image_url" : product['image']['url'],
                        "small_image_url" : product['image']['url'],
                        "product_name" : product['name'],
                        "brand" : product['brand']['name']
                    }
                    result.update(output)

                # find product categories
                elif _type == "BreadcrumbList":
                    categories = []
                    for item in product['itemListElement'][1:]:
                        categories.append(item['name'])
                    result.update({"categories": categories})
                    
            except: pass

        # find product nutriscore
        for script in page.find_all("script",{"type":"application/json"}):
            try:
                data = json.loads(script.text)
                if "title" in data.keys():
                    for tag in data['tags']:
                        x = re.search("nutri_\w+",tag)
                        if x != None:
                            result.update({"nutriscore": x.group()[-1]})
                            break
            except: pass

        # find product ingredients and calories
        details = {}
        more = page.find("div",{"class":"product__more-info"})
        for tag in more.find_all("div",{"class":"u-marg-t-sm"}):
            if tag.find("p") != None:
                raw_title = tag.find("p").text.strip()
                text = tag.text.replace(raw_title,"").strip()
                title = raw_title.replace(":","").strip()
                if title == "Composition":
                    ingredients = text.strip(".").split("-")
                    ingredients = [l.strip() for l in ingredients if l.strip() != ""]
                    result.update({"ingredients_text":text,"ingredients":ingredients})
                elif "Valeurs énergétiques pour" in title:
                    per = title.replace("Valeurs énergétiques pour","").strip()
                    calories = re.search("kcal [0-9\,\.]+|[0-9\,\.]+ kcal|[0-9\,\.]+kcal|kcal [0-9\,\.]+",text)
                    if calories != None:
                        unit = re.search("[0-9\,\.]+",calories.group()).group()
                        calories = f"{unit}kcal/{per}"
                    result.update({"calories": calories})
    
        yield result