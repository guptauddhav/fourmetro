from django.db import models

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    
    class Meta:
        app_label = 'category'
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __unicode__(self):
        return self.title
    
class SubCategory(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)    
    
    parent = models.ForeignKey(Category)
    
    class Meta:
        app_label = 'category'
        verbose_name = 'subcategory'
        verbose_name_plural = 'subcategories'

    def __unicode__(self):
        return self.title
