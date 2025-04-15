from django.shortcuts import render
from .forms import LyricsForm
import requests
from .fractal_generator import generate_fractal_from_text


def home(request):
    fractal_image = None
    error_msg = None

    if request.method == "POST":
        form = LyricsForm(request.POST)
        if form.is_valid():
            song_name = form.cleaned_data.get("song_name")
            artist_name = form.cleaned_data.get("artist_name")
            lyrics = form.cleaned_data.get("lyrics_text")

            if not lyrics:
                # Fetch lyrics from API
                try:
                    artist = artist_name or "Unknown"
                    response = requests.get(f"https://api.lyrics.ovh/v1/{artist}/{song_name}")
                    data = response.json()
                    lyrics = data.get("lyrics", "")
                    if not lyrics:
                        error_msg = "Lyrics not found. Try entering them manually."
                except Exception as e:
                    error_msg = f"Error fetching lyrics: {str(e)}"

            if lyrics:
                # ✅ This is where we'll add fractal generation next
                print("Using these lyrics for analysis:\n", lyrics[:300])
                fractal_image = generate_fractal_from_text(lyrics)
    else:
        form = LyricsForm()

    return render(request, 'analyzer/home.html', {
        'form': form,
        'fractal_image': fractal_image,
        'error_msg': error_msg
    })

