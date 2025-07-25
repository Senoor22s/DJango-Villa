from django.contrib.syndication.views import Feed
from blog.models import Post

class LatestEntriesFeed(Feed):
    title="blog newest ever"
    link="/rss/feed"
    description="best blog ever"

    def items(self):
        return Post.objects.filter(status=1)
    def item_title(self,item):
        return item.title
    def item_description(self,item):
        return item.content[:100]
    def item_link(self, item):
        return f"/blog/{item.pk}/"