from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, EmailField, TelField, SelectField
from wtforms.validators import DataRequired, Email, Length, Optional
import os
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import json
from googleapiclient.discovery import build
from datetime import datetime
import requests

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dcfence-secret-key-2024'

# Blog articles data
blog_articles = [
    {
        'id': 1,
        'image': 'https://austexfenceanddeck.com/wp-content/uploads/2023/02/wood-dog-ear-fence-scaled.jpg',   
        'title': 'Types of Security Fences: Complete Guide',
        'tags': ['security fences', 'types of fences', 'security systems'],
        'excerpt': 'Discover the different types of security fences available to protect your property.',
        'content': '''
                    <h1>Types of Security Fences</h1>
                    <br>
                    <p>At <strong>DCFence</strong>, we understand that each property has different security needs. That's why we offer a complete range of fencing solutions tailored to specific threats, environments, and budgets.</p>

                    <h3>1. Barbed Wire Fences</h3>
                    <p>Barbed wire fences are designed to offer <strong>maximum deterrence</strong>. Frequently used in commercial and industrial areas, this type of fence combines a robust metal frame with tightly spaced barbed wire at the top to discourage climbing or tampering.</p>
                    <ul>
                        <li><strong>Use Cases:</strong> Warehouses, farms, and storage yards</li>
                        <li><strong>Advantages:</strong> Low cost, high deterrent, easy to maintain</li>
                    </ul>

                    <h3>2. Chain Link Fences</h3>
                    <p>Chain link fences are a cost-effective solution that balances <strong>security and visibility</strong>. With galvanized steel and optional vinyl coatings, they are ideal for both residential and light commercial use.</p>
                    <ul>
                        <li><strong>Use Cases:</strong> Residential backyards, schools, parks</li>
                        <li><strong>Advantages:</strong> Fast installation, durable, customizable height</li>
                    </ul>

                    <h3>3. Rigid Panel Fences</h3>
                    <p>Rigid panel fences are known for their <strong>structural strength and anti-climbing features</strong>. Constructed from welded steel panels, they provide a sleek modern look while offering high protection.</p>
                    <ul>
                        <li><strong>Use Cases:</strong> Gated communities, corporate offices, power plants</li>
                        <li><strong>Advantages:</strong> Highly secure, aesthetic, low maintenance</li>
                    </ul>

                    <h3>4. Electrified Fences</h3>
                    <p>Electrified fences combine a physical barrier with a psychological deterrent. These systems are <strong>regulated for safety</strong> and include warning signs, pulse generators, and tamper alarms.</p>
                    <ul>
                        <li><strong>Use Cases:</strong> Data centers, military facilities, critical infrastructure</li>
                        <li><strong>Advantages:</strong> Immediate intrusion response, customizable voltage, remote monitoring</li>
                    </ul>

                    <p>Every property is unique. Our security experts analyze your location, threat level, and legal requirements to recommend the most effective fencing system. <em>We don’t just sell fences — we build peace of mind.</em></p>
                            ''',
        'date': '2024-01-15',
        'author': 'DCFence Team'
    },
    {           
        'id': 2,
        'image': 'https://www.greenwayfence.com/wp-content/uploads/2021/07/different-types-of-fences.jpg',   
        'title': 'Benefits of Perimeter Security',
        'tags': ['perimeter security', 'security fences', 'security systems'],
        'excerpt': 'Learn why a security fence is the first line of defense for your property.',
        'content': '''
                    <h2>Benefits of Perimeter Security</h2>
                    <p>Whether you're protecting your home, business, or institution, a professional security fence is a fundamental component of any complete safety strategy. At <strong>DCFence</strong>, we believe a good fence is both <em>proactive</em> and <em>preventive</em>.</p>

                    <h3>Main Benefits:</h3>

                    <h4>1. Visual Deterrence</h4>
                    <p>Intruders are far less likely to approach a property that is visibly protected. A security fence sends a clear message: “This property is protected.”</p>

                    <h4>2. Access Control</h4>
                    <p>Fences help establish clear boundaries and funnel visitors through controlled entry points, reducing unauthorized access and increasing accountability.</p>

                    <h4>3. Asset Protection</h4>
                    <p>Equipment, materials, vehicles, and even landscaping are better protected from theft or vandalism when behind a secure perimeter.</p>

                    <h4>4. Integration with Security Systems</h4>
                    <p>Modern fences work in tandem with advanced technologies like motion sensors, security cameras, and automated gates — creating a smart perimeter defense.</p>

                    <h4>5. Regulatory Compliance</h4>
                    <p>In sectors like logistics, government, or utilities, security fencing is often a <strong>legal requirement</strong>. Our solutions comply with local and industry-specific regulations.</p>

                    <h4>6. Added Property Value</h4>
                    <p>A secure property is more attractive to buyers, tenants, and insurers. Professionally installed fencing adds both aesthetic and functional value.</p>

                    <p><strong>DCFence</strong> combines physical barriers with intelligent technology to protect what matters most. Our mission is to make high-quality perimeter security accessible, affordable, and effective for everyone.</p>
                            ''',
        'date': '2024-01-10',
        'author': 'DCFence Team'
    },
    {
        'id': 3,
        'image': 'https://dam.thdstatic.com/content/production/Z2d4MKjVh4h20acxBam07Q/zziQnlpGGxh_lp0qleyivA/Original%20file/types-of-fences-section-5.jpg',   
        'title': 'Success Cases: Protecting Communities',
        'tags': ['success cases', 'security fences', 'security systems'],
        'excerpt': 'Discover how we have helped entire communities improve their perimeter security.',
        'content': '''
                        <h2>Success Cases: Protecting Communities</h2>
                        <p>Our commitment goes beyond products — it’s about results. Below are three of our most impactful projects where we significantly improved security and peace of mind for entire communities.</p>

                        <h3>🏡 Residential Project "Safe Villa"</h3>
                        <p><strong>Location:</strong> Gated residential community in Bogotá<br>
                        <strong>Scope:</strong> 150 single-family homes<br>
                        <strong>Duration:</strong> 3 months</p>

                        <p><strong>Challenges:</strong> Frequent break-ins, unguarded entry points, lack of defined perimeter.</p>

                        <p><strong>Solutions:</strong></p>
                        <ul>
                            <li>2.5 km of 3-meter rigid panel fencing</li>
                            <li>8 electronic access gates with remote monitoring</li>
                            <li>Integrated lighting system with motion detectors</li>
                            <li>Connection to community surveillance cameras</li>
                        </ul>

                        <p><strong>Result:</strong> 95% drop in reported incidents within the first year, increased resident satisfaction and property values.</p>

                        <h3>🏬 Shopping Center "Central Plaza"</h3>
                        <p><strong>Location:</strong> Urban shopping center with high foot traffic<br>
                        <strong>Scope:</strong> 50,000 m²<br>
                        <strong>Duration:</strong> 6 weeks</p>

                        <p><strong>Challenges:</strong> Perimeter vandalism, car thefts in parking lots, unmonitored delivery zones.</p>

                        <p><strong>Solutions:</strong></p>
                        <ul>
                            <li>High-voltage electric fencing around sensitive areas</li>
                            <li>Motion-activated lighting and surveillance cameras</li>
                            <li>Vehicle plate recognition at delivery gates</li>
                            <li>24/7 security center integration</li>
                        </ul>

                        <p><strong>Result:</strong> Theft and vandalism incidents reduced to zero. Increased commercial lease renewals and visitor traffic.</p>

                        <h3>🏛️ Government Installation</h3>
                        <p><strong>Type:</strong> National security institution (classified)<br>
                        <strong>Requirements:</strong> Military-grade security, 24/7 monitoring<br>
                        <strong>Duration:</strong> 4 months</p>

                        <p><strong>Challenges:</strong> Need for highest-level perimeter protection, sensitive operations inside.</p>

                        <p><strong>Solutions:</strong></p>
                        <ul>
                            <li>4-meter-high anti-climb fencing with reinforced steel</li>
                            <li>Advanced vibration and cut detection sensors</li>
                            <li>Anti-ram vehicle barriers at entrances</li>
                            <li>AI-driven surveillance with automated alert systems</li>
                        </ul>

                        <p><strong>Result:</strong> Successfully obtained military-grade security certification. Project recognized for innovation and execution speed.</p>

                        <p>These case studies illustrate our adaptability and deep expertise in perimeter security. From neighborhoods to national defense, <strong>DCFence</strong> is your trusted partner in protection.</p>
        ''',
        'date': '2024-01-05',
        'author': 'DCFence Team'
    }
]

app.config['RECAPTCHA_PUBLIC_KEY'] = '6LcJsoorAAAAAA9eEYl3DhnY1MaTEjEXhM5l9rDH'
app.config['RECAPTCHA_PRIVATE_KEY'] = os.environ.get('RECAPTCHA_PRIVATE_KEY')  # Reemplaza esto con tu clave privada real

# Configuración de Google Sheets
service_account_json = os.environ.get('GOOGLE_SERVICE_ACCOUNT_JSON')
if not service_account_json:
    raise RuntimeError('La variable de entorno GOOGLE_SERVICE_ACCOUNT_JSON no está definida o está vacía.')

info = json.loads(service_account_json)
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_service_account_info(info, scopes=SCOPES)

service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()
SPREADSHEET_ID = os.environ.get('SHEET_ID')

def save_to_sheet(data):
    body = {'values': [data]}
    sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="contacts_us!A1",
        valueInputOption="RAW",
        body=body
    ).execute()

# Contact form
class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone = TelField('Phone', validators=[DataRequired(), Length(min=10, max=15)])
    type_of_request = SelectField('Type of Request', choices=[('maintenance', 'Maintenance'), ('installation', 'Installation'), ('other', 'Other')], validators=[DataRequired()])
    address = StringField('Project Address (optional)', validators=[Optional(), Length(max=100)])
    referral = SelectField('How did you find us?', choices=[('google', 'Google'), ('social', 'Social Media'), ('friend', 'Friend'), ('other', 'Other')], validators=[Optional()])
    other_details = TextAreaField('Other Details (if applicable)', validators=[Optional(), Length(max=500)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=500)])
    recaptcha = RecaptchaField()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/free-quote', methods=['GET', 'POST'])
def free_quote():
    form = ContactForm()
    if form.validate_on_submit():
        user_ip = request.remote_addr
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data = [
            user_ip,
            now,
            form.name.data,
            form.email.data,
            form.phone.data,
            form.type_of_request.data,
            form.address.data,
            form.referral.data,
            form.other_details.data,
            form.message.data
        ]
        try:
            save_to_sheet(data)
        except Exception as e:
            flash(f'Error al guardar en Google Sheets: {e}', 'danger')
        flash('Thank you for your quote request! We will contact you within 24 hours with your free estimate.', 'success')
        return redirect(url_for('home'))
    return render_template('home.html', form=form)

@app.route('/blog')
def blog():
    return render_template('blog.html', articles=blog_articles)

@app.route('/blog/<int:article_id>')
def article(article_id):
    article = next((a for a in blog_articles if a['id'] == article_id), None)
    if article is None:
        return redirect(url_for('blog'))
    # Excluye el actual y toma los 3 más recientes
    related_articles = [a for a in blog_articles if a['id'] != article_id][:3]
    return render_template('article.html', article=article, related_articles=related_articles)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        user_ip = request.remote_addr
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data = [
            user_ip,
            now,
            form.name.data,
            form.email.data,
            form.phone.data,
            form.type_of_request.data,
            form.address.data,
            form.referral.data,
            form.other_details.data,
            form.message.data
        ]
        try:
            save_to_sheet(data)
        except Exception as e:
            flash(f'Error al guardar en Google Sheets: {e}', 'danger')
        flash('Thank you for your message! We will contact you soon.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form)

@app.route('/chat-advisor', methods=['POST'])
def chat_advisor():
    data = request.get_json()
    user_ip = request.remote_addr
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone', '')
    type_of_request = data.get('type_of_request', 'chat')
    address = data.get('address', '')
    referral = data.get('referral', '')
    other_details = data.get('other_details', '')
    message = data.get('message')
    recaptcha_token = data.get('recaptcha')

    # Validar reCAPTCHA con Google
    recaptcha_secret = app.config.get('RECAPTCHA_PRIVATE_KEY') or os.environ.get('RECAPTCHA_PRIVATE_KEY')
    recaptcha_url = 'https://www.google.com/recaptcha/api/siteverify'
    recaptcha_response = requests.post(recaptcha_url, data={
        'secret': recaptcha_secret,
        'response': recaptcha_token,
        'remoteip': user_ip
    })
    recaptcha_result = recaptcha_response.json()
    if not recaptcha_result.get('success'):
        return jsonify({'success': False, 'error': 'Invalid reCAPTCHA'}), 400

    sheet_data = [
        user_ip,
        now,
        name,
        email,
        phone,
        message,
        address,
        referral,
        '',
        other_details,
    ]
    try:
        save_to_sheet(sheet_data)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/newsletter-subscribe', methods=['POST'])
def newsletter_subscribe():
    data = request.get_json()
    email = data.get('email')
    user_ip = request.remote_addr
    if not email:
        return jsonify({'success': False, 'error': 'Email is required'}), 400
    try:
        # Lee los registros existentes de la hoja
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range="newsletters_email!A:C"
        ).execute()
        rows = result.get('values', [])
        # Cuenta cuántas veces aparece la IP
        ip_count = sum(1 for row in rows if len(row) > 2 and row[2] == user_ip)
        if ip_count >= 5:
            return jsonify({'success': False, 'error': 'You have reached the maximum number of subscriptions from this IP.'}), 429
        # Guarda el email, fecha e IP
        sheet.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range="newsletters_email!A1",
            valueInputOption="RAW",
            body={'values': [[email, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user_ip]]}
        ).execute()
        return jsonify({'success': True})
    except Exception as e:
        print('NEWSLETTER ERROR:', e)
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/residential')
def residential():
    return render_template('residential.html')

@app.route('/commercial')
def commercial():
    return render_template('commercial.html')

@app.route('/governmental')
def governmental():
    return render_template('governmental.html')

@app.route('/security')
def security():
    return render_template('security.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

if __name__ == '__main__':
    app.run() 