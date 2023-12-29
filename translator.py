from flask import Flask, render_template, request, send_file
from googletrans import Translator
from gtts import gTTS
import io
import base64

app = Flask(__name__)

def translate_text(text, target_language='hi'):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text

def speak_text(text, lang='en'):
    tts = gTTS(text=text, lang=lang, slow=False)
    mp3_data = io.BytesIO()
    tts.write_to_fp(mp3_data)
    mp3_data.seek(0)
    return mp3_data

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_text = request.form['input_text']
        target_language = request.form['target_language']
        translated_text = translate_text(input_text, target_language)

        # Get in-memory MP3 file
        mp3_data = speak_text(translated_text, target_language)

        # Convert mp3_data to base64 for embedding in HTML
        mp3_base64 = base64.b64encode(mp3_data.read()).decode('utf-8')

        # Render the template with data
        return render_template('index.html', input_text=input_text, target_language=target_language, translated_text=translated_text, mp3_base64=mp3_base64)

    return render_template('index.html')

@app.route('/get_audio')
def get_audio():
    # Endpoint to serve the in-memory MP3 file
    mp3_data = request.args.get('mp3_data')
    return send_file(io.BytesIO(base64.b64decode(mp3_data)), mimetype='audio/mp3')

if __name__ == "__main__":
    app.run(debug=True)
