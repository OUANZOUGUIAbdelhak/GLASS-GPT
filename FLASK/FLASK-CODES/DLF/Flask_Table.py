from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
import os
import subprocess
import requests
import openpyxl
import pandas as pd
from io import BytesIO
import logging
from PyPDF2 import PdfReader

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///documents.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
socketio = SocketIO(app)
logging.basicConfig(level=logging.DEBUG)  # Niveau DEBUG pour voir tous les détails
logger = logging.getLogger(__name__)

# Initialiser SQLAlche
db = SQLAlchemy(app)

# Modèle de base de données
class GlassData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_document = db.Column(db.String(100), nullable=True)
    titre = db.Column(db.String(200), nullable=True)
    reference = db.Column(db.String(200), nullable=True)
    premier_auteur = db.Column(db.String(100), nullable=True)
    nombre_types_verres = db.Column(db.Integer, nullable=True)
    glass_types = db.relationship('GlassType', backref='glass_data', lazy=True, cascade='all, delete-orphan')

class GlassType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    glass_data_id = db.Column(db.Integer, db.ForeignKey('glass_data.id', ondelete='CASCADE'), nullable=False)
    type = db.Column(db.String(100), nullable=True)
    Li = db.Column(db.String(100), nullable=True)
    B = db.Column(db.String(100), nullable=True)
    O = db.Column(db.String(100), nullable=True)
    Na = db.Column(db.String(100), nullable=True)
    Mg = db.Column(db.String(100), nullable=True)
    Al = db.Column(db.String(100), nullable=True)
    Si = db.Column(db.String(100), nullable=True)
    P = db.Column(db.String(100), nullable=True)
    K = db.Column(db.String(100), nullable=True)
    Ca = db.Column(db.String(100), nullable=True)
    Ti = db.Column(db.String(100), nullable=True)
    V = db.Column(db.String(100), nullable=True)
    Cr = db.Column(db.String(100), nullable=True)
    Mn = db.Column(db.String(100), nullable=True)
    Fe = db.Column(db.String(100), nullable=True)
    Co = db.Column(db.String(100), nullable=True)
    Ni = db.Column(db.String(100), nullable=True)
    Cu = db.Column(db.String(100), nullable=True)
    Zn = db.Column(db.String(100), nullable=True)
    Ga = db.Column(db.String(100), nullable=True)
    Ge = db.Column(db.String(100), nullable=True)
    As = db.Column(db.String(100), nullable=True)
    Se = db.Column(db.String(100), nullable=True)
    Rb = db.Column(db.String(100), nullable=True)
    Sr = db.Column(db.String(100), nullable=True)
    Y = db.Column(db.String(100), nullable=True)
    Zr = db.Column(db.String(100), nullable=True)
    Nb = db.Column(db.String(100), nullable=True)
    Mo = db.Column(db.String(100), nullable=True)
    Tc = db.Column(db.String(100), nullable=True)
    Ru = db.Column(db.String(100), nullable=True)
    Rh = db.Column(db.String(100), nullable=True)
    Pd = db.Column(db.String(100), nullable=True)
    Ag = db.Column(db.String(100), nullable=True)
    Cd = db.Column(db.String(100), nullable=True)
    In = db.Column(db.String(100), nullable=True)
    Sn = db.Column(db.String(100), nullable=True)
    Sb = db.Column(db.String(100), nullable=True)
    Te = db.Column(db.String(100), nullable=True)
    I = db.Column(db.String(100), nullable=True)
    Cs = db.Column(db.String(100), nullable=True)
    Ba = db.Column(db.String(100), nullable=True)
    La = db.Column(db.String(100), nullable=True)
    Hf = db.Column(db.String(100), nullable=True)
    Ta = db.Column(db.String(100), nullable=True)
    W = db.Column(db.String(100), nullable=True)
    Re = db.Column(db.String(100), nullable=True)
    Os = db.Column(db.String(100), nullable=True)
    Ir = db.Column(db.String(100), nullable=True)
    Pt = db.Column(db.String(100), nullable=True)
    Au = db.Column(db.String(100), nullable=True)
    Hg = db.Column(db.String(100), nullable=True)
    Tl = db.Column(db.String(100), nullable=True)
    Pb = db.Column(db.String(100), nullable=True)
    Bi = db.Column(db.String(100), nullable=True)
    Po = db.Column(db.String(100), nullable=True)
    At = db.Column(db.String(100), nullable=True)
    Rn = db.Column(db.String(100), nullable=True)
    Ce = db.Column(db.String(100), nullable=True)
    Pr = db.Column(db.String(100), nullable=True)
    Nd = db.Column(db.String(100), nullable=True)
    S_autres_TR = db.Column(db.String(100), nullable=True)
    Th = db.Column(db.String(100), nullable=True)
    U = db.Column(db.String(100), nullable=True)
    Pu = db.Column(db.String(100), nullable=True)
    Np = db.Column(db.String(100), nullable=True)
    Am = db.Column(db.String(100), nullable=True)
    Cm = db.Column(db.String(100), nullable=True)
    S_autres_An = db.Column(db.String(100), nullable=True)
    Somme = db.Column(db.String(100), nullable=True)
    Densité = db.Column(db.String(100), nullable=True)
    Homogénéité = db.Column(db.String(100), nullable=True)
    B_IV = db.Column(db.String(100), nullable=True)
    Irradié = db.Column(db.String(100), nullable=True)
    Caractéristiques_si_irradié = db.Column(db.String(100), nullable=True)
    Température = db.Column(db.String(100), nullable=True)
    Statique_dynamique = db.Column(db.String(100), nullable=True)
    Plage_granulométrique_si_poudre = db.Column(db.String(100), nullable=True)
    Surface_spécifique_géométrique_si_poudre = db.Column(db.String(100), nullable=True)
    Surface_spécifique_BET_si_poudre = db.Column(db.String(100), nullable=True)
    Qualité_de_polissage_si_monolithe = db.Column(db.String(100), nullable=True)
    Masse_du_verre = db.Column(db.String(100), nullable=True)
    Surface_du_verre_S = db.Column(db.String(100), nullable=True)
    Volume_de_la_solution_V = db.Column(db.String(100), nullable=True)
    Débit_de_la_solution = db.Column(db.String(100), nullable=True)
    pH_initial_T_amb = db.Column(db.String(100), nullable=True)
    pH_initial_T_essai = db.Column(db.String(100), nullable=True)
    Composition_de_la_solution = db.Column(db.String(100), nullable=True)
    Durée_de_l_expérience = db.Column(db.String(100), nullable=True)
    pH_final_T_amb = db.Column(db.String(100), nullable=True)
    pH_final_T_essai = db.Column(db.String(100), nullable=True)
    Normalisation_de_la_vitesse_Sgeo_ou_SBET = db.Column(db.String(100), nullable=True)
    V0_Si_ou_r0_Si = db.Column(db.String(100), nullable=True)
    r2_Si = db.Column(db.String(100), nullable=True)
    Ordonnée_à_l_origine_Si = db.Column(db.String(100), nullable=True)
    V0_B_ou_r0_B = db.Column(db.String(100), nullable=True)
    Ordonnée_à_l_origine_B = db.Column(db.String(100), nullable=True)
    V0_Na_ou_r0_Na = db.Column(db.String(100), nullable=True)
    r2_Na = db.Column(db.String(100), nullable=True)
    Ordonnée_à_l_origine_Na = db.Column(db.String(100), nullable=True)
    V0_ΔM_ou_r0_ΔM = db.Column(db.String(100), nullable=True)
    Congruence = db.Column(db.String(100), nullable=True)

# Créer la base de données si elle n'existe pas
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    glass_data = GlassData.query.all()
    return render_template('index.html', glass_data=glass_data)

@app.route('/add_glass_data', methods=['POST'])
def add_glass_data():
    data = request.get_json()
    try:
        # Créer l'entrée principale dans GlassData
        new_entry = GlassData(
            type_document=data.get('type'),
            titre=data.get('titre'),
            reference=data.get('reference'),
            premier_auteur=data.get('premier_auteur'),
            nombre_types_verres=data.get('nombre_types_verres')
        )
        db.session.add(new_entry)
        db.session.commit()

        # Ajouter les types de verre
        for verre in data.get('verres', []):
            glass_type_entry = GlassType(
                glass_data_id=new_entry.id,
                type=verre.get('type'),
                Li=str(verre.get('Li')),
                B=str(verre.get('B')),
                O=str(verre.get('O')),
                Na=str(verre.get('Na')),
                Mg=str(verre.get('Mg')),
                Al=str(verre.get('Al')),
                Si=str(verre.get('Si')),
                P=str(verre.get('P')),
                K=str(verre.get('K')),
                Ca=str(verre.get('Ca')),
                Ti=str(verre.get('Ti')),
                V=str(verre.get('V')),
                Cr=str(verre.get('Cr')),
                Mn=str(verre.get('Mn')),
                Fe=str(verre.get('Fe')),
                Co=str(verre.get('Co')),
                Ni=str(verre.get('Ni')),
                Cu=str(verre.get('Cu')),
                Zn=str(verre.get('Zn')),
                Ga=str(verre.get('Ga')),
                Ge=str(verre.get('Ge')),
                As=str(verre.get('As')),
                Se=str(verre.get('Se')),
                Rb=str(verre.get('Rb')),
                Sr=str(verre.get('Sr')),
                Y=str(verre.get('Y')),
                Zr=str(verre.get('Zr')),
                Nb=str(verre.get('Nb')),
                Mo=str(verre.get('Mo')),
                Tc=str(verre.get('Tc')),
                Ru=str(verre.get('Ru')),
                Rh=str(verre.get('Rh')),
                Pd=str(verre.get('Pd')),
                Ag=str(verre.get('Ag')),
                Cd=str(verre.get('Cd')),
                In=str(verre.get('In')),
                Sn=str(verre.get('Sn')),
                Sb=str(verre.get('Sb')),
                Te=str(verre.get('Te')),
                I=str(verre.get('I')),
                Cs=str(verre.get('Cs')),
                Ba=str(verre.get('Ba')),
                La=str(verre.get('La')),
                Hf=str(verre.get('Hf')),
                Ta=str(verre.get('Ta')),
                W=str(verre.get('W')),
                Re=str(verre.get('Re')),
                Os=str(verre.get('Os')),
                Ir=str(verre.get('Ir')),
                Pt=str(verre.get('Pt')),
                Au=str(verre.get('Au')),
                Hg=str(verre.get('Hg')),
                Tl=str(verre.get('Tl')),
                Pb=str(verre.get('Pb')),
                Bi=str(verre.get('Bi')),
                Po=str(verre.get('Po')),
                At=str(verre.get('At')),
                Rn=str(verre.get('Rn')),
                Ce=str(verre.get('Ce')),
                Pr=str(verre.get('Pr')),
                Nd=str(verre.get('Nd')),
                S_autres_TR=str(verre.get("S_autres_TR")),
                Th=str(verre.get('Th')),
                U=str(verre.get('U')),
                Pu=str(verre.get('Pu')),
                Np=str(verre.get('Np')),
                Am=str(verre.get('Am')),
                Cm=str(verre.get('Cm')),
                S_autres_An=str(verre.get("S_autres_An")),
                Somme=str(verre.get('Somme')),
                Densité=str(verre.get('Densité')),
                Homogénéité=str(verre.get('Homogénéité')),
                B_IV=str(verre.get('B_IV')),
                Irradié=str(verre.get('Irradié')),
                Caractéristiques_si_irradié=str(verre.get('Caractéristiques_si_irradié')),
                Température=str(verre.get('Température')),
                Statique_dynamique=str(verre.get('Statique_dynamique')),
                Plage_granulométrique_si_poudre=str(verre.get('Plage_granulométrique_si_poudre')),
                Surface_spécifique_géométrique_si_poudre=str(verre.get('Surface_spécifique_géométrique_si_poudre')),
                Surface_spécifique_BET_si_poudre=str(verre.get('Surface_spécifique_BET_si_poudre')),
                Qualité_de_polissage_si_monolithe=str(verre.get('Qualité_de_polissage_si_monolithe')),
                Masse_du_verre=str(verre.get('Masse_du_verre')),
                Surface_du_verre_S=str(verre.get('Surface_du_verre_S')),
                Volume_de_la_solution_V=str(verre.get('Volume_de_la_solution_V')),
                Débit_de_la_solution=str(verre.get('Débit_de_la_solution')),
                pH_initial_T_amb=str(verre.get('pH_initial_T_amb')),
                pH_initial_T_essai=str(verre.get('pH_initial_T_essai')),
                Composition_de_la_solution=str(verre.get('Composition_de_la_solution')),
                Durée_de_l_expérience=str(verre.get('Durée_de_l_expérience')),
                pH_final_T_amb=str(verre.get('pH_final_T_amb')),
                pH_final_T_essai=str(verre.get('pH_final_T_essai')),
                Normalisation_de_la_vitesse_Sgeo_ou_SBET=str(verre.get('Normalisation_de_la_vitesse_Sgeo_ou_SBET')),
                V0_Si_ou_r0_Si=str(verre.get('V₀(Si) ou r₀(Si)')),
                r2_Si=str(verre.get('r²(Si)')),
                Ordonnée_à_l_origine_Si=str(verre.get("Ordonnée_à_l'origine_Si")),
                V0_B_ou_r0_B=str(verre.get('V₀(B) ou r₀(B)')),
                Ordonnée_à_l_origine_B=str(verre.get("Ordonnée_à_l'origine_B")),
                V0_Na_ou_r0_Na=str(verre.get('V₀(Na) ou r₀(Na)')),
                r2_Na=str(verre.get('r²(Na)')),
                Ordonnée_à_l_origine_Na=str(verre.get("Ordonnée_à_l'origine_Na")),
                V0_ΔM_ou_r0_ΔM=str(verre.get('V₀(ΔM) ou r₀(ΔM)')),
                Congruence=str(verre.get('Congruence'))
            )
            db.session.add(glass_type_entry)
        db.session.commit()

        return "Données sur le verre ajoutées avec succès !", 200

    except Exception as e:
        db.session.rollback()
        return f"Erreur : {str(e)}", 500
@app.route('/delete_document_reference/<int:id>', methods=['POST'])
def delete_document_reference(id):
    glass_data = GlassData.query.get(id)
    if glass_data:
        db.session.delete(glass_data)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        logger.error("Aucun fichier dans la requête")
        return "No file part", 400
    
    file = request.files['file']
    if file.filename == '':
        logger.error("Aucun fichier sélectionné")
        return "No selected file", 400
    
    if file:
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
            logger.info(f"Dossier {app.config['UPLOAD_FOLDER']} créé")
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        logger.info(f"Sauvegarde du fichier à : {filepath}")
        file.save(filepath)

        try:
            # Lire le contenu du fichier
            if file.filename.endswith(('.txt', '.md')):
                logger.info("Traitement d'un fichier texte")
                with open(filepath, 'r', encoding='utf-8') as f:
                    file_content = f.read()
            elif file.filename.endswith('.pdf'):
                logger.info("Traitement d'un fichier PDF")
                pdf_reader = PdfReader(filepath)
                file_content = ""
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    text = page.extract_text()
                    if text:
                        file_content += text
                    else:
                        logger.warning(f"Aucun texte extrait de la page {page_num}")
                if not file_content:
                    logger.error("Aucun contenu extrait du PDF")
                    return "Aucun contenu extrait du PDF", 400
            else:
                logger.error("Format de fichier non supporté")
                return "Unsupported file format", 400
            
            logger.debug(f"Contenu extrait (premiers 500 caractères) : {file_content[:500]}")

            # Envoyer à Langflow
            langflow_url = "http://127.0.0.1:7860/api/v1/run/0130294b-d3dd-4db9-84ec-bd9043e6bc1d?stream=false"
            logger.info(f"Envoi à Langflow : {langflow_url}")
            response = requests.post(
                langflow_url,
                json={
                    "input_value": file_content,
                    "output_type": "chat",
                    "input_type": "text",
                    "tweaks": {
                        "ParseData-O3xbr": {},
                        "Prompt-CvBi7": {},
                        "GoogleGenerativeAIModel-uYxja": {},
                        "Prompt-Prpyc": {},
                        "Prompt-95tm9": {},
                        "Prompt-BTfkR": {},
                        "GlassCompositionConverter-nDAxX": {},
                        "CombineText-2gWvC": {},
                        "Prompt-KHumU": {},
                        "GoogleGenerativeAIModel-FfeYQ": {},
                        "GoogleGenerativeAIModel-H9Xox": {},
                        "GlassCompositionConverter-Sblyw": {},
                        "CombineText-DHXvR": {},
                        "Prompt-Uyk32": {},
                        "GoogleGenerativeAIModel-yDfoE": {},
                        "Prompt-VOPkO": {},
                        "GlassCompositionConverter-WHWvv": {},
                        "CombineText-bA6y9": {},
                        "Prompt-po5vR": {},
                        "GoogleGenerativeAIModel-ppBan": {},
                        "Prompt-LEw60": {},
                        "GoogleGenerativeAIModel-VXx57": {},
                        "GlassCompositionConverter-IieDF": {},
                        "CombineText-1leNx": {},
                        "Prompt-Bia8u": {},
                        "GoogleGenerativeAIModel-7qjJi": {},
                        "Prompt-0TzDg": {},
                        "GoogleGenerativeAIModel-Ai3sG": {},
                        "GlassCompositionConverter-FrgZ2": {},
                        "CombineText-438mj": {},
                        "Prompt-KDx27": {},
                        "GoogleGenerativeAIModel-Qa1Vw": {},
                        "Prompt-QYsZH": {},
                        "GoogleGenerativeAIModel-vEuJf": {},
                        "GlassCompositionConverter-s1NNy": {},
                        "CombineText-QVHkJ": {},
                        "Prompt-YXgUi": {},
                        "GoogleGenerativeAIModel-HTcbf": {},
                        "Prompt-YSKtu": {},
                        "GoogleGenerativeAIModel-AdnE6": {},
                        "GlassCompositionConverter-TZNTF": {},
                        "CombineText-skF0K": {},
                        "Prompt-7lvWp": {},
                        "GoogleGenerativeAIModel-X88mX": {},
                        "Prompt-aYNdd": {},
                        "GoogleGenerativeAIModel-tyjTA": {},
                        "GlassCompositionConverter-kzRW8": {},
                        "CombineText-BONhX": {},
                        "Prompt-a7YLm": {},
                        "GoogleGenerativeAIModel-ry2Rb": {},
                        "Prompt-yPJsv": {},
                        "GoogleGenerativeAIModel-dGFo2": {},
                        "GlassCompositionConverter-zZa6D": {},
                        "CombineText-2XThH": {},
                        "Prompt-Hrgu7": {},
                        "GoogleGenerativeAIModel-oTIYg": {},
                        "Prompt-QOkbs": {},
                        "GoogleGenerativeAIModel-EIUXq": {},
                        "GlassCompositionConverter-sufyN": {},
                        "CombineText-pJSlb": {},
                        "Prompt-uyXpe": {},
                        "GoogleGenerativeAIModel-itbVX": {},
                        "Prompt-pseV4": {},
                        "GoogleGenerativeAIModel-ZfQia": {},
                        "GlassCompositionConverter-9R3Fe": {},
                        "CombineText-p56dl": {},
                        "Prompt-DpcNf": {},
                        "GoogleGenerativeAIModel-SL95I": {},
                        "Prompt-Vuct4": {},
                        "GoogleGenerativeAIModel-jtUke": {},
                        "GlassCompositionConverter-vOZgf": {},
                        "CombineText-HtGPx": {},
                        "Prompt-MsQev": {},
                        "GoogleGenerativeAIModel-F9HPH": {},
                        "Prompt-zKzbb": {},
                        "GoogleGenerativeAIModel-1vipg": {},
                        "GlassCompositionConverter-pCf0i": {},
                        "CombineText-dWWyZ": {},
                        "Prompt-IDdkJ": {},
                        "GoogleGenerativeAIModel-JwW1V": {},
                        "Prompt-R5RgD": {},
                        "GoogleGenerativeAIModel-Tkx8P": {},
                        "GlassCompositionConverter-7yzWp": {},
                        "CombineText-FU0VT": {},
                        "Prompt-mzw6H": {},
                        "GoogleGenerativeAIModel-Uhy9L": {},
                        "Prompt-OwAmP": {},
                        "GoogleGenerativeAIModel-41cGM": {},
                        "GlassCompositionConverter-2zfLq": {},
                        "CombineText-w9zLG": {},
                        "Prompt-7xuDl": {},
                        "GoogleGenerativeAIModel-evcyx": {},
                        "GoogleGenerativeAIModel-NTWiN": {},
                        "GoogleGenerativeAIModel-Y5uD2": {},
                        "EnvoyerDonneesVerreTableComponent-D5zFJ": {},
                        "GoogleGenerativeAIModel-fa2Vp": {},
                        "CombineText-JV5OM": {},
                        "File-2qZjd": {}
                    }
                }
            )

            response.raise_for_status()  # Lever une exception si la requête échoue
            
            # Vérifier la réponse brute
            logger.debug(f"Réponse brute de Langflow : {response.text[:500]}")  # Limite à 500 caractères
            
            # Tenter de parser en JSON, sinon renvoyer le texte brut
            try:
                langflow_data = response.json()
                logger.debug(f"Réponse JSON de Langflow : {langflow_data}")
            except ValueError as e:
                logger.warning(f"La réponse de Langflow n'est pas JSON : {response.text}")
                langflow_data = {"raw_response": response.text}  # Fallback : encapsuler le texte brut

            return jsonify({"message": "File processed successfully", "data": langflow_data})

        except requests.exceptions.RequestException as e:
            logger.error(f"Erreur lors de la requête à Langflow : {str(e)}")
            return f"Erreur de connexion à Langflow : {str(e)}", 500
        except Exception as e:
            logger.error(f"Erreur de traitement : {str(e)}")
            return f"Error processing file: {str(e)}", 500
@app.route('/download_excel', methods=['GET'])
def download_excel():
    glass_data = GlassData.query.all()
    data = []
    for entry in glass_data:
        for glass_type in entry.glass_types:
            data.append({
                "Type Document": entry.type_document,
                "Titre": entry.titre,
                "Référence": entry.reference,
                "Premier Auteur": entry.premier_auteur,
                "Type de verre": glass_type.type,
                "Li": glass_type.Li,
                "B": glass_type.B,
                "O": glass_type.O,
                "Na": glass_type.Na,
                "Mg": glass_type.Mg,
                "Al": glass_type.Al,
                "Si": glass_type.Si,
                "P": glass_type.P,
                "K": glass_type.K,
                "Ca": glass_type.Ca,
                "Ti": glass_type.Ti,
                "V": glass_type.V,
                "Cr": glass_type.Cr,
                "Mn": glass_type.Mn,
                "Fe": glass_type.Fe,
                "Co": glass_type.Co,
                "Ni": glass_type.Ni,
                "Cu": glass_type.Cu,
                "Zn": glass_type.Zn,
                "Ga": glass_type.Ga,
                "Ge": glass_type.Ge,
                "As": glass_type.As,
                "Se": glass_type.Se,
                "Rb": glass_type.Rb,
                "Sr": glass_type.Sr,
                "Y": glass_type.Y,
                "Zr": glass_type.Zr,
                "Nb": glass_type.Nb,
                "Mo": glass_type.Mo,
                "Tc": glass_type.Tc,
                "Ru": glass_type.Ru,
                "Rh": glass_type.Rh,
                "Pd": glass_type.Pd,
                "Ag": glass_type.Ag,
                "Cd": glass_type.Cd,
                "In": glass_type.In,
                "Sn": glass_type.Sn,
                "Sb": glass_type.Sb,
                "Te": glass_type.Te,
                "I": glass_type.I,
                "Cs": glass_type.Cs,
                "Ba": glass_type.Ba,
                "La": glass_type.La,
                "Hf": glass_type.Hf,
                "Ta": glass_type.Ta,
                "W": glass_type.W,
                "Re": glass_type.Re,
                "Os": glass_type.Os,
                "Ir": glass_type.Ir,
                "Pt": glass_type.Pt,
                "Au": glass_type.Au,
                "Hg": glass_type.Hg,
                "Tl": glass_type.Tl,
                "Pb": glass_type.Pb,
                "Bi": glass_type.Bi,
                "Po": glass_type.Po,
                "At": glass_type.At,
                "Rn": glass_type.Rn,
                "Ce": glass_type.Ce,
                "Pr": glass_type.Pr,
                "Nd": glass_type.Nd,
                "S_autres_TR": glass_type.S_autres_TR,
                "Th": glass_type.Th,
                "U": glass_type.U,
                "Pu": glass_type.Pu,
                "Np": glass_type.Np,
                "Am": glass_type.Am,
                "Cm": glass_type.Cm,
                "S_autres_An": glass_type.S_autres_An,
                "Somme": glass_type.Somme,
                "Densité": glass_type.Densité,
                "Homogénéité": glass_type.Homogénéité,
                "B_IV": glass_type.B_IV,
                "Irradié": glass_type.Irradié,
                "Caractéristiques_si_irradié": glass_type.Caractéristiques_si_irradié,
                "Température": glass_type.Température,
                "Statique_dynamique": glass_type.Statique_dynamique,
                "Plage_granulométrique_si_poudre": glass_type.Plage_granulométrique_si_poudre,
                "Surface_spécifique_géométrique_si_poudre": glass_type.Surface_spécifique_géométrique_si_poudre,
                "Surface_spécifique_BET_si_poudre": glass_type.Surface_spécifique_BET_si_poudre,
                "Qualité_de_polissage_si_monolithe": glass_type.Qualité_de_polissage_si_monolithe,
                "Masse_du_verre": glass_type.Masse_du_verre,
                "Surface_du_verre_S": glass_type.Surface_du_verre_S,
                "Volume_de_la_solution_V": glass_type.Volume_de_la_solution_V,
                "Débit_de_la_solution": glass_type.Débit_de_la_solution,
                "pH_initial_T_amb": glass_type.pH_initial_T_amb,
                "pH_initial_T_essai": glass_type.pH_initial_T_essai,
                "Composition_de_la_solution": glass_type.Composition_de_la_solution,
                "Durée_de_l_expérience": glass_type.Durée_de_l_expérience,
                "pH_final_T_amb": glass_type.pH_final_T_amb,
                "pH_final_T_essai": glass_type.pH_final_T_essai,
                "Normalisation_de_la_vitesse_Sgeo_ou_SBET": glass_type.Normalisation_de_la_vitesse_Sgeo_ou_SBET,
                "V0_Si_ou_r0_Si": glass_type.V0_Si_ou_r0_Si,
                "r2_Si": glass_type.r2_Si,
                "Ordonnée_à_l_origine_Si": glass_type.Ordonnée_à_l_origine_Si,
                "V0_B_ou_r0_B": glass_type.V0_B_ou_r0_B,
                "Ordonnée_à_l_origine_B": glass_type.Ordonnée_à_l_origine_B,
                "V0_Na_ou_r0_Na": glass_type.V0_Na_ou_r0_Na,
                "r2_Na": glass_type.r2_Na,
                "Ordonnée_à_l_origine_Na": glass_type.Ordonnée_à_l_origine_Na,
                "V0_ΔM_ou_r0_ΔM": glass_type.V0_ΔM_ou_r0_ΔM,
                "Congruence": glass_type.Congruence
            })

    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Glass Data')
    output.seek(0)

    return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name='glass_data.xlsx')


@socketio.on('connect')
def handle_connect():
    emit('status', {'msg': 'Connecté'})

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    socketio.run(app, debug=True, port=5002)
