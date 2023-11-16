from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Coupon
from .forms import CouponApplicaForm

# Create your views here.

@require_POST
def coupon_applica(request):
    now = timezone.now() #ricordo l'ora e la data di somministrazione del coupon
    form = CouponApplicaForm(request.POST)
    if form.is_valid():
        codice = form.cleaned_data['codice']
        #controllo se esiste codice inserito e se è ancora valido o attivo
        try:
            coupon = Coupon.objects.get(codice__iexact=codice,valido_da__lte=now, valido_a__gte=now, attivo=True) #iexact= codice esatto case sensitive, lte=less the or egual to, gte=greater then or equal to
            #siccome stiamo usando il carrello, ricordo che il carrello è nella sessione
            request.session['coupon_id']=coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id']=None
        return redirect('cart:cart_detail')