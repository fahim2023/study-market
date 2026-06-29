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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["file"].required = False

    def clean_file(self):
        file = self.cleaned_data.get("file")
        if file and hasattr(file, "size") and file.size > 10 * 1024 * 1024:
            raise forms.ValidationError(
                "File size must be under 10MB. Please compress your PDF and try again."
            )
        return file
