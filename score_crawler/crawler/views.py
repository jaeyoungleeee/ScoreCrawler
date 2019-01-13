from django.db.models import Q
from django.http import Http404
from django.utils import timezone
from django.views.generic import TemplateView, DetailView

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
        if queryset is None:
            queryset = self.get_queryset()

        name = self.kwargs.get(self.slug_url_kwarg)
        queryset = queryset.filter(
            Q(github_username=name)|Q(boj_username=name)
        )

        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
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
