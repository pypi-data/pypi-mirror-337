from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from huscy.subject_contact_history.serializer import ContactHistorySerializer
from huscy.subject_contact_history.services import get_contact_history
from huscy.subjects.models import Subject


class ContactHistoryViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Subject.objects.all()
    serializer_class = ContactHistorySerializer

    def retrieve(self, request, pk=None):
        subject = self.get_object()
        contact_history = get_contact_history(subject)
        serializer = self.get_serializer(contact_history)
        return Response(serializer.data)
