# from django.db import models
# from products.models import *

# class Invoice(models.Model):
#     order = models.ForeignKey('products.Order', on_delete=models.SET_NULL, null=True)
#     invoice = models.FileField(upload_to="sf_invoices/")

#     def __str__(self):
#         return f"invoice for {self.order}"