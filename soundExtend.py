from pydub import AudioSegment

# Load the audio file
audio = AudioSegment.from_file("Equalizer/sounds/mixed_animal_sounds.wav")  # Change to your file path

# Define the target duration (in milliseconds)
target_duration = 60000  # 1 minute, for example

# Calculate how many times we need to repeat
repeat_times = target_duration // len(audio) + 1

# Repeat the audio and trim to match the target duration
extended_audio = audio * repeat_times
extended_audio = extended_audio[:target_duration]  # Trim to exact duration

# Export the result as a .wav file
extended_audio.export("Equalizer/sounds/extended_audio.wav", format="wav")
