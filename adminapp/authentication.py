from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from .models import UserToken, CustomerToken

class CustomTokenAuthentication(TokenAuthentication):
    # print("satya")
    def authenticate_credentials(self, key):
        # print('pradeep')
        try:
            user_token = UserToken.objects.select_related('user').get(key=key)
            # if not user_token.user.is_active:
            #     raise exceptions.AuthenticationFailed('User inactive or deleted')
            return (user_token.user, user_token)
        except UserToken.DoesNotExist:
            pass
        
        try:
            customer_token = CustomerToken.objects.select_related('user').get(key=key)
            # if not customer_token.user.is_active:
            #     raise exceptions.AuthenticationFailed('Customer inactive or deleted')
            return (customer_token.user, customer_token)
        except CustomerToken.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')