from django.shortcuts import render
from django.views.generic import View
# Create your views here.


class RegistrationView(View):
    def get(self,request,*args,**kw):
        return render(request,"register.html")