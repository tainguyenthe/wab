from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.shortcuts import redirect
from rest_framework.authtoken.models import Token

from wab.utils.token_expire_handler import expires_in, token_expire_handler


@login_required
def obtain_auth_code(request, url):
    """
        Return list option of choice
    """
    try:
        Site.objects.get(domain=url)
    except Exception:
        return redirect("https://"+url+"?status=False&message=SITENOTEXIST")

    token, _ = Token.objects.get_or_create(user=request.user)
    _, token = token_expire_handler(token)
    return redirect("https://"+url+"?status=True&auth_code=" + token.key + "&message=DONE&expires_in="+str(expires_in(token)))
