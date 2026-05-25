from flask import Flask, render_template, request, session
from ciphers import caesar, vigenere, affine, hill, playfair

app = Flask(__name__)
app.secret_key = "kunci_rahasia_simulasi_kripto_123"

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'history' not in session:
        session['history'] = []
        
    output = ""
    steps = []
    
    if request.method == 'POST':
        cipher_type = request.form.get('cipher_type')
        mode = request.form.get('mode') # encrypt / decrypt
        text = request.form.get('text', '')
        
        if cipher_type == 'caesar':
            key = int(request.form.get('caesar_key', 3))
            output, steps = caesar(text, mode, key)
            
        elif cipher_type == 'vigenere':
            key = request.form.get('vigenere_key', 'KEY')
            output, steps = vigenere(text, mode, key)
            
        elif cipher_type == 'affine':
            a = int(request.form.get('affine_a', 5))
            b = int(request.form.get('affine_b', 8))
            output, steps = affine(text, mode, a, b)
            
        elif cipher_type == 'hill':
            size = int(request.form.get('hill_size', 2))
            # Parsing flat matrix input (e.g. "4 3 2 1")
            matrix_raw = request.form.get('hill_matrix', '4 3 2 1')
            matrix_flat = [int(x) for x in matrix_raw.split()]
            output, steps = hill(text, mode, matrix_flat, size)
            
        elif cipher_type == 'playfair':
            key = request.form.get('playfair_key', 'KEYWORD')
            output, steps = playfair(text, mode, key)

        # Simpan ke Riwayat (Maksimal 5 riwayat terakhir)
        if output != "ERROR":
            history_list = session['history']
            history_list.insert(0, {
                'cipher': cipher_type.upper(),
                'mode': mode.upper(),
                'input': text,
                'output': output
            })
            session['history'] = history_list[:5]
            session.modified = True

    return render_template('index.html', output=output, steps=steps, history=session.get('history', []))

@app.route('/clear-history')
def clear_history():
    session['history'] = []
    return render_template('index.html', output="", steps=[], history=[])

if __name__ == '__main__':
    app.run(debug=True)