from django.core.management.base import BaseCommand
from ewex.models import *
from qcra.models import SubstanceModel, MatrixModel, TreatmentModel, ReferenceConcentrationModel, RemovalReferenceModel
import pandas as pd


class Command(BaseCommand):

    def handle(self, *inputs, **kwargs):
        for name, attr in vars(Substances).items():
            if isinstance(attr, Substance):
                SubstanceModel.from_domain(attr).save()

        for name, attr in vars(Matrices).items():
            if isinstance(attr, Matrix):
                MatrixModel.from_domain(attr).save()

        for name, attr in vars(Treatments).items():
            if isinstance(attr, Treatment):
                treatment, input_matrices = TreatmentModel.from_domain(attr)
                treatment.save()
                for mat in input_matrices:
                    treatment.input_matrix.add(mat)

        references = pd.read_csv(
            os.path.join("data", "reference_lit.csv"),
            encoding='cp1252',
            sep=';',
            dtype={
                "substance_id": str,
                "matrix_id": str,
                "reference_value_ng_l": float,
                "reference_id": str,
                "year": pd.Int64Dtype(),
                "comments": str}
        )
        for ref in references.itertuples(index=False):
            r = Reference(
                id=ref.reference_id,
                ref_value_ng_l=ref.reference_value_ng_l,
                year=ref.year if not pd.isna(ref.year) else None,
                comments=ref.comments
            )
            s_attr = ("_" if ref.substance_id[0].isnumeric() else "") + ref.substance_id
            if hasattr(Substances, s_attr):
                s = getattr(Substances, s_attr)
                m = getattr(Matrices, ref.matrix_id)
                ReferenceConcentrationModel.from_domain(r, m, s).save()

        removals = pd.read_csv(
            os.path.join("data", "process_removal_lit.csv"),
            encoding='cp1252',
            sep=';',
            na_values="",
            keep_default_na=False,
            dtype={"removal_percent": float}
        )
        for ref in removals.itertuples(index=False):
            s_attr = ("_" if ref.substance_id[0].isnumeric() else "") + ref.substance_id
            if hasattr(Substances, s_attr) and hasattr(Treatments, ref.treatment_id):
                print(ref)
                s = getattr(Substances, s_attr)
                t = getattr(Treatments, ref.treatment_id)
                RemovalReferenceModel.from_tuple(ref, s, t).save()
