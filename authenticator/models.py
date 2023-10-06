from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class AccountManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("User must have a email")
        if not username:
            raise ValueError("User must have an username")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        # change when email verificartion addedd
        user.is_active = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# Custom user model
class Account(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=254, unique=True)

    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = AccountManager()

    def __str__(self):
        return self.email

    # Check user permissions
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Check user module permissions
    def has_module_perms(self, add_label):
        return True


class user_profile(models.Model):
    account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    full_name = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=50, default='0000000000')
    profile_img = models.ImageField(
        upload_to="user/profile", blank=True, null=True)
    nationality = models.CharField(max_length=50, null=True)
    DOB = models.DateField(null=True)


class AddressBook(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=20)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    pincode = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_default = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.is_default:
            # Set is_default=False for other addresses of the same user
            AddressBook.objects.filter(user=self.user).exclude(
                pk=self.pk).update(is_default=False)
        super(AddressBook, self).save(*args, **kwargs)

    def get_user_full_address(self):
        address_parts = [self.name, self.phone, self.address_line_1]
        if self.address_line_2:
            address_parts.append(self.address_line_2)
        address_parts.append(f'<b>Pin: {self.pincode}</b>')
        address_parts.extend([self.city, self.state, self.country])
        return ', '.join(address_parts)

    def __str__(self):
        return self.name
