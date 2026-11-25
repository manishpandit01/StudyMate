from asyncio import constants

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Subject(models.Model):
    SEMESTER_CHOICES = [("winter", "Winter"), ("summer", "Summer")]
    user=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subjects",
    )
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True)
    semester=models.CharField(max_length=30,
                              choices=SEMESTER_CHOICES,
                              default="winter")
    created_at=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering=["-created_at"]
        constraints=[
            models.UniqueConstraint(fields=["user", "name"], 
                                    name="unique_subject_per_user")
        ]
    
    def __str__(self):
        return self.name