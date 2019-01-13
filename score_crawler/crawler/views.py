from django.views.generic import TemplateView, CreateView


class MainView(TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        pass
