import openpyxl
from django.contrib import admin
from django.http import HttpResponse
from .models import Guest


@admin.action(description="Експорт на избраните в Excel")
def export_to_excel(modeladmin, request, queryset):
	workbook = openpyxl.Workbook()
	sheet = workbook.active
	sheet.title = "Списък гости"

	headers = [
		"Име", "Поканени места", "Ще присъства ли",
		"Потвърдени хора", "Храна/Бележки", "Песен", "Линк код"
	]
	sheet.append(headers)

	for guest in queryset:
		status = "Очаква се"
		if guest.is_attending is True:
			status = "Да"
		elif guest.is_attending is False:
			status = "Не"

		sheet.append([
			guest.invitation_name,
			guest.max_guests,
			status,
			guest.attending_count,
			guest.dietary_notes or "",
			guest.music_wish or "",
			guest.slug
		])

	response = HttpResponse(
		content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
	)
	response["Content-Disposition"] = 'attachment; filename="svatba_gosti.xlsx"'
	workbook.save(response)
	return response


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
	list_display = (
		'invitation_name',
		'max_guests',
		'is_attending',
		'attending_count',
		'slug',
		'updated_at'
	)
	list_filter = ('is_attending',)
	search_fields = ('invitation_name', 'slug')
	actions = [export_to_excel]