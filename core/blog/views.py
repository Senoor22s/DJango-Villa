from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .models import Post
from comment.models import Comment
from comment.forms import CommentForm
from django.views.generic.edit import FormMixin
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


class PostList(ListView):
    model = Post
    template_name = "post_list.html"
    context_object_name = "posts"
    paginate_by = 3

    def get_queryset(self):
        posts = Post.objects.filter(status=True)
        cat_name = self.kwargs.get("cat_name")
        if cat_name:
            posts = posts.filter(category__name=cat_name)
        return posts.order_by("-published_date")


class PostDetail(LoginRequiredMixin, FormMixin, DetailView):
    model = Post
    template_name = "post_detail.html"
    context_object_name = "post"
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = Comment.objects.filter(post=self.object, approved=True)
        context["form"] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.save()
            messages.success(request, "Submitted")
            return HttpResponseRedirect(self.get_success_url())
        messages.error(request, "Something went wrnog")
        return self.form_invalid(form)

    def get_success_url(self):
        return reverse("blog:post-detail", kwargs={"pk": self.object.pk})

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.counted_view = obj.counted_view + 1
        obj.save(update_fields=["counted_view"])
        return obj
