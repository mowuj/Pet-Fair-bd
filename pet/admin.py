from django.contrib import admin
from .models import Category,Pet,Review
# Register your models here.


class CategoryModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'slug']

admin.site.register(Category,CategoryModelAdmin)

class PetModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price','description','image']

    def category(self, obj):
        return obj.category.name
admin.site.register(Pet,PetModelAdmin)


class ReviewModelAdmin(admin.ModelAdmin):
    list_display = ['reviewer', 'pet_name', 'rating', 'body', 'timestamps']

    def reviewer(self, obj):
        return obj.user.username
    
    def pet_name(self, obj):
        return obj.pet.name

admin.site.register(Review,ReviewModelAdmin)