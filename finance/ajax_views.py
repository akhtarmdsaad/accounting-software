from rest_framework import viewsets
from .models import RelatedFile
from .serializers import RelatedFileSerializer

class RelatedFileAJAXView(viewsets.ModelViewSet):
  serializer_class = RelatedFileSerializer
  queryset = RelatedFile.objects.all()