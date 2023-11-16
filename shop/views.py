from django.shortcuts import render, get_object_or_404
from .models import Categorie, Prodotti
from cart.forms import CartAddProductForm

#Regole per la paginazione
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

def lista_prodotti(request,categoria_slug=None):
    categoria = None
    categorie = Categorie.objects.all()
    prodotti = Prodotti.objects.filter(pubblicato=True)

    if categoria_slug: #se viene passato slug di categoria faccio i filtri
        categoria = get_object_or_404(Categorie, slug=categoria_slug)#salvo in categoria nome dello slug
        prodotti = Prodotti.objects.filter(categoria=categoria).filter(pubblicato=True) #estraggo solo i prodotti della categoria passata

    paginator = Paginator(prodotti,3)
    page_number= request.GET.get('page',1)
    try:
        prodotti = paginator.page(page_number)
    except PageNotAnInteger:
        prodotti = paginator.page(1)
    except EmptyPage:
        prodotti = paginator.page(paginator.num_pages)
        
    return render(request,'shop/lista_prodotti.html',{'categorie':categorie,'prodotti':prodotti,'categoria':categoria})


def dettaglio_prodotto(request, id,slug):
    prodotto = get_object_or_404(Prodotti, id=id, slug=slug, pubblicato=True)
    prodotti_correlati = Prodotti.objects.filter(categoria=prodotto.categoria).filter(pubblicato=True).exclude(id=prodotto.id)
    #print(prodotto.categoria) #stampa nel teminale la categoria del prodotto che sto visionando
    cart_prodotto_form = CartAddProductForm()
    return render(request, 'shop/dettaglio_prodotto.html',{'prodotto':prodotto,'prodotti_correlati':prodotti_correlati, 'cart_prodotto_form':cart_prodotto_form, 'max_buy':range(1,prodotto.quantita+1)})

