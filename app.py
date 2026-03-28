import os
import smtplib
import threading
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

def send_email(subject, body, reply_to):
    try:
        msg = MIMEMultipart()
        msg['From']     = SMTP_USER
        msg['To']       = CONTACT_EMAIL
        msg['Subject']  = subject
        msg['Reply-To'] = reply_to
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, CONTACT_EMAIL, msg.as_string())
        app.logger.info('Mail sent OK')
    except Exception as e:
        app.logger.error(f'Mail error: {e}')

BLOG_POSTS = {
    'divorcio-colombia-sin-viajar': {
        'slug': 'divorcio-colombia-sin-viajar',
        'date': '2026-03-28',
        'date_display': {'es': '28 de marzo de 2026', 'en': 'March 28, 2026'},
        'title': {
            'es': 'Divorcio en Colombia sin viajar: guía para extranjeros casados con colombianos',
            'en': 'Divorce in Colombia Without Traveling: Guide for Foreigners Married to Colombians',
        },
        'meta_description': {
            'es': '¿Puedes divorciarte en Colombia sin viajar? Sí. Descubre cómo extranjeros casados con colombianos pueden tramitar su divorcio 100% a distancia, de forma legal y ágil.',
            'en': 'Can you get divorced in Colombia without traveling? Yes. Learn how foreigners married to Colombians can process their divorce 100% remotely, legally and efficiently.',
        },
        'excerpt': {
            'es': '¿Tienes que viajar a Colombia para divorciarte? La respuesta es no. Te explicamos cómo funciona el proceso a distancia.',
            'en': 'Do you need to travel to Colombia to get divorced? The answer is no. Here is how the remote process works.',
        },
        'content': {
            'es': [
                {'type': 'intro', 'text': 'Si te casaste en Colombia o con una persona colombiana y hoy estás considerando el divorcio, es completamente normal tener dudas, especialmente si ya no resides en el país.'},
                {'type': 'question', 'text': '¿Tengo que viajar a Colombia para divorciarme?'},
                {'type': 'answer', 'text': 'La respuesta es <strong>no</strong>. Sí es posible divorciarte sin viajar a Colombia, de manera legal, ágil y segura.'},
                {'type': 'p', 'text': 'En Pathy Higuera Abogados contamos con más de 6 años de experiencia acompañando a extranjeros en este tipo de procesos. Sabemos que la distancia, el tiempo y la incertidumbre pueden generar preocupación, por eso trabajamos para que puedas gestionar tu divorcio de forma clara, organizada y sin complicaciones.'},
                {'type': 'h2', 'text': 'Proceso 100% a distancia'},
                {'type': 'p', 'text': 'No es necesario que te desplaces a Colombia. Puedes adelantar un proceso 100% legal y completamente a distancia, evitando procedimientos judiciales largos que pueden extenderse durante años. Nuestro objetivo es ayudarte a cerrar esta etapa y avanzar con tranquilidad, en el menor tiempo posible y con total seguridad jurídica.'},
                {'type': 'p', 'text': 'En la mayoría de los casos, el divorcio de mutuo acuerdo se realiza ante notaría, lo que permite que el trámite sea mucho más rápido y menos desgastante a nivel emocional.'},
                {'type': 'h2', 'text': '¿Qué pasa si hay hijos menores?'},
                {'type': 'p', 'text': 'Si existen hijos menores de edad, el acuerdo debe ser revisado por el defensor de familia, con el fin de garantizar sus derechos. Esta etapa puede tardar algunas semanas, ya que el Instituto Colombiano de Bienestar Familiar (ICBF) realiza un análisis detallado del caso. Posteriormente, el trámite ante notaría puede tomar entre 2 y 4 semanas, dependiendo de factores como la existencia de bienes que deban liquidarse.'},
                {'type': 'h2', 'text': 'Documentos necesarios'},
                {'type': 'list', 'items': [
                    'Registro civil de matrimonio',
                    'Copia del documento de identidad de ambos cónyuges',
                    'Registro civil de nacimiento de los cónyuges (apostillado para extranjeros)',
                    'Acuerdo firmado entre las partes (apostillado si aplica)',
                    'Poder otorgado al abogado (apostillado si te encuentras en el exterior)',
                    'Si existen hijos: registro civil de nacimiento de los menores',
                ]},
                {'type': 'h2', 'text': 'Ventajas del divorcio de mutuo acuerdo'},
                {'type': 'p', 'text': 'El divorcio de mutuo acuerdo evita conflictos innecesarios, reduce costos, ahorra tiempo y permite cerrar esta etapa de forma tranquila y organizada.'},
                {'type': 'p', 'text': 'El divorcio no tiene que convertirse en una batalla. Cuando existe voluntad entre las partes, es posible llevar el proceso de manera respetuosa, clara y eficiente. Contar con una asesoría adecuada marca la diferencia entre un trámite complejo y uno que fluye con seguridad.'},
                {'type': 'cta', 'text': 'Si te encuentras fuera de Colombia y estás considerando iniciar tu proceso de divorcio, podemos acompañarte de principio a fin, gestionando todo de forma remota, con atención personalizada y enfoque en resultados.'},
            ],
            'en': [
                {'type': 'intro', 'text': 'If you got married in Colombia or to a Colombian national and are now considering divorce, it is completely normal to have questions—especially if you no longer live in the country.'},
                {'type': 'question', 'text': 'Do I have to travel to Colombia to get divorced?'},
                {'type': 'answer', 'text': 'The answer is <strong>no</strong>. It is possible to get divorced without traveling to Colombia, legally, efficiently, and safely.'},
                {'type': 'p', 'text': 'At Pathy Higuera Abogados, we have more than 6 years of experience guiding foreigners through these processes. We understand that distance, time, and uncertainty can cause concern, which is why we work to help you manage your divorce in a clear, organized, and stress-free way.'},
                {'type': 'h2', 'text': '100% Remote Process'},
                {'type': 'p', 'text': 'You do not need to travel to Colombia. You can carry out a 100% legal process entirely from a distance, avoiding lengthy court proceedings that can drag on for years. Our goal is to help you close this chapter and move forward with peace of mind, in the shortest time possible and with complete legal security.'},
                {'type': 'p', 'text': 'In most cases, a mutual consent divorce is conducted before a notary, which makes the process much faster and less emotionally draining.'},
                {'type': 'h2', 'text': 'What if There Are Minor Children?'},
                {'type': 'p', 'text': 'If there are minor children, the agreement must be reviewed by a family defender to ensure their rights are protected. This stage may take several weeks, as the Colombian Institute for Family Wellbeing (ICBF) conducts a detailed review. The subsequent notarial process typically takes 2 to 4 weeks, depending on factors such as whether there are assets to be divided.'},
                {'type': 'h2', 'text': 'Required Documents'},
                {'type': 'list', 'items': [
                    'Civil marriage certificate',
                    'Copy of both spouses\' identity documents',
                    'Birth certificate of both spouses (apostilled for foreigners)',
                    'Signed agreement between the parties (apostilled if applicable)',
                    'Power of attorney granted to the attorney (apostilled if you are abroad)',
                    'If there are children: their birth certificates',
                ]},
                {'type': 'h2', 'text': 'Benefits of Mutual Consent Divorce'},
                {'type': 'p', 'text': 'Mutual consent divorce avoids unnecessary conflict, reduces costs, saves time, and allows this chapter to be closed peacefully and in an organized manner.'},
                {'type': 'p', 'text': 'Divorce does not have to become a battle. When both parties are willing, the process can be handled respectfully, clearly, and efficiently. Having the right legal counsel makes the difference between a complex procedure and one that moves forward with security.'},
                {'type': 'cta', 'text': 'If you are outside Colombia and considering starting your divorce process, we can guide you from start to finish, managing everything remotely, with personalized attention and a results-focused approach.'},
            ],
        },
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/blog')
def blog():
    lang = request.args.get('lang', 'es')
    posts = list(BLOG_POSTS.values())
    return render_template('blog.html', posts=posts, lang=lang)

@app.route('/blog/<slug>')
def blog_post(slug):
    post = BLOG_POSTS.get(slug)
    if not post:
        return redirect(url_for('blog'))
    lang = request.args.get('lang', 'es')
    return render_template('blog_post.html', post=post, lang=lang)

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
    subject = f'Legal en Colombia — Consulta de {name} ({matter_label})'
    threading.Thread(target=send_email, args=(subject, body, email), daemon=True).start()

    flash('¡Gracias! Le responderé en menos de 24 horas. / Thank you! I\'ll respond within 24 hours.', 'success')
    return redirect(url_for('index') + '#contacto')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
