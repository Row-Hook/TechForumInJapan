import logging

from django.urls import reverse_lazy

from django.views import generic

from .forms import InquiryForm, PagesCreateForm

from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.shortcuts import get_object_or_404

from .models import Pages

class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        #URLに埋め込まれた主キーからページデータを１件取得。取得できなかった場合は４０４エラー
        pages = get_object_or_404(Pages, pk=self.kwargs['pk'])
        #ログインユーザーとページの作成ユーザーを比較し、異なればraise_exceptionの設定に従う
        return self.request.user == pages.user

logger = logging.getLogger(__name__)

class IndexView(generic.TemplateView):
    template_name='index.html'

class InquiryView(generic.FormView):
    template_name = "inquiry.html"
    form_class = InquiryForm
    success_url = reverse_lazy('pages:inquiry')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'Your mail has been sent.')
        logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)

class PagesListView(LoginRequiredMixin, generic.ListView):
    model = Pages
    template_name = 'pages_list.html'
    paginate_by = 2

    def get_queryset(self):
        pages = Pages.objects.filter(user=self.request.user).order_by('-created_at')
        return pages

class PagesDetailView(LoginRequiredMixin, OnlyYouMixin, generic.DetailView):
    model = Pages
    template_name = 'pages_detail.html'

class PagesCreateView(LoginRequiredMixin, generic.CreateView):
    model = Pages
    template_name = 'pages_create.html'
    form_class = PagesCreateForm
    success_url = reverse_lazy('pages:pages_list')

    def form_valid(self, form):
        pages = form.save(commit=False)
        pages.user = self.request.user
        pages.save()
        messages.success(self.request, "You've successfully made a page!")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request, "Oops!  Something went wrong with your page.")
        return super().form_invalid(form)

class PagesUpdateView(LoginRequiredMixin, OnlyYouMixin, generic.UpdateView):
    model = Pages
    template_name = 'pages_update.html'
    form_class = PagesCreateForm

    def get_success_url(self):
        return reverse_lazy('pages:pages_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        messages.success(self.request, "Your page update was successful!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Sorry.  There was an error with your page update.")
        return super().form_invalid(form)

class PagesDeleteView(LoginRequiredMixin, OnlyYouMixin, generic.DeleteView):
    model = Pages
    template_name = 'pages_delete.html'
    success_url = reverse_lazy('pages:pages_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Your page was deleted.")
        return super().delete(request, *args,**kwargs)

