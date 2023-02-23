from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site

from django.template.loader import render_to_string

from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str

from django.contrib.auth import authenticate
from django.contrib.auth.models import User, auth

from .forms import NewUserForm, LoginForm
from .token import user_tokenizer_generate

from .models import UserInfo, CategoryPerson, Images, Reviews

from django.db.models import Sum, Count

from django.template.defaulttags import register


@register.filter
def get_range(value):
    return range(value)


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
            user.email_user(subject=subject, message=message)
            return redirect('verification-sent')

    context = {
        'form': form
    }
    return render(request, 'user/register.html', context)


def login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('home-page')

    context = {
        'form': form,
    }
    return render(request, 'user/login.html', context)


def logout(request):
    try:
        for key in list(request.session.keys()):
            del request.session[key]
    except KeyError:
        pass

    return redirect('home-page')


def trainers_info(request):
    trainer_category = CategoryPerson.objects.get(category='T')
    trainers = Images.objects.filter(user__category=trainer_category)
    reviews_stars = {}
    reviews = Reviews.objects.all()
    for review in reviews:
        if reviews_stars.get(review.trainer_id, None):
            reviews_stars[review.trainer_id][0] += review.stars
            reviews_stars[review.trainer_id][1] += 1
            reviews_stars[review.trainer_id][2] = reviews_stars[review.trainer_id][0] // \
                                                  reviews_stars[review.trainer_id][1]
            reviews_stars[review.trainer_id][3] = 5 - reviews_stars[review.trainer_id][2]

        else:
            reviews_stars[review.trainer_id] = [review.stars, 1, review.stars, 5 - review.stars]

    print(reviews_stars.items())
    context = {
        'trainers': trainers,
        'reviews_stars': reviews_stars,
    }
    return render(request, 'trainer/trainers-info.html', context)


def trainer_info(request, id_trainer):
    return render(request, 'trainer/trainer-info.html')


def verification(request, uidb64, token):
    unique_id = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=unique_id)

    if user and user_tokenizer_generate.check_token(user, token):
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
