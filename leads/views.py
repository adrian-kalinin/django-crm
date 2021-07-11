from django.shortcuts import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from agents.mixins import OrganiserAndLoginRequiredMixin

from .models import Lead, Category
from .forms import (
    LeadModelForm, CustomUserCreationForm,
    AssignAgentForm, LeadCategoryUpdateForm,
    CategoryModelForm
)


class SignupView(generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse('login')


class LandingPageView(generic.TemplateView):
    template_name = 'landing.html'


class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = 'leads/lead_list.html'
    context_object_name = 'leads'

    def get_queryset(self):
        user = self.request.user

        if self.request.user.is_organiser:
            queryset = Lead.objects.filter(organisation=user.userprofile, agent__isnull=False)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation, agent__isnull=False)
            queryset = queryset.filter(agent__user=user)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_organiser:
            queryset = Lead.objects.filter(organisation=user.userprofile, agent__isnull=True)
            context.update({
                'unassigned_leads': queryset
            })

        return context


class LeadDetailView(OrganiserAndLoginRequiredMixin, generic.DetailView):
    template_name = 'leads/lead_detail.html'

    def get_queryset(self):
        return Lead.objects.filter(organisation=self.request.user.userprofile)


class LeadCreateView(OrganiserAndLoginRequiredMixin, generic.CreateView):
    template_name = 'leads/lead_create.html'
    form_class = LeadModelForm

    def form_valid(self, form):
        lead = form.save(commit=False)
        user = self.request.user

        if user.is_organiser:
            lead.organisation = user.userprofile
        else:
            lead.organisation = user.agent.organisation

        lead.save()

        return super(LeadCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('leads:lead-list')


class LeadUpdateView(OrganiserAndLoginRequiredMixin, generic.UpdateView):
    template_name = 'leads/lead_update.html'
    form_class = LeadModelForm

    def get_queryset(self):
        return Lead.objects.filter(organisation=self.request.user.userprofile)

    def get_success_url(self):
        return reverse('leads:lead-detail', kwargs={'pk': self.get_object().pk})


class LeadDeleteView(OrganiserAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'leads/lead_delete.html'

    def get_queryset(self):
        return Lead.objects.filter(organisation=self.request.user.userprofile)

    def get_success_url(self):
        return reverse('leads:lead-list')


class AssignAgentView(OrganiserAndLoginRequiredMixin, generic.FormView):
    template_name = 'leads/assign_agent.html'
    form_class = AssignAgentForm

    def get_form_kwargs(self):
        kwargs = super(AssignAgentView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        lead = Lead.objects.get(id=self.kwargs.get('pk'))
        lead.agent = form.cleaned_data.get('agent')
        lead.save()
        return super(AssignAgentView, self).form_valid(form)

    def get_success_url(self):
        return reverse('leads:lead-list')


class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = 'leads/category_list.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_organiser:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)

        context.update({
            'unassigned_lead_count': queryset.filter(category__isnull=True).count()
        })

        return context

    def get_queryset(self):
        user = self.request.user

        if user.is_organiser:
            return Category.objects.filter(organisation=user.userprofile)
        else:
            return Category.objects.filter(organisation=user.agent.organisation)


class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'leads/category_detail.html'

    def get_queryset(self):
        user = self.request.user

        if user.is_organiser:
            return Category.objects.filter(organisation=user.userprofile)
        else:
            return Category.objects.filter(organisation=user.agent.organisation)


class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'leads/category_update.html'
    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user

        if self.request.user.is_organiser:
            queryset = Lead.objects.filter(organisation=user.userprofile, agent__isnull=False)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation, agent__isnull=False)
            queryset = queryset.filter(agent__user=user)

        return queryset

    def get_success_url(self):
        return reverse('leads:lead-detail', kwargs={'pk': self.get_object().pk})


class CategoryCreateView(OrganiserAndLoginRequiredMixin, generic.CreateView):
    template_name = 'leads/category_create.html'
    form_class = CategoryModelForm
    
    def form_valid(self, form):
        category = form.save(commit=False)
        category.organisation = self.request.user.userprofile
        category.save()
        return super(CategoryCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('leads:category-list')


class CategoryUpdateView(OrganiserAndLoginRequiredMixin, generic.UpdateView):
    template_name = 'leads/category_update.html'
    form_class = CategoryModelForm

    def get_queryset(self):
        user = self.request.user

        if user.is_organiser:
            return Category.objects.filter(organisation=user.userprofile)
        else:
            return Category.objects.filter(organisation=user.agent.organisation)

    def get_success_url(self):
        return reverse('leads:category-list')


class CategoryDeleteView(OrganiserAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'leads/lead_delete.html'

    def get_queryset(self):
        user = self.request.user

        if user.is_organiser:
            return Category.objects.filter(organisation=user.userprofile)
        else:
            return Category.objects.filter(organisation=user.agent.organisation)

    def get_success_url(self):
        return reverse('leads:category-list')
