from django.views.generic import TemplateView


class IndexView(TemplateView):
    """Main page"""
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['turn_on_block'] = True
        context['content'] = 'Content of index page'
        context['title'] = 'Index page'
        context['user'] = getattr(self.request, 'user', 'Unknown')

        return context

