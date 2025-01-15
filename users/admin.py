from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )


@login_required
def article_form_page1(request):
    # Existing code...
    pass

@login_required
def article_form_page2(request):
    # Existing code...
    pass


from django.contrib.auth.models import Group

Group.objects.get_or_create(name='Admin')
Group.objects.get_or_create(name='Journalist')
Group.objects.get_or_create(name='Editor')
Group.objects.get_or_create(name='User')




