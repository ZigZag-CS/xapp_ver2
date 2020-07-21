# -*- coding: utf-8 -*-
from django.shortcuts import render

def eroare_404(request):
    print("=== 404 ===")
    return render(request,'404.html', {})
