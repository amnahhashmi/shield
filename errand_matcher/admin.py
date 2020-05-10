from django.contrib import admin
from errand_matcher.models import User, Volunteer, Requestor
from errand_matcher.models import ConfirmationToken
from errand_matcher.models import Errand
import csv
from django.http import HttpResponse

class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"

@admin.register(User)
class UserAdmin(admin.ModelAdmin, ExportCsvMixin):
	actions = ["export_as_csv"]

@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin, ExportCsvMixin):
	actions = ["export_as_csv"]

@admin.register(ConfirmationToken)
class ConfirmationTokenAdmin(admin.ModelAdmin, ExportCsvMixin):
    actions = ["export_as_csv"]

admin.site.register(Requestor)
admin.site.register(Errand)


