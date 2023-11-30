from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View

from .models import Todo


class IndexView(LoginRequiredMixin, View):
    template_name = 'index.html'
    model = Todo
    
    def get(self, request):
        tasks = Todo.objects.all().order_by('-created_at')
        context = {
            'tasks': tasks,
        }
        return render(request, self.template_name, context)

