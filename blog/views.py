from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render,get_object_or_404,redirect
from .models import BlogPost
from django.http import Http404
from .forms import BlogPostForm, BlogPostModelForm

# Create your views here.

# get -> 1 object
# filter -> [] objects

#CRUD:

#GET -> Retrive / List
# POST -> Create / Update / Delete

#CRUD -> Create Retrive Update Delete

def blog_post_list_view(request):
    qs = BlogPost.objects.all().published()
    if request.user.is_authenticated:
        my_qs = BlogPost.objects.filter(user=request.user)
        qs = (qs | my_qs).distinct()
    template_name = 'blog/list.html'
    context = {'object_list': qs}
    return render(request, template_name, context)

#@login_required(login_url='/about')
@staff_member_required
def blog_post_create_view(request):
    form = BlogPostModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user 
        obj.save()
        form = BlogPostModelForm()

    template_name = 'form.html'
    context = {'form': form}
    return render(request, template_name, context)

def blog_post_details_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug) 
    template_name = 'blog/detail.html'
    context = {'object': obj}
    return render(request, template_name, context)


def blog_post_update_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug) 
    form = BlogPostModelForm(request.POST or None,  instance=obj)
    if form.is_valid():
        form.save()
        #form = BlogPostModelForm()
    template_name = 'form.html'
    context = {'form': form, 'title': f"Update {obj.title} "}
    return render(request, template_name, context)

def blog_post_delete_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug) 
    template_name = 'blog/delete.html'
    if request.method == "POST":
        obj.delete()
        return redirect('/blog')
    context = {'object': obj}
    return render(request, template_name, context)
