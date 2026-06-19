from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, render

from .forms import (
    CustomUserChangeForm,
    CustomUserCreationForm,
    ProfilePictureForm,
    UserSettingsForm,
)
from .models import UserSettings


## REGISTER ##
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Benutzer erfolgreich registriert!")
            return redirect("login")
        else:
            messages.error(request, "Bitte korrigiere die Fehler im Formular.")
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})


## DASHBOARD ##
@login_required
def dashboard(request):
    return render(request, "dashboard/dashboard.html")


def e404(request):
    return render(request, "e404.html")


## ADD FAMILY MEMBER ##
@login_required
def add_family_members(request):
    if request.method == "POST":
        username = request.POST.get("username")
        try:
            new_member = get_user_model().objects.get(username=username)
            request.user.family_members.add(new_member)
            messages.success(
                request, f"{new_member.username} wurde zur Familie hinzugefügt!"
            )
            return redirect("settings")
        except get_user_model().DoesNotExist:
            messages.error(request, "Benutzer nicht gefunden.")
            return render(
                request,
                "accounts/add_family_member.html",
                {"error": "Benutzer nicht gefunden."},
            )
    return render(request, "accounts/add_family_member.html")


## Settings ##
@login_required
def settings(request):
    user_settings, created = UserSettings.objects.get_or_create(user=request.user)
    family_members = request.user.family_members.all()

    settings_form = UserSettingsForm(instance=user_settings)
    password_form = PasswordChangeForm(request.user)
    user_form = CustomUserChangeForm(instance=request.user)
    profile_picture_form = ProfilePictureForm(instance=request.user)

    if request.method == "POST":
        if "change_design" in request.POST:
            settings_form = UserSettingsForm(request.POST, instance=user_settings)
            if settings_form.is_valid():
                settings_form.save()
                messages.success(request, "Design Einstellungen gespeichert!")
                return redirect("settings")
            else:
                messages.error(request, "Fehler im Design Formular.")

        elif "change_password" in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(
                    request, user
                )  # Verhindert, dass der Benutzer ausgeloggt wird
                messages.success(request, "Passwort erfolgreich geändert!")
                return redirect("settings")
            else:
                messages.error(request, "Fehler im Passwort Formular.")

        elif "change_username_email" in request.POST:
            user_form = CustomUserChangeForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, "Benutzername/Email erfolgreich geändert!")
                return redirect("settings")
            else:
                messages.error(request, "Fehler im Benutzername/Email Formular.")

        elif "change_profile_picture" in request.POST:
            profile_picture_form = ProfilePictureForm(
                request.POST, request.FILES, instance=request.user
            )
            if profile_picture_form.is_valid():
                profile_picture_form.save()
                messages.success(request, "Profilbild erfolgreich geändert!")
                return redirect("settings")
            else:
                messages.error(request, "Fehler im Profilbild Formular.")

        elif "clear_profile_picture" in request.POST:
            if request.user.profile_picture:
                request.user.profile_picture.delete(save=True)
                messages.success(request, "Profilbild entfernt.")
            return redirect("settings")

        elif "add_family_member" in request.POST:
            username = request.POST.get("family_username", "")
            try:
                new_member = get_user_model().objects.get(username=username)
                if new_member == request.user:
                    messages.error(request, "Du kannst dich nicht selbst hinzufügen.")
                else:
                    request.user.family_members.add(new_member)
                    messages.success(
                        request, f"{new_member.username} wurde zur Familie hinzugefügt!"
                    )
                return redirect("settings")
            except get_user_model().DoesNotExist:
                messages.error(request, "Benutzer nicht gefunden.")
                return redirect("settings")

    return render(
        request,
        "accounts/settings.html",
        {
            "settings_form": settings_form,
            "password_form": password_form,
            "user_form": user_form,
            "profile_picture_form": profile_picture_form,
            "family_members": family_members,
        },
    )


def beta_settings(request):
    return render(request, "accounts/beta_settings.html")
