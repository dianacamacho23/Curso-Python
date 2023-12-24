from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import BlogPost,Category, Tag,UserProfile, User
from .forms import CategoryForm, TagForm,UserProfileForm
from django.http import Http404
from django.db.models import Q

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # Check if the user has a profile, and if not, redirect to profile creation
            if not UserProfile.objects.filter(user=user).exists():
                return redirect('create_profile')

            # User has a profile, so redirect to home or any other desired page
            return redirect('home')

    else:
        form = UserCreationForm()
    
    
    return render(request, 'registration/signup.html', {'form': form})


def user_logout(request):
    logout(request)
    return render(request,'registration/logout.html')


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog/blogpost_list.html'
    context_object_name = 'blogposts'  # Define the context variable name


class BlogPostCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    template_name = 'blog/blogpost_form.html'
    fields = ['title', 'content', 'categories', 'tags']
    success_url = reverse_lazy('blogpost_list')


    def form_valid(self, form):
        form.instance.author = self.request.user  # Set the author to the logged-in user
        return super().form_valid(form)
    
class BlogPostUpdateView(UpdateView):
    model = BlogPost
    template_name = 'blog/blogpost_form.html'
    fields = ['title', 'content', 'categories', 'tags']

class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blog/blogpost_confirm_delete.html'
    success_url = reverse_lazy('blogpost_list')

class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blogpost_detail.html'
    context_object_name = 'blogpost'

class SearchResultsView(ListView):
    model = BlogPost
    template_name = 'search_results.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            
            return BlogPost.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            ).distinct()
        else:
            
            return BlogPost.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        context['query'] = query

       
        if 'posts' not in context or not context['posts']:
            context['no_results'] = True

        return context
    

class CustomLoginView(LoginView):
    def form_valid(self, form):
        if self.request.user.is_authenticated:
            user = self.request.user
            if not UserProfile.objects.filter(user=user).exists():
                return redirect('create_profile')
        return super().form_valid(form)



def home(request):
    return render(request, 'home.html')

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'category/category_form.html', {'form': form})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category/category_list.html', {'categories': categories})

def tag_create(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tag_list')
    else:
        form = TagForm()
    return render(request, 'tag/tag_form.html', {'form': form})

def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'tag/tag_list.html', {'tags': tags})
# Create your views here.

def profile(request, username):
    try:
        user_profile = UserProfile.objects.get(user__username=username)
        return render(request, 'profile/profile.html', {'user_profile': user_profile})
    except UserProfile.DoesNotExist:
        # If the UserProfile doesn't exist, check if it's the current user's profile
        if request.user.username == username:
            return redirect('edit_profile')
        else:
            raise Http404("User's profile does not exist")
        
            
def edit_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'profile/edit_profile.html', {'form': form})

def create_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the profile associated with the current user
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile', username=request.user.username)
    else:
        form = UserProfileForm()

    return render(request, 'profile/create_profile.html', {'form': form})