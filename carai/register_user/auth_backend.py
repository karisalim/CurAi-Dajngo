import jwt
from typing import Optional, Sequence, Type
from rest_framework.authentication import BaseAuthentication
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import get_authorization_header
from rest_registration.auth_token_managers import AbstractAuthTokenManager, AuthToken, AuthTokenNotRevoked
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

class AuthJWTManager(AbstractAuthTokenManager):

    def get_authentication_class(self) -> Type[BaseAuthentication]:
        return JWTAuthentication

    def get_app_names(self) -> Sequence[str]:
        return [
            'register_user',  # update with your Django app
        ]

    def provide_token(self, user: 'AbstractBaseUser') -> AuthToken:
        refresh = RefreshToken.for_user(user)
        token_dict = {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        }
        return AuthToken(token_dict)

    def revoke_token(
            self, user: 'AbstractBaseUser', *,
            token: Optional[AuthToken] = None) -> None:
        raise AuthTokenNotRevoked()


# class AuthJWTManager(AbstractAuthTokenManager):
#     """
#     Manages JWT authentication tokens for Django REST Registration.
#     """

#     def get_authentication_class(self) -> Type[BaseAuthentication]:
#         return JWTAuthentication  # يرجّع كلاس المصادقة اللي هيتم استخدامه

#     def get_app_names(self) -> Sequence[str]:
#         """
#         Specifies which Django apps this manager is applied to.
#         """
#         return [
#             'register_user',  # تأكد من ضبط اسم التطبيق بشكل صحيح
#         ]

#     def provide_token(self, user: 'AbstractBaseUser') -> AuthToken:
#         """
#         Generates access and refresh JWT tokens for a user.
#         """
#         refresh = RefreshToken.for_user(user)
#         token_dict = {
#             "access_token": str(refresh.access_token),
#             "refresh_token": str(refresh),
#         }
#         return AuthToken(token_dict)

#     def revoke_token(
#             self, user: 'AbstractBaseUser', *,
#             token: Optional[AuthToken] = None) -> None:
#         """
#         Raises an exception because revoking tokens is not supported by default.
#         """
#         raise AuthTokenNotRevoked()


# class JWTAuthentication(BaseAuthentication):
#     ALGORITHM = "HS256"

#     def authenticate(self, request):
#         """
#         Returns a `User` if a correct username and password have been supplied
#         using HTTP Basic authentication.  Otherwise returns `None`.
#         """
#         auth = get_authorization_header(request).split()

#         if not auth or auth[0].lower() != b'bearer':
#             return None

#         if len(auth) == 1:
#             msg = _('Invalid authorization header. No credentials provided.')
#             raise AuthenticationFailed(msg)
#         if len(auth) > 2:
#             msg = _(
#                 'Invalid authorization header. Credentials string should not'
#                 ' contain spaces.'
#             )
#             raise AuthenticationFailed(msg)

#         encoded_jwt = auth[1]

#         try:
#             jwt_data = jwt.decode(
#                 encoded_jwt,
#                 settings.SECRET_KEY,
#                 algorithms=[self.ALGORITHM],
#             )
#         except jwt.ExpiredSignatureError:
#             msg = _('Expired JWT.')
#             raise AuthenticationFailed(msg) from None
#         except jwt.InvalidTokenError:
#             msg = _('Invalid JWT payload.')
#             raise AuthenticationFailed(msg) from None

#         try:
#             user_id = jwt_data["user_id"]
#         except KeyError:
#             msg = _('Missing user info in JWT.')
#             raise AuthenticationFailed(msg) from None

#         user_class = get_user_model()
#         try:
#             user = user_class.objects.get(pk=user_id)
#         except user_class.DoesNotExist:
#             msg = _('User not found.')
#             raise AuthenticationFailed(msg) from None

#         return (user, encoded_jwt)

# Karim

class JWTAuthentication(BaseAuthentication):
    
    ALGORITHM = "HS256"

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'bearer':
            return None

        if len(auth) == 1:
            raise AuthenticationFailed(_('Invalid authorization header. No credentials provided.'))
        if len(auth) > 2:
            raise AuthenticationFailed(_('Invalid authorization header. Credentials string should not contain spaces.'))

        encoded_jwt = auth[1]

        try:
            jwt_data = jwt.decode(
                encoded_jwt,
                settings.SECRET_KEY,
                algorithms=[self.ALGORITHM],
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed(_('Expired JWT.'))
        except jwt.InvalidTokenError:
            raise AuthenticationFailed(_('Invalid JWT payload.'))

        try:
            user_id = jwt_data["user_id"]
        except KeyError:
            raise AuthenticationFailed(_('Missing user info in JWT.'))

        user_class = get_user_model()
        try:
            user = user_class.objects.get(pk=user_id)
        except user_class.DoesNotExist:
            raise AuthenticationFailed(_('User not found.'))

        return (user, encoded_jwt)
    
# class JWTAuthentication(BaseAuthentication):
#     """
#     Custom JWT authentication class.
#     """

#     ALGORITHM = "HS256"

#     def authenticate(self, request):
#         """
#         Handles authentication by extracting and verifying JWT tokens from the request.
#         """
#         auth = get_authorization_header(request).split()

#         if not auth or auth[0].lower() != b'bearer':
#             return None  # السماح للمستخدمين غير المسجلين بالدخول بدون خطأ

#         if len(auth) == 1:
#             raise AuthenticationFailed(_('Invalid authorization header. No credentials provided.'))
#         if len(auth) > 2:
#             raise AuthenticationFailed(_('Invalid authorization header. Credentials string should not contain spaces.'))

#         encoded_jwt = auth[1].decode('utf-8')  # تحويل الـ bytes إلى string

#         try:
#             jwt_data = jwt.decode(
#                 encoded_jwt,
#                 settings.SECRET_KEY,
#                 algorithms=[self.ALGORITHM],
#                 options={"verify_exp": True}  # التأكد من أن التوكن لم ينتهي
#             )
#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed(_('Expired JWT. Please log in again.'))
#         except jwt.InvalidTokenError:
#             raise AuthenticationFailed(_('Invalid JWT token.'))

#         user_id = jwt_data.get("user_id")
#         if not user_id:
#             raise AuthenticationFailed(_('Missing user info in JWT.'))

#         user_class = get_user_model()
#         try:
#             user = user_class.objects.get(pk=user_id)
#         except user_class.DoesNotExist:
#             raise AuthenticationFailed(_('User not found.'))

#         return (user, encoded_jwt)

#     def authenticate_header(self, request):
#         """
#         Defines the authentication scheme for API documentation tools (e.g., Swagger).
#         """
#         return 'Bearer'    
    