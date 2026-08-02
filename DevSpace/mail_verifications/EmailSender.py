from django.core.mail import send_mail
from DevSpace import settings

class EmailSender:

    @staticmethod
    def send_verification_code(email, code):
        send_mail(subject='Code Verification',
                  message=f'Verification Code: {code}',
                  from_email=settings.DEFAULT_FROM_EMAIL,
                  recipient_list=[email],)



