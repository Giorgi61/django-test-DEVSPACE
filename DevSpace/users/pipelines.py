from django.contrib.auth import get_user_model
from django.shortcuts import render
from social_core.pipeline.partial import partial

from DevSpace.settings import SOCIAL_AUTH_USER_FIELDS as USER_FIELDS


@partial
def bind_user(strategy, backend, request, social, **kwargs):
    request = strategy.request
    user = request.user

    model = get_user_model()
    details = kwargs.get('details', {})
    email = details.get('email')

    if social is not None or (user_object := model.objects.filter(email=email).first()) is not None :
        return None

    else:

        form_password = strategy.request_data().get('password')

        if form_password:
            return {'password': form_password}


        return render(request, 'users/social_register.html', context={'backend': backend.name} )


def custom_create_user(strategy, backend, details, *args, **kwargs):

    print(kwargs)
    user = kwargs.get('user', False)

    if user:
        return

    model = get_user_model()

    username, email, first_name, last_name, password = (field if (field := kwargs.get(f, False)) else details.get(f, '') for f in USER_FIELDS)

    user = model.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password)

    return {'user': user}






