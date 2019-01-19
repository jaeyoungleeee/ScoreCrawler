from django.db.models import Q
from django.http import Http404
from django.utils import timezone
from django.views.generic import TemplateView, DetailView

import requests

from .models import Member, GitHubLog


class MainView(TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        names = []
        for m in Member.objects.all():
            if m.github_username:
                names.append(m.github_username)
            if m.boj_username:
                names.append(m.boj_username)

        context.update(
            {
                'names': names,
            }
        )
        return context


class MemberDetailView(DetailView):
    model = Member
    slug_url_kwarg = 'name'
    template_name = 'detail.html'

    def get_object(self, queryset=None):

        name = self.kwargs.get(self.slug_url_kwarg)
        queryset = self.get_queryset()

        if not queryset.filter(Q(github_username=name)|Q(boj_username=name)).exists():
            url = f'https://github.com/users/{name}/contributions'
            resp = requests.get(url)
            if resp.status_code == 404 :
                raise Http404(f"No {name} on github")
            else :
                Member.objects.create(github_username=name, boj_username=name)
                queryset = self.get_queryset() # 위에것과 중복인 것 같음... ㅋㅋ

        obj = queryset.get()

        return obj

    def get_context_data(self, **kwargs):
        context = super(MemberDetailView, self).get_context_data(**kwargs)
        context.update(
            {
                'github_week_data': self.get_github_weeK_data()
            }
        )
        return context

    def get_github_weeK_data(self):
        now = timezone.localtime()
        last_week = now - timezone.timedelta(days=6)
        logs = GitHubLog.objects.filter(date__gte=last_week, member=self.object)
        return [log.point for log in logs]


    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        member = self.object
        assert isinstance(member, Member)
        now = timezone.localtime()
        if not member.crawl_logs.filter(date__year=now.year, date__month=now.month, date__day=now.day).exists():
            member.process()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

