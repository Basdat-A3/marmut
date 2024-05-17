from django import forms

class AddUserPlaylistForm(forms.Form):
    judul = forms.CharField(max_length=100, label='Judul')
    deskripsi = forms.CharField(max_length=500, label='Deskripsi', widget=forms.Textarea)

class EditUserPlaylistForm(forms.Form):
    judul = forms.CharField(label='Judul', max_length=100)
    deskripsi = forms.CharField(label='Deskripsi', widget=forms.Textarea)