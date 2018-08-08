from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """
    UserManager class for Custom User Model
    """
    use_in_migrations = True

    def _create_user(self, username, email, password, fullname, mobile, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, name=fullname, mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password, name, mobile, **extra_fields):
        from . import user_settings

        vals = user_settings

        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', vals['DEFAULT_ACTIVE_STATE'])

        return self._create_user(username, email, password, name, mobile, **extra_fields)

    def create_superuser(self, username, email, password, name, mobile, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, name, mobile, **extra_fields)