from django.contrib.contenttypes.models import ContentType

from huscy.pseudonyms.services import get_or_create_pseudonym
# from huscy.recruitment.services.participation_requests import get_participation_requests
from huscy.subject_contact_history.models import ContactHistory, ContactHistoryItem


def get_contact_history(subject):
    content_type = ContentType.objects.get_by_natural_key('subject_contact_history',
                                                          'contacthistory')
    pseudonym = get_or_create_pseudonym(subject, content_type)

    contact_history, _created = ContactHistory.objects.get_or_create(pseudonym=pseudonym.code)
    return contact_history


def get_contact_history_items(participation_request):
    return (ContactHistoryItem.objects.filter(participation_request=participation_request)
                                      .order_by('created_at'))


"""
def get_contact_history_items_by_subject(subject, project=None):
    participation_requests = get_participation_requests(subject=subject)

    if project:
        participation_requests = participation_requests.filter(project=project)

    return (ContactHistoryItem.objects.filter(participation_request__in=participation_requests)
                                      .order_by('created_at'))
"""


def create_contact_history_item(participation_request, status=0):
    return ContactHistoryItem.objects.create(participation_request=participation_request,
                                             status=status)
