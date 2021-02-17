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
    export_as_csv.short_description = "Download selected rows"

    def download_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse
        meta = self.model._meta
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        writer.writerow(["id", "username", "email", "first_name", "last_name", "last_login", "date_joined" ,'is_superuser'])

        for s in queryset:
            writer.writerow([s.id, s.username, s.email, s.first_name, s.last_name, s.last_login, s.date_joined, s.is_superuser])

        return response
    download_csv.short_description = "Download selected rows"