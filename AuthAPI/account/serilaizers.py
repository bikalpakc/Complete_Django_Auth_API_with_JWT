from django.forms import ValidationError
from rest_framework import serializers
from account.models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util

class UserRegistrationSerializer(serializers.ModelSerializer):
    #We are writing this because we have no confirm password field in our user model, so serializer cannot generate it automaticlly, So, we need to manually define inorder to confirm password field in our Registration request.
    password2=serializers.CharField(style={'input_type':'password'})

    class Meta:
        model=User
        fields=['email', 'name', 'password','password2', 'tc']
        extra_kwargs={
            'password':{'write_only':True}
        }

    def validate(self, data):
        password=data.get('password')
        password2=data.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match.")
        else:
            return data

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)  


class UserLoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=User
        fields=['email', 'password']  

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id', 'email', 'name']       

class UserChangePasswordSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)               
    password2=serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)               
    class Meta:
        fields=['password', 'password2']

    def validate(self, data):
        password=data.get('password')
        password2=data.get('password2') 
        user=self.context.get('user')  
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match.")
        else:
            user.set_password(password)
            user.save()
            return data 
        
class SendPasswordResetEmailSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        fields=['email']

    def validate(self, data):
        email=data.get('email')
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID', uid)
            token=PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token', token)
            link='http://localhost:3000/api/uesr/reset/'+uid+'/'+token
            print('Password Reset Link', link)
            #send Email
            body='Click the following link to reset your Password.' + link
            data={
                'subject':'Reset your Password.',
                'body':body,
                'to_email': user.email
            }
            Util.send_email(data)
            return data
        else:
            raise serializers.ValidationError('This email is not registered.')


class UserPasswordResetSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)               
    password2=serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)               
    class Meta:
        fields=['password', 'password2']

    def validate(self, data):
        try:
            password=data.get('password')
            password2=data.get('password2') 
            uid=self.context.get('uid')  
            token=self.context.get('token')  
            if password != password2:
                raise serializers.ValidationError("Password and Confirm Password doesn't match.")
            else:
                id=smart_str(urlsafe_base64_decode(uid))
                user=User.objects.get(id=id)
                if not PasswordResetTokenGenerator().check_token(user, token):
                    raise ValidationError('Token is not Valid or Expired.')
                else:
                    user.set_password(password)
                    user.save()
                    return data 
            
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise ValidationError('Token is not Valid or Expired.')
    