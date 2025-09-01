from django.db import models

class Trade(models.Model):
    trade_id = models.AutoField(primary_key=True)
    symbol = models.CharField(max_length=10)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    trade_date = models.DateTimeField(auto_now_add=True)
    trade_type = models.CharField(max_length=4, choices=[('BUY', 'Buy'), ('SELL', 'Sell')])

    def __str__(self):
        return f"{self.trade_type} {self.quantity} of {self.symbol} at {self.price} on {self.trade_date}"