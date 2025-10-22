from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
import requests
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests as google_requests

from .serializers import (
    RegisterSerializer, UsernameAvailabilitySerializer, VerifyOtpSerializer,
    LoginSerializer, GoogleAuthSerializer, ForgotPasswordRequestSerializer,
    ResetPasswordSerializer
)
from .models import CustomUser as User
from .utils import set_otp, otp_is_valid

User = get_user_model()


def issue_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {"access": str(refresh.access_token), "refresh": str(refresh)}


class UsernameAvailabilityView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        serializer = UsernameAvailabilitySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        exists = User.objects.filter(username__iexact=username).exists()
        return Response({"available": not exists})


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        otp = set_otp(user, purpose="verify", minutes_valid=10)
        send_mail(
            subject="Your Bitmore verification OTP",
            message=f"Your OTP is {otp}. It expires in 10 minutes.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )
        return user

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)   # ✅ FIXED
        user = self.perform_create(serializer)
        return Response({"message": "Registered. OTP sent to email."}, status=status.HTTP_201_CREATED)


class VerifyOtpView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = VerifyOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        otp = serializer.validated_data["otp"]

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=404)

        if otp_is_valid(user, otp, "verify"):
            user.is_verified = True
            user.otp = None
            user.otp_expires_at = None
            user.otp_purpose = None
            user.save(update_fields=["is_verified", "otp", "otp_expires_at", "otp_purpose"])
            tokens = issue_tokens_for_user(user)
            return Response({"message": "Verified successfully.", **tokens})
        return Response({"detail": "Invalid or expired OTP."}, status=400)

class JwtLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "No account found with this email."}, status=400)

        if user.is_google_account:
            return Response(
                {"detail": "This account was registered via Google. Please login with Google."},
                status=400
            )

        if not user.check_password(password):
            return Response({"detail": "Incorrect email or password."}, status=400)

        if not user.is_verified:
            return Response({"detail": "Please verify your email first."}, status=400)

        tokens = issue_tokens_for_user(user)
        return Response({"message": "Login successful.", **tokens})

# class JwtLoginView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data["user"]

#         if user.is_google_account:
#             return Response(
#                 {"detail": "This account was created with Google. Please sign in using Google Login."},
#                 status=400
#             )

#         tokens = issue_tokens_for_user(user)
#         return Response({"message": "Login successful.", **tokens})

# class JwtLoginView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data["user"]
#         tokens = issue_tokens_for_user(user)
#         return Response({"message": "Login successful.", **tokens})

class GoogleLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = GoogleAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data["id_token"]

        try:
            # Verify Google ID token
            idinfo = google_id_token.verify_oauth2_token(
                token,
                google_requests.Request(),
                settings.GOOGLE_CLIENT_ID
            )

            email = idinfo.get("email")
            name = idinfo.get("name") or email.split("@")[0]

            if not email:
                return Response({"detail": "Google token missing email."}, status=400)

            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "username": email.split("@")[0],
                    "first_name": name,
                    "is_verified": True,
                    "is_google_account": True,   # ✅ mark as google account
                },
            )
            
            # # ✅ Create or get user
            # user, created = User.objects.get_or_create(
            #     email=email,
            #     defaults={
            #         "username": email.split("@")[0],
            #         "first_name": name,
            #         "is_verified": True,
            #     },
            # )

            # ✅ Ensure username is unique
            if created:
                base = user.username
                i = 1
                while User.objects.filter(username=user.username).exclude(pk=user.pk).exists():
                    user.username = f"{base}{i}"
                    i += 1
                user.save()

            # ✅ Auto-verify Google users
            if not user.is_verified:
                user.is_verified = True
                user.save(update_fields=["is_verified"])

            # ✅ Issue JWT tokens
            tokens = issue_tokens_for_user(user)

            return Response(
                {
                    "message": "Google login successful.",
                    "email": user.email,
                    "is_new": created,   # <-- tells frontend if this was a registration
                    **tokens,
                }
            )

        except Exception as e:
            return Response({"detail": f"Invalid Google token. {str(e)}"}, status=400)

# # class GoogleLoginView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         serializer = GoogleAuthSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         token = serializer.validated_data["id_token"]

#         try:
#             idinfo = google_id_token.verify_oauth2_token(
#                 token,
#                 google_requests.Request(),
#                 settings.GOOGLE_CLIENT_ID
#             )
#             email = idinfo.get("email")
#             if not email:
#                 return Response({"detail": "Google token missing email."}, status=400)

#             user, created = User.objects.get_or_create(
#                 email=email,
#                 defaults={
#                     "username": email.split("@")[0],
#                     "is_verified": True
#                 }
#             )
#             if created:
#                 # ensure unique username
#                 base = user.username
#                 i = 1
#                 while User.objects.filter(username=user.username).exclude(pk=user.pk).exists():
#                     user.username = f"{base}{i}"
#                     i += 1
#                 user.save()

#             if not user.is_verified:
#                 user.is_verified = True
#                 user.save(update_fields=["is_verified"])

#             tokens = issue_tokens_for_user(user)
#             return Response({"message": "Google login successful.", "email": user.email, **tokens})

#         except Exception:
#             return Response({"detail": "Invalid Google token."}, status=400)


class ForgotPasswordRequestView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ForgotPasswordRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"message": "If the email exists, an OTP has been sent."})

        if user.is_google_account:
            return Response(
                {"detail": "This account was registered via Google. Please login with Google."},
                status=400
            )

        otp = set_otp(user, purpose="reset", minutes_valid=10)
        send_mail(
            subject="Bitmore password reset OTP",
            message=f"Your password reset OTP is {otp}. It expires in 10 minutes.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=True,
        )
        return Response({"message": "If the email exists, an OTP has been sent."})

# class ForgotPasswordRequestView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         serializer = ForgotPasswordRequestSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         email = serializer.validated_data["email"]

#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return Response({"message": "If the email exists, an OTP has been sent."})

#         otp = set_otp(user, purpose="reset", minutes_valid=10)
#         send_mail(
#             subject="Bitmore password reset OTP",
#             message=f"Your password reset OTP is {otp}. It expires in 10 minutes.",
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             recipient_list=[email],
#             fail_silently=True,
#         )
#         return Response({"message": "If the email exists, an OTP has been sent."})


class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]
        new_password = serializer.validated_data["new_password"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "Invalid email or OTP."}, status=400)

        if not otp_is_valid(user, otp, "reset"):
            return Response({"detail": "Invalid or expired OTP."}, status=400)

        user.set_password(new_password)
        user.otp = None
        user.otp_expires_at = None
        user.otp_purpose = None
        user.save(update_fields=["password", "otp", "otp_expires_at", "otp_purpose"])
        return Response({"message": "Password reset successful."})

#resend OTP:
class ResendOtpView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        purpose = request.data.get("purpose", "verify")  # "verify" or "reset"

        if not username:
            return Response({"detail": "Username is required."}, status=400)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=404)

        otp = set_otp(user, purpose=purpose, minutes_valid=10)
        send_mail(
            subject=f"Your Bitmore {purpose.capitalize()} OTP",
            message=f"Your OTP is {otp}. It expires in 10 minutes.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )
        return Response({"message": "OTP resent successfully."})

