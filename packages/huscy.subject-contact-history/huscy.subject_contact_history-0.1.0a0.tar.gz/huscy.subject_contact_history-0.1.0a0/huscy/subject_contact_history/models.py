from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from huscy.projects.models import Project


class Status(models.IntegerChoices):
    not_reached = 0, _('Not reached')
    recall = 1, _('Recall')
    invited = 2, _('Invited')


class ContactHistory(models.Model):
    pseudonym = models.CharField(primary_key=True, editable=False, max_length=64)


class ContactHistoryItem(models.Model):
    contact_history = models.ForeignKey(ContactHistory, on_delete=models.CASCADE,
                                        related_name='contact_history_items')
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)

    status = models.PositiveSmallIntegerField(choices=Status.choices,
                                              default=Status.not_reached,
                                              verbose_name=_('Status'))

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
