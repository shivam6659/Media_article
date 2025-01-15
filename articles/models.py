from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date


class Article(models.Model):
    CATEGORY_CHOICES = [
        ('News', 'News'),
        ('Opinion', 'Opinion'),
        ('Feature', 'Feature'),
    ]

    TAG_CHOICES = [
        ('Politics', 'Politics'),
        ('Sports', 'Sports'),
        ('Tech', 'Tech'),
        ('Health', 'Health'),
    ]
    
    STATUS_CHOICES=[
       ('draft', 'Draft'),
       ('reviewed', 'Reviewed'),
       ('approved', 'Approved'),
       ('is_published', 'Is_Published'),
       ('rejected', 'Rejected'),
            
                   
    ]


    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    content = models.TextField()
    author_name= models.TextField(max_length=50, null=True)
    author= models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='articles', null=True)
    email = models.EmailField()
    image = models.ImageField(upload_to='article_images/', blank=True,)
    tags = models.CharField(max_length=100, choices=TAG_CHOICES, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    publish_date = models.DateField(null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='draft', blank=True)

    # Location-related fields
    city = models.CharField(max_length=50, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)  # Suitable for storing latitude
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)  # Suitable for storing longitude
     

    def __str__(self):
        return self.title

    def clean(self):
        # Ensure the publish date is a future date
        if self.publish_date <= timezone.now().date():
            raise ValidationError("Publish date must be a future date.")

class Meta:
        permissions = [
            ("can_submit_article", "Can submit article"),
            ("can_review_article", "Can review article"),
            ("can_publish_article", "Can publish article"),
        ]


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


def load_tags():
    tags = ['Politics', 'Sports', 'Tech', 'Lifestyle']
    for tag in tags:
        Tag.objects.get_or_create(name=tag)





