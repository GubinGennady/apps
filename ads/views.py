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
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView, LogoutView
from .forms import RegistrationForm


# ============= Вьюхи для работы с объявлениями =============

class AdListView(ListView):
    """Показывает список всех объявлений с фильтрацией"""
    model = Ad
    template_name = 'ads/ad_list.html'
    context_object_name = 'ads'  # Имя переменной в шаблоне
    paginate_by = 9  # Пагинация по 9 элементов на странице

    def get_queryset(self):
        """Фильтрация объявлений по параметрам запроса"""
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')  # Поисковый запрос
        category = self.request.GET.get('category')  # Выбранная категория
        condition = self.request.GET.get('condition')  # Состояние товара

        # Фильтрация по поисковому запросу (заголовок или описание)
        if search_query:
            queryset = queryset.filter(
                models.Q(title__icontains=search_query) |
                models.Q(description__icontains=search_query)
            )

        # Фильтрация по категории
        if category:
            queryset = queryset.filter(category=category)

        # Фильтрация по состоянию
        if condition:
            queryset = queryset.filter(condition=condition)

        return queryset

    def get_context_data(self, **kwargs):
        """Добавляет в контекст список категорий для фильтра"""
        context = super().get_context_data(**kwargs)
        context['category_choices'] = Ad.CATEGORY_CHOICES
        return context


class HomeView(AdListView):
    """Главная страница с расширенным функционалом"""
    template_name = 'ads/main.html'

    def get_context_data(self, **kwargs):
        """Добавляет выбор состояния в контекст"""
        context = super().get_context_data(**kwargs)
        context['condition_choices'] = Ad.CONDITION_CHOICES
        return context


class AdDetailView(DetailView):
    """Детальное отображение объявления"""
    model = Ad
    template_name = 'ads/ad_detail.html'
    context_object_name = 'ad'

    def get_context_data(self, **kwargs):
        """Добавляет список объявлений пользователя для обмена"""
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Исключаем текущее объявление из списка
            context['user_ads'] = Ad.objects.filter(user=self.request.user).exclude(id=self.object.id)
        return context


class AdCreateView(LoginRequiredMixin, CreateView):
    """Создание нового объявления (только для авторизованных)"""
    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:ad-list')

    def form_valid(self, form):
        """Привязываем объявление к текущему пользователю"""
        form.instance.user = self.request.user
        messages.success(self.request, 'Объявление успешно создано!')
        return super().form_valid(form)


class AdUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирование объявления (только автор)"""
    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_form.html'
    context_object_name = 'ad'

    def test_func(self):
        """Проверка прав на редактирование"""
        ad = self.get_object()
        return ad.user == self.request.user

    def handle_no_permission(self):
        """Обработка отказа в доступе"""
        messages.error(self.request, 'Вы не можете редактировать это объявление!')
        return redirect('ad-list')

    def get_success_url(self):
        """Редирект после успешного обновления"""
        messages.success(self.request, 'Объявление успешно обновлено!')
        return reverse_lazy('ads:ad-detail', kwargs={'pk': self.object.pk})


class AdDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление объявления (только автор)"""
    model = Ad
    template_name = 'ads/ad_confirm_delete.html'
    success_url = reverse_lazy('ads:ad-list')

    def test_func(self):
        """Проверка прав на удаление"""
        ad = self.get_object()
        return ad.user == self.request.user

    def handle_no_permission(self):
        """Обработка отказа в доступе"""
        messages.error(self.request, 'Вы не можете удалить это объявление!')
        return redirect('ad-list')


# ============= Вьюхи для работы с предложениями обмена =============

class ProposalCreateView(LoginRequiredMixin, CreateView):
    """Создание предложения обмена"""
    model = ExchangeProposal
    form_class = ExchangeProposalForm
    template_name = 'ads/proposal_form.html'

    def get_success_url(self):
        """Редирект после создания предложения"""
        return reverse_lazy('ads:ad-detail', kwargs={'pk': self.ad_receiver.pk})

    def dispatch(self, request, *args, **kwargs):
        """Получаем объявление-получатель перед обработкой"""
        self.ad_receiver = get_object_or_404(Ad, pk=kwargs['receiver_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """Автоматически подставляем ad_receiver в форму"""
        kwargs = super().get_form_kwargs()
        kwargs['data'] = kwargs.get('data', {}).copy()
        kwargs['data']['ad_receiver'] = self.ad_receiver.id
        return kwargs

    def get_context_data(self, **kwargs):
        """Добавляем в контекст объявление-получатель"""
        context = super().get_context_data(**kwargs)
        context['ad_receiver'] = self.ad_receiver
        context['user_ads'] = Ad.objects.filter(
            user=self.request.user
        ).exclude(id=self.ad_receiver.id)
        return context

    def form_valid(self, form):
        """Валидация и сохранение предложения"""
        # Проверка принадлежности объявления отправителя
        # print(form.cleaned_data['ad_sender'].id)
        form.instance.ad_sender = get_object_or_404(
            Ad,
            id=form.cleaned_data['ad_sender'].id,
            user=self.request.user
        )
        form.instance.ad_receiver = self.ad_receiver
        form.instance.status = 'pending'  # Статус по умолчанию

        # Проверка на попытку обмена с самим собой
        if form.instance.ad_sender == form.instance.ad_receiver:
            form.add_error(None, "Нельзя предлагать обмен на то же объявление")
            return self.form_invalid(form)

        # Проверка существующего предложения
        if ExchangeProposal.objects.filter(
                ad_sender=form.instance.ad_sender,
                ad_receiver=form.instance.ad_receiver
        ).exists():
            form.add_error(None, "Вы уже отправляли это предложение")
            return self.form_invalid(form)

        messages.success(self.request, 'Предложение успешно отправлено!')
        return super().form_valid(form)


class ProposalUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Обновление статуса предложения (только получатель)"""
    model = ExchangeProposal
    fields = ['status']
    template_name = 'ads/proposal_update.html'

    def test_func(self):
        """Проверка прав на обновление (только получатель)"""
        proposal = self.get_object()
        return proposal.ad_receiver.user == self.request.user

    def form_valid(self, form):
        """Уведомление об успешном обновлении"""
        messages.success(self.request, 'Статус предложения обновлен!')
        return super().form_valid(form)

    def get_success_url(self):
        """Редирект на объявление получателя"""
        return reverse_lazy('ads:ad-detail', kwargs={'pk': self.object.ad_receiver.pk})


# ============= Аутентификация =============

class CustomLoginView(LoginView):
    """Кастомный вход с перенаправлением"""
    template_name = 'ads/registration/login.html'
    redirect_authenticated_user = True  # Автоперенаправление для авторизованных

    def get_success_url(self):
        """Редирект после входа"""
        return reverse_lazy('ads:ad-list')


def logout_user(request):
    """Выход из системы"""
    logout(request)
    return redirect('/')


class RegistrationView(CreateView):
    """Регистрация новых пользователей"""
    form_class = RegistrationForm
    template_name = 'ads/registration/register.html'
    success_url = reverse_lazy('ads:ad-list')

    def form_valid(self, form):
        """Автоматический вход после регистрации"""
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response
