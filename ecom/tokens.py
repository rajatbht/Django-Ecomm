# from datetime import datetime
from auth1.exceptions import ExpiredTokenException, InvalidTokenException, NotAdminException
from datetime import datetime, timedelta
from django.http.response import JsonResponse
import jwt
from rest_framework import status
from auth1.models import User
from auth1.serializers import UserSerializer
# import datetime


def createToken(payload):
    current_time = datetime.now()
    hours_added = timedelta(hours=1)
    expiry_time = current_time + hours_added
    expiry_time = expiry_time.timestamp()
    payload['expiry'] = expiry_time
    user_email = payload['email']
    all_data = User.objects.get(email=user_email)
    all_data_serial = UserSerializer(all_data)
    payload['admin'] = all_data_serial.data['is_admin']
    token = jwt.encode(payload, 'secret', algorithm="HS256")
    return token


def checkToken(argument):
    def decorator_factory(func):
        def inner(request):
            try:
                print('I am ' + argument)
                if 'Authorization' not in request.headers:
                    raise InvalidTokenException("This API is protected. Please use authentication")
                token = request.headers['Authorization']
                token = token[len('Bearer '):]
                user = jwt.decode(token, "secret", algorithms=["HS256"])
                if datetime.now().timestamp() > user['expiry']:
                    raise ExpiredTokenException("Please provide valid token")
                if argument == "admin" and user['admin'] is False:
                    raise NotAdminException("Only admins has access to this API")
                return func(request, user)
            except InvalidTokenException as ex:
                return JsonResponse({'message': ex.message}, safe=False, status=status.HTTP_401_UNAUTHORIZED)
            except ExpiredTokenException as ex:
                return JsonResponse({'message': ex.message}, safe=False, status=status.HTTP_401_UNAUTHORIZED)
            except ExpiredTokenException as ex:
                return JsonResponse({'message': ex.message}, safe=False, status=status.HTTP_403_FORBIDDEN)
            except NotAdminException as ex:
                return JsonResponse({'message': ex.message}, safe=False, status=status.HTTP_403_FORBIDDEN)
            except Exception as ex:
                print(ex.__class__.__name__)
                return JsonResponse({'message': 'Invalid Token'}, safe=False, status=status.HTTP_401_UNAUTHORIZED)
        return inner
    return decorator_factory
