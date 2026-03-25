import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'legalencolombia-2026')

CONTACT_EMAIL = os.environ.get('CONTACT_EMAIL', 'pathy.higuera@gmail.com')
SMTP_HOST     = 'smtp.gmail.com'
SMTP_PORT     = 587
SMTP_USER     = 'heidimybot@gmail.com'
SMTP_PASS     = os.environ.get('SMTP_PASS', 'rdfsfbvwzbjahaia')

MATTER_LABELS = {
    'familia':  'Divorcio / Separación',
    'custodia': 'Custodia de hijos',
    'visa':     'Visa / Migración',
    'cuenta':   'Apertura cuenta bancaria',
    'empresa':  'Constitución de empresa',
    'contrato': 'Contratos / Documentos',
    'otro':     'Otro asunto',
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contacto', methods=['POST'])
def contacto():
    name    = request.form.get('name', '').strip()
    email   = request.form.get('email', '').strip()
    country = request.form.get('country', '').strip()
    phone   = request.form.get('phone', '').strip()
    matter  = request.form.get('matter', '')
    message = request.form.get('message', '').strip()

    if not name or not email:
        flash('Por favor complete nombre y correo / Please fill in name and email.', 'error')
        return redirect(url_for('index') + '#contacto')

    matter_label = MATTER_LABELS.get(matter, matter or 'No especificado')

    body = f"""Nueva consulta — Legal en Colombia

Nombre:   {name}
Email:    {email}
País:     {country or 'No indicado'}
Teléfono: {phone or 'No indicado'}
Asunto:   {matter_label}

Mensaje:
{message or '(sin mensaje)'}
"""

    try:
        msg = MIMEMultipart()
        msg['From']     = SMTP_USER
        msg['To']       = CONTACT_EMAIL
        msg['Subject']  = f'Legal en Colombia — Consulta de {name} ({matter_label})'
        msg['Reply-To'] = email
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, CONTACT_EMAIL, msg.as_string())

        flash('¡Gracias! Le responderé en menos de 24 horas. / Thank you! I\'ll respond within 24 hours.', 'success')
    except Exception as e:
        app.logger.error(f'Mail error: {e}')
        flash(f'Error: {e}', 'error')

    return redirect(url_for('index') + '#contacto')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
