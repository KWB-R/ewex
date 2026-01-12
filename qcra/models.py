from django.db import models

from hhea import SubstanceGroup, TreatmentGroup, Treatment, Reference, Substance, Matrix


class SubstanceModel(models.Model):
    CAS = models.CharField(max_length=16, primary_key=True)
    name = models.CharField(max_length=128)
    short_name = models.CharField(max_length=10)
    group = models.CharField(choices=SubstanceGroup.choices())

    @classmethod
    def from_domain(cls, substance):
        return SubstanceModel(
            CAS=substance.CAS,
            name=substance.name,
            group=substance.group.value,
            short_name=substance.id
        )

    def __str__(self):
        return f"{self.name} ({self.short_name})"


class MatrixModel(models.Model):
    id = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=128)

    @classmethod
    def from_domain(cls, matrix):
        return MatrixModel(
            id=matrix.id,
            name=matrix.name,
            description=matrix.description
        )

    def __str__(self):
        return f"{self.name} ({self.id})"


class TreatmentModel(models.Model):
    id = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=128)
    group = models.CharField(choices=TreatmentGroup.choices())
    input_matrix = models.ManyToManyField(to=MatrixModel, related_name="input_to_treatments")
    output_matrix = models.ForeignKey(MatrixModel, blank=True, null=True, on_delete=models.CASCADE)

    @classmethod
    def from_domain(cls, treatment: Treatment) -> tuple["TreatmentModel", list[MatrixModel]]:
        # return the model and the input_matrices separately because
        # django doesn't allow to have m2m fields populated on an unsaved model
        model = TreatmentModel(
            id=treatment.id,
            name=treatment.name,
            group=treatment.group.name,
            output_matrix=MatrixModel.objects.get(
                id=treatment.output_matrix.id) if treatment.output_matrix is not None else None
        )
        return model, [MatrixModel.objects.get(id=m.id) for m in treatment.input_matrix]

    def __str__(self):
        return f"{self.name} ({self.id})"


class ReferenceConcentrationModel(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False)
    substance = models.ForeignKey(SubstanceModel, blank=False, null=False, on_delete=models.CASCADE)
    matrix = models.ForeignKey(MatrixModel, blank=False, null=False, on_delete=models.CASCADE)
    value_ng_l = models.FloatField(blank=False, null=False)
    year = models.IntegerField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    @classmethod
    def from_domain(cls, reference: Reference, matrix: Matrix, substance: Substance):
        return ReferenceConcentrationModel(
            name=reference.id,
            value_ng_l=reference.ref_value_ng_l,
            year=reference.year,
            comments=reference.comments,
            substance_id=substance.CAS,
            matrix_id=matrix.id
        )

    def __str__(self):
        return self.name


class RemovalReferenceModel(models.Model):
    name = models.TextField(blank=False, null=False)
    substance = models.ForeignKey(to=SubstanceModel, blank=False, null=False, on_delete=models.CASCADE)
    treatment = models.ForeignKey(to=TreatmentModel, blank=False, null=False, on_delete=models.CASCADE)
    removal_percent = models.IntegerField(blank=False, null=False)
    DOI = models.CharField(max_length=64, blank=False, null=True)
    year = models.IntegerField(blank=False, null=True)
    figure = models.CharField(max_length=64, blank=False, null=True)

    @classmethod
    def from_tuple(cls, reference: tuple, substance: Substance, treatment: Treatment):
        return RemovalReferenceModel(
            name=reference.reference_id,
            substance_id=substance.CAS,
            treatment_id=treatment.id,
            removal_percent=reference.removal_percent,
            DOI=reference.DOI,
            year=reference.Year,
            figure=reference.table_graphic_no
        )
