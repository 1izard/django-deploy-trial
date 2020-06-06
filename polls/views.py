from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse

from .models import Question, Choice


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def register(request):
    if request.method == "POST":
        question_text = request.POST['question_text']
        choice0_text = request.POST['choice0_text']
        choice1_text = request.POST['choice1_text']
        choice2_text = request.POST['choice2_text']
        print(question_text)
        question = Question.objects.create(
            question_text=question_text,
        )
        for text in (choice0_text, choice1_text, choice2_text):
            Choice.objects.create(
                question=question,
                choice_text=text
            )
        return HttpResponseRedirect(reverse('polls:register'))
    return render(request, 'polls/register.html')


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html',
                      {'question': question, 'error_message': "You didn't select a choice."})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
