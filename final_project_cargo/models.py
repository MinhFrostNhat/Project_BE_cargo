import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse
from django.db import models
# Create your models here.
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail

from django_rest_passwordreset.signals import reset_password_token_created


from django.core.validators import RegexValidator
# signal used for is_active=False to is_active=True
from django.core.validators import MinValueValidator, MaxValueValidator


class User_inf(AbstractUser):
    image = models.ImageField(upload_to='Img_media', default='x.jpg')
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{8,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=225, default="root", unique=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Manage User account'
        verbose_name_plural = 'Manage User account'

    @property
    def group(self):
        groups = self.groups.all()
        return groups[0].name if groups else None


class Send_cargo(models.Model):
    REQUESTED = 'REQUESTED'
    STARTED = 'STARTED'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    CANCELD = 'CANCELD'
    STATUSES = (
        (REQUESTED, REQUESTED),
        (STARTED, STARTED),
        (IN_PROGRESS, IN_PROGRESS),
        (COMPLETED, COMPLETED),
        (CANCELD, CANCELD),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    create_work = models.DateTimeField(auto_now_add=True)
    update_work = models.DateTimeField(auto_now=True)
    pick_up_address = models.CharField(max_length=255)
    drop_off_address = models.CharField(max_length=255)
    get_cargo_name = models.CharField(max_length=255, blank=False)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{8,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number_get_cargo = models.CharField(
        validators=[phone_regex], max_length=17, blank=False)
    cargo_weight = models.FloatField(
        validators=[MinValueValidator(0.001), MaxValueValidator(1000)], blank=False)
    cargo_note = models.CharField(max_length=225)

    cargo_price = models.CharField(max_length=100, blank=False)
    cargo_distance = models.FloatField(
        validators=[MinValueValidator(0.000001), MaxValueValidator(1000)], blank=False)

    status = models.CharField(
        max_length=20, choices=STATUSES, default=REQUESTED)
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='Send_cargo_as_driver'
    )
    rider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='Send_cargo_as_rider'
    )

    def __str__(self):
        return f'{self.id}'

    def get_absoluted_url(self):
        return reverse('trip:trip_detail', kwargs={'taxi_id': self.id})

    class Meta:
        verbose_name = "Manage Trip of cargo"
        verbose_name_plural = "Manage Trip of cargo"


@receiver(post_save, sender=User_inf, dispatch_uid='active')
def banner(sender, instance, **kwargs):
    if User_inf.objects.filter(pk=instance.pk, is_active=False).exists():
        subject = 'Baner account'
        mesagge = ('Dear our valued client Your account have been banned, because of some violations related to community standards, such as non-standard naming... etc. Please contact me by email or hotline 1009699669')
        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, mesagge, from_email, [instance.email])


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = " Please input your password reset key {} into form and choose new own password. Your key will auto delete after 15min if you not use ".format(
        reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Get back password"),
        # message:
        email_plaintext_message,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [reset_password_token.user.email]
    )
