from eveuniverse.models.universe_1 import EveType
from eveuniverse.models.universe_2 import EveSolarSystem

from django.contrib import admin
from django.forms import ModelChoiceField

from allianceauth.services.hooks import get_extension_logger

from .models import (
    Agent, LocateChar, LocateCharMsg, Note, Target, TargetAlt, TargetGroup,
)

logger = get_extension_logger(__name__)

# Eve Category IDs
SHIP = 6


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ("character", "corporation", "division", "level")
    list_filter = ["corporation", "division", "level"]


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("target", "author", "created_at", "text")
    list_filter = ["target", "author"]


@admin.register(LocateChar)
class LocateCharAdmin(admin.ModelAdmin):
    list_display = ("character", "created_at", "cache_expiry")


@admin.register(LocateCharMsg)
class LocateCharMsgAdmin(admin.ModelAdmin):
    list_display = ("locate_character", "character", "timestamp")
    list_filter = ("locate_character", "character")


@admin.register(TargetAlt)
class TargetAltAdmin(admin.ModelAdmin):
    list_display = ("character", "hard_cyno", "beacon_cyno", "scout", "pilot")
    list_filter = ("hard_cyno", "beacon_cyno", "scout", "pilot")


@admin.register(Target)
class TargetAdmin(admin.ModelAdmin):
    list_display = ("character", "ship", "last_ship_location")

    def formfield_for_foreignkey(self, db_field, request, **kwargs) -> ModelChoiceField:
        # Only items that have market groups?
        if db_field.name == "ship":
            kwargs["queryset"] = EveType.objects.filter(
                eve_market_group__isnull=False, published=1, eve_group__eve_category=SHIP)
        if db_field.name == "last_ship_location":
            kwargs["queryset"] = EveSolarSystem.objects.filter(id__lt="31000000")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(TargetGroup)
class TargetGroupAdmin(admin.ModelAdmin):
    list_display = ('id', )
