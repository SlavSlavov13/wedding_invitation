import uuid
from django.db import models


def generate_short_code():
	return uuid.uuid4().hex[:8]


class Guest(models.Model):
	slug = models.CharField(
		max_length=12,
		unique=True,
		default=generate_short_code,
		verbose_name="Уникален код (линк)"
	)
	invitation_name = models.CharField(
		max_length=120,
		verbose_name="Име/Обръщение на поканата"
	)
	max_guests = models.PositiveIntegerField(
		default=2,
		verbose_name="Позволен брой места"
	)

	# RSVP статус
	is_attending = models.BooleanField(
		null=True,
		blank=True,
		verbose_name="Присъства ли"
	)
	attending_count = models.PositiveIntegerField(
		default=0,
		verbose_name="Потвърден брой гости"
	)
	dietary_notes = models.CharField(
		max_length=255,
		blank=True,
		null=True,
		verbose_name="Предпочитания за храна / Бележки"
	)
	music_wish = models.CharField(
		max_length=200,
		blank=True,
		null=True,
		verbose_name="Музикално желание"
	)
	updated_at = models.DateTimeField(
		auto_now=True,
		verbose_name="Последна промяна"
	)

	class Meta:
		verbose_name = "Гост"
		verbose_name_plural = "Гости"

	def __str__(self):
		return f"{self.invitation_name} ({self.slug})"