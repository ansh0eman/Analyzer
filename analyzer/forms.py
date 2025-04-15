from django import forms

class LyricsForm(forms.Form):
    song_name = forms.CharField(required=False, label="Song Name", max_length=200)
    artist_name = forms.CharField(required=False, label="Artist Name (optional)", max_length=200)
    lyrics_text = forms.CharField(widget=forms.Textarea, required=False, label="Lyrics or Poem Text")

    def clean(self):
        cleaned_data = super().clean()
        song = cleaned_data.get("song_name")
        lyrics = cleaned_data.get("lyrics_text")
        if not song and not lyrics:
            raise forms.ValidationError("Please enter a song name or paste lyrics.")
        return cleaned_data
