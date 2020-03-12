from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import generic

@login_required
def ViewHomePage(request):
    if not request.user:
        redirect('/accounts/login')
    return redirect('/service/posts/')