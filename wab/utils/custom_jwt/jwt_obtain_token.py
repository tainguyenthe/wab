from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.serializers import CharField, Serializer
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import JSONWebTokenAPIView

from wab.utils.token_expire_handler import is_token_expired

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
User = get_user_model()


class JSONWebTokenSerializer(Serializer):
    """
    Serializer class to show info to swagger
    """
    url = CharField(max_length=200)
    token = CharField(max_length=200)


class LoginView(JSONWebTokenAPIView):
    """
    API View that returns a token (with new expiration) based on
    auth code
    """
    serializer_class = JSONWebTokenSerializer

    def post(self, request, *args, **kwargs):
        url = request.POST.get('url', None)
        token = request.POST.get('token', None)
        if url is None or token is None:
            return Response(
                {
                    'success': False,
                    'message': 'Missing or incorrect credentials',
                    'data': []
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            Site.objects.get(domain=url)
        except Exception:
            return Response(
                {
                    'success': False,
                    'message': 'This application is not available',
                    'data': []
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            token = Token.objects.get(key=token)
        except Exception:
            return Response(
                {
                    'success': False,
                    'message': 'Token not found',
                    'data': []
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if is_token_expired(token):
            return Response(
                {
                    'success': False,
                    'message': 'This token is expired',
                    'data': []
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = token.user
        # make token from user found by token
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        return Response({'success': True,
                         'message': 'Successfully logged in',
                         'token': token},
                        status=status.HTTP_200_OK)


obtain_jwt_token = LoginView.as_view()
