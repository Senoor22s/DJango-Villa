from django.views.generic import ListView,TemplateView
from django.views.generic.detail import DetailView
from .models import Post
from comment.models import Comment
from comment.forms import CommentForm
from django.views.generic.edit import FormMixin
from django.urls import reverse
from django.shortcuts import redirect,get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from urllib.parse import urlencode
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

class PostListAPIView(TemplateView):
    template_name='blog/post_list_api.html'

@method_decorator(cache_page(60), name='dispatch')
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
    

class PostDetail(FormMixin, DetailView):
    model = Post
    template_name = "post_detail.html"
    context_object_name = "post"
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):

        obj = get_object_or_404(Post, pk=kwargs.get('pk'))
        if obj.login_require and not request.user.is_authenticated:
            current_url = request.get_full_path()
            login_url = f"{reverse('accounts:login')}?{urlencode({'next': current_url})}"
            return redirect(login_url)
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        obj.counted_view = obj.counted_view + 1
        obj.save(update_fields=["counted_view"])
        return obj

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
        messages.error(request, "Something went wrong")
        return self.form_invalid(form)

    def get_success_url(self):
        return reverse("blog:post-detail", kwargs={"pk": self.object.pk})