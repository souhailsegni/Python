# app.py

from flask import (                        # Import Flask classes/functions # type: ignore
    Flask,                                # Main Flask application class
    render_template,                      # To render HTML templates
    request,                              # To access incoming request data
    send_file,                            # To send files as HTTP responses
    jsonify                               # To return JSON error messages
)
import tts_engine                        # type: ignore # Import our TTS wrapper module
import os                                  # To remove temp files after use

app = Flask(__name__)                      # Create the Flask application instance

@app.route('/')                            # Route for the home page
def index():
    """
    Render the main page with voice options.
    """
    voices = tts_engine.list_voices()     # Get available voices from TTS engine
    return render_template('index.html', voices=voices)
                                           # Render index.html, passing voice list

@app.route('/speak', methods=['POST'])     # Route to handle speech synthesis
def speak():
    """
    Accept text + settings, synthesize to WAV, and stream back.
    """
    if request.is_json:                   # Check if client sent a JSON payload
        data = request.get_json()         # Parse JSON body into a dict
        text   = data.get('text', '').strip()   # Extract and trim text
        voice  = data.get('voice')              # Optional: voice ID
        rate   = data.get('rate')               # Optional: rate value
        volume = data.get('volume')             # Optional: volume value
    else:                                  # Fallback if not JSON
        text   = request.form.get('text', '').strip()
        voice  = request.form.get('voice')
        rate   = request.form.get('rate')
        volume = request.form.get('volume')

    if not text:                           # If no text provided
        return jsonify({'error': 'No text provided'}), 400
                                           # Return HTTP 400 with JSON error

    if voice:                              # If a voice was selected
        tts_engine.set_voice(voice)        # Apply that voice setting
    if rate:                               # If a rate was provided
        try:
            tts_engine.set_rate(int(rate))# Convert to int and apply
        except ValueError:
            pass                           # Ignore invalid rate
    if volume:                             # If a volume was provided
        try:
            tts_engine.set_volume(float(volume))
                                          # Convert to float and apply
        except ValueError:
            pass                           # Ignore invalid volume

    wav_path = tts_engine.save_to_file(text)
    # Synthesize the text to a temporary WAV file

    response = send_file(wav_path, mimetype='audio/wav')
    # Stream that WAV file back to the browser

    @response.call_on_close                # Register cleanup callback
    def _cleanup():
        try:
            os.remove(wav_path)           # Delete the temporary file
        except OSError:
            pass                          # Ignore if deletion fails

    return response                       # Return the streaming response

if __name__ == '__main__':               # Only run if this script is executed
    app.run(debug=True)                  # Start Flask dev server in debug mode
