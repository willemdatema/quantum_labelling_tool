from django.contrib import admin

from webapp.models import *


# Register your models here.

class UserOrganizationAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserOrganization, UserOrganizationAdmin)


class OrganizationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Organization, OrganizationAdmin)


class CatalogueAdmin(admin.ModelAdmin):
    pass


admin.site.register(Catalogue, CatalogueAdmin)


class DatasetAdmin(admin.ModelAdmin):
    pass


admin.site.register(Dataset, DatasetAdmin)


class DQAssessmentAdmin(admin.ModelAdmin):
    pass


admin.site.register(DQAssessment, DQAssessmentAdmin)


class EHDSCategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(EHDSCategory, EHDSCategoryAdmin)


class DQDimensionAdmin(admin.ModelAdmin):
    pass


admin.site.register(DQDimension, DQDimensionAdmin)


class DQMetricAdmin(admin.ModelAdmin):
    pass


admin.site.register(DQMetric, DQMetricAdmin)


class DQCategoricalMetricAdmin(admin.ModelAdmin):
    pass


admin.site.register(DQCategoricalMetric, DQCategoricalMetricAdmin)


class DQCategoricalMetricCategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(DQCategoricalMetricCategory, DQCategoricalMetricCategoryAdmin)


class DQMetricValueAdmin(admin.ModelAdmin):
    pass


admin.site.register(DQMetricValue, DQMetricValueAdmin)


class MaturityDimensionValueAdmin(admin.ModelAdmin):
    pass


admin.site.register(MaturityDimensionValue, MaturityDimensionValueAdmin)


class MaturityDimensionAdmin(admin.ModelAdmin):
    pass


admin.site.register(MaturityDimension, MaturityDimensionAdmin)


class MaturityDimensionLevelAdmin(admin.ModelAdmin):
    pass


admin.site.register(MaturityDimensionLevel, MaturityDimensionLevelAdmin)
