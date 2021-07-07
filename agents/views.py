from django.shortcuts import reverse
from django.views import generic

from leads.models import Agent

from .mixins import OrganiserAndLoginRequiredMixin
from .forms import AgentModelForm


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
        agent = form.save(commit=False)
        agent.organisation = self.request.user.userprofile
        agent.save()
        return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(OrganiserAndLoginRequiredMixin, generic.DetailView):
    template_name = 'agents/agent_detail.html'

    def get_queryset(self):
        return Agent.objects.filter(organisation=self.request.user.userprofile)


class AgentUpdateView(OrganiserAndLoginRequiredMixin, generic.UpdateView):
    template_name = 'agents/agent_update.html'
    form_class = AgentModelForm

    def get_queryset(self):
        return Agent.objects.filter(organisation=self.request.user.userprofile)

    def get_success_url(self):
        return reverse('agents:agent-list')


class AgentDeleteView(OrganiserAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'agents/agent_delete.html'

    def get_queryset(self):
        return Agent.objects.filter(organisation=self.request.user.userprofile)

    def get_success_url(self):
        return reverse('agents:agent-list')
