from .models import MailCodeVerification
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password, check_password
import secrets

class VerificationService:
    EXPIRATION_INTERVAL_SECONDS = 0
    EXPIRATION_INTERVAL_MINUTES = 15
    EXPIRATION_INTERVAL_HOURS = 0

    model = MailCodeVerification

    def __init__(self, user):
        self.user = user

    def _get_register_expiration_date(self) -> tuple[datetime, datetime]:
        now = timezone.now()
        delta = timedelta(seconds=self.EXPIRATION_INTERVAL_SECONDS,
                          minutes=self.EXPIRATION_INTERVAL_MINUTES,
                          hours=self.EXPIRATION_INTERVAL_HOURS)

        return now, now + delta

    @staticmethod
    def _generate_verification_code() -> str:
        code = ''.join(str(secrets.randbelow(10)) for _ in range(6))

        return code

    @staticmethod
    def hash_verification_code(code: str) -> str:

        return make_password(code)

    def verify_verification_code(self, code: str) -> MailCodeVerification | None:

        model_object = self.model.objects.filter(user_id=self.user.id,
                                                 expires_at__gt=timezone.now(),
                                                 status=self.model.Status.NOT_USED,
                                                 attempts_count__lt=self.model.MAX_ATTEMPTS_COUNT).first()

        if not model_object:
            return None

        if check_password(code, model_object.code):
            model_object.set_used_status()
            model_object.save(update_fields=["status"])
            return model_object

        else:
            model_object.increase_attempts_count()
            model_object.save(update_fields=["attempts_count", "status"])
            return None



    def register_verification(self):
        self.model.objects.filter(user=self.user,
                              status=self.model.Status.NOT_USED,
                              expires_at__gt=timezone.now()).update(status=self.model.Status.REJECTED)

        code = self._generate_verification_code()
        hashed_code = self.hash_verification_code(code)

        created_at, expires_at = self._get_register_expiration_date()

        self.model.objects.create(user=self.user, code=hashed_code, created_at=created_at, expires_at=expires_at)

        return code
