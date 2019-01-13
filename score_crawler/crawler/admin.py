from django.contrib import admin
from .models import Member, GitHubLog, BojLog, CrawlLog


admin.site.register(Member)
admin.site.register(GitHubLog)
admin.site.register(BojLog)
admin.site.register(CrawlLog)
