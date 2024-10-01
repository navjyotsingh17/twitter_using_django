from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from django.contrib import messages

# Create your views here.

def index(request):

    return render(request, "index.html")

@login_required
def tweet_list(request):

    tweets = Tweet.objects.all().order_by('-created_at')

    return render(request, 'tweet.html', {'tweets' : tweets,'page':'X / Home'})

@login_required
def tweet_create(request):

    if request.method == 'POST':
       
       form = TweetForm(request.POST, request.FILES)

       if form.is_valid():
           
           tweet = form.save(commit=False) 

           tweet.user = request.user

           tweet.save()

           return redirect('tweet_list')

    else:
        
        form = TweetForm()

    return render(request,'tweet_form.html',{'form':form,'page':'X / Post'})


@login_required
def tweet_edit(request, tweet_id):

    tweet= get_object_or_404(Tweet, pk = tweet_id, user = request.user)

    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)

        if form.is_valid():
           
           tweet = form.save(commit=False) 

           tweet.user = request.user

           tweet.save()

           return redirect('tweet_list')

    else:
        form = TweetForm(instance=tweet)

    return render(request,'tweet_form.html',{'form':form,'page':'X / Edit'})

@login_required
def tweet_delete(request, tweet_id):
    
    tweet= get_object_or_404(Tweet, pk = tweet_id, user = request.user)

    if request.method == 'POST':

        tweet.delete()

        return redirect('tweet_list')
    
    return render(request,'tweet_confirm_delete.html',{'tweet':tweet,'page':'X / Delete'})


def register(request):

    # if request.method == 'POST':
    #     form = UserRegistrationForm(request.POST)

    #     if form.is_valid():
            
    #         user = form.save(commit=False)
            
    #         user.set_password(form.cleaned_data['password1'])
            
    #         user.save()
            
            

    # else:
    #     form = UserRegistrationForm()

    # return render(request, "registration/register.html",{'form':form})

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        profile_photo = request.FILES.get("profile_photo")

        if User.objects.filter(username=username).exists():
            messages.error(request, f"Username {username} already taken!!!")
            return redirect("/register/")
        else:
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password
            )

            UserProfile.objects.create(
                user=user,
                profile_pic=profile_photo
            )

            print("Account created successfully!!!")
            login(request, user)
            return redirect('tweet_list')

    return render(request, "registration/register.html",{'page':'X / Sign up'})
