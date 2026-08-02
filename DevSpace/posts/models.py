from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
from uuid import uuid4
from unidecode import unidecode
from django.urls import reverse
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, blank=True, null=True)
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='posts/%Y/%m', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='posts')

    class Meta:
        verbose_name = 'POST'
        verbose_name_plural = 'POSTS'


    def save(self, *args, **kwargs):
        if not self.slug:
            slug = unidecode(self.title)
            self.slug = slugify(slug)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('posts:detail_post', kwargs={'slug': self.slug, 'uuid': self.uuid})

    def get_edit_url(self):
        return reverse('posts:edit_post', kwargs={'uuid': self.uuid, 'slug': self.slug})