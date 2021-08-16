import time

from django.db import models
from django.contrib.auth.models import User
from location_field.models.plain import PlainLocationField
from django.utils import timezone


# User
class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    lend_state = models.BooleanField(default=False)
    borrow_state = models.BooleanField(default=False)
    point = models.PositiveIntegerField(default=0)

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
    context = models.TextField(null=True)
    target_amount = models.IntegerField(default=0)
    current_amount = models.IntegerField(default=0)
    deadline = models.DateTimeField(null=True)
    like = models.ManyToManyField(User, null=True)


class DonationUser(models.Model):
    item = models.ForeignKey(Donation, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    amount = models.IntegerField(default=0)


class DonationComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Donation, on_delete=models.CASCADE, null=True)
    context = models.TextField()
    date = models.DateTimeField(null=True)


# Borrow
class BorrowState(models.Model):
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="borrower")
    lender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="lender")
    date = models.DateTimeField(null=True)


# Community
class CommunityPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    context = models.TextField()
    like = models.ManyToManyField(User, related_name='post_like_user', blank=True)
    date = models.DateTimeField(blank=True, default=timezone.now())


class CommunityComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, blank=True)
    context = models.TextField()
    like = models.ManyToManyField(User, related_name='comment_like_user', blank=True)
    date = models.DateTimeField(blank=True, default=timezone.now())
