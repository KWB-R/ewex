from django.contrib import admin
from qcra.models import *


@admin.register(SubstanceModel)
class SubstanceAdmin(admin.ModelAdmin):
    list_display = ["name", "group", "CAS"]


@admin.register(MatrixModel)
class MatrixAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(TreatmentModel)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ["name", "group"]
    filter_horizontal = ["input_matrix"]


@admin.register(ReferenceConcentrationModel)
class ReferenceConcentrationAdmin(admin.ModelAdmin):
    list_display = ["name", "substance__name", "matrix__name", "value_ng_l", "year"]


@admin.register(RemovalReferenceModel)
class RemovalReferenceAdmin(admin.ModelAdmin):
    list_display = ["name", "substance__name", "treatment__name", "removal_percent", "DOI", "year"]