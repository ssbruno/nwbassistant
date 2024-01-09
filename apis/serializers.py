from rest_framework import serializers 
from apis.models import AssistantResponse

class AssistantResponseSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = AssistantResponse
        fields = ('text_rsp',
                  'audio_rsp')