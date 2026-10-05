import openpyxl
from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.html import format_html

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
		'open_status',
		'rsvp_status',
		'attending_count',
		'copy_link_action',
	)
	list_filter = ('is_attending', 'opened_at')
	search_fields = ('invitation_name', 'slug')

	def open_status(self, obj):
		if obj.opened_at:
			time_str = obj.opened_at.strftime("%d.%m %H:%M")
			return format_html('<span style="color: #2e7d32; font-weight: 600;">✓ Отворена ({})</span>', time_str)
		return format_html('<span style="color: #888;">Не е отворена</span>')
	open_status.short_description = "Статус на отваряне"

	def rsvp_status(self, obj):
		if obj.is_attending is True:
			return format_html('<span style="background: #e8f5e9; color: #2e7d32; padding: 3px 8px; border-radius: 12px; font-weight: 600;">Идва</span>')
		elif obj.is_attending is False:
			return format_html('<span style="background: #ffebee; color: #c62828; padding: 3px 8px; border-radius: 12px; font-weight: 600;">Отказва</span>')
		return format_html('<span style="color: #f57c00;">Очаква се</span>')
	rsvp_status.short_description = "RSVP"

	def copy_link_action(self, obj):
		relative_url = reverse('invitation_detail', args=[obj.slug])
		return format_html(
			'''
			<button type="button" 
					onclick="(function(btn, path) {{
						const fullUrl = window.location.origin + path;
						navigator.clipboard.writeText(fullUrl).then(() => {{
							const oldText = btn.innerText;
							btn.innerText = '✓ Копирано!';
							btn.style.background = '#2e7d32';
							setTimeout(() => {{
								btn.innerText = oldText;
								btn.style.background = '#541420';
							}}, 2000);
						}}).catch(() => prompt('Копирайте линка:', fullUrl));
					}})(this, '{url}')" 
					style="background: #541420; color: #fff; border: none; padding: 5px 12px; border-radius: 4px; cursor: pointer; font-size: 12px; font-weight: bold; transition: background 0.2s;">
				📋 Копирай линк
			</button>
			''',
			url=relative_url
		)
	copy_link_action.short_description = "Действие"