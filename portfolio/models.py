from django.db import models

# Create your models here.
class PortfolioModel(models.Model):
    username = models.CharField(max_length=200)
    cash = models.CharField(max_length=200)
    market = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    detail = models.TextField()

    def __str__(self):
        return self.username + ":" + self.type

class CurrentPortfolio(models.Model):
    username = models.CharField(max_length=200)
    current = models.CharField(max_length=200)

    def __str__(self):
        return self.username + ":" + self.current

class CurrentOrders(models.Model):
    username = models.CharField(max_length=200)
    ordertime = models.DateTimeField()
    ticker = models.CharField(max_length=200)
    amount = models.CharField(max_length=200)
    type = models.CharField(max_length=200)

    def __str__(self):
        return self.username + ":" + self.type

class TickerSet(models.Model):
    ticker = models.CharField(max_length=200)

class PendingOrders(models.Model):
    username = models.CharField(max_length=200)
    ordertime = models.DateTimeField()
    ticker = models.CharField(max_length=200)
    amount = models.CharField(max_length=200)
    quantity = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    condition = models.TextField()

    def __str__(self):
        return self.username + ":" + self.type + ":" + str(self.ordertime)
