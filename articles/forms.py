from django import forms
from .models import Article
from datetime import date
from django.utils import timezone
from django.core.exceptions import ValidationError




class ArticlePage1Form(forms.Form):
    title = forms.CharField(
        max_length=50, 
        min_length=10, 
        widget=forms.TextInput(attrs={'placeholder': 'Enter a title'}),
        error_messages={'min_length': 'The title must be at least 10 characters long.'}
    )
    subtitle = forms.CharField(
        max_length=30, 
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'Enter a subtitle (optional)'}),
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Write your article content here...'}),
    )
    author_name = forms.CharField(
        max_length=15, 
        widget=forms.TextInput(attrs={'placeholder': 'Enter author name'}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter author email'}),
    )
   



class ArticlePage2Form(forms.Form):
    article_image = forms.ImageField(required=False)
    
    TAG_CHOICES = [
        ('Politics', 'Politics'),
        ('Sports', 'Sports'),
        ('Tech', 'Tech'),
        ('Health', 'Health'),
    ]
    tags = forms.MultipleChoiceField(
        required=True,
        choices=TAG_CHOICES, 
        widget=forms.CheckboxSelectMultiple,
    )
    
    CATEGORY_CHOICES = [
        ('News', 'News'),
        ('Opinion', 'Opinion'),
        ('Feature', 'Feature'),
    ]
    category = forms.ChoiceField(
        required=True,
        choices=CATEGORY_CHOICES, 
        widget=forms.Select(attrs={'placeholder': 'Select a category'}),
    )
    
    publish_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'min': date.today().isoformat(),}),
    )
      # City input field
    city = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'city',
            'placeholder': 'Enter city name',
            
        })
    )
    latitude = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'latitude',
            'placeholder': 'Latitude',
            'readonly': True,  # Prevent manual entry
        })
    )
    longitude = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'longitude',
            'placeholder': 'Longitude',
            'readonly': True,  # Prevent manual entry
        })
    )
   
     
    
# class ArticleForm(forms.ModelForm):
    agreed_to_terms = forms.BooleanField(
        required=True,
        label="I agree to the terms and conditions",
        error_messages={'required': 'You must agree to the terms to submit the article.'}
    )

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'subtitle', 'content', 'author_name','image', 'tags', 'category', 'publish_date', ]

        

def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        # Tags is a MultipleChoiceField, so we get a list of selected tags
        # The Article model uses a CharField to store tags, so we'll join them into a string
        if tags:
            return ','.join(tags)  # Convert list of tags into a comma-separated string
        return ''


def clean_publish_date(self):
        publish_date = self.cleaned_data.get('publish_date')
        if publish_date and publish_date <= timezone.now().date():
            raise forms.ValidationError("Publish date must be in the future.")
        return publish_date


