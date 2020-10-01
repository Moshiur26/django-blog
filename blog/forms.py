from django import forms
from .models import BlogPost


class BlogPostForm(forms.Form):
    title   = forms.CharField()
    slug    = forms.SlugField()
    content = forms.CharField(widget=forms.Textarea)

class BlogPostModelForm(forms.ModelForm):
    class Meta:
        #title   = forms.CharField()
        model = BlogPost
        fields = ['title', 'image', 'slug', 'content', 'publish_date']

    def clean_title(self, *args, **kwargs):
        instance = self.instance
        title = self.cleaned_data.get('title')
        qs = BlogPost.objects.filter(title__iexact=title)#(title__icontains=title)#(title__iexact=title)#(title=title)
        if instance is not None:
            qs = qs.exclude(pk=instance.pk) # id = instance.idS
        if qs.exists():
            raise forms.ValidationError('This title has already been used. Please try again')
        return title