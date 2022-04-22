import csv
import io

from django.contrib import admin
from django import forms
from django.urls import path
from django.shortcuts import redirect, render
from django.db import IntegrityError

from .models import Topic

# Register your models here.

class CsvImportForm(forms.Form):
    csv_file = forms.FileField()

class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'keyword', 'case_sensitivity')

    change_list_template = "entities/topics_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            csv_file.seek(0)
            reader = csv.DictReader(io.StringIO(csv_file.read().decode('utf-8')))
            for row in reader:
                try:
                    t = Topic(name=row['name'], keyword=row['keyword'])
                    t.save()
                except IntegrityError:
                    pass
            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "admin/csv_form.html", payload
        )


admin.site.register(Topic, TopicAdmin)
