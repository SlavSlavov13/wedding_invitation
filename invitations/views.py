from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Guest


def invitation_detail(request, slug):
	guest = get_object_or_404(Guest, slug=slug)

	if request.method == "POST":
		# Защита: Ако вече е отговорено веднъж, не позволяваме промяна
		if guest.is_attending is not None:
			messages.warning(request, "Вече сте изпратили своя отговор за тази покана.")
			return redirect("invitation_detail", slug=slug)

		attending = request.POST.get("is_attending") == "yes"
		count = request.POST.get("attending_count", 1)
		dietary = request.POST.get("dietary_notes", "").strip()
		music = request.POST.get("music_wish", "").strip()

		guest.is_attending = attending
		guest.attending_count = int(count) if attending else 0
		guest.dietary_notes = dietary
		guest.music_wish = music
		guest.save()

		messages.success(request, "Благодарим ви от сърце! Вашият отговор беше записан успешно.")
		return redirect("invitation_detail", slug=slug)

	return render(request, "invitations/invitation.html", {
		"guest": guest,
	})