from django.contrib.sitemaps import Sitemap
# from seller.models import Seller 
from products.models import Item

class ProductSitemap(Sitemap):
    def items(self):
        return Item.objects.all()