from dataclasses import field
import select

from django import forms
from django.forms import widgets
from .models import Question, StudyMaterial, Subject

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
            "file": forms.ClearableFileInput(attrs={"class": "visually-hidden","accept": ".pdf,.docx","data-file-input":""}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        
        self.fields["subject"].queryset = Subject.objects.filter(user=user)
        
class QuestionForm(forms.ModelForm):
    class Meta:
        model=Question
        fields=['subject','material','question']
        
        widgets={
            "subject":forms.Select(attrs={
                "class":"form-select",
                "id":"subject"
            }),
            "material":forms.Select(attrs={
                "class":"form-select",
                "id":"document"
            }),
            "question":forms.Textarea(attrs={
                "class":"form-control",
                "id":"question",
                "rows":5,
                "maxlength":1000,
                "placeholder":"Find your answer here!!!",
            "data-question-input":"",
            "required":True
             }),
        }
    
    def __init__(self, *args, **kwargs):
        user=kwargs.pop("user")
        super().__init__(*args, **kwargs)
        
        self.fields["subject"].queryset=Subject.objects.filter(
            user=user
        )
        
        self.fields["material"].required=False
        self.fields["material"].queryset=StudyMaterial.objects.filter(user=user)
        self.fields["material"].empty_label="All study materials"
    
    def clean(self):
        cleaned_data=super().clean()
        
        subject=cleaned_data.get("subject")
        material=cleaned_data.get("material")
        
        if material and subject and material.subject_id != subject.id:
            self.add_error(
                "material",
                "please select a document to the belonging to this subject."
            )
        return cleaned_data
            