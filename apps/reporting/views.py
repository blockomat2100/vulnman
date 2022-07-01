from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.db.models import Q
from django.urls import reverse_lazy
from vulnman.views import generic
from apps.reporting import models, forms
from apps.reporting import tasks


class ReportList(generic.ProjectListView):
    template_name = "reporting/report_list.html"
    context_object_name = "reports"

    def get_queryset(self):
        return models.Report.objects.filter(project=self.get_project())


class ReportCreate(generic.ProjectCreateView):
    template_name = "reporting/report_create.html"
    form_class = forms.ReportCreateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["project"] = self.get_project()
        return kwargs


class ReportDetail(generic.ProjectDetailView):
    template_name = "reporting/report_detail.html"
    model = models.Report

    def get_queryset(self):
        return models.Report.objects.filter(project=self.get_project())

    def get_context_data(self, **kwargs):
        kwargs["report_mgmt_summary_form"] = forms.ReportManagementSummaryForm(
            initial={
                "recommendation": self.get_object().recommendation,
                "evaluation": self.get_object().evaluation
            }
        )
        return super().get_context_data(**kwargs)


class ReportReleaseList(generic.ProjectListView):
    template_name = "reporting/report_releases.html"
    context_object_name = "releases"

    def get_context_data(self, **kwargs):
        kwargs["report"] = models.Report.objects.get(pk=self.kwargs.get("pk"), project=self.get_project())
        kwargs["wip_form"] = forms.ReportReleaseWIPForm()
        qs = models.ReportRelease.objects.filter(
            report__pk=self.kwargs.get("pk"), work_in_progress=True, report__project=self.get_project())
        if qs.exists():
            kwargs["wip_report"] = qs.get()
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return models.ReportRelease.objects.filter(report__pk=self.kwargs.get("pk"),
                                                   work_in_progress=False,
                                                   report__project=self.get_project())


class ReportReleaseDelete(generic.ProjectDeleteView):
    http_method_names = ["post"]

    def get_queryset(self):
        return models.ReportRelease.objects.filter(report__project=self.get_project())

    def get_success_url(self):
        return reverse_lazy("projects:reporting:report-release-list", kwargs={"pk": self.get_object().report.pk})


class ReportReleaseCreate(generic.ProjectCreateView):
    template_name = "reporting/report_create.html"
    form_class = forms.ReportReleaseForm

    def get_success_url(self):
        return reverse_lazy("projects:reporting:report-release-list", kwargs={"pk": self.kwargs.get("pk")})

    def get_report(self):
        try:
            obj = models.Report.objects.get(pk=self.kwargs.get("pk"), project=self.get_project())
        except models.Report.DoesNotExist:
            return Http404()
        return obj

    def get_queryset(self):
        return models.ReportRelease.objects.filter(report__pk=self.kwargs.get("pk"))

    def form_valid(self, form):
        form.instance.project = self.get_project()
        form.instance.report = self.get_report()
        form.instance.creator = self.request.user
        instance = form.save()
        task = tasks.do_create_report.delay(instance.pk)
        self.request.session["active_report_task"] = (task.task_id, str(instance.pk))
        return HttpResponseRedirect(self.get_success_url())


class ReportReleaseWIPCreate(generic.ProjectCreateView):
    template_name = "reporting/report_release_create.html"
    http_method_names = ["post"]
    form_class = forms.ReportReleaseWIPForm

    def get_success_url(self):
        return reverse_lazy("projects:reporting:report-release-list", kwargs={"pk": self.kwargs.get("pk")})

    def get_report(self):
        try:
            obj = models.Report.objects.get(pk=self.kwargs.get("pk"), project=self.get_project())
        except models.Report.DoesNotExist:
            return Http404()
        return obj

    def form_valid(self, form):
        qs = models.ReportRelease.objects.filter(report__pk=self.kwargs.get("pk"), project=self.get_project(),
                                                 work_in_progress=True)
        if qs.exists():
            qs.delete()
        form.instance.project = self.get_project()
        form.instance.report = self.get_report()
        form.instance.creator = self.request.user
        form.instance.name = "WIP"
        form.instance.release_type = models.ReportRelease.RELEASE_TYPE_DRAFT
        form.instance.work_in_progress = True
        instance = form.save()
        _task = tasks.do_create_report.delay(instance.pk)
        return super().form_valid(form)


class ReportReleaseUpdate(generic.ProjectUpdateView):
    template_name = "reporting/report_release_update.html"
    form_class = forms.ReportReleaseUpdateForm

    def get_queryset(self):
        return models.ReportRelease.objects.filter(pk=self.kwargs.get("pk"), project=self.get_project())

    def get_success_url(self):
        return reverse_lazy("projects:reporting:report-release-list")


class ReportReleaseDetail(generic.ProjectDetailView):
    context_object_name = "report"

    def get_queryset(self):
        return models.ReportRelease.objects.filter(project=self.get_project())

    def render_to_response(self, context, **response_kwargs):
        obj = self.get_object()
        response = HttpResponse(obj.compiled_source, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        return response


class ReportDelete(generic.ProjectDeleteView):
    http_method_names = ["post"]
    success_url = reverse_lazy("projects:reporting:report-list")

    def get_queryset(self):
        return models.Report.objects.filter(project=self.get_project())
