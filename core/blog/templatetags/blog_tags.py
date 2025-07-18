from django import template
from blog.models import Post, Category

register = template.Library()


@register.inclusion_tag("blog/blog-category.html")
def postcategories():
    posts = Post.objects.filter(status=1)
    categories = Category.objects.all()
    cat_dict = {}
    for name in categories:
        cat_dict[name] = posts.filter(category=name)
    return {"categories": cat_dict}
