from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class MailCodeVerification(models.Model):

    MAX_ATTEMPTS_COUNT = 5



    class Status(models.IntegerChoices):
        NOT_USED = 0, 'Not Used'
        USED  = 1, 'Used'
        REJECTED = 2, 'Rejected'



    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='mail_code_verifications')
    code = models.CharField(max_length=256)
    created_at = models.DateTimeField()
    expires_at = models.DateTimeField()
    attempts_count = models.PositiveIntegerField(default=0)
    status = models.IntegerField(choices=Status, default=Status.NOT_USED)


    class Meta:
        verbose_name = 'Mail Code Verification'
        verbose_name_plural = 'Mail Codes Verification'
        ordering = ('-created_at',)


    def set_used_status(self):

        self.status = self.Status.USED


    def set_rejected_status(self):
        self.status = self.Status.REJECTED

    def increase_attempts_count(self):
        self.attempts_count +=  1

        if self.attempts_count >= self.MAX_ATTEMPTS_COUNT:
            self.set_rejected_status()

