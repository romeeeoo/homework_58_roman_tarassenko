from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView

from todo_app.forms import TaskForm
from todo_app.models import Task


# Create your views here.
class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = Task.objects.all()
        return context


class AddTaskView(TemplateView):
    template_name = "add_new_task.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = TaskForm()
        context["form"] = form
        return self.render_to_response(context)


    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            return redirect("detailed_task", pk=task.pk)
        return render(request, "add_new_task.html", context={"form": form})




class TaskView(TemplateView):
    template_name = "detailed_task.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task"] = get_object_or_404(Task, pk=kwargs["pk"])
        print(context)
        return context


class UpdateTaskView(TemplateView):
    template_name = "update_task.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task"] = get_object_or_404(Task, pk=kwargs["pk"])
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = TaskForm(instance=context["task"])
        context["form"] = form
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs["pk"])
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            return redirect("detailed_task", pk=task.pk)
        return render(request, "add_new_task.html", context={"form": form})


class DeleteTaskView(TemplateView):
    template_name = "task_confirm_delete.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task"] = get_object_or_404(Task, pk=kwargs["pk"])
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class ConfirmDeleteView(TemplateView):
    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs["pk"])
        task.delete()
        return redirect('index')
