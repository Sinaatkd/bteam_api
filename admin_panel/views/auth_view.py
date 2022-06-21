from django.shortcuts import redirect, render, resolve_url
from django.contrib.auth import authenticate, login

def admin_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,
                            password=password, is_staff=True)
        if user is not None:
            login(request, user)
            return redirect(resolve_url('home'))
    context = {}
    return render(request, 'authentication/login.html', context)