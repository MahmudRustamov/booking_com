from rest_framework import serializers
from apps.rooms.models import Room


class RoomDetailSerializer(serializers.ModelSerializer):
    media_files = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = '__all__'


    @staticmethod
    def get_media_files(obj):
        return [
            {
                "id": media.id,
                "file": media.file.url if media.file else None,
                "type": media.media_type
            }
            for media in obj.media_files.all()
        ]
