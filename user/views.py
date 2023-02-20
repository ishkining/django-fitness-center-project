from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site

from django.template.loader import render_to_string

from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str

from .forms import NewUserForm
from .token import user_tokenizer_generate


def register(request):
    form = NewUserForm()

    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Верификация электронной почты'
            message = render_to_string('user/email/verification.html',
                                       {
                                           'user': user,
                                           'domain': current_site.domain,
                                           'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                           'token': user_tokenizer_generate.make_token(user),
                                       })
            user.email(subject=subject, message=message)
            return redirect('verification-sent')

    context = {
        'form': form
    }
    return render(request, 'user/register.html', context)


def verification(request, uidb64, token):
    unique_id = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=unique_id)

    if user and user_tokenizer_generate.check_token(user,token):
        user.is_active = True
        user.save()
        return redirect('verification-success')
    else:
        return redirect('verification-failed')


def verification_sent(request):
    return render(request, 'user/email/verification-sent.html')


def verification_success(request):
    return render(request, 'user/email/verification-success.html')


def verification_failed(request):
    return render(request, 'user/email/verification-failed.html')
