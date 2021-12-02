from django.conf import settings
from django.contrib.auth.hashers import check_password
from custom_user.models import CustomUser

class CustomUserBackend:
	def authenticate(self,request,email=None,password=None):
		if email and password:
			try:
				user = CustomUser.objects.get(email=email)
				if check_password(password,user.password):
					if user.is_active:
						return user
			except CustomUser.DoesNotExist:
				return None
		return None

	def get_user(self,user_id):
		try:
			return CustomUser.objects.get(pk=user_id)
		except CustomUser.DoesNotExist:
			return None
