from django.http import HttpResponse  # noqa: F401
from django.shortcuts import render, redirect  # noqa: F401
from .forms import SignUpForm
from django.contrib.auth import get_user_model, login

User = get_user_model()


def signup_view(request):
    form = SignUpForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")
        # TODO check if are equals in html
        # password2 = form.cleaned_data.get("password2")
        try:
            user = User.objects.create_user(email, password)
        # TODO handle errors
        except:  # noqa: E722
            user = None
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            request.session['register_error'] = 1
    return render(request, "forms.html", {"form": form})
