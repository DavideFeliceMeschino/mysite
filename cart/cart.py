from decimal import Decimal
from django.conf import settings
from shop.models import Prodotti
from coupons.models import Coupon #importo tabella coupon della app coupons

class Cart:
    #creo costruttore della classe
    def __init__(self, request):
        #inizzializzo carrello
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if  not cart:
            #creo e salvo la sessione del carrello vuota, snenza oggetti
            cart = self.session[settings.CART_SESSION_ID]={}
        
        self.cart = cart
        #memorizzo il coupon applicato
        self.coupon_id = self.session.get('coupon_id')

    #funzione per aggiornare il prezzo in base alla quantità
    def __iter__(self):
        prodotti_ids = self.cart.keys()
         #Prendo i prodotti e li aggiungo al carrello
        prodotti = Prodotti.objects.filter(id__in=prodotti_ids)
        cart = self.cart.copy()
        for prodotto in prodotti:
            cart[str(prodotto.id)]['prodotto'] = prodotto
        for item in cart.values():
            item['prezzo'] = Decimal(item['prezzo'])
            item['prezzo_totale'] = item['prezzo'] * item['quantita']
            yield item

    
    #Conoscere la quantità di prodotti nel carrello
    def __len__(self):
        return sum(item['quantita'] for item in self.cart.values())

    
    #dunzione per aggiungere prodotti al carrello
    def add(self, prodotto, quantita=1, override_quantita=False):
        #Aggiungo un prodotto al carrello o aumento la quantità

        prodotto_id = str(prodotto.id)

        if prodotto_id not in self.cart:
            self.cart[prodotto_id] = {'quantita':0, 'prezzo': str(prodotto.prezzo)}

        if override_quantita:
            self.cart[prodotto_id]['quantita'] = quantita
        else:
            self.cart[prodotto_id]['quantita'] += quantita
        
        self.save()

    
    #Creo il metodo per salvare le modifiche al carrello
    def save(self):
        self.session.modified = True


    #funzione per rimuovere prodotto dal carrello
         
    def remove(self, prodotto):
        """Rimuovo un prodotto dal carello"""
        prodotto_id = str(prodotto.id)
        if prodotto_id in self.cart:
            del self.cart[prodotto_id]
            self.save()

    #Calcolo il prezzo di tutti i prodotti moltiplicati per le loro quantità
    def get_total_price(self):
        return sum(Decimal(item['prezzo']) * item['quantita'] for item in self.cart.values())
    
    
    #Cancellare il carrello dalla sessione
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()


#proprita del coupon
    @property
    def coupon(self): #prendore il coupon
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass # non fare nulla
        return None
    
    #calcolo sconto
    def get_discount(self):
        if self.coupon:
            return (self.coupon.sconto/Decimal(100))* self.get_total_price()
        return Decimal(0)
    
    #aggiorno totale dopo aver applicato lo sconto ai prezzi del prodotto
    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()