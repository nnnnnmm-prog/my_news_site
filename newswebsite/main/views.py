from django.shortcuts import render, get_object_or_404 ,  redirect
from .models import News
from django.contrib.auth import login
from .forms import RegisterForm
from .forms import NewsForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
@login_required
def home (request):
    news_list = News.objects.all()
    for news in news_list:
        if news.created_at > timezone.now() - timezone.timedelta(hours=6):
            news.is_hot = True
        else:
            news.is_hot = False

    return render(request, 'main/home.html', {'news_list':news_list })
@login_required
def news_detail (request, pk):
    news = get_object_or_404(News , pk = pk )
    return render (request, 'main/news_detail.html', {'news':news })
@login_required
def news_create  (request):
    if request.method =="POST":
        form = NewsForm(request.POST)
        if form.is_valid ():
            form.save ()
            return redirect('home')
    else:
        form = NewsForm()
    return render(request, 'main/news_form.html', {'form':form})
@login_required
def news_update (request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.method == "POST":
        form = NewsForm (request.POST, instance= news )
        if form.is_valid ():
            form.save ()
            return redirect('news_detail' , pk=news.pk )
    else:
        form = NewsForm(instance=news )
        return render(request, 'main/news_form.html', {'form': form})
@login_required
def news_delete(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        news.delete()
        return redirect('home')
    return render(request, 'main/news_delete.html', {'news': news})
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})
