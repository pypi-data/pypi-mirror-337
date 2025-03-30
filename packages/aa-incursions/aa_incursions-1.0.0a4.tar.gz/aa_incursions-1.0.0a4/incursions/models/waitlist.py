from corptools.models import EveItemType
from solo.models import SingletonModel

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from allianceauth.eveonline.models import (
    EveAllianceInfo, EveCharacter, EveCorporationInfo,
)

from incursions.providers import get_fleet_members, get_fleet_wings


class Role(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(null=True, blank=True)
    power = models.IntegerField(default=0, help_text="Bigger is better, user can assign a power level lower than this")

    class Meta:
        default_permissions = ()
        verbose_name = _("Waitlist - Role")
        verbose_name_plural = _("Waitlist - Roles")

    def __str__(self) -> str:
        return f"{self.name}"

    @property
    def member_count(self) -> int:
        return CharacterRoles.objects.filter(role=self).count()


class Announcement(models.Model):

    message = models.TextField()
    is_alert = models.BooleanField(default=False)
    pages = models.TextField(null=True, blank=True)  # DEPRECATE THIS

    created_by = models.ForeignKey(
        EveCharacter,
        on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    revoked_by = models.ForeignKey(
        EveCharacter,
        on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    revoked_at = models.DateTimeField(default=None, blank=True, null=True)

    class Meta:
        default_permissions = ()
        verbose_name = _("Waitlist - Announcement")
        verbose_name_plural = _("Waitlist - Announcements")

    def __str__(self) -> str:
        return f"Announcement #{self.pk}"


class Ban(models.Model):
    class entity_choices(models.TextChoices):
        CHARACTER = 'Character', _('Character')
        CORPORATION = 'Corporation', _('Corporation')
        ALLIANCE = 'Alliance', _('Alliance')

    entity_type = models.CharField(max_length=12, choices=entity_choices.choices, default=entity_choices.CHARACTER)
    entity_character = models.ForeignKey(
        EveCharacter,
        on_delete=models.CASCADE, null=True, blank=True, related_name='+')
    entity_corporation = models.ForeignKey(
        EveCorporationInfo,
        on_delete=models.CASCADE, null=True, blank=True, related_name='+')
    entity_alliance = models.ForeignKey(
        EveAllianceInfo,
        on_delete=models.CASCADE, null=True, blank=True, related_name='+')

    public_reason = models.CharField(max_length=512, null=True, blank=True)
    reason = models.CharField(max_length=512)

    issued_at = models.DateTimeField(auto_now_add=True)
    issued_by = models.ForeignKey(
        EveCharacter, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    revoked_at = models.DateTimeField(blank=True, null=True, default=None)
    revoked_by = models.ForeignKey(
        EveCharacter, on_delete=models.SET_NULL,null=True,blank=True, related_name='+')

    class Meta:
        default_permissions = ()
        verbose_name = _("Waitlist - Ban")
        verbose_name_plural = _("Waitlist - Bans")

    def __str__(self) -> str:
        return f"Ban #{self.pk} on {self.entity_type} {self.pk}"

    @property
    def entity_name(self) -> str:
        if self.entity_type == self.entity_choices.CHARACTER:
            return self.entity_character.character_name
        elif self.entity_type == self.entity_choices.CORPORATION:
            return self.entity_corporation.corporation_name
        elif self.entity_type == self.entity_choices.ALLIANCE:
            return self.entity_alliance.alliance_name
        return "Unknown Name"


class Badge(models.Model):
    name = models.CharField(max_length=64, unique=True)
    exclude_badge = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,null=True,blank=True,related_name='excluded_by')  # Mutually Exclusive Badges i think?

    class Meta:
        default_permissions = ()
        verbose_name = _("Waitlist - Badge")
        verbose_name_plural = _("Waitlist - Badges")

    def __str__(self) -> str:
        return f"{self.name}"

    @property
    def member_count(self) -> int:
        return CharacterBadges.objects.filter(badge=self).count()


class CharacterRoles(models.Model):
    character = models.OneToOneField(
        EveCharacter,
        on_delete=models.CASCADE, primary_key=True)
    role = models.ForeignKey(
        Role,
        verbose_name=_("Incursion Role"), on_delete=models.CASCADE, related_name='incursion_role')

    granted_at = models.DateTimeField(auto_now_add=True)
    granted_by = models.ForeignKey(
        EveCharacter,
        on_delete=models.SET_NULL, blank=True, null=True, related_name='+')

    class Meta:
        default_permissions = ()
        verbose_name = _("Waitlist - Character Role")
        verbose_name_plural = _("Waitlist - Character Roles")

    def __str__(self) -> str:
        return f"Role: {self.role} for {self.character}"


class CharacterBadges(models.Model):

    character = models.ForeignKey(
        EveCharacter,
        on_delete=models.CASCADE, related_name='+')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='+')

    granted_at = models.DateTimeField(auto_now_add=True)
    granted_by = models.ForeignKey(
        EveCharacter,
        on_delete=models.SET_NULL, blank=True, null=True, related_name='+')

    class Meta:
        default_permissions = ()
        verbose_name = _("Waitlist - Character Badge")
        verbose_name_plural = _("Waitlist - Character Badges")

    def __str__(self) -> str:
        return f"{self.character} has badge {self.badge}"


class CharacterNote(models.Model):

    character = models.ForeignKey(
        EveCharacter,
        on_delete=models.CASCADE,related_name='+')
    note = models.TextField()

    author = models.ForeignKey(
        EveCharacter,
        null=True, on_delete=models.SET_NULL, related_name='+')

    logged_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        default_permissions = ()
        verbose_name = _("Waitlist - Character Note")
        verbose_name_plural = _("Waitlist - Character Note")

    def __str__(self) -> str:
        return f"Note #{self.pk} for {self.character}"


class ApprovedImplantSet(models.Model):
    class set_choices(models.TextChoices):  # ARIEL This is not Dynamic on the Frontend, hence CHOICES
        AMULET = "Amulet", _("Amulet")
        ASCENDENCY = "Ascendency", _("Ascendency")
        NONE = "None", _("None")  # Helpful for just DPS hardwirings or something idk

    name = models.CharField(max_length=255)
    set = models.CharField(max_length=16, choices=set_choices.choices, default=set_choices.AMULET)
    implants = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = _("Waitlist - Approved Implant Set")
        verbose_name_plural = _("Waitlist - Approved Implant Sets")

    def __str__(self) -> str:
        return self.implants


class ApprovedFitting(models.Model):
    class tier_choices(models.TextChoices):  # ARIEL This is not Dynamic on the Frontend, hence CHOICES
        BASIC = "Basic", _("Sponge")
        MAINLINE = "Mainline", _("Mainline")
        ALT = "Alt", _("Alt")
        OTHER = "Other", _("Other")

    ship = models.ForeignKey(
        EveItemType,
        verbose_name=_("Ship"), on_delete=models.CASCADE, related_name='+')
    name = models.CharField(max_length=255)
    dna = models.TextField(max_length=1024, unique=True)
    tier = models.CharField(max_length=16, choices=tier_choices.choices, default=tier_choices.MAINLINE)
    description = models.CharField(max_length=255, null=True, blank=True)
    implants = models.ForeignKey(
        ApprovedImplantSet,
        on_delete=models.SET_NULL, related_name='+', null=True, blank=True)

    class Meta:
        verbose_name = _("Waitlist - Approved Fitting")
        verbose_name_plural = _("Waitlist - Approved Fittings")

    def __str__(self) -> str:
        return self.name

    def is_logi(self) -> bool:
        return WaitlistCategoryRule.objects.get(ship=self.ship).waitlist_category.name == "LOGI"  # ARIEL this is a hardcoded requirement by frontend, not sure i like it

    def implant_set(self) -> str:
        return self.implants.set if self.implants else "None"


class Fitting(models.Model):
    ship = models.ForeignKey(
        EveItemType,
        verbose_name=_("Ship"), on_delete=models.CASCADE, related_name='+')
    dna = models.TextField(max_length=1024, unique=True)

    class Meta:
        default_permissions = ()
        verbose_name = _("Waitlist - Waitlist Fit")
        verbose_name_plural = _("Waitlist - Waitlist Fits")

    def __str__(self) -> str:
        return f"Fitting {self.pk} (Hull: {self.ship})"


class ImplantSet(models.Model):
    implants = models.CharField(max_length=255, unique=True)

    class Meta:
        default_permissions = ()
        verbose_name = _("Waitlist - Waitlist Implant Set")
        verbose_name_plural = _("Waitlist - Waitlist Implant Sets")

    def __str__(self) -> str:
        return f"ImplantSet #{self.pk}: {self.implants}"


class FittingHistory(models.Model):
    character = models.ForeignKey(EveCharacter, on_delete=models.CASCADE, related_name='+')
    fit = models.ForeignKey(Fitting, on_delete=models.CASCADE, related_name='+')
    implant_set = models.ForeignKey(ImplantSet, on_delete=models.CASCADE, related_name='+')

    logged_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        default_permissions = ()
        verbose_name = _("Waitlist - Fitting History")
        verbose_name_plural = _("Waitlist - Fitting Histories")

    def __str__(self):
        return f"FitHistory #{self.pk} for {self.character}"


class SkillHistory(models.Model):
    # Faux this whole return, i really dont think i care about this
    character = models.ForeignKey(EveCharacter,on_delete=models.CASCADE, related_name='+')
    skill = models.ForeignKey(EveItemType, verbose_name=_("Skill"), on_delete=models.CASCADE, related_name='+')
    old_level = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    new_level = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    logged_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        default_permissions = ()
        verbose_name = _("Waitlist - Skill History")
        verbose_name_plural = _("Waitlist - Skill Histories")

    def __str__(self) -> str:
        return f"SkillHistory #{self.pk} for {self.character}"


class SkillCheck(models.Model):
    skill = models.ForeignKey(EveItemType, verbose_name=_("Skill"), on_delete=models.CASCADE, related_name='+')

    min = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=3)
    elite = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=4)
    gold = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=5)

    class Meta:
        default_permissions = ()
        verbose_name = _("Waitlist - Skill Check")
        verbose_name_plural = _("Waitlist - Skill Check")

    def __str__(self) -> str:
        return f"Skill: {self.skill} - Min: {self.min}, Elite: {self.elite}, Gold: {self.gold}"


class ApprovedSkills(models.Model):
    hull = models.OneToOneField(EveItemType, verbose_name=_("Hull"), on_delete=models.CASCADE, related_name='+')
    skill_checks = models.ManyToManyField(SkillCheck, verbose_name=_("Skill Checks"), related_name='+')

    class Meta:
        default_permissions = ()
        verbose_name = _("Waitlist - Approved Skills")
        verbose_name_plural = _("Waitlist - Approved Skills")

    def __str__(self) -> str:
        return f"Hull: {self.hull}"


class WaitlistCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        default_permissions = ()
        verbose_name = _("Waitlist - Category")
        verbose_name_plural = _("Waitlist - Categories")

    def __str__(self) -> str:
        return f"{self.name}"


class WaitlistCategoryRule(models.Model):

    waitlist_category = models.ForeignKey(
        WaitlistCategory, verbose_name=_("Waitlist Category"), on_delete=models.CASCADE, related_name='+')
    ship = models.OneToOneField(
        EveItemType, verbose_name=_("Ship"), on_delete=models.CASCADE, related_name='+')

    class Meta:
        default_permissions = ()
        verbose_name = _("Waitlist - Category Rule")
        verbose_name_plural = _("Waitlist - Category Rules")

    def __str__(self) -> str:
        return f"{self.waitlist_category} - {self.ship}"


class Fleet(models.Model):
    boss = models.ForeignKey(EveCharacter, on_delete=models.CASCADE, related_name='+')
    is_updating = models.BooleanField(default=False)

    class Meta:
        default_permissions = ()
        verbose_name = _("Waitlist - Fleet")
        verbose_name_plural = _("Waitlist - Fleets")

    def __str__(self) -> str:
        return f"Fleet #{self.pk}"

    def get_fleet_members(self):
        # /api/members/{character_id} uses me
        # But if i pass it through here I can dump some info to DB while im at it.
        fleet_members = get_fleet_members(self.boss.character_id, self.pk)
        for fleet_member in fleet_members:
            # Save or update fleet members in the DB
            pass
        return fleet_members

    def get_fleet_wings(self):
        # /api/members/{character_id} uses me
        # But if i pass it through here I can dump some info to DB while im at it.
        fleet_wings = get_fleet_wings(self.boss.character_id, self.pk)
        for wing in fleet_wings:
            # Save or update fleet Wings in the DB
            pass
        return fleet_wings


class ActiveFleet(SingletonModel):
    fleet = models.ForeignKey(Fleet, on_delete=models.CASCADE, related_name='+')

    class Meta:
        default_permissions = ()
        verbose_name = _("Waitlist - Fleet (Active)")
        verbose_name_plural = _("Waitlist - Fleet (Active)")

    def __str__(self) -> str:
        return f"Active Fleet {self.fleet}"


class FleetActivity(models.Model):
    character = models.ForeignKey(EveCharacter,on_delete=models.CASCADE, related_name='+')
    ship = models.ForeignKey(EveItemType, verbose_name=_("Ship"), on_delete=models.CASCADE, related_name='+')
    fleet = models.ForeignKey(
        Fleet, verbose_name=_(""), on_delete=models.CASCADE)

    first_seen = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)
    has_left = models.BooleanField(default=False)
    is_boss = models.BooleanField(default=False)

    class Meta:
        default_permissions = ()
        verbose_name = _("Waitlist - Fleet Activity")
        verbose_name_plural = _("Waitlist - Fleet Activities")

    def __str__(self) -> str:
        return f"FleetActivity #{self.pk} for {self.character}"


class FleetSquad(models.Model):
    """
    This is not explicitly a list of Squads in the Fleet
    This is a mapping of Squads to their configured Category a Character will be invited to
    """
    fleet = models.ForeignKey(Fleet, on_delete=models.CASCADE, related_name='+')
    category = models.ForeignKey(
        WaitlistCategory,
        verbose_name=_("Waitlist Category"), on_delete=models.CASCADE, related_name='+')
    wing_id = models.BigIntegerField()
    squad_id = models.BigIntegerField()

    class Meta:
        default_permissions = ()
        unique_together = (('fleet', 'category'),)
        verbose_name = _("Waitlist - Fleet Squad")
        verbose_name_plural = _("Waitlist - Fleet Squad")

    def __str__(self) -> str:
        return f"FleetSquad in Fleet {self.pk}, category {self.category}"

# The following Models are Specifically for the ACTIVE Waitlist, they are not historical
# They are used to manage the current state of the waitlist and its members


class Waitlist(SingletonModel):

    name = models.CharField(max_length=255, default="Waitlist")
    is_open = models.BooleanField(default=False)

    class Meta:
        default_permissions = ()
        verbose_name = _("Waitlist - Waitlist")
        verbose_name_plural = _("Waitlist - Waitlist")

    def __str__(self) -> str:
        return f"{self.name}"


class WaitlistEntry(models.Model):
    waitlist = models.ForeignKey(Waitlist, on_delete=models.CASCADE, related_name='+')
    main_character = models.ForeignKey(EveCharacter,on_delete=models.CASCADE, related_name='+')

    joined_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        default_permissions = ()
        verbose_name = _("Waitlist - Waitlist Entry")
        verbose_name_plural = _("Waitlist - Waitlist Entry")

    def __str__(self) -> str:
        return f"WaitlistEntry {self.main_character.character_name}"


class WaitlistEntryFit(models.Model):
    """
    WailistEntry - Fit
    An Entry can contain a series of fits for boxers
    """
    character = models.ForeignKey(EveCharacter,on_delete=models.CASCADE, related_name='+')
    waitlist_entry = models.ForeignKey(WaitlistEntry, on_delete=models.CASCADE, related_name='+')

    fit = models.ForeignKey(Fitting,on_delete=models.CASCADE, related_name='+')
    implant_set = models.ForeignKey(ImplantSet,on_delete=models.CASCADE, related_name='+')

    approved = models.BooleanField(default=False)
    tags = models.CharField(max_length=255,help_text="Comma Seperated List")
    category = models.ForeignKey(WaitlistCategory, verbose_name=_("Waitlist Category"), on_delete=models.CASCADE, related_name='+')
    fit_analysis = models.TextField(null=True, blank=True, help_text="[] apparently")
    review_comment = models.TextField(null=True, blank=True)
    is_alt = models.BooleanField(default=False)
    messagexup = models.TextField(null=True, blank=True)

    cached_time_in_fleet = models.BigIntegerField()  # Saved here to avoid repeated stats calls

    class Meta:
        default_permissions = ()
        verbose_name = _("Waitlist - Waitlist Entry Fit")
        verbose_name_plural = _("Waitlist - Waitlist Entry Fit")

    def __str__(self) -> str:
        return f"WaitlistEntry: {self.waitlist_entry.main_character.character_name} Fit: {self.character.character_name} - {self.fit.ship.name}"
