from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout

from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum


def get_signup(request):
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Signup successfully")
            return redirect("stack:signin")

    else:
        form = UserForm()
    context = {"form": form}

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
    context = {"form": form}
    return render(request, "pages/signin.html", context)


def get_logout(request):
    logout(request)
    messages.success(request, "Logout successfully")
    return redirect("stack:signin")


def dashboard(request):
    # import pdb ;pdb.set_trace()
    enquires = Question.objects.annotate(
        total_votes=Sum(F("upvote") + F("downvote"))).order_by("-total_votes")

    tag = request.GET.get("tag", None)
    search = request.GET.get("search-area", None)
    id_value = request.POST.get("question", None)

    if tag:
        enquires = Question.objects.filter(tag=tag)
    if search:
        enquires = Question.objects.filter(name__icontains=search)



    if 'Like' in request.POST:
        question_value = Question.objects.get(id=id_value)
        question_user_reaction = question_value.user_reaction.all()
        if 'Like' in request.POST and (request.user not in question_user_reaction):
            question_value.upvote += 1
            question_value.user_reaction.add(request.user)
            question_value.save()

    if "dislike" in request.POST:
        question_value = Question.objects.get(id=id_value)
        question_value.downvote += 1
        question_value.save()

    context = {
        "enquires": enquires,
    }
    return render(request, "pages/index.html", context)
@login_required(login_url="stack:signin")

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
        form = QuestionForm()
    context = {"form": form}
    return render(request, "pages/question.html", context)

@login_required(login_url="stack:signin")
def get_answer(request, pk):

    questions = Question.objects.get(id=pk)
    id_value = request.POST.get("answer", None)
    if "Like" in request.POST:
        question_value = Answer.objects.get(id=id_value)
        question_value.upvote += 1
        question_value.save()

    if "dislike" in request.POST:
        question_value = Answer.objects.get(id=id_value)
        question_value.downvote += 1
        question_value.save()

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.created_by = request.user
            data.question = questions
            form.save()
            messages.success(request, "Answer Added successfully")
            return redirect("stack:addanswer", pk=pk)
    else:
        form = AnswerForm()

    context = {
        "form": form,
        "questions": questions,
    }
    return render(request, "pages/answer.html", context)

@login_required(login_url="stack:signin")
def get_reply(request, pk):
    answers = Answer.objects.get(id=pk)

    if request.method == "POST":
        form = ReplyForm(request.POST)
        form.is_valid()
        data = form.save(commit=False)
        data.created_by = request.user
        data.answer = answers
        form.save()
        messages.success(request, "Reply Added successfully")
        return redirect("stack:reply", pk=pk )

    else:
        form = AnswerForm()
    context = {"form": form, "answers": answers}
    return render(request, "pages/reply.html", context)

@login_required(login_url="stack:signin")
def profile(request, pk):
    get_question = Question.objects.filter(created_by__id=pk)
    if request.method == "POST":
        get_user = User.objects.get(id=pk)
        form = UserUpdateForm(request.POST, request.FILES, instance=get_user)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer update successfully")
            return redirect("stack:userprofile", pk=pk)
    else:
        get_user = User.objects.get(id=pk)
        form = UserUpdateForm(instance=get_user)

    context = {
        "get_user": get_user,
        "form": form,
        "get_question": get_question
    }

    return render(request, "pages/userprofil.html", context)

@login_required(login_url="stack:signin")
def delete_question(request, pk):
    delete_user = Question.objects.filter(id=pk)
    delete_user.delete()
    messages.success(request, "Question Delete")
    return redirect("stack:userprofile", pk=pk)

@login_required(login_url="stack:signin")
def question_update(request, pk):
    if request.method == "POST":
        update_question = Question.objects.get(id=pk)
        form = QuestionUpdateForm(request.POST, instance=update_question)
        if form.is_valid():
            form.save()
            messages.success(request, "Question update successfully")
            return redirect("stack:question-update", pk=pk)
    else:
        update_question = Question.objects.get(id=pk)
        form = QuestionUpdateForm(instance=update_question)

        context = {
            "form": form,
        }
    return render(request, "pages/questionupdate.html", context)
