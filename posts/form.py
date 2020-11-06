from django import forms
from .models import UserPost
import os

class PostCreateForm(forms.Form):
    
    class Meta:
        model=UserPost
        fields=[
        'song',
        'cover',
        'songname' 
        ]

    def clean_song(self,*args,**kwargs):
        cleaned_data = super(PostCreateForm,self).clean()
        song = cleaned_data.get("song")
        if song._size>4*1024*1024:
            raise forms.ValidationError("Audio file too large ( > 4mb )")
        if not song.content-type in ["audio/mpeg","audio/wav"]:
            raise forms.ValidationError("Content-Type is not mpeg")
        if not os.path.splitext(song.name)[1] in [".mp3",".wav"]:
            raise forms.ValidationError("Doesn't have proper extension")
            
            return song
        else:
            raise forms.ValidationError("couldn't read file")
        # if '.mp3' not in song:
        #     raise forms.ValidationError("File must be .Mp3 or .wav type")
        # elif '.wav' not in song:
        #     raise forms.ValidationError("File must be .Mp3 or .wav type")
        # else:
        #     return songif file._size > 4*1024*1024:
    #     raise ValidationError("Audio file too large ( > 4mb )")
    # if not file.content-type in ["audio/mpeg","audio/wav"]:
    #     raise ValidationError("Content-Type is not mpeg")
    # if not os.path.splitext(file.name)[1] in [".mp3",".wav"]:
    #     raise ValidationError("Doesn't have proper extension")

    #     return file
    # else:
    #     raise ValidationError("Couldn't read uploaded file")