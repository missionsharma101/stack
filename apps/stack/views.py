from django.http import JsonResponse
from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout


from django.contrib.auth.decorators import login_required


def get_signup(request):
    if request.method == "POST":
        form = UserForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Signup successfully")
            return redirect("stack:signin")

    else:
        form = UserForm()
    context = {'form': form}

    return render(request, "pages/signup.html", context)


def get_signin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Signin successfully")

                return redirect("/")
    else:
        form = AuthenticationForm()
    context={
        'form':form
    }    
    return render(request, "pages/signin.html",context)

def get_logout(request):
    logout(request)
    messages.success(request, "Logout successfully")
    return redirect("stack:signin")
    
@login_required(login_url="stack:signin")
def dashboard(request):
    enquires=Question.objects.order_by("-created_at")
    context={
        'enquires':enquires,
    }
    return render(request, "pages/index.html",context)

def get_question(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.created_by = request.user
            data.save()
            messages.success(request, "Question Added successfully")
            return redirect("/")
    else:
        form=QuestionForm()
    context={
        "form":form
    }         
    return render(request,"pages/question.html",context) 


def get_answer(request,pk):
    questions=Question.objects.get(id=pk)

    if request.method=="POST":
        form=AnswerForm(request.POST)
        form.is_valid()
        data=form.save(commit=False)
        data.created_by=request.user
        data.question=questions

        form.save()
        messages.success(request, "Answer Added successfully")
        return redirect('/')
    else:
        form=AnswerForm()
    context={
        "form":form,
        'questions':questions,

    }  
    return render(request,"pages/answer.html",context)

def get_reply(request,pk):
    answers=Answer.objects.get(id=pk)
    if request.method=="POST":
        form=ReplyForm(request.POST)
        form.is_valid()
        data=form.save(commit=False)
        data.created_by=request.user
        data.answer= answers
        form.save()
        messages.success(request, "Reply Added successfully")
        return redirect('/')
    else:
        form=AnswerForm()
    context={
        "form":form,
        'answers':answers
    }  
    return render(request,"pages/reply.html",context)



