from django.db import models

# Create your models here.

class Products(models.Model):
    name = models.CharField(max_length=240)
    details = models.TextField(max_length=1000)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
