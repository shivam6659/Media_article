from django.shortcuts import render, redirect
from .forms import ArticlePage1Form, ArticlePage2Form
from .models import Article
from .forms import ArticleForm
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from rest_framework import generics, permissions
from .serializers import ArticleSerializer
from django.contrib.auth.decorators import login_required, user_passes_test
from PIL import Image
from django.contrib.auth.decorators import permission_required
from .models import Article
# from django.http import HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import render
from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from users.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.urls import reverse
from django.db.models import Q 



def article_form_page1(request):
    if request.method == 'POST':
        form = ArticlePage1Form(request.POST)
        if form.is_valid():
            request.session['page1_data'] = form.cleaned_data  # Save data to session
            return redirect('article_form_page2')
    else:
        form = ArticlePage1Form()
         # Prepopulate the form with data from the session if available
        initial_data = request.session.get('page1_data', {})
        form = ArticlePage1Form(initial=initial_data)

    return render(request, 'articles/article_form_page1.html', {'form': form})

def article_form_page2(request):
    if 'page1_data' not in request.session:  # Ensure page1 data exists
        return redirect('article_form_page1')
    
    if request.method == 'POST':
        form = ArticlePage2Form(request.POST, request.FILES)
        if form.is_valid():
            # Combine page 1 and page 2 data
            article_data = {**request.session['page1_data'], **form.cleaned_data}
            print(article_data)
            article = Article.objects.create(
                title=article_data['title'], 
                subtitle=article_data['subtitle'], 
                content=article_data['content'], 
                author_name=article_data['author_name'],
                # author=article_data['author'], 
                # author = request.POST.get('author', None),
                author=request.user,
                email=article_data['email'], 
                image=article_data['article_image'],
                tags=article_data['tags'], 
                category=article_data['category'], 
                publish_date=article_data['publish_date'], 
                
                city = form.cleaned_data.get('city'),
                latitude = form.cleaned_data.get('latitude'),
                longitude = form.cleaned_data.get('longitude'),
                
                # Add other fields as necessary
            )
            article.save()
        
            del request.session['page1_data']  # Clear session data
            return redirect('journalist_dashboard')  # Redirect to a success page
       
    else:
        form = ArticlePage2Form()
    return render(request, 'articles/article_form_page2.html', {'form': form })

import ast
# def article_success(request):
#     return render(request, 'articles/article_success.html')

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'article_detail.html', {'article': article})


# articles/views.py
def csrf_failure(request, reason=""):
    return HttpResponseForbidden("CSRF verification failed. Please try again.")




@login_required
@user_passes_test(lambda u: u.groups.filter(name='Journalist').exists())
def journalist_dashboard(request):
    print("Logged-in User:", request.user)  # Debugging User
    # Get the search query from the request (if any)
    search_query = request.GET.get('search', '')

    # Filter articles based on the search query
    if search_query:
        articles = Article.objects.filter(author=request.user, title__icontains=search_query)
    else:
        articles = Article.objects.filter(author=request.user)

    # Pagination
    paginator = Paginator(articles, 10)  # Show 10 articles per page
    page_number = request.GET.get('page')  # Get the page number from the request
    page_obj = paginator.get_page(page_number)


    print("Fetched Articles:", articles)  # Debugging Articles
    return render(request, 'journalist_dashboard.html', {'articles': page_obj, 'search_query': search_query})



@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    # Get the search query from the request (if any)
    search_query = request.GET.get('search', '')

    # Filter articles based on the search query (search in title and content)
    if search_query:
        articles = Article.objects.filter(title__icontains=search_query)
    else:
        articles = Article.objects.all()

    # Pagination
    paginator = Paginator(articles, 10)  # Show 10 articles per page
    page_number = request.GET.get('page')  # Get the page number from the request
    page_obj = paginator.get_page(page_number)

    # Passing the data to the template
    return render(request, 'admin_dashboard.html', {'page_obj': page_obj, 'search_query': search_query})



@login_required
@user_passes_test(lambda u: u.groups.filter(name='Editor').exists())
def editor_dashboard(request):
    # Get the search query from the request (if any)
    search_query = request.GET.get('search', '')

    # Filter articles based on the search query (search in title or content)
    if search_query:
        articles = Article.objects.filter(title__icontains=search_query)
    else:
        articles = Article.objects.all()

    # Pagination
    paginator = Paginator(articles, 10)  # Show 10 articles per page
    page_number = request.GET.get('page')  # Get the page number from the request
    page_obj = paginator.get_page(page_number)

    # Passing the data to the template
    return render(request, 'editor_dashboard.html', {'page_obj': page_obj, 'search_query': search_query})



@login_required
@user_passes_test(lambda u: u.groups.filter(name='Journalist').exists())
def login(request):
    return render(request, 'login.html')

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Journalist').exists())
def article_list(request):
    articles = Article.objects.all()  # Fetch all articles
    return render(request, 'articles/article_list.html', {'articles': articles})



# Journalist view - Can submit an article
@permission_required('articles.can_submit_article', raise_exception=True)
def submit_article(request):
    if request.method == 'POST':
        # Logic to submit an article
        title = request.POST['title']
        content = request.POST['content']
        article = Article.objects.create(title=title, content=content, author=request.user)
        return redirect('article_list')
    return render(request, 'submit_article.html')

# Editor view - Can review articles
# @permission_required('articles.can_review_article', raise_exception=False)
def review_article(request, id):
    article = Article.objects.get(id=id)
    
    if request.method == 'POST':
        # Logic to update the article status based on the form submission
        status = request.POST.get('status')
        if status in ['draft', 'approved', 'rejected']:
            article.status = status
            article.save()
        return redirect('editor_dashboard')
    
    # Render the template and pass the article data to it
    return render(request, 'review_article.html', {'article': article})


# Admin view - Can publish articles
# @permission_required('articles.can_publish_article', raise_exception=False)
def publish_article(request, id):
    article = get_object_or_404(Article, id=id)

    # Print all articles for debugging
    print(Article.objects.all())

    # If the form is submitted (POST request), publish the article
    if request.method == 'POST':
        article.published_at = timezone.now()
        article.is_published = True
        article.save()
        return redirect('editor_dashboard')

    # Render the template and pass the article data to it
    return render(request, 'publish_article.html', {'article': article})


def article_delete(request, id):
    # Fetch the article by its ID
    article = get_object_or_404(Article, id=id)

    if request.method == 'POST':
        article.delete()  # Delete the article from the database
        return redirect('editor_dashboard')  # Redirect to a list page after deletion
    
             
    return render(request, 'article_delete.html', {'article': article})

def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'article_detail.html', {'article': article})

def edit_article(request, article_id):
    # Get the article object or return 404 if not found
    article = get_object_or_404(Article, id=article_id)
   
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()  # Save the updated article
            return redirect('article_detail', article_id=article.id)  # Redirect to the article detail page after saving
    else:
        form = ArticleForm(instance=article)  # Pre-fill the form with the current article data

    return render(request, 'edit_article.html', {'form': form, 'article': article})




class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/article_form.html'
    success_url = reverse_lazy('journalist_dashboard')  # Redirect to the article list after successful creation

    def form_valid(self, form):
        form.instance.author = self.request.user  # Automatically assign the current user as the author
        return super().form_valid(form)

    # def form_valid(self, form):
    #     form.instance.author = self.request.user  # Assign the current user as the author
    #     response = super().form_valid(form)
    #     print(f"Article created: {form.instance}, Author: {form.instance.author}")
    #     return response


class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/article_form.html'
    success_url = reverse_lazy('article_list')

    def get_queryset(self):
        # Ensure that users can only edit their own articles
         return Article.objects.filter(author=self.request.user)
    


# @login_required
# @user_passes_test(lambda u: u.groups.filter(name='Home').exists())
def home_dashboard(request):

    # Querying all articles from the database
    # articles = Article.objects.all()
    articles = Article.objects.filter(is_published='1')
    # Get the search query from the request (if any)
    search_query = request.GET.get('search', '')
    # Filter articles based on the search query (search in title and content)
    if search_query:
        articles = Article.objects.filter( 
            Q(title__icontains=search_query) | Q(author_name__icontains=search_query)
            )
    # Pagination
    paginator = Paginator(articles, 10)  # Show 10 articles per page
    page_number = request.GET.get('page')  # Get the page number from the request
    page_obj = paginator.get_page(page_number)
    # Passing the data to the template
    return render(request, 'home_dashboard.html', {'page_obj': page_obj})

    
def article_view(request, id):
    article = get_object_or_404(Article, id=id)
    return render(request, 'article_view.html', {'article': article})






# View to display the user dashboard
@login_required
def user_dashboard(request):
    search_query = request.GET.get('search', '')  # Get the search query from the URL
    if search_query:
        # Filter users by username or email containing the search query
        users = User.objects.filter(
            Q(username__icontains=search_query) | Q(email__icontains=search_query)
        )
    else:
        # If no search query, get all users
        users = User.objects.all()

    return render(request, 'user_dashboard.html', {'users': users, 'search_query': search_query})

# View to update the user role
@csrf_exempt  # Exempt CSRF protection for API requests (add security as needed)
@login_required
def update_user_role(request, user_id):
   
    if request.user.is_superuser:  # Check if the user is an admin
        if request.method == 'POST':
            
            user = get_object_or_404(User, id=user_id)  # Get the user by ID
            try:
                # Get the new role from the request data
                data = json.loads(request.body)
               
                new_role = data.get('role')

                # Validate the role
                if new_role in ['Admin', 'Editor', 'Journalist', 'User']:
                    user.role = new_role
                    user.save()
                    return JsonResponse({'success': True, 'message': 'Role updated successfully'})
                
                
                else:
                    return JsonResponse({'success': False, 'error': 'Invalid role'})

            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})

        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    else:
        return JsonResponse({'success': False, 'error': 'You do not have permission to update roles.'})




@csrf_exempt
@login_required
def delete_user(request, user_id):
    if request.method == 'DELETE' and request.user.is_superuser:
        try:
            user = get_object_or_404(User, id=user_id)
            user.delete()
            return JsonResponse({'success': True, 'message': 'User deleted successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request or insufficient permissions.'}, status=400)







