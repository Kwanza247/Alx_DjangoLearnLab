from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Post

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save (self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("bio", "avatar")
        widgets = {
            'bio': forms.Textarea(attrs={'rows':3}),
        }

class PostForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        help_text="Add tags seperated by commas(e.g. django,python,web)",
    )
    class Meta:
        model = Post
        fields = ("title", "content")
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Post title"}),
            "content": forms.Textarea(attrs={"rows":8, "placeholder": "Write your post..."}),
        }
    
    def clean_tags(self):
        raw = self.cleaned_data.get("tags", "")
        #normalize: split, strip, lowercase, unique
        tags = [t.strip() for t in raw.split(",") if t.strip()]
        normalized = []
        for t in tags:
            name = t.lower()
            if name not in normalized:
                normalized.append(name)
            return normalized