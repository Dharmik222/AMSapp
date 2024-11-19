from django import forms
from .models import Alumni

class AlumniForm(forms.ModelForm):
    class Meta:
        model = Alumni
        fields = [
            'full_name', 
            'university_affiliation', 
            'date_of_death', 
            'obituary_url', 
            'family_info', 
            'funeral_details', 
            'notable_info'
        ]

        labels = {
            'full_name': 'Full Name',
            'university_affiliation': 'University Affiliation (e.g., University of Windsor, Degree, Graduation Year)',
            'date_of_death': 'Date of Death',
            'obituary_url': 'Obituary URL',
            'family_info': 'Family or Survivor Information',
            'funeral_details': 'Funeral or Memorial Details',
            'notable_info': 'Other Notable Information',
        }

        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'e.g., John Doe'}),
            'university_affiliation': forms.Textarea(attrs={'placeholder': 'e.g., University of Windsor, B.Sc., 2010', 'rows': 3}),
            'date_of_death': forms.DateInput(attrs={'type': 'date'}),
            'obituary_url': forms.URLInput(attrs={'placeholder': 'e.g., https://example.com/obituary'}),
            'family_info': forms.Textarea(attrs={'placeholder': 'e.g., Spouse, Children, etc.', 'rows': 3}),
            'funeral_details': forms.Textarea(attrs={'placeholder': 'e.g., Service details, dates, locations', 'rows': 3}),
            'notable_info': forms.Textarea(attrs={'placeholder': 'e.g., Alumni accomplishments, affiliations, etc.', 'rows': 3}),
        }