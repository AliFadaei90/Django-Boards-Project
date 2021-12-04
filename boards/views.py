from django.contrib.auth.models import User
from .forms import NewTopicForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import Board,Topic,Post

# Create your views here.

def home(request):
    boards=Board.objects.all()
    return render(request,'home.html',{'boards':boards}) 

def board_topics(request, number):
    board=get_object_or_404(Board, pk=number)
    return render(request,'topics.html' ,{'board':board}) 

def new_topic(request, number):
    board=get_object_or_404(Board, pk=number)
    user=User.objects.first()

    if request.method == "POST" :
        form=NewTopicForm(request.POST)
        if form.is_valid():
            topic=form.save(commit=False)
            topic.board=board
            topic.starter=user
            topic.save()

            post=Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user)

        return redirect ('board_topics' , number=board.pk)

    else:
        form=NewTopicForm()
        
    return render(request,'new_topic.html' ,{'board':board, 'form':form}) 

