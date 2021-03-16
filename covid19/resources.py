from import_export import resources
from .models import Covid19


class Covid19Resource(resources.ModelResource):
    class Meta:
        model = Covid19
