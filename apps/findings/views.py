from django.http import HttpResponse
from django.urls import reverse_lazy
from vulnman.core.views import generics
from vulnman.views import generic
from apps.findings import models
from apps.findings import forms
from apps.reporting.tasks import export_single_vulnerability
from apps.assets.models import WebApplication, WebRequest, Host, Service


class TemplateList(generics.VulnmanAuthListView):
    model = models.Template
    paginate_by = 20
    template_name = "findings/template_list.html"
    context_object_name = "templates"


class VulnList(generic.ProjectListView):
    template_name = "findings/vulnerability_list.html"
    context_object_name = "vulns"
    model = models.Vulnerability


class VulnCreate(generic.ProjectCreateView):
    model = models.Vulnerability
    form_class = forms.VulnerabilityForm
    template_name = "findings/vulnerability_create.html"

    def form_valid(self, form):
        if not models.Template.objects.filter(vulnerability_id=form.cleaned_data["template_id"]).exists():
            form.add_error("template_id", "Template does not exist!")
            return super().form_invalid(form)
        form.instance.template = models.Template.objects.get(vulnerability_id=form.cleaned_data["template_id"])
        form.instance.severity = form.instance.template.severity
        if form.cleaned_data["asset_type"] == WebApplication.ASSET_TYPE:
            form.instance.asset_webapp = WebApplication.objects.get(project=self.get_project(), pk=form.cleaned_data["f_asset"])
        elif form.cleaned_data["asset_type"] == WebRequest.ASSET_TYPE:
            form.instance.asset_webrequest = WebRequest.objects.get(project=self.get_project(), pk=form.cleaned_data["f_asset"])
        elif form.cleaned_data["asset_type"] == Host.ASSET_TYPE:
            form.instance.asset_host = Host.objects.get(project=self.get_project(), pk=form.cleaned_data["f_asset"])
        elif form.cleaned_data["asset_type"] == Service.ASSET_TYPE:
            form.instance.asset_service = Service.objects.get(project=self.get_project(), pk=form.cleaned_data["f_asset"])
        else:
            form.add_error("asset_type", "invalid asset type")
            return super().form_invalid(form)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.get_project()
        return kwargs


class AddTextProof(generic.ProjectCreateView):
    http_method_names = ["post"]
    model = models.TextProof
    form_class = forms.TextProofForm

    def form_valid(self, form):
        vuln = self.get_project().vulnerability_set.filter(pk=self.kwargs.get('pk'))
        if not vuln.exists():
            form.add_error("name", "Vulnerability does not exist!")
            return super().form_invalid(form)
        form.instance.vulnerability = vuln.get()
        form.instance.project = self.get_project()
        self.success_url = vuln.get().get_absolute_url()
        return super().form_valid(form)


class TextProofUpdate(generic.ProjectUpdateView):
    template_name = "findings/proof_update.html"
    model = models.TextProof
    form_class = forms.TextProofForm

    def get_success_url(self):
        return reverse_lazy("projects:findings:vulnerability-detail", kwargs={"pk": self.get_object().vulnerability.pk})


class ImageProofUpdate(generic.ProjectUpdateView):
    template_name = "findings/proof_update.html"
    model = models.ImageProof
    form_class = forms.ImageProofForm

    def get_success_url(self):
        return reverse_lazy("projects:findings:vulnerability-detail", kwargs={"pk": self.get_object().vulnerability.pk})


class AddImageProof(generic.ProjectCreateView):
    http_method_names = ["post"]
    model = models.ImageProof
    form_class = forms.ImageProofForm

    def form_invalid(self, form):
        return super().form_invalid(form)

    def form_valid(self, form):
        vuln = self.get_project().vulnerability_set.filter(pk=self.kwargs.get('pk'))
        if not vuln.exists():
            form.add_error("name", "Vulnerability does not exist!")
            return super().form_invalid(form)
        form.instance.vulnerability = vuln.get()
        form.instance.project = self.get_project()
        self.success_url = vuln.get().get_absolute_url()
        return super().form_valid(form)


class VulnDetail(generic.ProjectDetailView):
    template_name = "findings/vuln_detail.html"
    context_object_name = "vuln"
    model = models.Vulnerability

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["text_proof_form"] = forms.TextProofForm()
        context["image_proof_form"] = forms.ImageProofForm()
        context["change_cvss_form"] = forms.VulnerabilityCVSSBaseForm(initial={
            "cvss_av": context["vuln"].cvss_av, "cvss_ac": context["vuln"].cvss_ac,
            "cvss_s": context["vuln"].cvss_s, "cvss_c": context["vuln"].cvss_c,
            "cvss_i": context["vuln"].cvss_i, "cvss_a": context["vuln"].cvss_a,
            "cvss_pr": context["vuln"].cvss_pr, "cvss_ui": context["vuln"].cvss_ui
        })
        return context


class VulnerabilityExport(generic.ProjectDetailView):
    model = models.Vulnerability

    def render_to_response(self, context, **response_kwargs):
        result = export_single_vulnerability(self.get_object())
        response = HttpResponse(result, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        return response


class VulnUpdate(generic.ProjectUpdateView):
    model = models.Vulnerability
    form_class = forms.VulnerabilityForm
    template_name = "findings/vulnerability_create.html"

    def form_valid(self, form):
        if not models.Template.objects.filter(vulnerability_id=form.cleaned_data["template_id"]).exists():
            form.add_error("template_id", "Template does not exist!")
            return super().form_invalid(form)
        form.instance.template = models.Template.objects.get(vulnerability_id=form.cleaned_data["template_id"])
        if not form.cleaned_data.get('severity'):
            form.instance.severity = form.instance.template.severity
        if form.cleaned_data["asset_type"] == WebApplication.ASSET_TYPE:
            form.instance.asset_webapp = WebApplication.objects.get(project=self.get_project(), pk=form.cleaned_data["f_asset"])
            form.instance.asset_host = None
            form.instance.asset_webrequest = None
        elif form.cleaned_data["asset_type"] == WebRequest.ASSET_TYPE:
            form.instance.asset_webrequest = WebRequest.objects.get(project=self.get_project(), pk=form.cleaned_data["f_asset"])
            form.instance.asset_webapp = None
            form.instance.asset_host = None
        elif form.cleaned_data["asset_type"] == Host.ASSET_TYPE:
            form.instance.asset_host = Host.objects.get(project=self.get_project(), pk=form.cleaned_data["f_asset"])
            form.instance.asset_webrequest = None
            form.instance.asset_webapp = None
        else:
            form.add_error("asset_type", "invalid asset type")
            return super().form_invalid(form)
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        initial["template_id"] = self.get_object().template.vulnerability_id
        initial["f_asset"] = (self.get_object().asset.pk, self.get_object().name)
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.get_project()
        return kwargs


class VulnDelete(generic.ProjectDeleteView):
    model = models.Vulnerability
    http_method_names = ["post"]
    allowed_project_roles = ["pentester"]

    def get_success_url(self):
        return reverse_lazy('projects:findings:vulnerability-list')

    def get_queryset(self):
        return models.Vulnerability.objects.filter(project=self.get_project())


class TextProofDelete(generic.ProjectDeleteView):
    model = models.TextProof
    http_method_names = ["post"]
    permission_required = ["projects.change_project"]

    def get_success_url(self):
        return reverse_lazy('projects:findings:vulnerability-list')

    def get_queryset(self):
        return models.TextProof.objects.filter(project=self.get_project())


class UserAccountList(generic.ProjectListView):
    model = models.UserAccount
    context_object_name = "user_accounts"
    template_name = "findings/user_account_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["account_create_form"] = forms.UserAccountForm()
        context["account_update_forms"] = []
        for qs in self.get_queryset():
            context["account_update_forms"].append(forms.UserAccountUpdateForm(instance=qs))
        return context


class UserAccountCreate(generic.ProjectCreateView):
    http_method_names = ["post"]
    model = models.UserAccount
    form_class = forms.UserAccountForm
    success_url = reverse_lazy("projects:findings:user-account-list")


class UserAccountUpdate(generic.ProjectUpdateView):
    http_method_names = ["post"]
    model = models.UserAccount
    form_class = forms.UserAccountUpdateForm
    success_url = reverse_lazy("projects:findings:user-account-list")


class UserAccountDelete(generic.ProjectDeleteView):
    model = models.UserAccount
    http_method_names = ["post"]
    permission_required = ["projects.change_project"]

    def get_success_url(self):
        return reverse_lazy('projects:findings:user-account-list')

    def get_queryset(self):
        return models.UserAccount.objects.filter(project=self.get_project())


class VulnerabilityCVSSUpdate(generic.ProjectUpdateView):
    model = models.Vulnerability
    form_class = forms.VulnerabilityCVSSBaseForm
    template_name = "findings/vuln_cvss_update.html"

    def get_queryset(self):
        return models.Vulnerability.objects.filter(project=self.get_project())


class ImageProofDelete(generic.ProjectDeleteView):
    model = models.ImageProof
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy('projects:findings:vulnerability-list')

    def get_queryset(self):
        return models.ImageProof.objects.filter(project=self.get_project())
