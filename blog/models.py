from django.db import models
from django.template.defaultfilters import slugify

from user.models import User


class Blog(models.Model):
    title = models.CharField(max_length=100)
    short_description = models.CharField(max_length=100, blank=False)
    main_text = models.TextField(blank=False)
    is_active = models.BooleanField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='static/blog/blog_images/')
    slug = models.SlugField(db_index=True)
    author = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.title},{self.author}'

    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'


class BlogVisit(models.Model):
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE, verbose_name='Blog visit')
    ip = models.CharField(max_length=30, verbose_name='User IP')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name='User Who Visited')

    def __str__(self):
        return f'{self.blog.title} / {self.ip}'

    class Meta:
        verbose_name = 'Blog visit'
        verbose_name_plural = 'Blog visits'


class BlogComments(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name='Blog')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Created Date')
    text = models.TextField(verbose_name='comment Text')
    def __str__(self):
        return f'{self.blog.slug}/{self.user}'

    class Meta:
        verbose_name = 'Blog Comment'
        verbose_name_plural = 'Blog Comments'