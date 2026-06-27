from django import forms
from .models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = [
            "title",
            "course",
            "price",
            "preview_text",
            "description",
            "file",
            "status",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "e.g. A-Level Biology Complete Notes"}
            ),
            "price": forms.NumberInput(
                attrs={"min": "0.50", "max": "50.00", "step": "0.01"}
            ),
            "preview_text": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "A short preview visible to all users before purchase...",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Full description shown after purchase...",
                }
            ),
        }
