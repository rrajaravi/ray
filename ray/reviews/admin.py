import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import Review
# Register your models here.

actions = ["export_as_csv"]

class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


class ReviewAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('id', 'review_date', 'rating', 'topic_display', 'review_text', 'title')
    list_filter = ('topic', 'product', 'rating')
    ordering = ('-id',)
    search_fields = ('review_text', 'title', 'topic__name')
    actions = ["export_as_csv"]
    # readonly_fields = [] 
    # fields = ('product', ('rating', 'review_date'), 'title', 'review_text')

    def topic_display(self, obj):
        return ", ".join([
            topic.name for topic in obj.topic.all()
        ])
        
    topic_display.short_description = "Topic"


admin.site.register(Review, ReviewAdmin)