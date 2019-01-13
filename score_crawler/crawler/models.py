from django.db import models


class Member(models.Model):
    github_username = models.CharField(
        max_legth=40,
        blank=True,
        null=True
    )
    boj_username = models.CharField(
        max_legth=40,
        blank=True,
        null=True
    )


class GitHubLog(models.Model):
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name='github_logs'
    )
    date = models.DateField()


class BojLog(models.Model):
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name='boj_logs'
    )


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
            (2, '에러')
        )
    )
