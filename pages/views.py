import logging

from django.urls import reverse_lazy

from django.views import generic

from .forms import InquiryForm, PagesCreateForm

from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Pages



logger = logging.getLogger(__name__)

class IndexView(generic.TemplateView):
    template_name='index.html'

class InquiryView(generic.FormView):
    template_name = "inquiry.html"
    form_class = InquiryForm
    success_url = reverse_lazy('pages:inquiry')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました。')
        logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)

class PagesListView(LoginRequiredMixin, generic.ListView):
    model = Pages
    template_name = 'pages_list.html'
    paginate_by = 2

    def get_queryset(self):
        pages = Pages.objects.filter(user=self.request.user).order_by('-created_at')
        return pages

class PagesDetailView(LoginRequiredMixin, generic.DetailView):
    model = Pages
    template_name = 'pages_detail.html'
    pk_url_kwarg = 'id'

class PagesCreateView(LoginRequiredMixin, generic.CreateView):
    model = Pages
    template_name = 'pages_create.html'
    form_class = PagesCreateForm
    success_url = reverse_lazy('pages:pages_list')

    def form_valid(self, form):
        pages = form.save(commit=False)
        pages.user = self.request.user
        pages.save()
        messages.success(self.request, "pagesを作成しました。")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request, "pagesの作成に失敗しました。")
        return super().form_invalid(form)

class PagesUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Pages
    template_name = 'pages.update.html'
    form_class = PagesCreateForm

    def get_success_url(self):
        return reverse_lazy('pages:pages_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        messages.error(self.request, 'ページの更新に失敗しました。')
        return super().form_invalid(form)

