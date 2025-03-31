from rest_framework import serializers

from huscy.subject_contact_history.models import ContactHistory, ContactHistoryItem


class ContactHistoryItemSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    creator_username = serializers.SerializerMethodField(source='get_creator_username')
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    project_title = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = ContactHistoryItem
        fields = (
            'contact_history',
            'created_at',
            'creator',
            'creator_username',
            'project',
            'project_title',
            'status',
            'status_display',
        )
        extra_kwargs = {
            'contact_history': {'write_only': True},
            'creator': {'write_only': True},
        }

    def get_creator_username(self, contact_history_item):
        return contact_history_item.creator.username

    def get_project_title(self, contact_history_item):
        project = contact_history_item.project
        return (project and project.title) or 'Deleted project'


class ContactHistorySerializer(serializers.ModelSerializer):
    contact_history_items = ContactHistoryItemSerializer(many=True, read_only=True)

    class Meta:
        model = ContactHistory
        fields = (
            'contact_history_items',
        )
