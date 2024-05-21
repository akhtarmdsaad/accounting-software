from rest_framework import serializers
from .models import RelatedFile
class RelatedFileSerializer(serializers.ModelSerializer):
  class Meta:
    model = RelatedFile
    fields = ('id', 'file')