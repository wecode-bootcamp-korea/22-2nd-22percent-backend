import json, re, uuid, random
import bcrypt

from django.http      import JsonResponse
from django.views     import View
from django.db        import IntegrityError
from django.db.models import Q

from users.models   import User

EMAIL_REGEX    = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
PASSWORD_REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$'

class EmailSignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if not re.match(EMAIL_REGEX, data['email']):
                return JsonResponse({"message": "INVALID_EMAIL"}, status=400)
            
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({"message": "DUPLICATE_EMAIL"}, status=400)

            if not re.match(PASSWORD_REGEX, data['password']):
                return JsonResponse({"message": "INVALID_PASSWORD"}, status=400)

            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

            user = User.objects.create(
                email              = data['email'],
                name               = data['name'],
                password           = hashed_password.decode(),
                deposit_bank_id    = random.randint(1, 8),
                deposit_account    = create_random_account(),
                withdrawal_bank_id = random.randint(1, 8),
                withdrawal_account = create_random_account()
            )
            
            access_token = jwt.encode({"user_id": user.id}, SECRET_KEY, ALGORITHM)

            return JsonResponse({"accessToken": access_token}, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        
        except IntegrityError:
            return JsonResponse({"message": "DUPLICATE_ERROR"}, status=400)

def create_random_account():
    random_account = str(uuid.uuid4().int>>64)[0:17]
    
    if User.objects.filter(Q(deposit_account=random_account) | Q(withdrawal_account=random_account)).exists():
        return create_random_account()

    return random_account
