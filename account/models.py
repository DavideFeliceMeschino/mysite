from django.db import models
#Per immagine preview in admin
from django.utils.html import mark_safe

#librerie per img resize link-->https://pypi.org/project/django-imagekit/
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToCover, ResizeToFit, ResizeToFill

# libreria per eliminare anche file caricati quando si cancella un oggetto models link->https://pypi.org/project/django-cleanup/
from django_cleanup import cleanup

#per caricare editor di testo avanzato
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField #aggiunge oissbilita di caricar img

#librerie per espandere info su utenti
from django.contrib.auth.admin import User
from django.dispatch import receiver
from  django.db.models.signals import post_save

#importo il validatore tramite regex
from django.core.validators import RegexValidator


# Create your models here.

class CarouselCat(models.Model):
    nome= models.CharField('Nome categoria', max_length=150)

    def __str__(self) -> str:
        return self.nome

@cleanup.select
class Carousel(models.Model):
    titolo = models.CharField("Titolo della slide", max_length=200)
    sottotitolo = models.CharField("Sottotitolo della slide", max_length=250, blank=True, null=True)
    #corpo = models.TextField("Contenuto della slide")
    corpo = RichTextUploadingField("Testo/Contenuto della slide")
    pubblicato =models.BooleanField('Pubblicato', default=False)
    categoria = models.ForeignKey(CarouselCat,on_delete=models.CASCADE, null=True, blank=True)
    img = models.ImageField("Immagine Slide", upload_to='slide/%Y/%m/', blank=True, null=True)
    img_resize = ImageSpecField(source='img',processors=[ResizeToCover(800,800)],format='png',options={'quality': 60})
    

    def __str__(self):
        return self.titolo
    
    #Per visualizzare immagine in Admin
    def img_preview(self):
        return mark_safe(f'<img src="{self.img.url}" width="150" />')



#models per utenti
@cleanup.select
class UserProfile(models.Model):
        #creo scelte per tipo_account
        ACCOUNT_TYPE_CHOICE=(
            ('admin','Admin'),
            ('developer','Developer'),
            ('cliente','Cliente')
        )
        PROVINCIA_TYPE_CHOICE=(
            ('Latina','LT'),
            ('Roma','RM'),
            ('Milano','MI')
        )
      

        user = models.OneToOneField(User, on_delete=models.CASCADE) #creo relazione una a uno con utente
        data_nascita =models.DateField('Data di nascita', null=True, blank=True)
        cf = models.CharField('Codice Fiscale',max_length=16, null=True,blank=True,validators=[RegexValidator(
            regex=r'^[A-Za-z]{6}[0-9]{2}[A-Za-z]{1}[0-9]{2}[A-Za-z]{1}[0-9]{3}[A-Za-z]{1}$',
            message='Inserisci un codice fiscale valido'
        )]) #r'(?i)...' (?i) rende case insensitive la regola
        indirizzo = models.CharField('Indirizzo di spedizione',max_length=250,null=True, blank=True)
        comune = models.CharField('Comune di residenza',max_length=250,null=True, blank=True)
        provincia = models.CharField('Provincia', max_length=100,null=True, blank=True, default=None, choices=PROVINCIA_TYPE_CHOICE)
        cap = models.CharField('C.A.P.',max_length=5, null=True, blank=True,validators=[RegexValidator(
            regex=r'^[0-9]{5}$', #scrivo la regex la stessa usata in js con apici'' invece di //
            message='Inserisci un CAP valido')]) #messaggio da far comparire in caso di errore
        tipo_account = models.CharField('Tipologia utente', max_length=50, default='Cliente', choices=ACCOUNT_TYPE_CHOICE)
        img_profilo = ProcessedImageField(upload_to='user_profile/%Y/%m/%d',processors=[ResizeToCover(128,128)],format='PNG',options={'quality': 60}, default='user_profile/profile_user.png')


        def __str__(self) -> str:
            return self.user.username
        
        def img_preview(self):
            return mark_safe(f"<img src='{self.img_profilo.url}' width='100' />")
        
        #salvo il cf  in maiuscolo nel db
        def save(self,*args,**kwargs):
            if self.cf:
                self.cf = self.cf.upper()
                super(UserProfile,self).save(*args,**kwargs)
            return None

        #salvo il profilo utente appena si crea un nuovo utente nel db 
        @receiver(post_save, sender=User)
        def create_user_profile(sender, instance, created, **kwargs):
            if created:
               UserProfile.objects.create(user=instance)
        

