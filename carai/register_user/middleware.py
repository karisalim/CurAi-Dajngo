# from django.utils.deprecation import MiddlewareMixin
# from .models import BlacklistedAccessToken
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework_simplejwt.authentication import JWTAuthentication
# import jwt

# class BlockBlacklistedTokensMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         auth_header = request.headers.get("Authorization", "")
#         if auth_header.startswith("Bearer "):
#             access_token = auth_header.split(" ")[1]
#             try:
#                 decoded_token = jwt.decode(access_token, options={"verify_signature": False})
#                 jti = decoded_token.get("jti")
                
#                 # تحقق من القائمة السوداء
#                 if BlacklistedAccessToken.objects.filter(jti=jti).exists():
#                     return Response(
#                         {"error": "This token has been revoked. Please log in again."}, 
#                         status=status.HTTP_401_UNAUTHORIZED
#                     )
#             except jwt.ExpiredSignatureError:
#                 return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
#             except jwt.InvalidTokenError:
#                 return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)


from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from .models import BlacklistedAccessToken, BlacklistedRefreshToken
import jwt

class BlockBlacklistedTokensMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            access_token = auth_header.split(" ")[1]
            try:
                decoded_token = jwt.decode(access_token, options={"verify_signature": False})
                jti = decoded_token.get("jti")

                if BlacklistedAccessToken.objects.filter(jti=jti).exists():
                    return JsonResponse(
                        {"error": "This token has been revoked. Please log in again."}, 
                        status=401
                    )

            except jwt.ExpiredSignatureError:
                return JsonResponse({"error": "Token has expired"}, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({"error": "Invalid token"}, status=401)


class BlockBlacklistedRefreshTokensMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path == '/api/token/refresh/':  # تحقق من أن الطلب لتجديد التوكن
            refresh_token = request.data.get('refresh')
            if refresh_token:
                try:
                    decoded_token = jwt.decode(refresh_token, options={"verify_signature": False})
                    jti = decoded_token.get("jti")

                    if BlacklistedRefreshToken.objects.filter(jti=jti).exists():
                        return JsonResponse(
                            {"error": "This refresh token has been revoked. Please log in again."}, 
                            status=401
                        )

                except jwt.ExpiredSignatureError:
                    return JsonResponse({"error": "Refresh token has expired"}, status=401)
                except jwt.InvalidTokenError:
                    return JsonResponse({"error": "Invalid refresh token"}, status=401)