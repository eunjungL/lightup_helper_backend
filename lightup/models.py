import time

from django.db import models
from django.contrib.auth.models import User
from location_field.models.plain import PlainLocationField


# User
class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    lend_state = models.BooleanField(default=False)
    borrow_state = models.BooleanField(default=False)
    point = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


# class UserBorrowState(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
#     lend = models.BooleanField(default=False)
#     borrow = models.BooleanField(default=False)


class UserLocation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    location = PlainLocationField()


# Donation
class Donation(models.Model):
    company = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    target_amount = models.CharField(max_length=45)
    current_amount = models.CharField(max_length=45)
    deadline = models.DateTimeField()


class DonationUser(models.Model):
    item = models.ForeignKey(Donation, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    amount = models.CharField(max_length=45)


# Borrow
class BorrowState(models.Model):
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="borrower")
    lender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="lender")
    date = models.DateTimeField(null=True)