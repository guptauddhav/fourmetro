from django.db import models
import sha
import random

from django.utils.encoding import smart_str
from django.utils.datetime_safe import datetime

class UserManager(models.Manager):
    # Manager object for User model.
    def user_by_password(self, phone_number, raw_password):
        """
        Returns a User object for the given phone number and raw password else
        returns None.
        """
        try:
            user = self.get(phone_number=phone_number)
        except self.model.DoesNotExist:
            return None
        if user.check_password(raw_password):
            return user
        return None

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    
    # TODO: to make phone number field a integer field.
    phone_number = models.CharField(max_length=11) 
    is_active = models.BooleanField(default=1)
    date_joined = models.DateTimeField(default=datetime.now())
    updates = models.BooleanField()
    is_verified_email = models.BooleanField()
    is_verified_phone = models.BooleanField()

    phone_activation_code = models.CharField(max_length=10)
    email_activation_key = models.CharField(max_length=100)
    
    objects = UserManager()
    
    # class Meta
    class Meta:
        app_label = 'account'
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __unicode__(self):
        return self.username

    def set_password(self, raw_password):
        """
        Hashes the password w/ random salt and stores it.
        """
        salt = sha.new(str(random.random())).hexdigest()[:7]
        hsh = sha.new(salt + smart_str(raw_password)).hexdigest()
        self.password = '%s$%s' % (salt, hsh)

    def check_password(self, raw_password):
        """
        Hashes the password and compares it to stored value
        """
        salt, hsh = self.password.split('$')
        return hsh == sha.new(smart_str(salt + raw_password)).hexdigest()

    def reset_password(self, length=7):
        """
        Resets the password to a random string.
        """
        new_password = sha.new(str(random.random())).hexdigest()[:length]
        self.set_password(new_password)
        return new_password    