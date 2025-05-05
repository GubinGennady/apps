from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Ad, ExchangeProposal
from .forms import AdForm, ExchangeProposalForm
from django.db import models
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from .forms import RegistrationForm


# views.py


class AdListView(ListView):
    model = Ad
    template_name = 'ads/ad_list.html'
    context_object_name = 'ads'
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        category = self.request.GET.get('category')
        condition = self.request.GET.get('condition')

        if search_query:
            queryset = queryset.filter(
                models.Q(title__icontains=search_query) |
                models.Q(description__icontains=search_query)
            )
        if category:
            queryset = queryset.filter(category=category)
        if condition:
            queryset = queryset.filter(condition=condition)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_choices'] = Ad.CATEGORY_CHOICES
        return context

class HomeView(AdListView):
    template_name = 'ads/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['condition_choices'] = Ad.CONDITION_CHOICES
        return context

class AdDetailView(DetailView):
    model = Ad
    template_name = 'ads/ad_detail.html'
    context_object_name = 'ad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_ads'] = Ad.objects.filter(user=self.request.user).exclude(id=self.object.id)
        return context


class AdCreateView(LoginRequiredMixin, CreateView):
    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:ad-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Объявление успешно создано!')
        return super().form_valid(form)


class AdUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_form.html'
    context_object_name = 'ad'

    def test_func(self):
        ad = self.get_object()
        return ad.user == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, 'Вы не можете редактировать это объявление!')
        return redirect('ad-list')

    def get_success_url(self):
        messages.success(self.request, 'Объявление успешно обновлено!')
        return reverse_lazy('ads:d-detail', kwargs={'pk': self.object.pk})


class AdDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ad
    template_name = 'ads/ad_confirm_delete.html'
    success_url = reverse_lazy('ads:ad-list')

    def test_func(self):
        ad = self.get_object()
        return ad.user == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, 'Вы не можете удалить это объявление!')
        return redirect('ad-list')


# views.py
class ProposalCreateView(LoginRequiredMixin, CreateView):
    model = ExchangeProposal
    form_class = ExchangeProposalForm
    template_name = 'ads/proposal_form.html'

    def get_success_url(self):
        return reverse_lazy('ads:ad-detail', kwargs={'pk': self.ad_receiver.pk})
    def dispatch(self, request, *args, **kwargs):
        self.ad_receiver = get_object_or_404(Ad, pk=kwargs['receiver_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['data'] = kwargs.get('data', {}).copy()
        kwargs['data']['ad_receiver'] = self.ad_receiver.id
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ad_receiver'] = self.ad_receiver
        context['user_ads'] = Ad.objects.filter(
            user=self.request.user
        ).exclude(id=self.ad_receiver.id)
        return context

    def form_valid(self, form):
        print(form.cleaned_data['ad_sender'].id)
        form.instance.ad_sender = get_object_or_404(
            Ad,
            id=form.cleaned_data['ad_sender'].id,
            user=self.request.user
        )
        form.instance.ad_receiver = self.ad_receiver
        form.instance.status = 'pending'

        if form.instance.ad_sender == form.instance.ad_receiver:
            form.add_error(None, "Нельзя предлагать обмен на то же объявление")
            return self.form_invalid(form)

        if ExchangeProposal.objects.filter(
            ad_sender=form.instance.ad_sender,
            ad_receiver=form.instance.ad_receiver
        ).exists():
            form.add_error(None, "Вы уже отправляли это предложение")
            return self.form_invalid(form)

        messages.success(self.request, 'Предложение успешно отправлено!')
        return super().form_valid(form)

class ProposalUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ExchangeProposal
    fields = ['status']
    template_name = 'ads/proposal_update.html'

    def test_func(self):
        proposal = self.get_object()
        return proposal.ad_receiver.user == self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Статус предложения обновлен!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('ads:ad-detail', kwargs={'pk': self.object.ad_receiver.pk})


class CustomLoginView(LoginView):
    template_name = 'ads/registration/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('ads:ad-list')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('ads:ad-list')


class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'ads/registration/register.html'
    success_url = reverse_lazy('ads:ad-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response
