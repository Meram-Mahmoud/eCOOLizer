from pydub import AudioSegment

# Load each animal sound
sound1 = AudioSegment.from_file("Equalizer/animal/birds.wav")
sound2 = AudioSegment.from_file("Equalizer/animal/cat.wav")
sound3 = AudioSegment.from_file("Equalizer/animal/grrrrr.wav")
sound4 = AudioSegment.from_file("Equalizer/animal/dogs.wav")


# # Adjust volume or apply effects if needed
# sound1 = sound1 + 5  # Increase volume of sound1 by 5 dB
# sound2 = sound2 - 2  # Decrease volume of sound2 by 2 dB

# Mix sounds by overlaying them
mixed_sound = sound1.overlay(sound2).overlay(sound3).overlay(sound4)

# Save the mixed sound
mixed_sound.export("mixed_animal_sounds.wav", format="wav")
