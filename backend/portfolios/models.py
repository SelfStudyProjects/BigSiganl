from django.db import models

class Portfolio(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class PortfolioItem(models.Model):
    portfolio = models.ForeignKey(Portfolio, related_name='items', on_delete=models.CASCADE)
    asset_name = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField()

    def __str__(self):
        return f"{self.quantity} of {self.asset_name} in {self.portfolio.name}"