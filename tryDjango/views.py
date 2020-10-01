from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from .forms import ContactForm
from blog.models import BlogPost

def home_page(request):
    qs = BlogPost.objects.all()[:5]
    context = {'title':'Welcome to Try Django','blog_list':qs}
    return render(request,'home.html',context)

def about_page(request):
    return render(request,'about.html',{'title':"About Page"})
def contact_page(request):
    print(request.POST)
    form = ContactForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        form = ContactForm()
    context = {
        'title': "Contact Page",
        'form': form
    }
    return render(request,'form.html',context)

def example_page(request):
    context     ={'title':'Example'}
    tempalte_name='helo_world.html'
    tempalte_obj = get_template(tempalte_name)
    render_item = tempalte_obj.render(context)
    return HttpResponse(render_item)
