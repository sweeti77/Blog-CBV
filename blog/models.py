from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from django.contrib.auth.models import User

from PIL import Image

def get_image_path(instance, filename):
    name = instance.title
    return '%s-%s'%(name,filename)

# def get_image():


class Category(models.Model):
    title = models.CharField(max_length=35, db_index=True)
    slug = models.SlugField(unique=True, max_length=35)

    class Meta:
        ordering=('title',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

class Blog(models.Model):
    category = models.ManyToManyField(Category)
    slug = models.SlugField(unique=True, max_length=35)
    title = models.CharField(max_length=100)
    content = models.TextField(blank=False)
    image = models.ImageField(upload_to='blog', blank=True)
    posted_date = models.DateField(default=timezone.now())
    updated_date = models.DateField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        ordering=('title',)

    def __str__(self):
        return self.title



    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile', default='default.jpg')


    def __str__(self):
        return f'{self.user.username} Profile'


    def save(self):
        super().save()

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
