from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from errand_matcher.models import User, Volunteer, Requestor, Partner
from errand_matcher.models import Errand
from errand_matcher.models import SiteConfiguration
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

admin.site.register(User, UserAdmin) 

@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('get_user_first_name', 'get_user_last_name',
        'get_user_email', 'mobile_number', 'lon', 'lat', 'frequency')
    actions = ["export_as_csv"]

    def get_user_first_name(self, obj):
        return obj.user.first_name

    def get_user_last_name(self, obj):
        return obj.user.last_name

    def get_user_email(self, obj):
        return obj.user.email

@admin.register(Requestor)
class RequestorAdmin(admin.ModelAdmin, ExportCsvMixin):
    actions = ["export_as_csv"]
    list_display = ('get_user_name', 'mobile_number', 'lon', 'lat')

    def get_user_name(self, obj):
        return '{} {}'.format(obj.user.first_name,
            obj.user.last_name)

admin.site.register(Partner)

@admin.register(Errand)
class ErrandAdmin(admin.ModelAdmin, ExportCsvMixin):
    actions = ["export_as_csv"]
    list_display = ('get_requestor_name', 'get_requestor_mobile_number', 
        'requested_time', 'status', 'due_by', 'request_round', 'claimed_time', 
        'get_claimed_volunteer_name', 'get_claimed_volunteer_mobile_number',
        'completed_time')

    def get_requestor_name(self, obj):
        return '{} {}'.format(obj.requestor.user.first_name,
            obj.requestor.user.last_name)

    def get_requestor_last_name(self, obj):
        return obj.requestor.user.last_name

    def get_requestor_mobile_number(self, obj):
        return obj.requestor.mobile_number

    def get_claimed_volunteer_name(self, obj):
        if obj.claimed_volunteer is not None:
            return '{} {}'.format(obj.claimed_volunteer.user.first_name,
                obj.claimed_volunteer.user.last_name)
        else:
            return None

    def get_claimed_volunteer_mobile_number(self, obj):
        if obj.claimed_volunteer is not None:
            return obj.claimed_volunteer.mobile_number
        else:
            return None
        

admin.site.register(SiteConfiguration)


