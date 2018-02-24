from django import forms

class NoticeForm(forms.Form):
    story_theme = forms.CharField(
            required=True,
            label="Story Theme",
            max_length=40,
            widget=forms.TextInput(
                attrs={ 
                    'placeholder': ''
                    }
                )
            )

    story_date = forms.DateField(
            required=True,
            label="Story Date/Time",
            widget=forms.TextInput(
                attrs={ 
                    'placeholder': 'Date'
                    }
                )
            )

    story_time = forms.TimeField(
            required=True,
            widget=forms.TextInput(
                attrs={ 
                    'placeholder': 'Time'
                    }
                )
            )

    story_venue = forms.CharField(
            required=True,
            label="Story Venue",
            max_length=50,
            widget=forms.TextInput(
                attrs={ 
                    'placeholder': ''
                    }
                )
            )

    story_address = forms.CharField(
            required=True,
            label="Story Address",
            max_length=50,
            widget=forms.TextInput(
                attrs={ 
                    'placeholder': ''
                    }
                )
            )

    story_host = forms.CharField(
            required=True,
            label="Story Host",
            max_length=10,
            widget=forms.TextInput(
                attrs={ 
                    'placeholder': ''
                    }
                )
            )

    story_size = forms.IntegerField(
            required=True,
            label="Story Size",
            min_value=1,
            max_value=50,
            widget=forms.TextInput(
                attrs={ 
                    'placeholder': ''
                    }
                )
            )


    reg_date = forms.DateField(
            required=True,
            label="Registration Date/Time",
            widget=forms.TextInput(
                attrs={ 
                    'placeholder': 'Reg Date'
                    }
                )
            )

    reg_time = forms.TimeField(
            required=True,
            label="Registration Time",
            widget=forms.TextInput(
                attrs={ 
                    'placeholder': 'Reg Time'
                    }
                )
            )
    story_activity_1 = forms.CharField(
            required=True,
            label="Story Activity 1",
            widget=forms.Textarea(
                attrs={ 
                    'rows': "2"
                    }
                )
            )

    story_activity_2 = forms.CharField(
            required=True,
            label="Story Activity 2",
            widget=forms.Textarea(
                attrs={ 
                    'rows': "2"
                    }
                )
            )

    story_activity_3 = forms.CharField(
            required=True,
            label="Story Activity 3",
            widget=forms.Textarea(
                attrs={ 
                    'rows': "2"
                    }
                )
            )

    story_activity_4 = forms.CharField(
            required=True,
            label="Story Activity 4",
            widget=forms.Textarea(
                attrs={ 
                    'rows': "2"
                    }
                )
            )

    story_activity_5 = forms.CharField(
            required=True,
            label="Story Activity 5",
            widget=forms.Textarea(
                attrs={ 
                    'rows': "2"
                    }
                )
            )


