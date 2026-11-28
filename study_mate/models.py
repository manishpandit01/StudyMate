from asyncio import constants
from encodings.punycode import T
from pyexpat import model

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Subject(models.Model):
    SEMESTER_CHOICES = [("Winter", "Winter"), ("Summer", "Summer")]
    user=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subjects",
    )
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True)
    semester=models.CharField(max_length=30,
                              choices=SEMESTER_CHOICES,
                              default="Winter")
    created_at=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering=["-created_at"]
        constraints=[
            models.UniqueConstraint(fields=["user", "name"], 
                                    name="unique_subject_per_user")
        ]
    
    def __str__(self):
        return self.name
    
class StudyMaterial(models.Model):
    user=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="study_materials")
    
    subject=models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="study_materials")
    title=models.CharField(max_length=200)
    file=models.FileField(upload_to="study_materials/")
    uploaded_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
class Question(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,
                           related_name="questions")
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE,related_name="questions")
    material=models.ForeignKey(StudyMaterial,
                               on_delete=models.SET_NULL,
                               null=True,blank=True,related_name="questions")
    question=models.TextField()
    answer=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.question[:50]