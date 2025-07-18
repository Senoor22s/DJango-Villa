from django.views.generic.edit import FormView
from django.contrib import messages
from django.urls import reverse_lazy
from comment.forms import ContactForm
from django.contrib.auth.mixins import LoginRequiredMixin


class ContactPage(LoginRequiredMixin, FormView):
    template_name = "contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("comment:contact")

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Successfully submitted!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Form submission failed.")
        return super().form_invalid(form)
