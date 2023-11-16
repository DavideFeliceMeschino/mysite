from django.contrib import admin
from .models import Carousel,CarouselCat, UserProfile
#per aggiungere UserProfile dentri la vista User
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


# Register your models here.

@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = ['titolo', 'sottotitolo','categoria', 'img_preview']
    search_fields = ['titolo', 'sottotitolo', 'corpo']
    list_filter = ['titolo', 'sottotitolo']
    readonly_fields = ['img_preview']

admin.site.register(CarouselCat)

#area utenti


class CustomUserAdmin(admin.StackedInline): #serve a inserire nella visualizzazione User altre tabelle
    model = UserProfile
    can_delete= False
    readonly_fields=['img_preview']

#creo nuova visualizzazine del account
class AccountUserAdmin(UserAdmin):
    #inlines = [CustomUserAdmin] versione alternativa

    def add_view(self,*args,**kwargs):
        self.inlines=[]
        return super(AccountUserAdmin, self).add_view(*args,**kwargs)


    def change_view(self,*args,**kwargs):
        self.inlines=[CustomUserAdmin]
        return super(AccountUserAdmin, self).change_view(*args,**kwargs)
         

admin.site.unregister(User)
admin.site.register(User,AccountUserAdmin)