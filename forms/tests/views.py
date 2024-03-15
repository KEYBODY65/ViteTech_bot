from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from .models import Test, Task, Results, Answer


@csrf_exempt
def form_view(request, form_id, *args, **kwargs):
    form = Test.objects.filter(id=form_id).first()
    if request.method == 'POST':
        name = request.POST.get('name', None)
        questions = dict()
        true_cnt = 0
        for x in list(dict(request.POST).items())[1:]:
            task = Task.objects.filter(id=x[0]).first()
            if not task:
                return render(request, 'form_not_found.html')
            questions[task.text] = x[1][0]
            if task.true_ans.text == x[1][0]:
                true_cnt += 1
        res = Results.objects.create(test=form, name=name, res=questions)
        res.save()
        return render(request, 'form_answer.html', {"true_cnt": true_cnt})
    if not form:
        return render(request, 'form_not_found.html')

    tasks = Task.objects.filter(test=form)
    data = {"tasks": [], "test": form}
    for task in tasks:
        task_d = {'title': task,
                  'choices': [x for x in task.choises.all()]}
        data["tasks"].append(task_d)

    return render(request, 'forms.html', data)


class CreateTest(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        data = request.data
        test = Test.objects.create(title=data.get('title'),
                                   description=data.get('description'))
        test.save()
        for task in data['tasks'].items():
            task = Task.objects.create(text=task[0],
                                       test=test)
            for ind, ans in enumerate(task[1]):
                answer = Answer.objects.create(text=ans)
                task.choises.add(answer)
                if ind == data['tasks']['true_ans']:
                    task.true_ans = answer
            task.save()
        return JsonResponse({"id": test.id}, status=200)


