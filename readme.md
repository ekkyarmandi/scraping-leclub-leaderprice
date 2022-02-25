# Scraping LeClub LeaderPrice

Scraping script for scraping product data from [LeClub Leader Price](leclubleaderprice.fr) using Scrapy.

### Output Example
```
{
    "code": "3760020500559",
    "image_url": "https://cdn.shopify.com/s/files/1/0533/8434/7812/products/321124152-CASINO-COCONUT_MILK_JARDIN_BIO-WHITE_front_1024x.png?v=1638380028",
    "small_image_url": "https://cdn.shopify.com/s/files/1/0533/8434/7812/products/321124152-CASINO-COCONUT_MILK_JARDIN_BIO-WHITE_front_1024x.png?v=1638380028",
    "product_name": "Lait de coco jardin Bio - 400ml",
    "brand": "Leader Price Dev",
    "nutriscore": null,
    "categories": [
        "Épicerie salée",
        "Produits du monde",
        "Autres produits exotiques",
        "Lait de coco jardin Bio - 400ml"
    ],
    "ingredients_text": "Ingrédients : noix de coco*, eau, épaississant : gomme guar. *Produit issu de l'agriculture biologique.",
    "calories": "2000kcal/100g",
    "ingredients": [
        "Ingrédients : noix de coco*, eau, épaississant : gomme guar. *Produit issu de l'agriculture biologique"
    ]
}
```

### Set up
First make sure scrapy have been installed on your local machine. You can use command line below to install all the module from this project.
```terminal
pip install -r requirements.txt
```
Second you can specify the collections url you want to crawl by looking into [leclub.py](spiders/leclub.py)

### How to run
Run the `leclub` crawler for collecting the product name and it's url by typing crawl command line below.
```terminal
scrapy crawl leclub
```
And run `products` crawler for collecting product details.
```terminal
scrapy crawl products
```

You also can add "-o" \<filename> output parameter on the crawl command line to have the output. For an example
```terminal
scrapy crawl products -o output/prodcuts.json
```