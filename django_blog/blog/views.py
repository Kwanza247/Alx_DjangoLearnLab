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
    template_name = "blog/post_list.html"
    context_object_name = "posts"

class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"

class PostCreateView(CreateView):
    model = Post
    template_name = "blog/post_form.html"
    fields = ["title", "content"]

class PostUpdateView(UpdateView):
    model = Post
    template_name = "blog/post_form.html"
    fields = ["title", "content"]

class PostDeleteView(DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("post_list")