from django.views.generic import TemplateView, DetailView
from django.http import Http404

from .models import Member


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
            **{'github_username': name, 'boj_username': name}
        )

        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

    def get_context_data(self, **kwargs):
        context = super(MemberDetailView, self).get_context_data(**kwargs)
        return context
