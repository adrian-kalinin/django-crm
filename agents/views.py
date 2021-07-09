from django.shortcuts import reverse
from django.views import generic
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
import random

from leads.models import Agent

from .mixins import OrganiserAndLoginRequiredMixin
from .forms import AgentModelForm


User = get_user_model()


class AgentListView(OrganiserAndLoginRequiredMixin, generic.ListView):
    template_name = 'agents/agent_list.html'
    context_object_name = 'agents'

    def get_queryset(self):
        return Agent.objects.filter(organisation=self.request.user.userprofile)


class AgentCreateView(OrganiserAndLoginRequiredMixin, generic.CreateView):
    template_name = 'agents/agent_create.html'
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse('agents:agent-list')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organiser = False
        user.set_password(f'{random.randint(0, 1000000)}')
        user.save()

        Agent.objects.create(
            user=user,
            organisation=self.request.user.userprofile
        )

        send_mail(
            subject='You are invited to be an agent',
            message='You were added as an agent on CRM. Please, come login to start working!',
            from_email='admin@example.com',
            recipient_list=[user.email]
        )

        return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(OrganiserAndLoginRequiredMixin, generic.DetailView):
    template_name = 'agents/agent_detail.html'
    context_object_name = 'agent'

    def get_queryset(self):
        return Agent.objects.filter(organisation=self.request.user.userprofile)


class AgentUpdateView(OrganiserAndLoginRequiredMixin, generic.UpdateView):
    template_name = 'agents/agent_update.html'
    form_class = AgentModelForm
    context_object_name = 'agent'

    def get_queryset(self):
        return User.objects.all()

    def get_success_url(self):
        return reverse('agents:agent-detail', kwargs={'pk': self.kwargs.get('pk')})


class AgentDeleteView(OrganiserAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'agents/agent_delete.html'

    def get_queryset(self):
        return Agent.objects.filter(organisation=self.request.user.userprofile)

    def get_success_url(self):
        return reverse('agents:agent-list')
