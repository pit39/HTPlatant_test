from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

User = get_user_model()


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                str(user.verified) + str(user.pk) + str(user.email) + str(timestamp)
        )


token_generator = EmailVerificationTokenGenerator()


def send_email_for_verify(request, user, change_mail=False):
    current_site = get_current_site(request)
    context = {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token_generator.make_token(user),
    }
    if not change_mail:
        link = 'users/verify_email.html'
        title = 'Verify email'
    else:
        link = 'users/email_change.html'
        title = 'Change email'

    message = render_to_string(
        link,
        context=context,
    )

    email = EmailMessage(
        title,
        message,
        to=[user.email],
    )
    email.send()


def get_user(uidb64):
    try:
        # urlsafe_base64_decode() decodes to bytestring
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError,
            User.DoesNotExist, ValidationError):
        user = None
    return user
