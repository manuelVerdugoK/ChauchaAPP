from django.contrib.auth.models import User,AbstractUser
from django.db import models
from django.core.mail import send_mail
from django.conf import settings


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=6, blank=True)
    is_verified = models.BooleanField(default=False)

    def generate_verification_code(self):
        # Aquí generamos un código de verificación aleatorio de 6 dígitos
        import random
        self.verification_code = str(random.randint(100000, 999999))

    def send_verification_email(self):
        subject = 'Código de verificación'
        message = f'Tu código de verificación es: {self.verification_code}'
        from_email = settings.EMAIL_HOST_USER
        to_email = self.user.email
        send_mail(subject, message, from_email, [to_email], fail_silently=False)

    def verify_account(self, code):
        if code == self.verification_code:
            self.is_verified = True
            self.save()
            return True
        return False
