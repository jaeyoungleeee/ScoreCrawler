from django.db import models, transaction
from django.utils import timezone

import requests
import re

from .exceptions import CrawlingException

class GitHubLog(models.Model):
    member = models.ForeignKey(
        'crawler.Member',
        on_delete=models.CASCADE,
        related_name='github_logs'
    )
    date = models.DateField()
    point = models.PositiveIntegerField()


class BojLog(models.Model):
    member = models.ForeignKey(
        'crawler.Member',
        on_delete=models.CASCADE,
        related_name='boj_logs'
    )
    date = models.DateField()
    point = models.PositiveIntegerField()


class Member(models.Model):
    github_username = models.CharField(
        max_length=40,
        blank=True,
        null=True
    )
    boj_username = models.CharField(
        max_length=40,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.github_username

    def process(self):
        crawl_log = CrawlLog(member=self, status=1)
        try:
            self.git_crawl()
        except CrawlingException:
            crawl_log.status = 1
        crawl_log.save()

    @transaction.atomic()
    def git_crawl(self):
        url = f'https://github.com/users/{self.github_username}/contributions'
        resp = requests.get(url)
        if resp.status_code == 200:
            pattern = re.compile(
                r'<rect .+ data-count="(?P<point>\d+)" data-date="(?P<date>.*)"/>'
            )
            html = resp.text
            data = pattern.findall(html)

            git_hub_logs = []
            now = timezone.now()
            for point, date in data:
                if not GitHubLog.objects.filter(date=date, member=self).exists():
                    git_hub_logs.append(
                        GitHubLog(point=point, date=date, member=self)
                    )
                elif date == now.strftime('%Y-%m-%d'):
                    git_hub_log = GitHubLog.objects.get(
                        date=date, member=self
                    )
                    git_hub_log.point = point
                    git_hub_log.save()
            GitHubLog.objects.bulk_create(git_hub_logs)

        else:
            raise CrawlingException()





class CrawlLog(models.Model):
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name='crawl_logs'
    )
    date = models.DateTimeField(
        auto_now_add=True
    )
    status = models.IntegerField(
        choices=(
            (1, '성공'),
            (2, 'github-실패'),
            (3, 'boj-실패'),
            (4, '실패')
        )
    )
