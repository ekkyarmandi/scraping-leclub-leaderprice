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

        def data_clean(text):
            
            def clean_ingredients(text):
                x = re.search("ingrédients",text.lower())
                if x != None:
                    w = text[x.start():x.end()]
                    text = text.replace(w,"").strip()
                while len(text) > 0 and text[0] == ":":
                    text = text.strip(":").strip()
                return text
            
            # clean text with "ingredient" text
            if type(text) == str and ("Ingrédients" in text or "ingrédients" in text):
                text = clean_ingredients(text)
            
            # clean asterix in text
            if type(text) == str and "*" in text:
                x = re.search("\.\*|\. \*",text)
                if x != None:
                    text = text[0:x.start()]
                text = text.replace("*","").strip(".")
                
            # split the text
            if type(text) == str and "- " in text:
                ingredients = [l.strip() for l in text.split("-") if l.strip() != ""]
            elif type(text) == str and ", " in text:
                ingredients = [l.strip() for l in text.split(",") if l.strip() != ""]
            else:
                ingredients = []

            return text, ingredients

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
                    text, ingredients = data_clean(text)
                    result.update({"ingredients_text":text,"ingredients":ingredients})
                elif "Valeurs énergétiques pour" in title:
                    per = title.replace("Valeurs énergétiques pour","").strip()
                    calories = re.search("kcal [0-9\,\.]+|[0-9\,\.]+ kcal|[0-9\,\.]+kcal|kcal [0-9\,\.]+",text)
                    if calories != None:
                        unit = re.search("[0-9\,\.]+",calories.group()).group()
                        calories = f"{unit}kcal/{per}"
                    result.update({"calories": calories})
    
        yield result