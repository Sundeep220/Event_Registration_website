from django.forms import ModelForm
from .models import *


class SubmissionForm(ModelForm):
    class Meta:
        model = Submission
        fields = ['details']
