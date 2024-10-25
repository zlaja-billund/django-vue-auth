from django.contrib.auth.base_user import BaseUserManager

'''
This class is designed to handle the creation of users and superusers. 
Superuser creation cannot handle email logins when the username is set to None in the model.
'''
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Enter an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user