from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin



class Organization(models.Model):
    name = models.CharField(max_length=255)
    email_domain = models.CharField(max_length=255, unique=True)
    organization_email = models.EmailField()


    def __str__(self):
        return self.name

class UserManager(BaseUserManager):

    def create_user(self, email, password, **args):

        if not email:
            raise ValueError("User hasn't enter the email")
        email = self.normalize_email(email)
        user = self.model(email=email, **args)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password, **args):
        args.setdefault('is_staff', True)
        args.setdefault('is_superuser', True)
        return self.create_user(email, password, **args)


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    email_domain = models.CharField(max_length=255)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_org_admin = models.BooleanField(default=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    register_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

