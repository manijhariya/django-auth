from django.db import models
from django.contrib.auth.models import (
	BaseUserManager, AbstractBaseUser, AbstractUser
)

# Create your models here.
class CustomUserManager(BaseUserManager):
	def create_user(self, password, email, username, address):
		if not email:
			raise ValueError("User must have Email")

		user = self.model(
			username = username,
			email = email,
			password = password,
			address = address,
		)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, password, email, username, address):
		user = self.create_user(
			username = username,
			password = password,
			email = email,
			address = address,
		)
		user.is_admin=True
		user.save(using=self._db)
		return user

class CustomUser(AbstractBaseUser):
	id = models.AutoField(primary_key=True)
	username = models.CharField(max_length=50,unique=True,null=False)
	email = models.EmailField(unique=True)
	password = models.CharField(max_length=24)
	address = models.TextField(max_length=100)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username', 'password']

	objects = CustomUserManager()

	def __str__(self):
		return "{} {}".format(self.email, self.password)

	@property
	def is_staff(self):
		return self.is_admin

	@property
	def is_anonymous(self):
		return False

	@property
	def is_authenticated(self):
		return True

	class Meta():
		db_table = 'auth_user'
		verbose_name = 'User'
		verbose_name_plural = 'Users'
