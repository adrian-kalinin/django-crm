from django.shortcuts import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from agents.mixins import OrganiserAndLoginRequiredMixin

from .models import Lead
from .forms import LeadModelForm, CustomUserCreationForm


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
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            queryset = queryset.filter(agent__user=user)

        return queryset


class LeadDetailView(OrganiserAndLoginRequiredMixin, generic.DetailView):
    template_name = 'leads/lead_detail.html'

    def get_queryset(self):
        return Lead.objects.filter(organisation=self.request.user.userprofile)


class LeadCreateView(OrganiserAndLoginRequiredMixin, generic.CreateView):
    template_name = 'leads/lead_create.html'
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse('leads:lead-list')


class LeadUpdateView(OrganiserAndLoginRequiredMixin, generic.UpdateView):
    template_name = 'leads/lead_update.html'
    form_class = LeadModelForm

    def get_queryset(self):
        return Lead.objects.filter(organisation=self.request.user.userprofile)

    def get_success_url(self):
        return reverse('leads:lead-list')


class LeadDeleteView(OrganiserAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'leads/lead_delete.html'

    def get_queryset(self):
        return Lead.objects.filter(organisation=self.request.user.userprofile)

    def get_success_url(self):
        return reverse('leads:lead-list')
