from django import forms
from .models import StudyMaterial, Subject

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'description', 'semester',]
        
        widgets = {
            "name": forms.TextInput(attrs=
                                    {"class": "form-control",
                                    "placeholder": "e.g. Computer Networks"}),
            "description": forms.Textarea(attrs=
                                    {"class": "form-control",
                                     "placeholder": "Enter subject description here",
                                     "rows": 3}),
            "semester": forms.Select(attrs={"class": "form-select"}),
        }
    
    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if not name:
            raise forms.ValidationError("Subject nameis required.")
        return name
    
class StudyMaterialForm(forms.ModelForm):
    class Meta:
        model = StudyMaterial
        fields = ['subject', 'title', 'file']
        
        widgets = {
            "subject": forms.Select(attrs={"class": "form-select"}),
            "title": forms.TextInput(attrs=
                                    {"class": "form-control",
                                    "placeholder": "Enter document title"}),
            "file": forms.ClearableFileInput(attrs={"class": "visually-hidden","accept": "application/pdf"}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        
        self.fields["subject"].queryset = Subject.objects.filter(user=user)