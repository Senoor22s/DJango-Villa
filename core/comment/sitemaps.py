from django.contrib import sitemaps
from django.urls import reverse

class CommentViewSitemap(sitemaps.Sitemap):
    priority= 0.5
    changefreq= "daily"

    def items(self):
        return ['comment:contact']
    
    def location(self,item):
        return reverse(item)