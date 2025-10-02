from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView,DetailView, CreateView, UpdateView, DeleteView
from .forms import CustomUserCreationForm, ProfileForm, PostForm
from .models import Post, Tag

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('blog:login')
    else:
        form = CustomUserCreationForm()
    return render(request, "blog/register.html", {"form": form})


class LoginView(auth_views.LoginView):
    template_name = "blog/login.html"


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy("blog:login")


@login_required
def profile_view(request):
    user = request.user
    try:
        profile = user.profile
    except Exception:
        profile = None

    if request.method == "POST":
        pform = ProfileForm(request.POST, request.FILES, instance=user.profile)
        if pform.is_valid():
            pform.save()

            # allow change of email via user model
            new_email = request.POST.get("email", "")
            if new_email:
                user.email = new_email
                user.save()

            messages.success(request, "Profile updated.")
            return redirect('blog:profile')
    else:
        pform = ProfileForm(instance=user.profile)

    return render(request, "blog/profile.html", {"pform": pform, "user": user})

# --- Post List & Detail (public) ----------------------------------------
class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 10
    ordering = ["-published_date"]

class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        #handle tag
        tag_names = form.cleaned_data.get("tags", [])
        if tag_names:
            for name in tag_names:
                tag_obj, _= Tag.objects.get_or_create(name=name)
                self.object.tags.add(tag_obj)
        messages.success(self.request, "Post created succesfully.")
        return response

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def get_initial(self):
        initial = super().get_initial()
        #prefill tags as comma-separated string
        initial['tags'] = ", ".join([t.name for t in self.get_obbject().tags.all()])
        return initial
    
    def form_vald(self, form):
        response = super().form_valid(form)
        #update tags: clear and re-add
        tag_names = form.cleaned_data.get("tags", [])
        self.objects.tags.clear()
        if tag_names:
            for name in tag_names:
                tag_obj, _= Tag.objects.get_or_create(name=name)
                self.objects.tags.add(tag_obj)
        messages.success(self.request, "post updated succesfully.")
        return response
    
    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("post_list")

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user
    

# --- Tag view: list posts for a tag -------------------------------------
class PostsByTagView(ListView):
    model = Post
    template_name = "blog/posts_by_tag.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        tag_name = self.kwargs.get("tag_name", "")
        return Post.objects.filter(tags__name=tag_name).order_by("-published_date")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["tag_name"] = self.kwargs.get("tag_name", "")
        return ctx

# --- Search view --------------------------------------------------------
class SearchResultsView(ListView):
    model = Post
    template_name = "blog/search_results.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        if not query:
            return Post.objects.none()
        # search title OR content OR tags__name (case-insensitive)
        return Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct().order_by("-published_date")