from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView,DetailView, CreateView, UpdateView, DeleteView
from .forms import CustomUserCreationForm, ProfileForm, PostForm
from .models import Post

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
    template_name = "blog/posts/post_list.html"   # blog/templates/blog/posts/post_list.html
    context_object_name = "posts"
    paginate_by = 10
    ordering = ['-published_date']

class PostDetailView(DetailView):
    model = Post
    template_name = "blog/posts/post_detail.html"
    context_object_name = "post"

# --- Create, Update, Delete (authenticated + author checks) -------------
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/posts/post_form.html"

    def form_valid(self, form):
        # set the author from the logged-in user
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "Post created successfully.")
        return response

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/posts/post_form.html"

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "You are not allowed to edit this post.")
        return super().handle_no_permission()

    def form_valid(self, form):
        messages.success(self.request, "Post updated successfully.")
        return super().form_valid(form)

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/posts/post_confirm_delete.html"
    success_url = reverse_lazy("blog:post-list")

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "You are not allowed to delete this post.")
        return super().handle_no_permission()