import csv
import datetime
from django.http import HttpResponse


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    content_disposition = f"attachment; filename={opts.verbose_name}.csv"
    # Create the HttpResponse object with the appropriate CSV header.
    # tell the browser that the response has to be treated as a CSV file
    response = HttpResponse(content_type="text/csv")
    # indicate that the HTTP response contains an attached file.
    response["Content-Disposition"] = content_disposition
    # Create a CSV writer object that will write to the response object.
    writer = csv.writer(response)
    # Get the model fields dynamically using the get_fields() method of the model’s _meta
    fields = [
        field
        for field in opts.get_fields()
        if not field.many_to_many and not field.one_to_many
    ]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime("%d/%m/%Y")
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = "Export to CSV"
