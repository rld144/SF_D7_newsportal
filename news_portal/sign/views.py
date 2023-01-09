from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from newsportal.models import Author, Category, Subcribers
from django.views.generic import ListView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .filters import CatFilter
from .forms import CatForm



class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/news/'


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    if not Author.objects.filter(user=user).exists():
        Author.objects.create(user=user)
    return redirect('/news/')


@login_required
def recipients_email(request):
    user = request.user
    recipients_group = Group.objects.get(name='recipients')
    if not request.user.groups.filter(name='recipients').exists():
        recipients_group.user_set.add(user)
    return redirect('/news/')



class Subscribtion(LoginRequiredMixin,ListView):
    model = Category
    template_name = 'sign/subscribe.html'
    context_object_name = 'cats'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = CatFilter(self.request.GET, queryset)
        if '?filter' in self.request.get_full_path():
            user = self.request.user
            categories = self.filterset.qs
            for category in categories:
                if not Subcribers.objects.filter(user=user, category=category).exists():
                    Subcribers.objects.create(user=user, category=category)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        user = self.request.user
        user_cats = user.subcribers_set.all()
        context['user_cats'] = user_cats
        return context





