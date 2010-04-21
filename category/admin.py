from django.contrib import admin
from category.models import Category
from category.models import SubCategory

class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)

class SubCategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(SubCategory, SubCategoryAdmin)
