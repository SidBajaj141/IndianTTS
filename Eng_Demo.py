from google.cloud import texttospeech
import os
from docx import Document

# Set Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\SIDDHARTH\codes\tts\login.json"

# Define a mapping of characters to Google TTS male voices
character_voices = {
    "Guard": "en-US-Neural2-A",  # Male voice for Guard
    "Assassin": "en-US-Neural2-C",  # Male voice for Assassin (lower pitch)
    "Boss": "en-US-Neural2-D"  # Male voice for Boss (higher pitch)
}

# Define pitch and speaking_rate adjustment for characters
character_pitches = {
    "Assassin": -4.0,  # Decrease pitch for Assassin (negative for lower voice)
    "Guard": 0.0,  # Neutral pitch for Guard
    "Boss": 4.0   # Increase pitch for Boss (positive for higher voice)
}

character_speaking_rates = {
    "Assassin": 1.2,  # Slightly faster for Assassin (intense/urgent)
    "Guard": 1.0,  # Normal speaking rate for Guard
    "Boss": 0.9   # Slightly slower for Boss (commanding tone)
}

def synthesize_speech(text, voice_name, pitch, speaking_rate, output_file):
    """Convert text to speech using specified voice with adjusted pitch and speaking rate."""
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request with a specific voice
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=voice_name
    )

    # Adjust pitch and speaking rate for each character
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        pitch=pitch,  # Apply pitch adjustment
        speaking_rate=speaking_rate  # Apply speaking rate adjustment
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Save the audio file
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
        print(f"Audio content written to {output_file}")

def parse_script_from_docx(file_path):
    """Parse the script from a .docx file into a structured format."""
    script = []
    document = Document(file_path)
    for paragraph in document.paragraphs:
        if ":" in paragraph.text:
            character, dialogue = paragraph.text.split(":", 1)
            character = character.strip()
            dialogue = dialogue.strip()
            if character in character_voices:  # Ensure character has a defined voice
                script.append((character, character_voices[character], character_pitches.get(character, 0.0), character_speaking_rates.get(character, 1.0), dialogue))
            else:
                print(f"Warning: No voice defined for character '{character}'")
    return script

def create_audio_drama(docx_file, output_file="audio_drama.mp3"):
    """Generate an audio drama from a .docx file script."""
    script = parse_script_from_docx(docx_file)
    temp_files = []

    for i, (character, voice_name, pitch, speaking_rate, dialogue) in enumerate(script):
        temp_file = f"temp_{i}.mp3"
        print(f"Synthesizing for {character}...")
        
        # Now we synthesize only the dialogue, with adjusted pitch and speaking rate
        synthesize_speech(dialogue, voice_name, pitch, speaking_rate, temp_file)
        temp_files.append(temp_file)
    
    # Combine all temp audio files into one
    with open(output_file, "wb") as outfile:
        for temp_file in temp_files:
            with open(temp_file, "rb") as infile:
                outfile.write(infile.read())
            os.remove(temp_file)  # Clean up temporary files

    print(f"Audio drama saved as {output_file}")

# Example usage with demo.docx
create_audio_drama(r"C:/Users/SIDDHARTH/codes/tts/demo.docx")
