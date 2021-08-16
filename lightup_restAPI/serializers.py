import datetime
import json

from rest_framework import serializers
from lightup.models import *
from chat.models import Message
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# User
class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(LoginSerializer, cls).get_token(user)

        token['username'] = user.username
        return token


class UserInfoSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UserInfo
        fields = "__all__"
        depth = 1

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "비밀번호가 일치하지 않습니다."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        user_info = UserInfo.objects.create(
            user=user,
        )
        user_info.save()

        return user_info


class UserBorrowStateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = "__all__"


class UserLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLocation
        fields = "__all__"

    def create(self, validated_data):
        location, created = UserLocation.objects.get_or_create(
            user=self.context['request'].user,
            location=validated_data['location']
        )

        if created:
            location.save()

        return location

    def to_representation(self, instance):
        ret = super(UserLocationSerializer, self).to_representation(instance)
        ret['user'] = instance.user.username

        return ret


# Donation
class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = "__all__"

    def to_representation(self, instance):
        ret = super(DonationSerializer, self).to_representation(instance)
        ret['like'] = instance.like.count()

        return ret


class DonationUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationUser
        fields = "__all__"

    def create(self, validated_data):
        donation = Donation.objects.get(title=self.context['request'].data['notice_title'])
        print(donation)

        userinfo = UserInfo.objects.get(user=self.context['request'].user)
        print(userinfo)
        print(userinfo.point)

        if userinfo.point >= validated_data['amount']:
            donation_user = DonationUser.objects.create(
                amount=validated_data['amount'],
                item=donation,
                user=self.context['request'].user
            )

            if donation.current_amount + validated_data['amount'] <= donation.target_amount:
                donation.current_amount = donation.current_amount + validated_data['amount']
                userinfo.point = userinfo.point - validated_data['amount']
                userinfo.save()

                if donation.current_amount >= donation.target_amount:
                    donation.title = "[후원 목표 달성]" + donation.title

                donation.save()
                donation_user.save()

            return donation_user
        else:
            raise serializers.ValidationError("포인트가 부족합니다.")


class DonationCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationComment
        fields = "__all__"

    def create(self, validated_data):
        donation = Donation.objects.get(title=self.context['request'].data['notice_title'])

        comment = DonationComment.objects.create(
            item=donation,
            user=self.context['request'].user,
            context=validated_data['context'],
            date=timezone.now()
        )

        comment.save()

        return comment

    def to_representation(self, instance):
        ret = super(DonationCommentSerializer, self).to_representation(instance)
        ret['user'] = instance.user.username

        return ret


# Borrow
class BorrowStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowState
        fields = "__all__"

    def create(self, validated_data):
        # username 으로 borrower 설정
        borrower = User.objects.get(username=self.context['request'].data['borrower_username'])

        borrower_userinfo = UserInfo.objects.get(user=borrower)
        borrower_userinfo.point = borrower_userinfo.point + 500
        borrower_userinfo.save()

        borrow_state = BorrowState.objects.create(
            borrower=borrower,
            lender=self.context['request'].user,
            date=timezone.now()
        )

        borrow_state.save()

        return borrow_state

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['borrower'] = instance.borrower.username
        ret['lender'] = instance.lender.username

        return ret


# Community
class CommunityPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityPost
        fields = "__all__"

    def create(self, validated_data):
        post = CommunityPost.objects.create(
            user=self.context['request'].user,
            context=validated_data['context'],
            date=timezone.now()
        )

        post.save()

        return post

    def to_representation(self, instance):
        ret = super(CommunityPostSerializer, self).to_representation(instance)
        ret['user'] = instance.user.username
        ret['like'] = instance.like.count()

        return ret


class CommunityCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityComment
        fields = "__all__"

    def create(self, validated_data):
        comment = CommunityComment.objects.create(
            post=CommunityPost.objects.get(id=self.context['request'].data['post']),
            user=self.context['request'].user,
            context=validated_data['context'],
            date=timezone.now()
        )

        comment.save()

        return comment

    def to_representation(self, instance):
        ret = super(CommunityCommentSerializer, self).to_representation(instance)
        ret['user'] = instance.user.username
        ret['like'] = instance.like.count()

        return ret


# Chat
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['user'] = instance.user.user.username

        return ret
