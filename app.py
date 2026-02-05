import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import hashlib
import json
import time
from faker import Faker
import warnings
import random
from io import BytesIO
import base64
import uuid
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="Système de Gestion Universitaire Pro",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #34495e;
        margin: 1.5rem 0;
        font-weight: bold;
    }
    .kpi-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        padding: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    .kpi-card-secondary {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 10px;
        padding: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    .kpi-card-tertiary {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        border-radius: 10px;
        padding: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    .kpi-card-employee {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        border-radius: 10px;
        padding: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    .kpi-title {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-bottom: 5px;
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: bold;
        margin: 10px 0;
    }
    .stButton > button {
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .success-text { color: #27ae60; }
    .warning-text { color: #f39c12; }
    .danger-text { color: #e74c3c; }
    .info-text { color: #3498db; }
    .card {
        background: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    .role-badge {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: bold;
        margin: 2px;
    }
    .badge-admin { background: #e74c3c; color: white; }
    .badge-prof { background: #3498db; color: white; }
    .badge-employee { background: #9b59b6; color: white; }
    .badge-student { background: #2ecc71; color: white; }
    .form-container {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #dee2e6;
    }
    .action-button {
        margin: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Classe pour la gestion d'authentification avec rôles
class AuthSystemPro:
    def __init__(self):
        self.users = self._load_users()
        self.logs = []
        self.actions_log = []
    
    def _load_users(self):
        # Utilisateurs par défaut avec tous les rôles
        return {
            "admin": {
                "password": self._hash_password("admin123"),
                "role": "admin",
                "name": "Projet Cloud",
                "email": "admin@university.edu",
                "phone": "+33 1 23 45 67 89",
                "specialite": "Administration",
                "experience": 10,
                "created_at": "2020-01-15"
            },
            "prof_dupont": {
                "password": self._hash_password("prof123"),
                "role": "professeur",
                "name": "Prof. Jean Dupont",
                "email": "j.dupont@university.edu",
                "phone": "+33 1 23 45 67 90",
                "specialite": "Informatique",
                "matieres": ["Algorithme", "Base de données"],
                "experience": 8,
                "heures_semaine": 18,
                "classes": ["Licence 1 Info", "Master 1 Info"],
                "created_at": "2020-03-20"
            },
            "employee_secretary": {
                "password": self._hash_password("emp123"),
                "role": "employee",
                "name": "Marie Lambert",
                "email": "m.lambert@university.edu",
                "phone": "+33 1 23 45 67 91",
                "service": "Secrétariat",
                "poste": "Secrétaire administrative",
                "date_recrutement": "2019-06-15",
                "created_at": "2019-06-15"
            },
            "etud_martin": {
                "password": self._hash_password("etu123"),
                "role": "etudiant",
                "name": "Jean Martin",
                "email": "j.martin@university.edu",
                "phone": "+33 6 12 34 56 78",
                "cne": "CNE100001",
                "filiere": "Informatique",
                "niveau": "Licence 2",
                "ville": "Paris",
                "sexe": "M",
                "date_naissance": "2002-05-15",
                "annee_inscription": 2021,
                "created_at": "2021-09-01"
            }
        }
    
    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def login(self, username, password):
        if username in self.users:
            if self.users[username]["password"] == self._hash_password(password):
                # Log de connexion
                self.logs.append({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "username": username,
                    "action": "login_success",
                    "ip": "192.168.1.1"
                })
                return {
                    "username": username,
                    "role": self.users[username]["role"],
                    "name": self.users[username]["name"],
                    "details": self.users[username]
                }
        
        # Log d'échec
        self.logs.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "username": username,
            "action": "login_failed",
            "ip": "192.168.1.1"
        })
        return None
    
    def log_action(self, user, action, details=""):
        """Journaliser les actions importantes"""
        self.actions_log.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user": user,
            "action": action,
            "details": details
        })

# Classe pour la gestion des données CRUD
class DataManager:
    def __init__(self):
        self.fake = Faker('fr_FR')
        self.students = self._load_initial_students()
        self.professors = self._load_initial_professors()
        self.employees = self._load_initial_employees()
        self.grades = self._generate_grades(self.students)
        self.timetable = self._generate_timetable(self.professors)
    
    def _load_initial_students(self):
        """Charger les étudiants initiaux"""
        students = []
        filieres = ['Informatique', 'Mathématiques', 'Physique', 'Chimie', 'Biologie', 'Économie', 'Droit']
        niveaux = ['Licence 1', 'Licence 2', 'Licence 3', 'Master 1', 'Master 2']
        villes = ['Paris', 'Lyon', 'Marseille', 'Toulouse', 'Nice', 'Nantes', 'Strasbourg']
        sexes = ['M', 'F']
        statuts = ['Actif', 'Suspendu', 'Diplômé']
        
        for i in range(50):
            sexe = np.random.choice(sexes, p=[0.55, 0.45])
            if sexe == 'M':
                prenom = self.fake.first_name_male()
            else:
                prenom = self.fake.first_name_female()
            
            filiere = np.random.choice(filieres, p=[0.25, 0.15, 0.15, 0.1, 0.1, 0.15, 0.1])
            
            student = {
                'id': str(uuid.uuid4())[:8],
                'cne': f'CNE{str(i+1000).zfill(6)}',
                'nom': self.fake.last_name(),
                'prenom': prenom,
                'sexe': sexe,
                'date_naissance': self.fake.date_of_birth(minimum_age=18, maximum_age=25).strftime('%Y-%m-%d'),
                'ville': np.random.choice(villes),
                'email': self.fake.email(),
                'telephone': self.fake.phone_number(),
                'specialite': filiere,
                'classe': f"{filiere[:3]}-{np.random.randint(1, 6)}",
                'niveau': np.random.choice(niveaux),
                'annee_universitaire': np.random.randint(2019, 2024),
                'statut': np.random.choice(statuts, p=[0.85, 0.1, 0.05]),
                'moyenne_generale': round(np.random.uniform(8, 18), 2),
                'taux_absence': round(np.random.uniform(0, 35), 1),
                'credits_obtenus': np.random.randint(0, 180),
                'credits_totaux': 180,
                'date_inscription': self.fake.date_between(start_date='-4years', end_date='today').strftime('%Y-%m-%d'),
                'valide': np.random.random() > 0.3
            }
            students.append(student)
        
        return pd.DataFrame(students)
    
    def _load_initial_professors(self):
        """Charger les professeurs initiaux"""
        professors = []
        specialites = ['Informatique', 'Mathématiques', 'Physique', 'Chimie', 'Biologie', 'Économie', 'Droit']
        statuts = ['Permanent', 'Vacataire']
        villes = ['Paris', 'Lyon', 'Marseille', 'Toulouse']
        
        for i in range(15):
            sexe = np.random.choice(['M', 'F'], p=[0.6, 0.4])
            if sexe == 'M':
                prenom = self.fake.first_name_male()
            else:
                prenom = self.fake.first_name_female()
            
            specialite = np.random.choice(specialites)
            
            professor = {
                'id': str(uuid.uuid4())[:8],
                'nom': self.fake.last_name(),
                'prenom': prenom,
                'sexe': sexe,
                'specialite': specialite,
                'matieres': ', '.join(self._get_matieres_by_specialite(specialite)[:3]),
                'experience': np.random.randint(2, 30),
                'email': f"{prenom.lower()}.{self.fake.last_name().lower()}@university.edu",
                'telephone': self.fake.phone_number(),
                'ville': np.random.choice(villes),
                'statut': np.random.choice(statuts, p=[0.7, 0.3]),
                'heures_semaine': np.random.randint(12, 25),
                'classes_assigned': np.random.randint(2, 6),
                'date_embauche': self.fake.date_between(start_date='-20years', end_date='-1year').strftime('%Y-%m-%d'),
                'salaire_grade': np.random.choice(['A', 'B', 'C', 'D'], p=[0.2, 0.4, 0.3, 0.1]),
                'taux_presence': round(np.random.uniform(85, 100), 1),
                'derniere_evaluation': round(np.random.uniform(3, 5), 1)
            }
            professors.append(professor)
        
        return pd.DataFrame(professors)
    
    def _load_initial_employees(self):
        """Charger les employés initiaux"""
        employees = []
        services = ['Secrétariat', 'Administration', 'Comptabilité', 'Bibliothèque', 'Technique / IT', 'Surveillance']
        postes = {
            'Secrétariat': ['Secrétaire administratif', 'Assistant de direction', 'Accueil'],
            'Administration': ['Responsable administratif', 'Gestionnaire', 'Coordinateur'],
            'Comptabilité': ['Comptable', 'Responsable financier', 'Assistant comptable'],
            'Bibliothèque': ['Bibliothécaire', 'Documentaliste', 'Assistant bibliothèque'],
            'Technique / IT': ['Technicien informatique', 'Administrateur réseau', 'Support technique'],
            'Surveillance': ['Agent de surveillance', 'Responsable sécurité', 'Veilleur']
        }
        statuts = ['Actif', 'Congé', 'Retraité']
        villes = ['Paris', 'Lyon', 'Marseille', 'Toulouse']
        
        for i in range(30):
            sexe = np.random.choice(['M', 'F'], p=[0.5, 0.5])
            if sexe == 'M':
                prenom = self.fake.first_name_male()
            else:
                prenom = self.fake.first_name_female()
            
            service = np.random.choice(services)
            poste = np.random.choice(postes[service])
            
            # Générer un salaire réaliste selon le poste
            salaire_base = {
                'Secrétaire administratif': 2200,
                'Assistant de direction': 2800,
                'Accueil': 1900,
                'Responsable administratif': 3500,
                'Gestionnaire': 2700,
                'Coordinateur': 3200,
                'Comptable': 2800,
                'Responsable financier': 4500,
                'Assistant comptable': 2300,
                'Bibliothécaire': 2400,
                'Documentaliste': 2500,
                'Assistant bibliothèque': 2000,
                'Technicien informatique': 2600,
                'Administrateur réseau': 3800,
                'Support technique': 2300,
                'Agent de surveillance': 2100,
                'Responsable sécurité': 3200,
                'Veilleur': 2000
            }.get(poste, 2500)
            
            # Ajouter de la variation
            salaire = salaire_base + np.random.randint(-200, 200)
            
            employee = {
                'id': str(uuid.uuid4())[:8],
                'nom': self.fake.last_name(),
                'prenom': prenom,
                'sexe': sexe,
                'poste': poste,
                'service': service,
                'date_recrutement': self.fake.date_between(start_date='-15years', end_date='-1month').strftime('%Y-%m-%d'),
                'salaire': salaire,
                'email': f"{prenom.lower()}.{self.fake.last_name().lower()}@university.edu",
                'telephone': self.fake.phone_number(),
                'ville': np.random.choice(villes),
                'statut': np.random.choice(statuts, p=[0.85, 0.1, 0.05]),
                'experience': np.random.randint(1, 20),
                'evaluation': round(np.random.uniform(3, 5), 1),
                'taux_presence': round(np.random.uniform(90, 100), 1)
            }
            employees.append(employee)
        
        return pd.DataFrame(employees)
    
    def _get_matieres_by_specialite(self, specialite):
        matieres_dict = {
            'Informatique': ['Algorithme', 'Base de données', 'Réseaux', 'Web', 'IA', 'Sécurité', 'DevOps'],
            'Mathématiques': ['Algèbre', 'Analyse', 'Probabilité', 'Statistique', 'Topologie', 'Calcul différentiel'],
            'Physique': ['Mécanique', 'Electromagnétisme', 'Quantique', 'Thermodynamique', 'Optique', 'Astrophysique'],
            'Chimie': ['Organique', 'Minérale', 'Analytique', 'Physico-chimie', 'Biochimie', 'Chimie verte'],
            'Biologie': ['Génétique', 'Biologie cellulaire', 'Écologie', 'Physiologie', 'Microbiologie', 'Bioinformatique'],
            'Économie': ['Microéconomie', 'Macroéconomie', 'Économétrie', 'Finance', 'Marketing', 'Stratégie'],
            'Droit': ['Droit civil', 'Droit pénal', 'Droit commercial', 'Droit international', 'Droit administratif']
        }
        return matieres_dict.get(specialite, ['Mathématiques', 'Sciences'])
    
    def _generate_grades(self, students_df):
        """Générer des notes"""
        grades = []
        
        for _, student in students_df.iterrows():
            modules = self._get_matieres_by_specialite(student['specialite'])
            
            for module in modules[:4]:
                for exam_type in ['Contrôle 1', 'Contrôle 2', 'Examen Final']:
                    base_note = student['moyenne_generale']
                    variation = np.random.uniform(-3, 3)
                    note = max(0, min(20, round(base_note + variation, 2)))
                    
                    grade = {
                        'student_id': student['id'],
                        'cne': student['cne'],
                        'nom': student['nom'],
                        'prenom': student['prenom'],
                        'module': module,
                        'examen': exam_type,
                        'note': note,
                        'coefficient': 1 if exam_type != 'Examen Final' else 2,
                        'date': self.fake.date_between(start_date='-6months', end_date='today').strftime('%Y-%m-%d'),
                        'professeur': self.fake.name(),
                        'valide': note >= 10
                    }
                    grades.append(grade)
        
        return pd.DataFrame(grades)
    
    def _generate_timetable(self, professors_df):
        """Générer un emploi du temps"""
        jours = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi']
        heures = ['08:00-10:00', '10:15-12:15', '14:00-16:00', '16:15-18:15']
        salles = ['A101', 'A102', 'A201', 'A202', 'B101', 'B102']
        
        timetable = []
        prof_names = list(professors_df['prenom'] + ' ' + professors_df['nom'])
        
        for _ in range(100):
            prof = np.random.choice(prof_names)
            
            seance = {
                'id': f"SE{_:04d}",
                'jour': np.random.choice(jours),
                'heure': np.random.choice(heures),
                'salle': np.random.choice(salles),
                'module': np.random.choice(['Algorithme', 'Base de données', 'Réseaux', 'Mathématiques', 'Physique']),
                'professeur': prof,
                'classe': f"Classe {np.random.randint(1, 10)}",
                'groupe': f"Groupe {np.random.choice(['A', 'B', 'C'])}",
                'type_cours': np.random.choice(['Cours', 'TD', 'TP'], p=[0.4, 0.3, 0.3]),
                'semestre': np.random.choice(['S1', 'S2', 'S3', 'S4']),
                'effectif': np.random.randint(20, 40),
                'presence_reelle': np.random.randint(15, 35)
            }
            seance['taux_presence'] = round((seance['presence_reelle'] / seance['effectif']) * 100, 1)
            timetable.append(seance)
        
        return pd.DataFrame(timetable)

# Initialisation des systèmes
auth_system = AuthSystemPro()
data_manager = DataManager()

# Session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_info' not in st.session_state:
    st.session_state.user_info = None
if 'students' not in st.session_state:
    st.session_state.students = data_manager.students
if 'professors' not in st.session_state:
    st.session_state.professors = data_manager.professors
if 'employees' not in st.session_state:
    st.session_state.employees = data_manager.employees
if 'grades' not in st.session_state:
    st.session_state.grades = data_manager.grades
if 'timetable' not in st.session_state:
    st.session_state.timetable = data_manager.timetable
if 'selected_student_id' not in st.session_state:
    st.session_state.selected_student_id = None
if 'selected_professor_id' not in st.session_state:
    st.session_state.selected_professor_id = None
if 'selected_employee_id' not in st.session_state:
    st.session_state.selected_employee_id = None
if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False

# Fonction de connexion
def login_page():
    st.markdown("<h1 class='main-header'> Système de Gestion Universitaire </h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("###  Connexion au Système")
        
        with st.form("login_form"):
            username = st.text_input("Nom d'utilisateur")
            password = st.text_input("Mot de passe", type="password")
            submit = st.form_submit_button("Se connecter", use_container_width=True)
            
            if submit:
                user_info = auth_system.login(username, password)
                if user_info:
                    st.session_state.authenticated = True
                    st.session_state.user_info = user_info
                    st.success(f"✅ Bienvenue {user_info['name']} !")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Identifiants incorrects !")
        
        st.markdown("---")
        st.markdown("#### 📋 Comptes de démo :")
        
        col_a, col_b, col_c, col_d = st.columns(4)
        
        with col_a:
            st.markdown("**Admin**")
            st.code("admin / admin123")
            st.markdown("<span class='badge badge-admin'>Administrateur</span>", unsafe_allow_html=True)
        
        with col_b:
            st.markdown("**Professeur**")
            st.code("prof_dupont / prof123")
            st.markdown("<span class='badge badge-prof'>Professeur</span>", unsafe_allow_html=True)
        
        with col_c:
            st.markdown("**Employé**")
            st.code("employee_secretary / emp123")
            st.markdown("<span class='badge badge-employee'>Employé</span>", unsafe_allow_html=True)
        
        with col_d:
            st.markdown("**Étudiant**")
            st.code("etud_martin / etu123")
            st.markdown("<span class='badge badge-student'>Étudiant</span>", unsafe_allow_html=True)

# Fonction principale de l'application
def main_app():
    # Sidebar
    with st.sidebar:
        role = st.session_state.user_info['role']
        badge_class = f"badge-{role}"
        
        st.markdown(f"### 👤 {st.session_state.user_info['name']}")
        st.markdown(f"<span class='role-badge {badge_class}'>{role.title()}</span>", unsafe_allow_html=True)
        
        if role == 'professeur':
            prof_details = st.session_state.user_info['details']
            st.markdown(f"**Spécialité:** {prof_details.get('specialite', 'Non spécifié')}")
        elif role == 'employee':
            emp_details = st.session_state.user_info['details']
            st.markdown(f"**Service:** {emp_details.get('service', 'Non spécifié')}")
        
        st.markdown("---")
        
        # Menu selon le rôle
        menu_options = ["📊 Tableau de Bord"]
        
        if role in ['admin', 'professeur']:
            menu_options.extend(["👨‍🎓 Gestion Étudiants", "📝 Système de Notes", "🕒 Emploi du Temps"])
        
        if role == 'professeur':
            menu_options.extend(["👨‍🏫 Mon Dashboard Professeur", "📚 Mes Matières"])
        
        if role == 'employee':
            menu_options.extend(["👔 Mon Espace Employé", "📋 Gestion Documents"])
        
        if role == 'etudiant':
            menu_options.extend(["📚 Mon Espace Étudiant", "📅 Mon Emploi du Temps", "📈 Ma Progression"])
        
        if role == 'admin':
            menu_options.extend([
                "👨‍🎓 CRUD Étudiants", 
                "👨‍🏫 CRUD Professeurs", 
                "👔 CRUD Employés",
                "📈 Statistiques Avancées",
                "📊 Dashboard Admin Global",
                "🔒 Administration Système"
            ])
        
        menu_options.append("❓ Aide & Support")
        
        selected_page = st.selectbox("Navigation", menu_options)
        
        st.markdown("---")
        
        # Informations rapides
        if role == 'admin':
            total_students = len(st.session_state.students)
            total_professors = len(st.session_state.professors)
            total_employees = len(st.session_state.employees)
            
            st.metric("Étudiants", total_students)
            st.metric("Professeurs", total_professors)
            st.metric("Employés", total_employees)
        
        st.markdown("---")
        
        if st.button("🚪 Déconnexion", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_info = None
            st.rerun()
    
    # Pages
    if selected_page == "📊 Tableau de Bord":
        show_main_dashboard()
    elif selected_page == "👨‍🎓 Gestion Étudiants":
        show_students_management()
    elif selected_page == "👨‍🎓 CRUD Étudiants":
        show_crud_students()
    elif selected_page == "👨‍🏫 CRUD Professeurs":
        show_crud_professors()
    elif selected_page == "👔 CRUD Employés":
        show_crud_employees()
    elif selected_page == "📊 Dashboard Admin Global":
        show_admin_global_dashboard()
    elif selected_page == "👔 Mon Espace Employé":
        show_employee_dashboard()
    elif selected_page == "🔒 Administration Système":
        show_system_administration()
    elif selected_page == "📝 Système de Notes":
        show_grades_system()
    elif selected_page == "🕒 Emploi du Temps":
        show_timetable_system()
    elif selected_page == "👨‍🏫 Mon Dashboard Professeur":
        show_professor_dashboard()
    elif selected_page == "📚 Mes Matières":
        show_professor_subjects()
    elif selected_page == "📚 Mon Espace Étudiant":
        show_student_dashboard()
    elif selected_page == "📅 Mon Emploi du Temps":
        show_student_timetable()
    elif selected_page == "📈 Ma Progression":
        show_student_progression()
    elif selected_page == "📈 Statistiques Avancées":
        show_advanced_statistics()
    elif selected_page == "📋 Gestion Documents":
        show_document_management()
    elif selected_page == "❓ Aide & Support":
        show_help_support()

# Page CRUD Étudiants
def show_crud_students():
    """CRUD complet pour les étudiants"""
    st.markdown("<h1 class='main-header'>👨‍🎓 CRUD Étudiants</h1>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Liste des Étudiants", "➕ Ajouter un Étudiant", "✏️ Modifier un Étudiant", "📊 Statistiques"])
    
    with tab1:
        # Filtres de recherche
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            search_term = st.text_input("Rechercher (nom, prénom, CNE)")
        
        with col2:
            filiere_filter = st.multiselect("Filière", 
                                          st.session_state.students['specialite'].unique())
        
        with col3:
            niveau_filter = st.multiselect("Niveau", 
                                         st.session_state.students['niveau'].unique())
        
        with col4:
            statut_filter = st.multiselect("Statut", 
                                         st.session_state.students['statut'].unique())
        
        # Appliquer les filtres
        filtered_students = st.session_state.students.copy()
        
        if search_term:
            mask = (filtered_students['nom'].str.contains(search_term, case=False) | 
                   filtered_students['prenom'].str.contains(search_term, case=False) |
                   filtered_students['cne'].str.contains(search_term, case=False))
            filtered_students = filtered_students[mask]
        
        if filiere_filter:
            filtered_students = filtered_students[filtered_students['specialite'].isin(filiere_filter)]
        
        if niveau_filter:
            filtered_students = filtered_students[filtered_students['niveau'].isin(niveau_filter)]
        
        if statut_filter:
            filtered_students = filtered_students[filtered_students['statut'].isin(statut_filter)]
        
        # Actions sur la liste
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📥 Importer CSV", use_container_width=True):
                show_import_csv('students')
        
        with col2:
            if st.button("📤 Exporter CSV", use_container_width=True):
                show_export_csv(filtered_students, 'etudiants')
        
        with col3:
            if st.button("🖨️ Générer Rapport", use_container_width=True):
                show_students_report(filtered_students)
        
        # Affichage des étudiants
        st.subheader(f"📋 Liste des Étudiants ({len(filtered_students)} résultats)")
        
        # Sélection des colonnes à afficher
        display_cols = ['cne', 'nom', 'prenom', 'sexe', 'specialite', 'niveau', 'classe', 
                       'ville', 'statut', 'moyenne_generale', 'taux_absence']
        
        # Affichage du tableau avec actions
        st.dataframe(
            filtered_students[display_cols],
            use_container_width=True,
            height=400,
            column_config={
                "cne": st.column_config.TextColumn("CNE", width="small"),
                "nom": st.column_config.TextColumn("Nom", width="medium"),
                "prenom": st.column_config.TextColumn("Prénom", width="medium"),
                "sexe": st.column_config.TextColumn("Sexe", width="small"),
                "specialite": st.column_config.TextColumn("Spécialité", width="medium"),
                "niveau": st.column_config.TextColumn("Niveau", width="medium"),
                "classe": st.column_config.TextColumn("Classe", width="medium"),
                "ville": st.column_config.TextColumn("Ville", width="medium"),
                "statut": st.column_config.SelectboxColumn(
                    "Statut",
                    options=["Actif", "Suspendu", "Diplômé"],
                    width="medium"
                ),
                "moyenne_generale": st.column_config.NumberColumn(
                    "Moyenne",
                    format="%.2f",
                    width="small"
                ),
                "taux_absence": st.column_config.NumberColumn(
                    "Absence %",
                    format="%.1f",
                    width="small"
                )
            }
        )
        
        # Actions sur les lignes sélectionnées
        if not filtered_students.empty:
            selected_index = st.number_input(
                "Sélectionner l'index de l'étudiant à modifier/supprimer",
                min_value=0,
                max_value=len(filtered_students)-1,
                value=0
            )
            
            selected_student = filtered_students.iloc[selected_index]
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("✏️ Modifier cet étudiant", use_container_width=True):
                    st.session_state.selected_student_id = selected_student['id']
                    st.session_state.edit_mode = True
                    st.rerun()
            
            with col2:
                if st.button("❌ Supprimer cet étudiant", type="secondary", use_container_width=True):
                    if st.checkbox("Confirmer la suppression"):
                        delete_student(selected_student['id'])
                        st.success("Étudiant supprimé avec succès !")
                        st.rerun()
    
    with tab2:
        show_add_student_form()
    
    with tab3:
        if st.session_state.edit_mode and st.session_state.selected_student_id:
            show_edit_student_form(st.session_state.selected_student_id)
        else:
            st.info("Veuillez sélectionner un étudiant à modifier depuis l'onglet 'Liste des Étudiants'")
    
    with tab4:
        show_students_statistics()

def show_add_student_form():
    """Formulaire d'ajout d'étudiant"""
    st.subheader("➕ Ajouter un Nouvel Étudiant")
    
    with st.form("add_student_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            cne = st.text_input("CNE *", help="Code National de l'Étudiant")
            nom = st.text_input("Nom *")
            prenom = st.text_input("Prénom *")
            sexe = st.selectbox("Sexe *", ["M", "F"])
            date_naissance = st.date_input("Date de naissance *", 
                                         min_value=datetime(1970, 1, 1),
                                         max_value=datetime(2006, 12, 31))
            ville = st.text_input("Ville *")
        
        with col2:
            email = st.text_input("Email *")
            telephone = st.text_input("Téléphone *")
            specialite = st.selectbox("Spécialité *", 
                                    ['Informatique', 'Mathématiques', 'Physique', 'Chimie', 
                                     'Biologie', 'Économie', 'Droit'])
            classe = st.text_input("Classe *", placeholder="Ex: INFO-3")
            niveau = st.selectbox("Niveau *", 
                                ['Licence 1', 'Licence 2', 'Licence 3', 'Master 1', 'Master 2'])
            annee_universitaire = st.number_input("Année universitaire *", 
                                                min_value=2010, max_value=2024, value=2023)
            statut = st.selectbox("Statut *", ["Actif", "Suspendu", "Diplômé"])
        
        # Champs optionnels
        col1, col2 = st.columns(2)
        
        with col1:
            moyenne_generale = st.number_input("Moyenne générale", min_value=0.0, max_value=20.0, value=10.0)
            taux_absence = st.number_input("Taux d'absence (%)", min_value=0.0, max_value=100.0, value=0.0)
        
        with col2:
            credits_obtenus = st.number_input("Crédits obtenus", min_value=0, max_value=180, value=0)
            date_inscription = st.date_input("Date d'inscription", value=datetime.now())
        
        submitted = st.form_submit_button("➕ Ajouter l'étudiant", use_container_width=True)
        
        if submitted:
            # Validation
            if not all([cne, nom, prenom, email, telephone, specialite, classe, niveau]):
                st.error("Veuillez remplir tous les champs obligatoires (*)")
            else:
                # Ajouter l'étudiant
                new_student = {
                    'id': str(uuid.uuid4())[:8],
                    'cne': cne,
                    'nom': nom,
                    'prenom': prenom,
                    'sexe': sexe,
                    'date_naissance': date_naissance.strftime('%Y-%m-%d'),
                    'ville': ville,
                    'email': email,
                    'telephone': telephone,
                    'specialite': specialite,
                    'classe': classe,
                    'niveau': niveau,
                    'annee_universitaire': annee_universitaire,
                    'statut': statut,
                    'moyenne_generale': moyenne_generale,
                    'taux_absence': taux_absence,
                    'credits_obtenus': credits_obtenus,
                    'credits_totaux': 180,
                    'date_inscription': date_inscription.strftime('%Y-%m-%d'),
                    'valide': moyenne_generale >= 10
                }
                
                # Ajouter à la liste
                new_df = pd.DataFrame([new_student])
                st.session_state.students = pd.concat([st.session_state.students, new_df], ignore_index=True)
                
                # Journaliser l'action
                auth_system.log_action(
                    st.session_state.user_info['username'],
                    "Ajout étudiant",
                    f"Étudiant ajouté: {nom} {prenom} ({cne})"
                )
                
                st.success(f"✅ Étudiant {nom} {prenom} ajouté avec succès !")
                st.balloons()

def show_edit_student_form(student_id):
    """Formulaire de modification d'étudiant"""
    student = st.session_state.students[st.session_state.students['id'] == student_id]
    
    if student.empty:
        st.error("Étudiant non trouvé")
        return
    
    student = student.iloc[0]
    
    st.subheader(f"✏️ Modification de l'étudiant: {student['nom']} {student['prenom']}")
    
    with st.form("edit_student_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            cne = st.text_input("CNE *", value=student['cne'])
            nom = st.text_input("Nom *", value=student['nom'])
            prenom = st.text_input("Prénom *", value=student['prenom'])
            sexe = st.selectbox("Sexe *", ["M", "F"], index=0 if student['sexe'] == 'M' else 1)
            date_naissance = st.date_input("Date de naissance *", 
                                         value=datetime.strptime(student['date_naissance'], '%Y-%m-%d'))
            ville = st.text_input("Ville *", value=student['ville'])
        
        with col2:
            email = st.text_input("Email *", value=student['email'])
            telephone = st.text_input("Téléphone *", value=student['telephone'])
            specialite = st.selectbox("Spécialité *", 
                                    ['Informatique', 'Mathématiques', 'Physique', 'Chimie', 
                                     'Biologie', 'Économie', 'Droit'],
                                    index=['Informatique', 'Mathématiques', 'Physique', 'Chimie', 
                                           'Biologie', 'Économie', 'Droit'].index(student['specialite']))
            classe = st.text_input("Classe *", value=student['classe'])
            niveau = st.selectbox("Niveau *", 
                                ['Licence 1', 'Licence 2', 'Licence 3', 'Master 1', 'Master 2'],
                                index=['Licence 1', 'Licence 2', 'Licence 3', 'Master 1', 'Master 2'].index(student['niveau']))
            annee_universitaire = st.number_input("Année universitaire *", 
                                                value=int(student['annee_universitaire']))
            statut = st.selectbox("Statut *", ["Actif", "Suspendu", "Diplômé"],
                                index=["Actif", "Suspendu", "Diplômé"].index(student['statut']))
        
        # Champs optionnels
        col1, col2 = st.columns(2)
        
        with col1:
            moyenne_generale = st.number_input("Moyenne générale", 
                                             value=float(student['moyenne_generale']))
            taux_absence = st.number_input("Taux d'absence (%)", 
                                         value=float(student['taux_absence']))
        
        with col2:
            credits_obtenus = st.number_input("Crédits obtenus", 
                                            value=int(student['credits_obtenus']))
            date_inscription = st.date_input("Date d'inscription", 
                                           value=datetime.strptime(student['date_inscription'], '%Y-%m-%d'))
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            submitted = st.form_submit_button("💾 Enregistrer les modifications", use_container_width=True)
        
        with col2:
            if st.form_submit_button("❌ Annuler", use_container_width=True):
                st.session_state.edit_mode = False
                st.session_state.selected_student_id = None
                st.rerun()
        
        with col3:
            if st.form_submit_button("🗑️ Supprimer cet étudiant", type="secondary", use_container_width=True):
                if st.checkbox("Confirmer la suppression", key="delete_confirm"):
                    delete_student(student_id)
                    st.session_state.edit_mode = False
                    st.session_state.selected_student_id = None
                    st.success("Étudiant supprimé avec succès !")
                    time.sleep(1)
                    st.rerun()
        
        if submitted:
            # Validation
            if not all([cne, nom, prenom, email, telephone, specialite, classe, niveau]):
                st.error("Veuillez remplir tous les champs obligatoires (*)")
            else:
                # Mettre à jour l'étudiant
                updated_student = {
                    'id': student_id,
                    'cne': cne,
                    'nom': nom,
                    'prenom': prenom,
                    'sexe': sexe,
                    'date_naissance': date_naissance.strftime('%Y-%m-%d'),
                    'ville': ville,
                    'email': email,
                    'telephone': telephone,
                    'specialite': specialite,
                    'classe': classe,
                    'niveau': niveau,
                    'annee_universitaire': annee_universitaire,
                    'statut': statut,
                    'moyenne_generale': moyenne_generale,
                    'taux_absence': taux_absence,
                    'credits_obtenus': credits_obtenus,
                    'credits_totaux': 180,
                    'date_inscription': date_inscription.strftime('%Y-%m-%d'),
                    'valide': moyenne_generale >= 10
                }
                
                # Mettre à jour dans le DataFrame
                idx = st.session_state.students[st.session_state.students['id'] == student_id].index
                if not idx.empty:
                    for key, value in updated_student.items():
                        st.session_state.students.at[idx[0], key] = value
                
                # Journaliser l'action
                auth_system.log_action(
                    st.session_state.user_info['username'],
                    "Modification étudiant",
                    f"Étudiant modifié: {nom} {prenom} ({cne})"
                )
                
                st.success(f"✅ Étudiant {nom} {prenom} modifié avec succès !")
                time.sleep(1)
                st.session_state.edit_mode = False
                st.session_state.selected_student_id = None
                st.rerun()

def delete_student(student_id):
    """Supprimer un étudiant"""
    st.session_state.students = st.session_state.students[st.session_state.students['id'] != student_id]
    
    # Journaliser l'action
    auth_system.log_action(
        st.session_state.user_info['username'],
        "Suppression étudiant",
        f"Étudiant supprimé: ID {student_id}"
    )

def show_import_csv(data_type):
    """Afficher l'interface d'import CSV"""
    st.subheader("📥 Import CSV/Excel")
    
    uploaded_file = st.file_uploader(
        f"Choisir un fichier {data_type}",
        type=['csv', 'xlsx', 'xls']
    )
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.success(f"Fichier chargé avec succès ({len(df)} enregistrements)")
            
            # Aperçu des données
            st.subheader("Aperçu des données")
            st.dataframe(df.head(), use_container_width=True)
            
            # Mapping des colonnes
            st.subheader("Mapping des colonnes")
            
            # Déterminer les colonnes attendues selon le type de données
            if data_type == 'students':
                expected_columns = ['cne', 'nom', 'prenom', 'sexe', 'date_naissance', 
                                  'ville', 'email', 'telephone', 'specialite', 'classe', 
                                  'niveau', 'annee_universitaire', 'statut']
            elif data_type == 'professors':
                expected_columns = ['nom', 'prenom', 'sexe', 'specialite', 'matieres',
                                  'experience', 'email', 'telephone', 'ville', 'statut']
            else:  # employees
                expected_columns = ['nom', 'prenom', 'sexe', 'poste', 'service',
                                  'date_recrutement', 'salaire', 'email', 'telephone', 'statut']
            
            col_mapping = {}
            for expected_col in expected_columns:
                available_cols = ['---'] + list(df.columns)
                selected_col = st.selectbox(
                    f"Colonne pour '{expected_col}'",
                    available_cols,
                    key=f"map_{expected_col}"
                )
                if selected_col != '---':
                    col_mapping[expected_col] = selected_col
            
            if st.button("✅ Confirmer l'import", use_container_width=True):
                # Vérifier que les colonnes obligatoires sont mappées
                required_cols = expected_columns[:5]  # Premières colonnes sont obligatoires
                missing_cols = [col for col in required_cols if col not in col_mapping]
                
                if missing_cols:
                    st.error(f"Colonnes obligatoires non mappées: {', '.join(missing_cols)}")
                else:
                    # Préparer les données
                    imported_data = []
                    
                    for _, row in df.iterrows():
                        record = {}
                        for target_col, source_col in col_mapping.items():
                            if source_col in df.columns:
                                record[target_col] = row[source_col]
                            else:
                                record[target_col] = None
                        
                        # Ajouter un ID unique
                        record['id'] = str(uuid.uuid4())[:8]
                        
                        # Ajouter des champs supplémentaires selon le type
                        if data_type == 'students':
                            record['moyenne_generale'] = 10.0
                            record['taux_absence'] = 0.0
                            record['credits_obtenus'] = 0
                            record['credits_totaux'] = 180
                            record['date_inscription'] = datetime.now().strftime('%Y-%m-%d')
                            record['valide'] = True
                        
                        imported_data.append(record)
                    
                    # Fusionner avec les données existantes
                    imported_df = pd.DataFrame(imported_data)
                    
                    if data_type == 'students':
                        st.session_state.students = pd.concat([st.session_state.students, imported_df], ignore_index=True)
                    elif data_type == 'professors':
                        st.session_state.professors = pd.concat([st.session_state.professors, imported_df], ignore_index=True)
                    else:
                        st.session_state.employees = pd.concat([st.session_state.employees, imported_df], ignore_index=True)
                    
                    # Journaliser l'action
                    auth_system.log_action(
                        st.session_state.user_info['username'],
                        f"Import {data_type}",
                        f"{len(imported_data)} enregistrements importés"
                    )
                    
                    st.success(f"✅ {len(imported_data)} enregistrements importés avec succès !")
                    st.balloons()
                    
        except Exception as e:
            st.error(f"Erreur lors du chargement du fichier: {str(e)}")

def show_export_csv(df, filename):
    """Exporter des données en CSV"""
    csv = df.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="📥 Télécharger le fichier CSV",
        data=csv,
        file_name=f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True
    )

def show_students_report(df):
    """Générer un rapport des étudiants"""
    st.subheader("📊 Rapport des Étudiants")
    
    # Statistiques
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total = len(df)
        st.metric("Total étudiants", total)
    
    with col2:
        active = len(df[df['statut'] == 'Actif'])
        st.metric("Actifs", active, f"{active/total*100:.1f}%")
    
    with col3:
        avg_grade = df['moyenne_generale'].mean()
        st.metric("Moyenne générale", f"{avg_grade:.2f}/20")
    
    with col4:
        avg_absence = df['taux_absence'].mean()
        st.metric("Absence moyenne", f"{avg_absence:.1f}%")
    
    # Visualisations
    col1, col2 = st.columns(2)
    
    with col1:
        # Répartition par spécialité
        specialite_counts = df['specialite'].value_counts()
        fig = px.bar(x=specialite_counts.index, y=specialite_counts.values,
                    title="Répartition par spécialité",
                    labels={'x': 'Spécialité', 'y': 'Nombre d\'étudiants'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Répartition par niveau
        niveau_counts = df['niveau'].value_counts()
        fig = px.pie(values=niveau_counts.values, names=niveau_counts.index,
                    title="Répartition par niveau")
        st.plotly_chart(fig, use_container_width=True)
    
    # Bouton de téléchargement du rapport complet
    if st.button("📄 Générer rapport PDF", use_container_width=True):
        st.info("Fonctionnalité PDF à implémenter")
        st.success("Rapport généré avec succès !")

def show_students_statistics():
    """Afficher les statistiques des étudiants"""
    st.subheader("📊 Statistiques Globales des Étudiants")
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total = len(st.session_state.students)
        st.metric("Total étudiants", total)
    
    with col2:
        validated = st.session_state.students['valide'].sum()
        rate = (validated / total * 100) if total > 0 else 0
        st.metric("Validés", validated, f"{rate:.1f}%")
    
    with col3:
        avg_grade = st.session_state.students['moyenne_generale'].mean()
        st.metric("Moyenne générale", f"{avg_grade:.2f}/20")
    
    with col4:
        avg_absence = st.session_state.students['taux_absence'].mean()
        st.metric("Absence moyenne", f"{avg_absence:.1f}%")
    
    # Graphiques avancés
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution des moyennes
        fig = px.histogram(st.session_state.students, x='moyenne_generale', nbins=20,
                          title="Distribution des moyennes",
                          color_discrete_sequence=['#3498db'])
        fig.add_vline(x=10, line_dash="dash", line_color="red", annotation_text="Seuil validation")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Corrélation absence/moyenne
        fig = px.scatter(st.session_state.students, x='taux_absence', y='moyenne_generale',
                        color='specialite', hover_data=['nom', 'prenom', 'classe'],
                        title="Corrélation absence ↔ moyenne")
        st.plotly_chart(fig, use_container_width=True)
    
    # Top 10 des étudiants
    st.subheader("🏆 Top 10 des Étudiants")
    
    top_students = st.session_state.students.nlargest(10, 'moyenne_generale')[['cne', 'nom', 'prenom', 'specialite', 'niveau', 'moyenne_generale']]
    top_students['Classement'] = range(1, len(top_students) + 1)
    
    st.dataframe(top_students, use_container_width=True)

# Page CRUD Professeurs
def show_crud_professors():
    """CRUD complet pour les professeurs"""
    st.markdown("<h1 class='main-header'>👨‍🏫 CRUD Professeurs</h1>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Liste des Professeurs", "➕ Ajouter un Professeur", "✏️ Modifier un Professeur", "📊 Statistiques"])
    
    with tab1:
        # Filtres de recherche
        col1, col2, col3 = st.columns(3)
        
        with col1:
            search_term = st.text_input("Rechercher (nom, prénom, spécialité)", key="prof_search")
        
        with col2:
            specialite_filter = st.multiselect("Spécialité", 
                                             st.session_state.professors['specialite'].unique())
        
        with col3:
            statut_filter = st.multiselect("Statut", 
                                         st.session_state.professors['statut'].unique())
        
        # Appliquer les filtres
        filtered_professors = st.session_state.professors.copy()
        
        if search_term:
            mask = (filtered_professors['nom'].str.contains(search_term, case=False) | 
                   filtered_professors['prenom'].str.contains(search_term, case=False) |
                   filtered_professors['specialite'].str.contains(search_term, case=False))
            filtered_professors = filtered_professors[mask]
        
        if specialite_filter:
            filtered_professors = filtered_professors[filtered_professors['specialite'].isin(specialite_filter)]
        
        if statut_filter:
            filtered_professors = filtered_professors[filtered_professors['statut'].isin(statut_filter)]
        
        # Actions sur la liste
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📥 Importer CSV", use_container_width=True, key="prof_import"):
                show_import_csv('professors')
        
        with col2:
            if st.button("📤 Exporter CSV", use_container_width=True, key="prof_export"):
                show_export_csv(filtered_professors, 'professeurs')
        
        with col3:
            if st.button("🖨️ Générer Rapport", use_container_width=True, key="prof_report"):
                show_professors_report(filtered_professors)
        
        # Affichage des professeurs
        st.subheader(f"📋 Liste des Professeurs ({len(filtered_professors)} résultats)")
        
        # Sélection des colonnes à afficher
        display_cols = ['nom', 'prenom', 'sexe', 'specialite', 'matieres', 'experience', 
                       'statut', 'heures_semaine', 'classes_assigned', 'taux_presence']
        
        # Affichage du tableau avec actions
        st.dataframe(
            filtered_professors[display_cols],
            use_container_width=True,
            height=400,
            column_config={
                "nom": st.column_config.TextColumn("Nom", width="medium"),
                "prenom": st.column_config.TextColumn("Prénom", width="medium"),
                "sexe": st.column_config.TextColumn("Sexe", width="small"),
                "specialite": st.column_config.TextColumn("Spécialité", width="medium"),
                "matieres": st.column_config.TextColumn("Matières", width="large"),
                "experience": st.column_config.NumberColumn("Expérience (ans)", format="%d", width="small"),
                "statut": st.column_config.SelectboxColumn(
                    "Statut",
                    options=["Permanent", "Vacataire"],
                    width="medium"
                ),
                "heures_semaine": st.column_config.NumberColumn("Heures/semaine", format="%d", width="small"),
                "classes_assigned": st.column_config.NumberColumn("Classes", format="%d", width="small"),
                "taux_presence": st.column_config.NumberColumn("Présence %", format="%.1f", width="small")
            }
        )
        
        # Actions sur les lignes sélectionnées
        if not filtered_professors.empty:
            selected_index = st.number_input(
                "Sélectionner l'index du professeur à modifier/supprimer",
                min_value=0,
                max_value=len(filtered_professors)-1,
                value=0,
                key="prof_select"
            )
            
            selected_professor = filtered_professors.iloc[selected_index]
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("✏️ Modifier ce professeur", use_container_width=True, key="prof_edit"):
                    st.session_state.selected_professor_id = selected_professor['id']
                    st.rerun()
            
            with col2:
                if st.button("❌ Supprimer ce professeur", type="secondary", use_container_width=True, key="prof_delete"):
                    if st.checkbox("Confirmer la suppression", key="prof_delete_confirm"):
                        delete_professor(selected_professor['id'])
                        st.success("Professeur supprimé avec succès !")
                        st.rerun()
    
    with tab2:
        show_add_professor_form()
    
    with tab3:
        if st.session_state.selected_professor_id:
            show_edit_professor_form(st.session_state.selected_professor_id)
        else:
            st.info("Veuillez sélectionner un professeur à modifier depuis l'onglet 'Liste des Professeurs'")
    
    with tab4:
        show_professors_statistics()

def show_add_professor_form():
    """Formulaire d'ajout de professeur"""
    st.subheader("➕ Ajouter un Nouveau Professeur")
    
    with st.form("add_professor_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            nom = st.text_input("Nom *")
            prenom = st.text_input("Prénom *")
            sexe = st.selectbox("Sexe *", ["M", "F"])
            specialite = st.selectbox("Spécialité *", 
                                    ['Informatique', 'Mathématiques', 'Physique', 'Chimie', 
                                     'Biologie', 'Économie', 'Droit'])
            matieres = st.text_area("Matières enseignées *", 
                                  placeholder="Séparer par des virgules\nEx: Algorithme, Base de données, Réseaux")
            experience = st.number_input("Expérience (années) *", min_value=0, max_value=50, value=5)
        
        with col2:
            email = st.text_input("Email professionnel *", placeholder="prenom.nom@university.edu")
            telephone = st.text_input("Téléphone *")
            ville = st.text_input("Ville *")
            statut = st.selectbox("Statut *", ["Permanent", "Vacataire"])
            heures_semaine = st.number_input("Heures/semaine *", min_value=0, max_value=40, value=18)
            classes_assigned = st.number_input("Classes assignées *", min_value=0, max_value=10, value=3)
        
        # Champs optionnels
        col1, col2 = st.columns(2)
        
        with col1:
            salaire_grade = st.selectbox("Grade salarial", ["A", "B", "C", "D"], index=1)
            taux_presence = st.number_input("Taux de présence (%)", min_value=0.0, max_value=100.0, value=95.0)
        
        with col2:
            derniere_evaluation = st.number_input("Dernière évaluation", min_value=1.0, max_value=5.0, value=4.0, step=0.1)
            date_embauche = st.date_input("Date d'embauche", value=datetime.now())
        
        submitted = st.form_submit_button("➕ Ajouter le professeur", use_container_width=True)
        
        if submitted:
            # Validation
            if not all([nom, prenom, email, telephone, specialite, matieres]):
                st.error("Veuillez remplir tous les champs obligatoires (*)")
            else:
                # Ajouter le professeur
                new_professor = {
                    'id': str(uuid.uuid4())[:8],
                    'nom': nom,
                    'prenom': prenom,
                    'sexe': sexe,
                    'specialite': specialite,
                    'matieres': matieres,
                    'experience': experience,
                    'email': email,
                    'telephone': telephone,
                    'ville': ville,
                    'statut': statut,
                    'heures_semaine': heures_semaine,
                    'classes_assigned': classes_assigned,
                    'salaire_grade': salaire_grade,
                    'taux_presence': taux_presence,
                    'derniere_evaluation': derniere_evaluation,
                    'date_embauche': date_embauche.strftime('%Y-%m-%d')
                }
                
                # Ajouter à la liste
                new_df = pd.DataFrame([new_professor])
                st.session_state.professors = pd.concat([st.session_state.professors, new_df], ignore_index=True)
                
                # Journaliser l'action
                auth_system.log_action(
                    st.session_state.user_info['username'],
                    "Ajout professeur",
                    f"Professeur ajouté: {nom} {prenom}"
                )
                
                st.success(f"✅ Professeur {nom} {prenom} ajouté avec succès !")
                st.balloons()

def show_edit_professor_form(professor_id):
    """Formulaire de modification de professeur"""
    professor = st.session_state.professors[st.session_state.professors['id'] == professor_id]
    
    if professor.empty:
        st.error("Professeur non trouvé")
        return
    
    professor = professor.iloc[0]
    
    st.subheader(f"✏️ Modification du professeur: {professor['nom']} {professor['prenom']}")
    
    with st.form("edit_professor_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            nom = st.text_input("Nom *", value=professor['nom'])
            prenom = st.text_input("Prénom *", value=professor['prenom'])
            sexe = st.selectbox("Sexe *", ["M", "F"], index=0 if professor['sexe'] == 'M' else 1)
            specialite = st.selectbox("Spécialité *", 
                                    ['Informatique', 'Mathématiques', 'Physique', 'Chimie', 
                                     'Biologie', 'Économie', 'Droit'],
                                    index=['Informatique', 'Mathématiques', 'Physique', 'Chimie', 
                                           'Biologie', 'Économie', 'Droit'].index(professor['specialite']))
            matieres = st.text_area("Matières enseignées *", value=professor['matieres'])
            experience = st.number_input("Expérience (années) *", 
                                       value=int(professor['experience']))
        
        with col2:
            email = st.text_input("Email professionnel *", value=professor['email'])
            telephone = st.text_input("Téléphone *", value=professor['telephone'])
            ville = st.text_input("Ville *", value=professor['ville'])
            statut = st.selectbox("Statut *", ["Permanent", "Vacataire"],
                                index=0 if professor['statut'] == 'Permanent' else 1)
            heures_semaine = st.number_input("Heures/semaine *", 
                                           value=int(professor['heures_semaine']))
            classes_assigned = st.number_input("Classes assignées *", 
                                             value=int(professor['classes_assigned']))
        
        # Champs optionnels
        col1, col2 = st.columns(2)
        
        with col1:
            salaire_grade = st.selectbox("Grade salarial", ["A", "B", "C", "D"],
                                       index=["A", "B", "C", "D"].index(professor['salaire_grade']))
            taux_presence = st.number_input("Taux de présence (%)", 
                                          value=float(professor['taux_presence']))
        
        with col2:
            derniere_evaluation = st.number_input("Dernière évaluation", 
                                                value=float(professor['derniere_evaluation']))
            date_embauche = st.date_input("Date d'embauche", 
                                        value=datetime.strptime(professor['date_embauche'], '%Y-%m-%d'))
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            submitted = st.form_submit_button("💾 Enregistrer les modifications", use_container_width=True)
        
        with col2:
            if st.form_submit_button("❌ Annuler", use_container_width=True):
                st.session_state.selected_professor_id = None
                st.rerun()
        
        with col3:
            if st.form_submit_button("🗑️ Supprimer ce professeur", type="secondary", use_container_width=True):
                if st.checkbox("Confirmer la suppression", key="prof_delete_form"):
                    delete_professor(professor_id)
                    st.session_state.selected_professor_id = None
                    st.success("Professeur supprimé avec succès !")
                    time.sleep(1)
                    st.rerun()
        
        if submitted:
            # Validation
            if not all([nom, prenom, email, telephone, specialite, matieres]):
                st.error("Veuillez remplir tous les champs obligatoires (*)")
            else:
                # Mettre à jour le professeur
                updated_professor = {
                    'id': professor_id,
                    'nom': nom,
                    'prenom': prenom,
                    'sexe': sexe,
                    'specialite': specialite,
                    'matieres': matieres,
                    'experience': experience,
                    'email': email,
                    'telephone': telephone,
                    'ville': ville,
                    'statut': statut,
                    'heures_semaine': heures_semaine,
                    'classes_assigned': classes_assigned,
                    'salaire_grade': salaire_grade,
                    'taux_presence': taux_presence,
                    'derniere_evaluation': derniere_evaluation,
                    'date_embauche': date_embauche.strftime('%Y-%m-%d')
                }
                
                # Mettre à jour dans le DataFrame
                idx = st.session_state.professors[st.session_state.professors['id'] == professor_id].index
                if not idx.empty:
                    for key, value in updated_professor.items():
                        st.session_state.professors.at[idx[0], key] = value
                
                # Journaliser l'action
                auth_system.log_action(
                    st.session_state.user_info['username'],
                    "Modification professeur",
                    f"Professeur modifié: {nom} {prenom}"
                )
                
                st.success(f"✅ Professeur {nom} {prenom} modifié avec succès !")
                time.sleep(1)
                st.session_state.selected_professor_id = None
                st.rerun()

def delete_professor(professor_id):
    """Supprimer un professeur"""
    st.session_state.professors = st.session_state.professors[st.session_state.professors['id'] != professor_id]
    
    # Journaliser l'action
    auth_system.log_action(
        st.session_state.user_info['username'],
        "Suppression professeur",
        f"Professeur supprimé: ID {professor_id}"
    )

def show_professors_report(df):
    """Générer un rapport des professeurs"""
    st.subheader("📊 Rapport des Professeurs")
    
    # Statistiques
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total = len(df)
        st.metric("Total professeurs", total)
    
    with col2:
        permanent = len(df[df['statut'] == 'Permanent'])
        st.metric("Permanents", permanent, f"{permanent/total*100:.1f}%")
    
    with col3:
        avg_experience = df['experience'].mean()
        st.metric("Expérience moyenne", f"{avg_experience:.1f} ans")
    
    with col4:
        total_hours = df['heures_semaine'].sum()
        st.metric("Heures totales/semaine", total_hours)
    
    # Visualisations
    col1, col2 = st.columns(2)
    
    with col1:
        # Répartition par spécialité
        specialite_counts = df['specialite'].value_counts()
        fig = px.bar(x=specialite_counts.index, y=specialite_counts.values,
                    title="Répartition par spécialité",
                    labels={'x': 'Spécialité', 'y': 'Nombre de professeurs'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Répartition par statut
        statut_counts = df['statut'].value_counts()
        fig = px.pie(values=statut_counts.values, names=statut_counts.index,
                    title="Répartition par statut")
        st.plotly_chart(fig, use_container_width=True)

def show_professors_statistics():
    """Afficher les statistiques des professeurs"""
    st.subheader("📊 Statistiques Globales des Professeurs")
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total = len(st.session_state.professors)
        st.metric("Total professeurs", total)
    
    with col2:
        permanent = len(st.session_state.professors[st.session_state.professors['statut'] == 'Permanent'])
        st.metric("Permanents", permanent, f"{permanent/total*100:.1f}%")
    
    with col3:
        avg_experience = st.session_state.professors['experience'].mean()
        st.metric("Expérience moyenne", f"{avg_experience:.1f} ans")
    
    with col4:
        total_hours = st.session_state.professors['heures_semaine'].sum()
        st.metric("Heures totales/semaine", total_hours)
    
    # Graphiques avancés
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution de l'expérience
        fig = px.histogram(st.session_state.professors, x='experience', nbins=15,
                          title="Distribution de l'expérience",
                          color_discrete_sequence=['#3498db'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Charge horaire par spécialité
        fig = px.box(st.session_state.professors, x='specialite', y='heures_semaine',
                    title="Charge horaire par spécialité",
                    color='specialite')
        st.plotly_chart(fig, use_container_width=True)

# Page CRUD Employés
def show_crud_employees():
    """CRUD complet pour les employés"""
    st.markdown("<h1 class='main-header'>👔 CRUD Employés</h1>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Liste des Employés", "➕ Ajouter un Employé", "✏️ Modifier un Employé", "📊 Dashboard Employés"])
    
    with tab1:
        # Filtres de recherche
        col1, col2, col3 = st.columns(3)
        
        with col1:
            search_term = st.text_input("Rechercher (nom, prénom, poste)", key="emp_search")
        
        with col2:
            service_filter = st.multiselect("Service", 
                                          st.session_state.employees['service'].unique())
        
        with col3:
            statut_filter = st.multiselect("Statut", 
                                         st.session_state.employees['statut'].unique())
        
        # Appliquer les filtres
        filtered_employees = st.session_state.employees.copy()
        
        if search_term:
            mask = (filtered_employees['nom'].str.contains(search_term, case=False) | 
                   filtered_employees['prenom'].str.contains(search_term, case=False) |
                   filtered_employees['poste'].str.contains(search_term, case=False))
            filtered_employees = filtered_employees[mask]
        
        if service_filter:
            filtered_employees = filtered_employees[filtered_employees['service'].isin(service_filter)]
        
        if statut_filter:
            filtered_employees = filtered_employees[filtered_employees['statut'].isin(statut_filter)]
        
        # Actions sur la liste
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📥 Importer CSV", use_container_width=True, key="emp_import"):
                show_import_csv('employees')
        
        with col2:
            if st.button("📤 Exporter CSV", use_container_width=True, key="emp_export"):
                show_export_csv(filtered_employees, 'employes')
        
        with col3:
            if st.button("🖨️ Générer Rapport", use_container_width=True, key="emp_report"):
                show_employees_report(filtered_employees)
        
        # Affichage des employés
        st.subheader(f"📋 Liste des Employés ({len(filtered_employees)} résultats)")
        
        # Sélection des colonnes à afficher
        display_cols = ['nom', 'prenom', 'sexe', 'poste', 'service', 'date_recrutement', 
                       'experience', 'salaire', 'statut', 'taux_presence']
        
        # Affichage du tableau avec actions
        st.dataframe(
            filtered_employees[display_cols],
            use_container_width=True,
            height=400,
            column_config={
                "nom": st.column_config.TextColumn("Nom", width="medium"),
                "prenom": st.column_config.TextColumn("Prénom", width="medium"),
                "sexe": st.column_config.TextColumn("Sexe", width="small"),
                "poste": st.column_config.TextColumn("Poste", width="medium"),
                "service": st.column_config.TextColumn("Service", width="medium"),
                "date_recrutement": st.column_config.DateColumn("Date recrutement", format="DD/MM/YYYY", width="medium"),
                "experience": st.column_config.NumberColumn("Expérience (ans)", format="%d", width="small"),
                "salaire": st.column_config.NumberColumn("Salaire (€)", format="%d", width="small"),
                "statut": st.column_config.SelectboxColumn(
                    "Statut",
                    options=["Actif", "Congé", "Retraité"],
                    width="medium"
                ),
                "taux_presence": st.column_config.NumberColumn("Présence %", format="%.1f", width="small")
            }
        )
        
        # Actions sur les lignes sélectionnées
        if not filtered_employees.empty:
            selected_index = st.number_input(
                "Sélectionner l'index de l'employé à modifier/supprimer",
                min_value=0,
                max_value=len(filtered_employees)-1,
                value=0,
                key="emp_select"
            )
            
            selected_employee = filtered_employees.iloc[selected_index]
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("✏️ Modifier cet employé", use_container_width=True, key="emp_edit"):
                    st.session_state.selected_employee_id = selected_employee['id']
                    st.rerun()
            
            with col2:
                if st.button("❌ Supprimer cet employé", type="secondary", use_container_width=True, key="emp_delete"):
                    if st.checkbox("Confirmer la suppression", key="emp_delete_confirm"):
                        delete_employee(selected_employee['id'])
                        st.success("Employé supprimé avec succès !")
                        st.rerun()
    
    with tab2:
        show_add_employee_form()
    
    with tab3:
        if st.session_state.selected_employee_id:
            show_edit_employee_form(st.session_state.selected_employee_id)
        else:
            st.info("Veuillez sélectionner un employé à modifier depuis l'onglet 'Liste des Employés'")
    
    with tab4:
        show_employees_dashboard()

def show_add_employee_form():
    """Formulaire d'ajout d'employé"""
    st.subheader("➕ Ajouter un Nouvel Employé")
    
    with st.form("add_employee_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            nom = st.text_input("Nom *")
            prenom = st.text_input("Prénom *")
            sexe = st.selectbox("Sexe *", ["M", "F"])
            poste = st.text_input("Poste *", placeholder="Ex: Secrétaire administratif")
            service = st.selectbox("Service *", 
                                 ['Secrétariat', 'Administration', 'Comptabilité', 
                                  'Bibliothèque', 'Technique / IT', 'Surveillance'])
            date_recrutement = st.date_input("Date de recrutement *", value=datetime.now())
        
        with col2:
            salaire = st.number_input("Salaire (€) *", min_value=1500, max_value=10000, value=2500, step=100)
            email = st.text_input("Email *", placeholder="prenom.nom@university.edu")
            telephone = st.text_input("Téléphone *")
            ville = st.text_input("Ville *")
            statut = st.selectbox("Statut *", ["Actif", "Congé", "Retraité"])
        
        # Champs optionnels
        col1, col2 = st.columns(2)
        
        with col1:
            experience = st.number_input("Expérience (années)", min_value=0, max_value=50, value=5)
            evaluation = st.number_input("Évaluation", min_value=1.0, max_value=5.0, value=4.0, step=0.1)
        
        with col2:
            taux_presence = st.number_input("Taux de présence (%)", min_value=0.0, max_value=100.0, value=95.0)
        
        submitted = st.form_submit_button("➕ Ajouter l'employé", use_container_width=True)
        
        if submitted:
            # Validation
            if not all([nom, prenom, poste, email, telephone]):
                st.error("Veuillez remplir tous les champs obligatoires (*)")
            else:
                # Ajouter l'employé
                new_employee = {
                    'id': str(uuid.uuid4())[:8],
                    'nom': nom,
                    'prenom': prenom,
                    'sexe': sexe,
                    'poste': poste,
                    'service': service,
                    'date_recrutement': date_recrutement.strftime('%Y-%m-%d'),
                    'salaire': salaire,
                    'email': email,
                    'telephone': telephone,
                    'ville': ville,
                    'statut': statut,
                    'experience': experience,
                    'evaluation': evaluation,
                    'taux_presence': taux_presence
                }
                
                # Ajouter à la liste
                new_df = pd.DataFrame([new_employee])
                st.session_state.employees = pd.concat([st.session_state.employees, new_df], ignore_index=True)
                
                # Journaliser l'action
                auth_system.log_action(
                    st.session_state.user_info['username'],
                    "Ajout employé",
                    f"Employé ajouté: {nom} {prenom} ({poste})"
                )
                
                st.success(f"✅ Employé {nom} {prenom} ajouté avec succès !")
                st.balloons()

def show_edit_employee_form(employee_id):
    """Formulaire de modification d'employé"""
    employee = st.session_state.employees[st.session_state.employees['id'] == employee_id]
    
    if employee.empty:
        st.error("Employé non trouvé")
        return
    
    employee = employee.iloc[0]
    
    st.subheader(f"✏️ Modification de l'employé: {employee['nom']} {employee['prenom']}")
    
    with st.form("edit_employee_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            nom = st.text_input("Nom *", value=employee['nom'])
            prenom = st.text_input("Prénom *", value=employee['prenom'])
            sexe = st.selectbox("Sexe *", ["M", "F"], index=0 if employee['sexe'] == 'M' else 1)
            poste = st.text_input("Poste *", value=employee['poste'])
            service = st.selectbox("Service *", 
                                 ['Secrétariat', 'Administration', 'Comptabilité', 
                                  'Bibliothèque', 'Technique / IT', 'Surveillance'],
                                 index=['Secrétariat', 'Administration', 'Comptabilité', 
                                        'Bibliothèque', 'Technique / IT', 'Surveillance'].index(employee['service']))
            date_recrutement = st.date_input("Date de recrutement *", 
                                           value=datetime.strptime(employee['date_recrutement'], '%Y-%m-%d'))
        
        with col2:
            salaire = st.number_input("Salaire (€) *", value=int(employee['salaire']))
            email = st.text_input("Email *", value=employee['email'])
            telephone = st.text_input("Téléphone *", value=employee['telephone'])
            ville = st.text_input("Ville *", value=employee['ville'])
            statut = st.selectbox("Statut *", ["Actif", "Congé", "Retraité"],
                                index=["Actif", "Congé", "Retraité"].index(employee['statut']))
        
        # Champs optionnels
        col1, col2 = st.columns(2)
        
        with col1:
            experience = st.number_input("Expérience (années)", value=int(employee['experience']))
            evaluation = st.number_input("Évaluation", value=float(employee['evaluation']))
        
        with col2:
            taux_presence = st.number_input("Taux de présence (%)", value=float(employee['taux_presence']))
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            submitted = st.form_submit_button("💾 Enregistrer les modifications", use_container_width=True)
        
        with col2:
            if st.form_submit_button("❌ Annuler", use_container_width=True):
                st.session_state.selected_employee_id = None
                st.rerun()
        
        with col3:
            if st.form_submit_button("🗑️ Supprimer cet employé", type="secondary", use_container_width=True):
                if st.checkbox("Confirmer la suppression", key="emp_delete_form"):
                    delete_employee(employee_id)
                    st.session_state.selected_employee_id = None
                    st.success("Employé supprimé avec succès !")
                    time.sleep(1)
                    st.rerun()
        
        if submitted:
            # Validation
            if not all([nom, prenom, poste, email, telephone]):
                st.error("Veuillez remplir tous les champs obligatoires (*)")
            else:
                # Mettre à jour l'employé
                updated_employee = {
                    'id': employee_id,
                    'nom': nom,
                    'prenom': prenom,
                    'sexe': sexe,
                    'poste': poste,
                    'service': service,
                    'date_recrutement': date_recrutement.strftime('%Y-%m-%d'),
                    'salaire': salaire,
                    'email': email,
                    'telephone': telephone,
                    'ville': ville,
                    'statut': statut,
                    'experience': experience,
                    'evaluation': evaluation,
                    'taux_presence': taux_presence
                }
                
                # Mettre à jour dans le DataFrame
                idx = st.session_state.employees[st.session_state.employees['id'] == employee_id].index
                if not idx.empty:
                    for key, value in updated_employee.items():
                        st.session_state.employees.at[idx[0], key] = value
                
                # Journaliser l'action
                auth_system.log_action(
                    st.session_state.user_info['username'],
                    "Modification employé",
                    f"Employé modifié: {nom} {prenom} ({poste})"
                )
                
                st.success(f"✅ Employé {nom} {prenom} modifié avec succès !")
                time.sleep(1)
                st.session_state.selected_employee_id = None
                st.rerun()

def delete_employee(employee_id):
    """Supprimer un employé"""
    st.session_state.employees = st.session_state.employees[st.session_state.employees['id'] != employee_id]
    
    # Journaliser l'action
    auth_system.log_action(
        st.session_state.user_info['username'],
        "Suppression employé",
        f"Employé supprimé: ID {employee_id}"
    )

def show_employees_report(df):
    """Générer un rapport des employés"""
    st.subheader("📊 Rapport des Employés")
    
    # Statistiques
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total = len(df)
        st.metric("Total employés", total)
    
    with col2:
        active = len(df[df['statut'] == 'Actif'])
        st.metric("Actifs", active, f"{active/total*100:.1f}%")
    
    with col3:
        avg_salary = df['salaire'].mean()
        st.metric("Salaire moyen", f"{avg_salary:.0f}€")
    
    with col4:
        avg_experience = df['experience'].mean()
        st.metric("Expérience moyenne", f"{avg_experience:.1f} ans")
    
    # Visualisations
    col1, col2 = st.columns(2)
    
    with col1:
        # Répartition par service
        service_counts = df['service'].value_counts()
        fig = px.bar(x=service_counts.index, y=service_counts.values,
                    title="Répartition par service",
                    labels={'x': 'Service', 'y': 'Nombre d\'employés'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Répartition par statut
        statut_counts = df['statut'].value_counts()
        fig = px.pie(values=statut_counts.values, names=statut_counts.index,
                    title="Répartition par statut")
        st.plotly_chart(fig, use_container_width=True)

def show_employees_dashboard():
    """Dashboard des employés"""
    st.subheader("📊 Dashboard Employés - Administration")
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total = len(st.session_state.employees)
        st.markdown(f"""
        <div class='kpi-card-employee'>
            <div class='kpi-title'>TOTAL EMPLOYÉS</div>
            <div class='kpi-value'>{total}</div>
            <div>Effectif total</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        active = len(st.session_state.employees[st.session_state.employees['statut'] == 'Actif'])
        rate = (active / total * 100) if total > 0 else 0
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-title'>EMPLOYÉS ACTIFS</div>
            <div class='kpi-value'>{active}</div>
            <div>{rate:.1f}% du total</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_salary = st.session_state.employees['salaire'].mean()
        st.markdown(f"""
        <div class='kpi-card-secondary'>
            <div class='kpi-title'>SALAIRE MOYEN</div>
            <div class='kpi-value'>{avg_salary:.0f}€</div>
            <div>Mensuel brut</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_experience = st.session_state.employees['experience'].mean()
        st.markdown(f"""
        <div class='kpi-card-tertiary'>
            <div class='kpi-title'>ANCIENNETÉ MOYENNE</div>
            <div class='kpi-value'>{avg_experience:.1f}</div>
            <div>années d'expérience</div>
        </div>
        """, unsafe_allow_html=True)
    
        # Graphiques détaillés
    st.subheader("📈 Analyses Détailées")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution des salaires
        fig = px.histogram(st.session_state.employees, x='salaire', nbins=15,
                          title="Distribution des salaires",
                          color_discrete_sequence=['#43e97b'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Présence par service
        presence_by_service = st.session_state.employees.groupby('service')['taux_presence'].mean().reset_index()
        fig = px.bar(presence_by_service.sort_values('taux_presence', ascending=False),
                    x='service', y='taux_presence',
                    title="Taux de présence moyen par service",
                    color='taux_presence',
                    color_continuous_scale='RdYlGn')
        st.plotly_chart(fig, use_container_width=True)
    
    # Tableau de bord avancé
    st.subheader("🏢 Vue par Service")
    
    services = st.session_state.employees['service'].unique()
    selected_service = st.selectbox("Sélectionner un service", services)
    
    if selected_service:
        service_data = st.session_state.employees[st.session_state.employees['service'] == selected_service]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(f"Employés {selected_service}", len(service_data))
        
        with col2:
            avg_salary = service_data['salaire'].mean()
            st.metric("Salaire moyen", f"{avg_salary:.0f}€")
        
        with col3:
            avg_presence = service_data['taux_presence'].mean()
            st.metric("Présence moyenne", f"{avg_presence:.1f}%")
        
        # Liste des employés du service
        st.subheader(f"👥 Liste des employés - {selected_service}")
        st.dataframe(service_data[['nom', 'prenom', 'poste', 'date_recrutement', 'salaire', 'statut']], 
                    use_container_width=True)

# Page Dashboard Admin Global
def show_admin_global_dashboard():
    """Dashboard administratif global"""
    st.markdown("<h1 class='main-header'>🏢 Dashboard Administration Global</h1>", unsafe_allow_html=True)
    
    # KPIs Globaux
    st.subheader("📊 Indicateurs Globaux de l'Université")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_students = len(st.session_state.students)
        active_students = len(st.session_state.students[st.session_state.students['statut'] == 'Actif'])
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-title'>ÉTUDIANTS</div>
            <div class='kpi-value'>{total_students}</div>
            <div>{active_students} actifs</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_professors = len(st.session_state.professors)
        permanent_prof = len(st.session_state.professors[st.session_state.professors['statut'] == 'Permanent'])
        st.markdown(f"""
        <div class='kpi-card-secondary'>
            <div class='kpi-title'>PROFESSEURS</div>
            <div class='kpi-value'>{total_professors}</div>
            <div>{permanent_prof} permanents</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_employees = len(st.session_state.employees)
        active_employees = len(st.session_state.employees[st.session_state.employees['statut'] == 'Actif'])
        st.markdown(f"""
        <div class='kpi-card-tertiary'>
            <div class='kpi-title'>EMPLOYÉS</div>
            <div class='kpi-value'>{total_employees}</div>
            <div>{active_employees} actifs</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        total_personnel = total_professors + total_employees
        ratio = total_students / total_professors if total_professors > 0 else 0
        st.markdown(f"""
        <div class='kpi-card-employee'>
            <div class='kpi-title'>PERSONNEL TOTAL</div>
            <div class='kpi-value'>{total_personnel}</div>
            <div>Ratio: {ratio:.1f} étudiants/prof</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Section Étudiants
    st.subheader("👨‍🎓 Dashboard Étudiants")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        validated = st.session_state.students['valide'].sum()
        rate = (validated / total_students * 100) if total_students > 0 else 0
        st.metric("Taux validation", f"{rate:.1f}%", f"{validated}/{total_students}")
    
    with col2:
        avg_grade = st.session_state.students['moyenne_generale'].mean()
        st.metric("Moyenne générale", f"{avg_grade:.2f}/20")
    
    with col3:
        avg_absence = st.session_state.students['taux_absence'].mean()
        st.metric("Absence moyenne", f"{avg_absence:.1f}%")
    
    with col4:
        best_grade = st.session_state.students['moyenne_generale'].max()
        st.metric("Meilleure note", f"{best_grade:.2f}/20")
    
    # Section Professeurs
    st.subheader("👨‍🏫 Dashboard Professeurs")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_hours = st.session_state.professors['heures_semaine'].sum()
        st.metric("Heures totales", f"{total_hours}h/sem")
    
    with col2:
        avg_experience = st.session_state.professors['experience'].mean()
        st.metric("Expérience moyenne", f"{avg_experience:.1f} ans")
    
    with col3:
        avg_presence = st.session_state.professors['taux_presence'].mean()
        st.metric("Présence moyenne", f"{avg_presence:.1f}%")
    
    with col4:
        avg_evaluation = st.session_state.professors['derniere_evaluation'].mean()
        st.metric("Évaluation moyenne", f"{avg_evaluation:.1f}/5")
    
    # Section Employés
    st.subheader("👔 Dashboard Employés")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_salary = st.session_state.employees['salaire'].sum()
        st.metric("Masse salariale", f"{total_salary:,.0f}€/mois")
    
    with col2:
        avg_emp_experience = st.session_state.employees['experience'].mean()
        st.metric("Ancienneté moyenne", f"{avg_emp_experience:.1f} ans")
    
    with col3:
        avg_emp_presence = st.session_state.employees['taux_presence'].mean()
        st.metric("Présence employés", f"{avg_emp_presence:.1f}%")
    
    with col4:
        avg_emp_evaluation = st.session_state.employees['evaluation'].mean()
        st.metric("Évaluation employés", f"{avg_emp_evaluation:.1f}/5")
    
    # Graphiques comparatifs
    st.subheader("📈 Analyses Comparatives")
    
    tab1, tab2, tab3 = st.tabs(["📊 Répartition Globale", "📈 Performance Académique", "💰 Coûts & Budgets"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Répartition population universitaire
            categories = ['Étudiants', 'Professeurs', 'Employés']
            values = [total_students, total_professors, total_employees]
            
            fig = px.pie(values=values, names=categories,
                        title="Répartition de la population universitaire",
                        color_discrete_sequence=['#3498db', '#e74c3c', '#2ecc71'])
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Ratio étudiants/professeurs par spécialité
            ratio_data = []
            for specialite in st.session_state.students['specialite'].unique():
                nb_students = len(st.session_state.students[st.session_state.students['specialite'] == specialite])
                nb_professors = len(st.session_state.professors[st.session_state.professors['specialite'] == specialite])
                ratio = nb_students / nb_professors if nb_professors > 0 else 0
                ratio_data.append({
                    'Spécialité': specialite,
                    'Ratio': ratio,
                    'Étudiants': nb_students,
                    'Professeurs': nb_professors
                })
            
            ratio_df = pd.DataFrame(ratio_data)
            
            fig = px.bar(ratio_df.sort_values('Ratio', ascending=False),
                        x='Spécialité', y='Ratio',
                        title="Ratio étudiants/professeurs par spécialité",
                        color='Ratio',
                        color_continuous_scale='RdYlGn_r')
            fig.add_hline(y=20, line_dash="dash", line_color="red", annotation_text="Seuil idéal")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            # Taux de validation par spécialité
            validation_by_specialite = st.session_state.students.groupby('specialite').agg({
                'id': 'count',
                'valide': 'sum'
            }).reset_index()
            
            validation_by_specialite['taux_validation'] = (validation_by_specialite['valide'] / validation_by_specialite['id'] * 100).round(1)
            
            fig = px.bar(validation_by_specialite.sort_values('taux_validation', ascending=False),
                        x='specialite', y='taux_validation',
                        title="Taux de validation par spécialité",
                        color='taux_validation',
                        color_continuous_scale='RdYlGn')
            fig.add_hline(y=70, line_dash="dash", line_color="orange", annotation_text="Objectif")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Corrélation expérience prof / réussite étudiants
            # Simulation de données pour l'exemple
            correlation_data = []
            for specialite in st.session_state.professors['specialite'].unique():
                prof_exp = st.session_state.professors[
                    st.session_state.professors['specialite'] == specialite
                ]['experience'].mean()
                
                student_success = st.session_state.students[
                    st.session_state.students['specialite'] == specialite
                ]['moyenne_generale'].mean()
                
                correlation_data.append({
                    'Spécialité': specialite,
                    'Expérience moyenne profs': prof_exp,
                    'Moyenne étudiants': student_success
                })
            
            correlation_df = pd.DataFrame(correlation_data)
            
            fig = px.scatter(correlation_df, 
                           x='Expérience moyenne profs', y='Moyenne étudiants',
                           size='Moyenne étudiants', color='Spécialité',
                           hover_name='Spécialité',
                           title="Corrélation expérience profs ↔ réussite étudiants")
            
            # Ligne de tendance
            if len(correlation_df) > 1:
                z = np.polyfit(correlation_df['Expérience moyenne profs'], 
                             correlation_df['Moyenne étudiants'], 1)
                p = np.poly1d(z)
                x_line = np.linspace(correlation_df['Expérience moyenne profs'].min(), 
                                   correlation_df['Expérience moyenne profs'].max(), 100)
                y_line = p(x_line)
                
                fig.add_trace(go.Scatter(x=x_line, y=y_line, mode='lines', 
                                       name='Tendance', line=dict(color='red', dash='dash')))
            
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            # Coûts salariaux par service
            salary_by_service = st.session_state.employees.groupby('service').agg({
                'salaire': 'sum',
                'id': 'count'
            }).reset_index()
            
            salary_by_service.columns = ['Service', 'Masse salariale', 'Nombre employés']
            salary_by_service['Coût moyen'] = (salary_by_service['Masse salariale'] / salary_by_service['Nombre employés']).round(0)
            
            fig = px.bar(salary_by_service.sort_values('Masse salariale', ascending=False),
                        x='Service', y='Masse salariale',
                        title="Masse salariale par service",
                        color='Coût moyen',
                        color_continuous_scale='Blues')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Coût par étudiant par spécialité (simulation)
            cost_data = []
            for specialite in st.session_state.students['specialite'].unique():
                nb_students = len(st.session_state.students[st.session_state.students['specialite'] == specialite])
                
                # Coût estimé (simulation)
                base_cost = {
                    'Informatique': 8000,
                    'Mathématiques': 6000,
                    'Physique': 7500,
                    'Chimie': 7000,
                    'Biologie': 6500,
                    'Économie': 5500,
                    'Droit': 5000
                }.get(specialite, 6000)
                
                total_cost = nb_students * base_cost
                cost_per_student = total_cost / nb_students if nb_students > 0 else 0
                
                cost_data.append({
                    'Spécialité': specialite,
                    'Nombre étudiants': nb_students,
                    'Coût total (k€)': total_cost / 1000,
                    'Coût/étudiant (€)': cost_per_student
                })
            
            cost_df = pd.DataFrame(cost_data)
            
            fig = px.bar(cost_df.sort_values('Coût/étudiant (€)', ascending=False),
                        x='Spécialité', y='Coût/étudiant (€)',
                        title="Coût moyen par étudiant par spécialité",
                        color='Coût total (k€)',
                        color_continuous_scale='Viridis')
            st.plotly_chart(fig, use_container_width=True)
    
    # Alertes administratives
    st.subheader("⚠️ Alertes Administratives")
    
    alerts = []
    
    # Vérifier les ratios étudiants/professeurs
    for specialite in st.session_state.students['specialite'].unique():
        nb_students = len(st.session_state.students[st.session_state.students['specialite'] == specialite])
        nb_professors = len(st.session_state.professors[st.session_state.professors['specialite'] == specialite])
        
        if nb_professors > 0:
            ratio = nb_students / nb_professors
            if ratio > 25:
                alerts.append({
                    "type": "danger",
                    "message": f"⚠️ Ratio élevé en {specialite}: {ratio:.1f} étudiants/professeur"
                })
            elif ratio > 20:
                alerts.append({
                    "type": "warning",
                    "message": f"⚠️ Ratio élevé en {specialite}: {ratio:.1f} étudiants/professeur"
                })
    
    # Vérifier les taux de validation bas
    for specialite in st.session_state.students['specialite'].unique():
        specialite_students = st.session_state.students[st.session_state.students['specialite'] == specialite]
        if len(specialite_students) > 0:
            validation_rate = (specialite_students['valide'].sum() / len(specialite_students) * 100)
            if validation_rate < 60:
                alerts.append({
                    "type": "danger",
                    "message": f"🎓 Taux de validation bas en {specialite}: {validation_rate:.1f}%"
                })
            elif validation_rate < 70:
                alerts.append({
                    "type": "warning",
                    "message": f"🎓 Taux de validation faible en {specialite}: {validation_rate:.1f}%"
                })
    
    # Vérifier les professeurs surchargés
    overloaded_profs = st.session_state.professors[st.session_state.professors['heures_semaine'] > 22]
    if len(overloaded_profs) > 0:
        alerts.append({
            "type": "warning",
            "message": f"👨‍🏫 {len(overloaded_profs)} professeurs avec charge horaire > 22h/semaine"
        })
    
    # Afficher les alertes
    if alerts:
        for alert in alerts:
            if alert["type"] == "danger":
                st.error(alert["message"])
            elif alert["type"] == "warning":
                st.warning(alert["message"])
    else:
        st.success("✅ Aucune alerte administrative critique")

# Page Espace Employé
def show_employee_dashboard():
    """Dashboard pour les employés"""
    employee_details = st.session_state.user_info['details']
    
    st.markdown(f"<h1 class='main-header'>👔 Espace Employé - {employee_details['name']}</h1>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📋 Mon Profil", "📅 Mes Tâches", "📊 Mes Statistiques"])
    
    with tab1:
        # Profil de l'employé
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📋 Mes Informations Professionnelles")
            
            info_cols = st.columns(2)
            
            with info_cols[0]:
                st.metric("Poste", employee_details.get('poste', 'Non spécifié'))
                st.metric("Service", employee_details.get('service', 'Non spécifié'))
                st.metric("Date recrutement", employee_details.get('date_recrutement', 'Non spécifié'))
            
            with info_cols[1]:
                st.metric("Statut", employee_details.get('statut', 'Non spécifié'))
                st.metric("Expérience", f"{employee_details.get('experience', 0)} ans")
                if 'salaire' in employee_details:
                    st.metric("Salaire", f"{employee_details['salaire']}€")
        
        with col2:
            # Photo de profil
            st.markdown("### 🖼️ Photo de profil")
            st.image("https://via.placeholder.com/200x200/9b59b6/ffffff?text=EMPLOYE", width=200)
            
            # Actions rapides
            st.markdown("### ⚡ Actions")
            if st.button("✏️ Modifier mon profil"):
                st.info("Fonctionnalité à implémenter")
            
            if st.button("📄 Mes documents"):
                st.info("Accès aux documents personnels")
    
    with tab2:
        st.subheader("📅 Mes Tâches et Activités")
        
        # Tâches simulées
        tasks = [
            {"id": 1, "tâche": "Traiter les inscriptions nouvelles", "priorité": "Haute", "échéance": "Aujourd'hui", "statut": "En cours"},
            {"id": 2, "tâche": "Préparer rapport mensuel", "priorité": "Moyenne", "échéance": "Demain", "statut": "À faire"},
            {"id": 3, "tâche": "Répondre aux emails étudiants", "priorité": "Basse", "échéance": "Cette semaine", "statut": "En cours"},
            {"id": 4, "tâche": "Mettre à jour les dossiers", "priorité": "Moyenne", "échéance": "15/01/2024", "statut": "Terminé"},
            {"id": 5, "tâche": "Préparer réunion service", "priorité": "Haute", "échéance": "10/01/2024", "statut": "Terminé"},
        ]
        
        # Filtres
        col1, col2 = st.columns(2)
        
        with col1:
            status_filter = st.multiselect("Filtrer par statut", 
                                         ["À faire", "En cours", "Terminé"],
                                         default=["À faire", "En cours"])
        
        with col2:
            priority_filter = st.multiselect("Filtrer par priorité", 
                                           ["Haute", "Moyenne", "Basse"],
                                           default=["Haute", "Moyenne", "Basse"])
        
        # Afficher les tâches filtrées
        filtered_tasks = [t for t in tasks if t['statut'] in status_filter and t['priorité'] in priority_filter]
        
        for task in filtered_tasks:
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                
                with col1:
                    st.markdown(f"**{task['tâche']}**")
                
                with col2:
                    if task['priorité'] == "Haute":
                        st.error("🔴 Haute")
                    elif task['priorité'] == "Moyenne":
                        st.warning("🟡 Moyenne")
                    else:
                        st.info("🔵 Basse")
                
                with col3:
                    st.markdown(f"📅 {task['échéance']}")
                
                with col4:
                    if task['statut'] == "Terminé":
                        st.success("✅ Terminé")
                    elif task['statut'] == "En cours":
                        st.info("🔄 En cours")
                    else:
                        st.warning("⏳ À faire")
                
                st.markdown("---")
        
        # Ajouter une nouvelle tâche
        with st.expander("➕ Ajouter une nouvelle tâche"):
            with st.form("new_task_form"):
                new_task = st.text_input("Description de la tâche")
                new_priority = st.selectbox("Priorité", ["Haute", "Moyenne", "Basse"])
                new_deadline = st.date_input("Échéance")
                
                if st.form_submit_button("➕ Ajouter la tâche"):
                    if new_task:
                        st.success("Tâche ajoutée avec succès !")
    
    with tab3:
        st.subheader("📊 Mes Statistiques de Performance")
        
        # KPIs personnels
        col1, col2, col3 = st.columns(3)
        
        with col1:
            presence_rate = employee_details.get('taux_presence', 95)
            st.markdown(f"""
            <div class='kpi-card'>
                <div class='kpi-title'>MA PRÉSENCE</div>
                <div class='kpi-value'>{presence_rate}%</div>
                <div>Taux mensuel</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            evaluation = employee_details.get('evaluation', 4.0)
            st.markdown(f"""
            <div class='kpi-card-secondary'>
                <div class='kpi-title'>MON ÉVALUATION</div>
                <div class='kpi-value'>{evaluation}/5</div>
                <div>Dernière évaluation</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            experience = employee_details.get('experience', 5)
            st.markdown(f"""
            <div class='kpi-card-tertiary'>
                <div class='kpi-title'>MON EXPÉRIENCE</div>
                <div class='kpi-value'>{experience}</div>
                <div>années dans l'établissement</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Graphiques de performance
        col1, col2 = st.columns(2)
        
        with col1:
            # Évolution de la présence (simulée)
            months = ['Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb']
            presence_rates = [92, 94, 95, 96, 95, 96]
            
            fig = px.line(x=months, y=presence_rates, markers=True,
                         title="Évolution de ma présence mensuelle",
                         color_discrete_sequence=['#3498db'])
            fig.update_layout(xaxis_title="Mois", yaxis_title="Taux de présence (%)")
            fig.add_hrect(y0=95, y1=100, line_width=0, fillcolor="green", opacity=0.1)
            fig.add_hrect(y0=90, y1=95, line_width=0, fillcolor="orange", opacity=0.1)
            fig.add_hrect(y0=0, y1=90, line_width=0, fillcolor="red", opacity=0.1)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Comparaison avec le service
            service = employee_details.get('service', 'Secrétariat')
            service_employees = st.session_state.employees[st.session_state.employees['service'] == service]
            
            if len(service_employees) > 0:
                service_avg_presence = service_employees['taux_presence'].mean()
                service_avg_evaluation = service_employees['evaluation'].mean()
                
                fig = go.Figure(data=[
                    go.Bar(name='Moyenne service', 
                          x=['Présence', 'Évaluation'], 
                          y=[service_avg_presence, service_avg_evaluation * 20]),
                    go.Bar(name='Mes résultats', 
                          x=['Présence', 'Évaluation'], 
                          y=[presence_rate, evaluation * 20])
                ])
                
                fig.update_layout(
                    title="Comparaison avec la moyenne du service",
                    barmode='group',
                    yaxis_title="Score (%)"
                )
                
                st.plotly_chart(fig, use_container_width=True)

# Page Administration Système
def show_system_administration():
    """Administration du système"""
    st.markdown("<h1 class='main-header'>🔒 Administration du Système</h1>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["👥 Gestion des Rôles", "📊 Journaux d'Activité", "⚙️ Configuration", "🔄 Maintenance"])
    
    with tab1:
        st.subheader("👥 Gestion des Rôles et Permissions")
        
        # Table des rôles et permissions
        roles_data = [
            {
                "Rôle": "Administrateur",
                "Description": "Accès complet au système",
                "Permissions": "CRUD étudiants, professeurs, employés, configuration système, logs",
                "Nombre": len([u for u in auth_system.users.values() if u['role'] == 'admin'])
            },
            {
                "Rôle": "Professeur",
                "Description": "Gestion pédagogique",
                "Permissions": "Saisie notes, consultation étudiants, emploi du temps",
                "Nombre": len([u for u in auth_system.users.values() if u['role'] == 'professeur'])
            },
            {
                "Rôle": "Employé",
                "Description": "Tâches administratives",
                "Permissions": "Gestion documents, consultation limitée, tâches spécifiques",
                "Nombre": len([u for u in auth_system.users.values() if u['role'] == 'employee'])
            },
            {
                "Rôle": "Étudiant",
                "Description": "Accès consultation",
                "Permissions": "Notes personnelles, emploi du temps, progression",
                "Nombre": len([u for u in auth_system.users.values() if u['role'] == 'etudiant'])
            }
        ]
        
        st.dataframe(pd.DataFrame(roles_data), use_container_width=True)
        
        # Gestion des permissions
        st.subheader("🔐 Attribution des Rôles")
        
        col1, col2 = st.columns(2)
        
        with col1:
            user_to_modify = st.selectbox("Sélectionner un utilisateur", 
                                        list(auth_system.users.keys()))
            
            current_user = auth_system.users[user_to_modify]
            st.info(f"Rôle actuel: {current_user['role'].title()}")
        
        with col2:
            new_role = st.selectbox("Nouveau rôle", 
                                  ["admin", "professeur", "employee", "etudiant"])
            
            if st.button("🔧 Modifier le rôle", use_container_width=True):
                auth_system.users[user_to_modify]['role'] = new_role
                
                # Journaliser l'action
                auth_system.log_action(
                    st.session_state.user_info['username'],
                    "Modification rôle utilisateur",
                    f"Rôle de {user_to_modify} changé en {new_role}"
                )
                
                st.success(f"✅ Rôle de {user_to_modify} modifié avec succès !")
                time.sleep(1)
                st.rerun()
    
    with tab2:
        st.subheader("📊 Journaux d'Activité du Système")
        
        # Afficher les logs
        if auth_system.actions_log:
            logs_df = pd.DataFrame(auth_system.actions_log)
            
            # Filtres
            col1, col2 = st.columns(2)
            
            with col1:
                user_filter = st.multiselect("Filtrer par utilisateur", 
                                           logs_df['user'].unique())
            
            with col2:
                action_filter = st.multiselect("Filtrer par action", 
                                             logs_df['action'].unique())
            
            # Appliquer filtres
            filtered_logs = logs_df.copy()
            
            if user_filter:
                filtered_logs = filtered_logs[filtered_logs['user'].isin(user_filter)]
            
            if action_filter:
                filtered_logs = filtered_logs[filtered_logs['action'].isin(action_filter)]
            
            # Afficher les logs
            st.dataframe(filtered_logs, use_container_width=True, height=400)
            
            # Statistiques des logs
            st.subheader("📈 Statistiques des Journaux")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Actions par utilisateur
                actions_by_user = filtered_logs['user'].value_counts()
                fig = px.bar(x=actions_by_user.index, y=actions_by_user.values,
                            title="Nombre d'actions par utilisateur",
                            color=actions_by_user.values,
                            color_continuous_scale='Blues')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Répartition des types d'actions
                action_types = filtered_logs['action'].value_counts()
                fig = px.pie(values=action_types.values, names=action_types.index,
                            title="Répartition des types d'actions")
                st.plotly_chart(fig, use_container_width=True)
            
            # Export des logs
            if st.button("📤 Exporter les journaux", use_container_width=True):
                csv = filtered_logs.to_csv(index=False).encode('utf-8')
                
                st.download_button(
                    label="📥 Télécharger les journaux",
                    data=csv,
                    file_name=f"journaux_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        else:
            st.info("Aucun journal d'activité disponible")
    
    with tab3:
        st.subheader("⚙️ Configuration du Système")
        
        # Paramètres généraux
        st.markdown("### 🎯 Paramètres Généraux")
        
        col1, col2 = st.columns(2)
        
        with col1:
            system_name = st.text_input("Nom de l'université", value="Université Paris-Saclay")
            academic_year = st.text_input("Année académique", value="2023-2024")
            language = st.selectbox("Langue", ["Français", "Anglais", "Espagnol"])
        
        with col2:
            timezone = st.selectbox("Fuseau horaire", ["Europe/Paris", "UTC", "America/New_York"])
            date_format = st.selectbox("Format de date", ["DD/MM/YYYY", "MM/DD/YYYY", "YYYY-MM-DD"])
            items_per_page = st.slider("Éléments par page", 10, 100, 25)
        
        # Paramètres de sécurité
        st.markdown("### 🔒 Paramètres de Sécurité")
        
        col1, col2 = st.columns(2)
        
        with col1:
            require_2fa = st.checkbox("Authentification à deux facteurs", value=False)
            session_timeout = st.slider("Délai expiration session (min)", 15, 240, 60)
            max_login_attempts = st.number_input("Tentatives de connexion max", 1, 10, 5)
        
        with col2:
            password_min_length = st.slider("Longueur min mot de passe", 6, 16, 8)
            password_complexity = st.checkbox("Exiger complexité mot de passe", value=True)
            log_failed_attempts = st.checkbox("Journaliser échecs connexion", value=True)
        
        # Paramètres de notification
        st.markdown("### 🔔 Paramètres de Notification")
        
        col1, col2 = st.columns(2)
        
        with col1:
            email_notifications = st.checkbox("Notifications email", value=True)
            sms_notifications = st.checkbox("Notifications SMS", value=False)
            push_notifications = st.checkbox("Notifications push", value=True)
        
        with col2:
            alert_emails = st.text_area("Emails pour alertes", 
                                      placeholder="Un email par ligne")
            notify_admins = st.checkbox("Notifier administrateurs", value=True)
        
        # Bouton de sauvegarde
        if st.button("💾 Sauvegarder la configuration", use_container_width=True):
            st.success("✅ Configuration sauvegardée avec succès !")
            
            # Journaliser l'action
            auth_system.log_action(
                st.session_state.user_info['username'],
                "Modification configuration système",
                "Paramètres système mis à jour"
            )
    
    with tab4:
        st.subheader("🔄 Maintenance du Système")
        
        # Outils de maintenance
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 🗃️ Base de Données")
            
            if st.button("🔄 Optimiser la base", use_container_width=True):
                with st.spinner("Optimisation en cours..."):
                    time.sleep(2)
                    st.success("Base de données optimisée")
            
            if st.button("💾 Sauvegarde", use_container_width=True):
                with st.spinner("Sauvegarde en cours..."):
                    time.sleep(3)
                    st.success("Sauvegarde complète effectuée")
            
            if st.button("📊 Statistiques", use_container_width=True):
                st.info("""
                **Statistiques DB:**
                - Étudiants: 150
                - Professeurs: 15
                - Employés: 30
                - Taille totale: 45 MB
                """)
        
        with col2:
            st.markdown("### 🧹 Nettoyage")
            
            retention_days = st.slider("Conserver les données (jours)", 30, 365, 90)
            
            if st.button("🗑️ Nettoyer logs anciens", use_container_width=True):
                st.success(f"Logs de plus de {retention_days} jours nettoyés")
            
            if st.button("🧽 Cache système", use_container_width=True):
                st.success("Cache système nettoyé")
            
            if st.button("📉 Purger temporaires", use_container_width=True):
                st.success("Fichiers temporaires purgés")
        
        with col3:
            st.markdown("### 🔧 Réparation")
            
            if st.button("🔍 Vérifier intégrité", use_container_width=True):
                with st.spinner("Vérification en cours..."):
                    time.sleep(2)
                    st.success("✅ Système vérifié - Aucune erreur")
            
            if st.button("🛠️ Réparer index", use_container_width=True):
                st.success("Index de la base réparés")
            
            if st.button("📋 État système", use_container_width=True):
                st.info("""
                **État du système:**
                - Services: ✅ Opérationnels
                - Performance: ⚡ Excellente
                - Stockage: 💾 65% utilisé
                - Sécurité: 🔒 Niveau élevé
                """)
        
        # Redémarrage contrôlé
        st.markdown("### 🔄 Contrôle du Système")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Redémarrer services", type="secondary", use_container_width=True):
                st.warning("Redémarrage des services...")
                time.sleep(2)
                st.success("Services redémarrés")
        
        with col2:
            if st.button("⚡ Mode maintenance", type="secondary", use_container_width=True):
                st.info("Mode maintenance activé")
        
        with col3:
            if st.button("🚨 Arrêt d'urgence", type="primary", use_container_width=True):
                st.error("⚠️ ARRÊT D'URGENCE - Confirmer ?")
                if st.checkbox("Je confirme l'arrêt d'urgence"):
                    st.stop()

# Page Dashboard Principal
def show_main_dashboard():
    st.markdown("<h1 class='main-header'>📊 Tableau de Bord Principal</h1>", unsafe_allow_html=True)
    
    role = st.session_state.user_info['role']
    
    if role == 'admin':
        show_admin_main_dashboard()
    elif role == 'professeur':
        show_professor_main_dashboard()
    elif role == 'employee':
        show_employee_main_dashboard()
    elif role == 'etudiant':
        show_student_main_dashboard()

def show_admin_main_dashboard():
    """Dashboard principal pour l'admin"""
    
    # KPIs Principaux
    st.subheader("📈 Indicateurs Clés de Performance")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_students = len(st.session_state.students)
        validated = st.session_state.students['valide'].sum()
        validation_rate = (validated / total_students * 100) if total_students > 0 else 0
        
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-title'>ÉTUDIANTS</div>
            <div class='kpi-value'>{total_students}</div>
            <div>{validation_rate:.1f}% validés</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_professors = len(st.session_state.professors)
        avg_experience = st.session_state.professors['experience'].mean()
        
        st.markdown(f"""
        <div class='kpi-card-secondary'>
            <div class='kpi-title'>PROFESSEURS</div>
            <div class='kpi-value'>{total_professors}</div>
            <div>{avg_experience:.1f} ans d'exp.</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_employees = len(st.session_state.employees)
        active_employees = len(st.session_state.employees[st.session_state.employees['statut'] == 'Actif'])
        
        st.markdown(f"""
        <div class='kpi-card-tertiary'>
            <div class='kpi-title'>EMPLOYÉS</div>
            <div class='kpi-value'>{total_employees}</div>
            <div>{active_employees} actifs</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        total_hours = st.session_state.professors['heures_semaine'].sum()
        total_salary = st.session_state.employees['salaire'].sum()
        
        st.markdown(f"""
        <div class='kpi-card-employee'>
            <div class='kpi-title'>CHARGES</div>
            <div class='kpi-value'>{total_hours}h</div>
            <div>{total_salary:,.0f}€/mois</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Actions rapides
    st.subheader("⚡ Actions Rapides")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("➕ Ajouter étudiant", use_container_width=True):
            st.session_state.selected_page = "👨‍🎓 CRUD Étudiants"
            st.rerun()
    
    with col2:
        if st.button("➕ Ajouter professeur", use_container_width=True):
            st.session_state.selected_page = "👨‍🏫 CRUD Professeurs"
            st.rerun()
    
    with col3:
        if st.button("➕ Ajouter employé", use_container_width=True):
            st.session_state.selected_page = "👔 CRUD Employés"
            st.rerun()
    
    with col4:
        if st.button("📊 Voir rapports", use_container_width=True):
            st.session_state.selected_page = "📊 Dashboard Admin Global"
            st.rerun()
    
    # Alertes récentes
    st.subheader("⚠️ Alertes Récentes")
    
    # Simuler des alertes
    recent_alerts = [
        {"type": "warning", "message": "3 étudiants avec moyenne < 8", "time": "Il y a 2h"},
        {"type": "info", "message": "Rapport mensuel à générer", "time": "Il y a 1 jour"},
        {"type": "danger", "message": "Professeur surchargé (25h/sem)", "time": "Il y a 3 jours"},
        {"type": "success", "message": "Tous les services opérationnels", "time": "Aujourd'hui"}
    ]
    
    for alert in recent_alerts:
        col1, col2 = st.columns([4, 1])
        
        with col1:
            if alert["type"] == "danger":
                st.error(alert["message"])
            elif alert["type"] == "warning":
                st.warning(alert["message"])
            elif alert["type"] == "info":
                st.info(alert["message"])
            else:
                st.success(alert["message"])
        
        with col2:
            st.caption(alert["time"])

def show_professor_main_dashboard():
    """Dashboard principal pour professeurs"""
    prof_details = st.session_state.user_info['details']
    
    st.markdown(f"<h2 class='sub-header'>👨‍🏫 Bienvenue, {prof_details['name']}</h2>", unsafe_allow_html=True)
    
    # Informations rapides
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Heures cette semaine", f"{prof_details.get('heures_semaine', 0)}h")
    
    with col2:
        st.metric("Classes assignées", prof_details.get('classes_assigned', 0))
    
    with col3:
        st.metric("Expérience", f"{prof_details.get('experience', 0)} ans")
    
    # Actions rapides
    st.subheader("📚 Mes Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝 Saisir notes", use_container_width=True):
            st.session_state.selected_page = "📝 Système de Notes"
            st.rerun()
    
    with col2:
        if st.button("📅 Emploi du temps", use_container_width=True):
            st.session_state.selected_page = "🕒 Emploi du Temps"
            st.rerun()
    
    with col3:
        if st.button("👨‍🎓 Mes étudiants", use_container_width=True):
            st.session_state.selected_page = "👨‍🏫 Mon Dashboard Professeur"
            st.rerun()

def show_employee_main_dashboard():
    """Dashboard principal pour employés"""
    emp_details = st.session_state.user_info['details']
    
    st.markdown(f"<h2 class='sub-header'>👔 Bienvenue, {emp_details['name']}</h2>", unsafe_allow_html=True)
    
    # Informations rapides
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Service", emp_details.get('service', 'Non spécifié'))
    
    with col2:
        st.metric("Poste", emp_details.get('poste', 'Non spécifié'))
    
    with col3:
        st.metric("Statut", emp_details.get('statut', 'Actif'))
    
    # Tâches du jour
    st.subheader("📋 Mes Tâches du Jour")
    
    today_tasks = [
        "Traiter les nouvelles inscriptions",
        "Répondre aux emails étudiants",
        "Mettre à jour les dossiers",
        "Préparer la réunion d'équipe"
    ]
    
    for task in today_tasks:
        st.checkbox(task)

def show_student_main_dashboard():
    """Dashboard principal pour étudiants"""
    student_details = st.session_state.user_info['details']
    
    st.markdown(f"<h2 class='sub-header'>👨‍🎓 Bienvenue, {student_details['name']}</h2>", unsafe_allow_html=True)
    
    # Informations rapides
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Filière", student_details.get('filiere', 'Non spécifié'))
    
    with col2:
        st.metric("Niveau", student_details.get('niveau', 'Non spécifié'))
    
    with col3:
        moyenne = student_details.get('moyenne_generale', 0)
        status = "✅ Validé" if moyenne >= 10 else "❌ Non validé"
        st.metric("Statut", status)
    
    # Actions rapides
    st.subheader("🎓 Mes Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📚 Mes notes", use_container_width=True):
            st.session_state.selected_page = "📚 Mon Espace Étudiant"
            st.rerun()
    
    with col2:
        if st.button("📅 Mon emploi du temps", use_container_width=True):
            st.session_state.selected_page = "📅 Mon Emploi du Temps"
            st.rerun()
    
    with col3:
        if st.button("📈 Ma progression", use_container_width=True):
            st.session_state.selected_page = "📈 Ma Progression"
            st.rerun()

# Fonctions restantes simplifiées pour la démonstration
def show_students_management():
    st.info("Gestion avancée des étudiants - Voir CRUD Étudiants pour les fonctionnalités complètes")
    st.write("Cette page offre une gestion avancée des étudiants avec:")
    st.write("- Recherche et filtres avancés")
    st.write("- Statistiques par classe et spécialité")
    st.write("- Analyses géographiques")
    st.write("- Rapports personnalisés")

def show_grades_system():
    st.info("Système de notes complet")
    st.write("Cette page implémente un système complet de gestion des notes avec:")
    st.write("- Saisie des notes avec validation")
    st.write("- Calcul automatique des moyennes")
    st.write("- Système de compensation")
    st.write("- Gestion des sessions de rattrapage")
    st.write("- Export des relevés de notes")

def show_timetable_system():
    st.info("Système d'emploi du temps complet")
    st.write("Cette page implémente un système complet de gestion des emplois du temps avec:")
    st.write("- Planning interactif")
    st.write("- Gestion des salles et ressources")
    st.write("- Conflits et chevauchements")
    st.write("- Export des plannings")
    st.write("- Notifications de changements")

def show_professor_dashboard():
    st.info("Dashboard professeur complet")
    st.write("Cet espace personnel permet aux professeurs de:")
    st.write("- Consulter leurs matières et classes")
    st.write("- Gérer les notes et évaluations")
    st.write("- Analyser les performances de leurs étudiants")
    st.write("- Communiquer avec les étudiants")
    st.write("- Gérer leur emploi du temps")

def show_professor_subjects():
    st.info("Matières du professeur")
    st.write("Cette page permet aux professeurs de:")
    st.write("- Consulter leurs matières assignées")
    st.write("- Voir les statistiques par matière")
    st.write("- Gérer le contenu pédagogique")
    st.write("- Communiquer avec les étudiants de chaque matière")

def show_student_dashboard():
    st.info("Espace étudiant complet")
    st.write("Cet espace personnel permet aux étudiants de:")
    st.write("- Consulter leurs notes et moyennes")
    st.write("- Voir leur progression académique")
    st.write("- Accéder à leur emploi du temps")
    st.write("- Recevoir des alertes personnalisées")
    st.write("- Gérer leur profil")

def show_student_timetable():
    st.info("Emploi du temps étudiant")
    st.write("Cet emploi du temps personnel inclut:")
    st.write("- Vue hebdomadaire et mensuelle")
    st.write("- Notifications des changements")
    st.write("- Export vers calendrier personnel")
    st.write("- Indicateurs de présence")

def show_student_progression():
    st.info("Progression étudiante")
    st.write("Ce module de progression permet de:")
    st.write("- Suivre l'évolution des notes")
    st.write("- Visualiser les crédits obtenus")
    st.write("- Prévoir la réussite aux examens")
    st.write("- Recevoir des recommandations personnalisées")

def show_advanced_statistics():
    st.info("Statistiques avancées")
    st.write("Ce module analytique inclut:")
    st.write("- Analyses prédictives")
    st.write("- Segmentation des étudiants")
    st.write("- Corrélations avancées")
    st.write("- Rapports personnalisables")
    st.write("- Visualisations interactives")

def show_document_management():
    st.info("Gestion des documents")
    st.write("Ce module permet aux employés de:")
    st.write("- Gérer les documents administratifs")
    st.write("- Archiver et classer les dossiers")
    st.write("- Partager des documents sécurisés")
    st.write("- Suivre les versions et modifications")

def show_help_support():
    st.info("Aide et support complet")
    st.write("Cette page offre:")
    st.write("- Documentation détaillée")
    st.write("- Tutoriels et guides")
    st.write("- FAQ organisée")
    st.write("- Support technique")
    st.write("- Système de feedback")



def show_students_management():
    """Gestion avancée des étudiants avec analytics"""
    st.markdown("<h1 class='main-header'>👨‍🎓 Gestion Avancée des Étudiants</h1>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Recherche Avancée", "📊 Analytics", "📍 Cartographie", "📄 Rapports"])
    
    with tab1:
        st.subheader("🔍 Recherche et Filtres Avancés")
        
        # Filtres multi-critères
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            search_nom = st.text_input("Recherche par nom")
        
        with col2:
            search_cne = st.text_input("Recherche par CNE")
        
        with col3:
            filiere_options = ["Toutes"] + st.session_state.students['specialite'].unique().tolist()
            selected_filiere = st.selectbox("Filière", filiere_options)
        
        with col4:
            niveau_options = ["Tous"] + st.session_state.students['niveau'].unique().tolist()
            selected_niveau = st.selectbox("Niveau", niveau_options)
        
        # Filtres supplémentaires
        col1, col2, col3 = st.columns(3)
        
        with col1:
            ville_options = ["Toutes"] + st.session_state.students['ville'].unique().tolist()
            selected_ville = st.selectbox("Ville", ville_options)
        
        with col2:
            statut_options = ["Tous"] + st.session_state.students['statut'].unique().tolist()
            selected_statut = st.selectbox("Statut", statut_options)
        
        with col3:
            min_moyenne = st.slider("Moyenne minimale", 0.0, 20.0, 0.0, 0.5)
        
        # Appliquer les filtres
        filtered_df = st.session_state.students.copy()
        
        if search_nom:
            filtered_df = filtered_df[filtered_df['nom'].str.contains(search_nom, case=False, na=False)]
        
        if search_cne:
            filtered_df = filtered_df[filtered_df['cne'].str.contains(search_cne, case=False, na=False)]
        
        if selected_filiere != "Toutes":
            filtered_df = filtered_df[filtered_df['specialite'] == selected_filiere]
        
        if selected_niveau != "Tous":
            filtered_df = filtered_df[filtered_df['niveau'] == selected_niveau]
        
        if selected_ville != "Toutes":
            filtered_df = filtered_df[filtered_df['ville'] == selected_ville]
        
        if selected_statut != "Tous":
            filtered_df = filtered_df[filtered_df['statut'] == selected_statut]
        
        filtered_df = filtered_df[filtered_df['moyenne_generale'] >= min_moyenne]
        
        # Affichage des résultats
        st.subheader(f"📋 Résultats de la recherche ({len(filtered_df)} étudiants)")
        
        if not filtered_df.empty:
            # Sélection des colonnes
            default_cols = ['cne', 'nom', 'prenom', 'specialite', 'niveau', 'ville', 
                           'moyenne_generale', 'taux_absence', 'statut']
            
            selected_cols = st.multiselect("Colonnes à afficher", 
                                         filtered_df.columns.tolist(),
                                         default=default_cols)
            
            if selected_cols:
                # Pagination
                page_size = st.selectbox("Éléments par page", [10, 25, 50, 100], index=1)
                total_pages = max(1, len(filtered_df) // page_size + (1 if len(filtered_df) % page_size > 0 else 0))
                
                page = st.number_input("Page", min_value=1, max_value=total_pages, value=1)
                start_idx = (page - 1) * page_size
                end_idx = min(page * page_size, len(filtered_df))
                
                st.write(f"Affichage {start_idx + 1} à {end_idx} sur {len(filtered_df)} étudiants")
                
                # Affichage avec style conditionnel
                def highlight_low_grades(val):
                    return 'background-color: #ffcccc' if val < 10 else ''
                
                def highlight_high_absence(val):
                    return 'background-color: #ffebcc' if val > 20 else ''
                
                display_df = filtered_df.iloc[start_idx:end_idx][selected_cols]
                
                if 'moyenne_generale' in selected_cols and 'taux_absence' in selected_cols:
                    styled_df = display_df.style.applymap(
                        highlight_low_grades, subset=['moyenne_generale']
                    ).applymap(
                        highlight_high_absence, subset=['taux_absence']
                    )
                    st.dataframe(styled_df, use_container_width=True, height=400)
                else:
                    st.dataframe(display_df, use_container_width=True, height=400)
                
                # Export des résultats
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("📤 Exporter en CSV", use_container_width=True):
                        csv = filtered_df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="📥 Télécharger CSV",
                            data=csv,
                            file_name=f"etudiants_recherche_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv"
                        )
                
                with col2:
                    if st.button("📊 Exporter en Excel", use_container_width=True):
                        # Créer un fichier Excel
                        output = BytesIO()
                        with pd.ExcelWriter(output, engine='openpyxl') as writer:
                            filtered_df.to_excel(writer, index=False, sheet_name='Étudiants')
                        output.seek(0)
                        
                        st.download_button(
                            label="📥 Télécharger Excel",
                            data=output,
                            file_name=f"etudiants_recherche_{datetime.now().strftime('%Y%m%d')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
        else:
            st.warning("Aucun étudiant ne correspond aux critères de recherche")
    
    with tab2:
        st.subheader("📊 Analytics Avancés")
        
        # KPIs
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total = len(st.session_state.students)
            st.metric("Total étudiants", total)
        
        with col2:
            active = len(st.session_state.students[st.session_state.students['statut'] == 'Actif'])
            st.metric("Étudiants actifs", active, f"{active/total*100:.1f}%")
        
        with col3:
            avg_grade = st.session_state.students['moyenne_generale'].mean()
            st.metric("Moyenne générale", f"{avg_grade:.2f}/20")
        
        with col4:
            avg_absence = st.session_state.students['taux_absence'].mean()
            st.metric("Absence moyenne", f"{avg_absence:.1f}%")
        
        # Graphiques analytics
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribution des notes avec densité
            fig = px.histogram(st.session_state.students, x='moyenne_generale', 
                              nbins=20, marginal='rug',
                              title="Distribution des moyennes avec densité",
                              color_discrete_sequence=['#3498db'])
            
            # Ajouter une courbe de densité
            import plotly.figure_factory as ff
            hist_data = [st.session_state.students['moyenne_generale'].dropna()]
            group_labels = ['Moyennes']
            
            fig2 = ff.create_distplot(hist_data, group_labels, show_hist=False, show_rug=False)
            fig.add_trace(fig2.data[0])
            
            fig.add_vline(x=10, line_dash="dash", line_color="red", annotation_text="Seuil")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Heatmap de corrélation
            corr_data = st.session_state.students[['moyenne_generale', 'taux_absence', 'credits_obtenus']].copy()
            corr_data['annee_inscription'] = st.session_state.students['annee_universitaire']
            
            corr_matrix = corr_data.corr()
            
            fig = px.imshow(corr_matrix,
                           text_auto='.2f',
                           title="Matrice de corrélation",
                           color_continuous_scale='RdBu',
                           aspect='auto')
            st.plotly_chart(fig, use_container_width=True)
        
        # Analyse par filière
        st.subheader("🎓 Analyse par Filière")
        
        filiere_stats = st.session_state.students.groupby('specialite').agg({
            'id': 'count',
            'moyenne_generale': ['mean', 'std', 'min', 'max'],
            'taux_absence': 'mean',
            'valide': 'sum'
        }).round(2)
        
        filiere_stats.columns = ['Effectif', 'Moyenne', 'Écart-type', 'Minimum', 'Maximum', 'Absence moyenne', 'Validés']
        filiere_stats['Taux validation'] = (filiere_stats['Validés'] / filiere_stats['Effectif'] * 100).round(1)
        
        st.dataframe(filiere_stats, use_container_width=True)
    
    with tab3:
        st.subheader("📍 Cartographie des Étudiants")
        
        # Données géographiques simulées
        villes_data = st.session_state.students.groupby('ville').agg({
            'id': 'count',
            'moyenne_generale': 'mean',
            'taux_absence': 'mean'
        }).reset_index()
        
        villes_data.columns = ['Ville', 'Nombre étudiants', 'Moyenne', 'Absence moyenne']
        
        # Coordonnées simulées pour les villes françaises
        ville_coords = {
            'Paris': (48.8566, 2.3522),
            'Lyon': (45.7640, 4.8357),
            'Marseille': (43.2965, 5.3698),
            'Toulouse': (43.6047, 1.4442),
            'Nice': (43.7102, 7.2620),
            'Nantes': (47.2184, -1.5536),
            'Strasbourg': (48.5734, 7.7521)
        }
        
        # Ajouter les coordonnées
        villes_data['Latitude'] = villes_data['Ville'].map(lambda x: ville_coords.get(x, (0, 0))[0])
        villes_data['Longitude'] = villes_data['Ville'].map(lambda x: ville_coords.get(x, (0, 0))[1])
        
        # Créer la carte
        fig = px.scatter_mapbox(villes_data,
                               lat='Latitude',
                               lon='Longitude',
                               size='Nombre étudiants',
                               color='Moyenne',
                               hover_name='Ville',
                               hover_data=['Nombre étudiants', 'Moyenne', 'Absence moyenne'],
                               color_continuous_scale='Viridis',
                               size_max=50,
                               zoom=5,
                               title="Répartition géographique des étudiants")
        
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Statistiques géographiques
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Statistiques par Ville")
            st.dataframe(villes_data.sort_values('Nombre étudiants', ascending=False), 
                        use_container_width=True)
        
        with col2:
            st.subheader("📍 Ville avec la meilleure moyenne")
            best_city = villes_data.loc[villes_data['Moyenne'].idxmax()]
            st.metric(f"🏆 {best_city['Ville']}", 
                     f"{best_city['Moyenne']:.2f}/20",
                     f"{best_city['Nombre étudiants']} étudiants")
            
            st.subheader("📍 Ville la plus représentée")
            largest_city = villes_data.loc[villes_data['Nombre étudiants'].idxmax()]
            st.metric(f"👥 {largest_city['Ville']}", 
                     f"{largest_city['Nombre étudiants']} étudiants",
                     f"Moyenne: {largest_city['Moyenne']:.2f}/20")
    
    with tab4:
        st.subheader("📄 Rapports Personnalisés")
        
        # Types de rapports
        report_types = {
            "Rapport académique complet": "Analyse détaillée des performances",
            "Rapport par filière": "Statistiques par spécialité",
            "Rapport de progression": "Évolution des résultats",
            "Rapport d'absentéisme": "Analyse des présences/absences",
            "Rapport de validation": "Taux de réussite par niveau"
        }
        
        selected_report = st.selectbox("Sélectionner le type de rapport", list(report_types.keys()))
        st.info(report_types[selected_report])
        
        # Paramètres du rapport
        col1, col2 = st.columns(2)
        
        with col1:
            date_debut = st.date_input("Date de début", value=datetime(2023, 9, 1))
            niveau_cible = st.multiselect("Niveau cible", 
                                        st.session_state.students['niveau'].unique())
        
        with col2:
            date_fin = st.date_input("Date de fin", value=datetime.now())
            filiere_cible = st.multiselect("Filière cible", 
                                         st.session_state.students['specialite'].unique())
        
        # Options d'export
        export_format = st.radio("Format d'export", ["PDF", "Excel", "HTML"], horizontal=True)
        
        # Bouton de génération
        if st.button("📊 Générer le rapport", use_container_width=True):
            with st.spinner("Génération du rapport en cours..."):
                time.sleep(2)
                
                # Simulation de rapport généré
                st.success(f"✅ Rapport '{selected_report}' généré avec succès !")
                
                # Afficher un aperçu
                with st.expander("👁️ Aperçu du rapport"):
                    st.subheader(f"Rapport: {selected_report}")
                    st.markdown(f"**Période:** {date_debut.strftime('%d/%m/%Y')} - {date_fin.strftime('%d/%m/%Y')}")
                    st.markdown(f"**Filières:** {', '.join(filiere_cible) if filiere_cible else 'Toutes'}")
                    st.markdown(f"**Niveaux:** {', '.join(niveau_cible) if niveau_cible else 'Tous'}")
                    
                    # Statistiques simulées
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Étudiants concernés", 150)
                        st.metric("Moyenne générale", "12.8/20")
                    
                    with col2:
                        st.metric("Taux de validation", "78.5%")
                        st.metric("Absence moyenne", "15.2%")
                    
                    with col3:
                        st.metric("Meilleure filière", "Informatique")
                        st.metric("Taux d'abandon", "8.3%")
                
                # Bouton de téléchargement
                if export_format == "PDF":
                    st.download_button(
                        label="📥 Télécharger le rapport PDF",
                        data="Simulation de contenu PDF",
                        file_name=f"rapport_{selected_report.replace(' ', '_').lower()}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                elif export_format == "Excel":
                    st.download_button(
                        label="📥 Télécharger le rapport Excel",
                        data="Simulation de contenu Excel",
                        file_name=f"rapport_{selected_report.replace(' ', '_').lower()}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                else:
                    st.download_button(
                        label="📥 Télécharger le rapport HTML",
                        data="<html><body><h1>Rapport HTML simulé</h1></body></html>",
                        file_name=f"rapport_{selected_report.replace(' ', '_').lower()}.html",
                        mime="text/html",
                        use_container_width=True
                    )

def show_grades_system():
    """Système complet de gestion des notes"""
    st.markdown("<h1 class='main-header'>📝 Système de Gestion des Notes</h1>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Saisie des Notes", "🧮 Calcul des Moyennes", "🔄 Compensation", "📅 Sessions", "📄 Relevés"])
    
    with tab1:
        st.subheader("📝 Saisie des Notes")
        
        # Sélection du professeur (simulé)
        prof_name = st.session_state.user_info['name']
        st.info(f"Professeur connecté: {prof_name}")
        
        # Sélection des paramètres
        col1, col2, col3 = st.columns(3)
        
        with col1:
            matieres = ['Algorithme', 'Base de données', 'Réseaux', 'Mathématiques', 'Physique']
            selected_matiere = st.selectbox("Matière", matieres)
        
        with col2:
            types_eval = ['Contrôle 1', 'Contrôle 2', 'Examen Final', 'Rattrapage', 'Projet']
            selected_type = st.selectbox("Type d'évaluation", types_eval)
        
        with col3:
            coefficient = st.selectbox("Coefficient", [1, 2, 3], index=1)
        
        # Recherche d'étudiants
        st.subheader("👨‍🎓 Étudiants à évaluer")
        
        search_class = st.text_input("Rechercher par classe", placeholder="Ex: INFO-3")
        
        if search_class:
            students_to_grade = st.session_state.students[
                st.session_state.students['classe'].str.contains(search_class, case=False, na=False)
            ]
        else:
            # Par défaut, les 10 premiers étudiants
            students_to_grade = st.session_state.students.head(10)
        
        # Formulaire de saisie des notes
        st.subheader("📋 Formulaire de saisie")
        
        with st.form("grades_form"):
            grades_data = []
            
            for idx, student in students_to_grade.iterrows():
                col1, col2, col3, col4 = st.columns([2, 2, 1, 2])
                
                with col1:
                    st.write(f"**{student['nom']} {student['prenom']}**")
                    st.caption(f"CNE: {student['cne']}")
                
                with col2:
                    st.write(f"Classe: {student['classe']}")
                    st.caption(f"Moyenne actuelle: {student['moyenne_generale']}/20")
                
                with col3:
                    note = st.number_input(
                        "Note",
                        min_value=0.0,
                        max_value=20.0,
                        value=10.0,
                        step=0.25,
                        key=f"note_{student['id']}"
                    )
                
                with col4:
                    absence = st.checkbox("Absent", key=f"abs_{student['id']}")
                    if absence:
                        st.warning("Absent")
                
                grades_data.append({
                    'student_id': student['id'],
                    'cne': student['cne'],
                    'nom': student['nom'],
                    'prenom': student['prenom'],
                    'note': note,
                    'absent': absence
                })
                
                st.markdown("---")
            
            # Options supplémentaires
            col1, col2 = st.columns(2)
            
            with col1:
                date_evaluation = st.date_input("Date de l'évaluation", value=datetime.now())
                commentaire = st.text_area("Commentaire général")
            
            with col2:
                validation_auto = st.checkbox("Validation automatique", value=True)
                notification = st.checkbox("Envoyer notification aux étudiants", value=False)
            
            submitted = st.form_submit_button("💾 Enregistrer les notes", use_container_width=True)
            
            if submitted:
                # Validation
                valid_notes = [g for g in grades_data if not g['absent']]
                
                if len(valid_notes) > 0:
                    # Enregistrer les notes
                    for grade in grades_data:
                        if not grade['absent']:
                            new_grade = {
                                'student_id': grade['student_id'],
                                'cne': grade['cne'],
                                'nom': grade['nom'],
                                'prenom': grade['prenom'],
                                'module': selected_matiere,
                                'examen': selected_type,
                                'note': grade['note'],
                                'coefficient': coefficient,
                                'date': date_evaluation.strftime('%Y-%m-%d'),
                                'professeur': prof_name,
                                'valide': grade['note'] >= 10,
                                'commentaire': commentaire
                            }
                            
                            # Ajouter à la liste des notes
                            new_df = pd.DataFrame([new_grade])
                            st.session_state.grades = pd.concat([st.session_state.grades, new_df], ignore_index=True)
                    
                    # Journaliser l'action
                    auth_system.log_action(
                        st.session_state.user_info['username'],
                        "Saisie de notes",
                        f"{len(valid_notes)} notes saisies pour {selected_matiere}"
                    )
                    
                    st.success(f"✅ {len(valid_notes)} notes enregistrées avec succès !")
                    
                    if notification:
                        st.info(f"📧 Notifications envoyées à {len(valid_notes)} étudiants")
                    
                    st.balloons()
                else:
                    st.warning("Aucune note à enregistrer (tous les étudiants sont absents)")
    
    with tab2:
        st.subheader("🧮 Calcul des Moyennes")
        
        # Sélection de la classe
        classes = st.session_state.students['classe'].unique()
        selected_class = st.selectbox("Sélectionner une classe", classes)
        
        if selected_class:
            class_students = st.session_state.students[
                st.session_state.students['classe'] == selected_class
            ]
            
            # Calculer les moyennes par matière
            st.subheader(f"📊 Moyennes pour la classe {selected_class}")
            
            # Récupérer les notes de la classe
            student_ids = class_students['id'].tolist()
            class_grades = st.session_state.grades[
                st.session_state.grades['student_id'].isin(student_ids)
            ]
            
            if not class_grades.empty:
                # Calculer les moyennes par matière
                matieres_moyennes = class_grades.groupby('module').agg({
                    'note': ['mean', 'std', 'count'],
                    'valide': 'mean'
                }).round(2)
                
                matieres_moyennes.columns = ['Moyenne', 'Écart-type', 'Nombre notes', 'Taux validation']
                matieres_moyennes['Taux validation'] = (matieres_moyennes['Taux validation'] * 100).round(1)
                
                st.dataframe(matieres_moyennes, use_container_width=True)
                
                # Graphique des moyennes par matière
                fig = px.bar(matieres_moyennes.reset_index(), 
                            x='module', y='Moyenne',
                            title=f"Moyennes par matière - {selected_class}",
                            color='Moyenne',
                            color_continuous_scale='RdYlGn')
                fig.add_hline(y=10, line_dash="dash", line_color="red", annotation_text="Seuil")
                st.plotly_chart(fig, use_container_width=True)
                
                # Classement des étudiants
                st.subheader("🏆 Classement de la classe")
                
                # Calculer la moyenne générale de chaque étudiant
                student_avg = class_grades.groupby(['student_id', 'nom', 'prenom']).apply(
                    lambda x: (x['note'] * x['coefficient']).sum() / x['coefficient'].sum()
                ).reset_index()
                
                student_avg.columns = ['student_id', 'nom', 'prenom', 'moyenne_generale']
                student_avg = student_avg.sort_values('moyenne_generale', ascending=False)
                student_avg['classement'] = range(1, len(student_avg) + 1)
                
                st.dataframe(student_avg[['classement', 'nom', 'prenom', 'moyenne_generale']], 
                            use_container_width=True)
            else:
                st.info("Aucune note disponible pour cette classe")
    
    with tab3:
        st.subheader("🔄 Système de Compensation")
        
        st.info("""
        Le système de compensation permet aux étudiants de compenser une mauvaise note 
        dans une matière par une bonne note dans une autre matière, selon les règles suivantes:
        
        - **Compensation automatique** : Si moyenne ≥ 10 et aucune note < 6
        - **Compensation par UE** : Compensation entre matières d'une même UE
        - **Compensation annuelle** : Compensation entre semestres
        """)
        
        # Simulation du système de compensation
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Règles de compensation")
            
            compensation_rules = [
                {"Règle": "Moyenne minimale", "Valeur": "10/20"},
                {"Règle": "Note éliminatoire", "Valeur": "< 6/20"},
                {"Règle": "Compensation UE", "Valeur": "Automatique"},
                {"Règle": "Compensation semestre", "Valeur": "Manuelle"},
                {"Règle": "Session rattrapage", "Valeur": "Si moyenne < 10"}
            ]
            
            st.table(pd.DataFrame(compensation_rules))
        
        with col2:
            st.subheader("🧮 Simulateur de compensation")
            
            note1 = st.number_input("Note matière 1", 0.0, 20.0, 12.0, 0.5)
            coef1 = st.number_input("Coefficient matière 1", 1, 5, 3)
            
            note2 = st.number_input("Note matière 2", 0.0, 20.0, 8.0, 0.5)
            coef2 = st.number_input("Coefficient matière 2", 1, 5, 2)
            
            # Calcul
            moyenne_ponderee = (note1 * coef1 + note2 * coef2) / (coef1 + coef2)
            
            # Vérification compensation
            can_compensate = moyenne_ponderee >= 10 and note1 >= 6 and note2 >= 6
            
            st.metric("Moyenne pondérée", f"{moyenne_ponderee:.2f}/20")
            
            if can_compensate:
                st.success("✅ Compensation possible")
                st.info(f"La note {note2}/20 peut être compensée par {note1}/20")
            else:
                st.error("❌ Compensation impossible")
                if moyenne_ponderee < 10:
                    st.warning("Moyenne insuffisante (< 10)")
                if note1 < 6 or note2 < 6:
                    st.warning("Note éliminatoire (< 6) détectée")
    
    with tab4:
        st.subheader("📅 Gestion des Sessions")
        
        sessions = [
            {"Session": "Principale - Semestre 1", "Date": "15/01/2024", "Statut": "Terminée", "Participants": 150},
            {"Session": "Rattrapage - Semestre 1", "Date": "05/02/2024", "Statut": "À venir", "Participants": 25},
            {"Session": "Principale - Semestre 2", "Date": "15/06/2024", "Statut": "Planifiée", "Participants": 160},
            {"Session": "Rattrapage - Semestre 2", "Date": "03/07/2024", "Statut": "Planifiée", "Participants": "À définir"}
        ]
        
        # Liste des sessions
        st.dataframe(pd.DataFrame(sessions), use_container_width=True)
        
        # Gestion des sessions de rattrapage
        st.subheader("🔄 Session de Rattrapage")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Étudiants en rattrapage")
            
            # Simuler des étudiants en rattrapage
            rattrapage_students = st.session_state.students[
                st.session_state.students['moyenne_generale'] < 10
            ].head(5)
            
            if not rattrapage_students.empty:
                for _, student in rattrapage_students.iterrows():
                    with st.container():
                        col_a, col_b, col_c = st.columns([2, 1, 1])
                        
                        with col_a:
                            st.write(f"**{student['nom']} {student['prenom']}**")
                            st.caption(f"{student['classe']}")
                        
                        with col_b:
                            st.write(f"{student['moyenne_generale']}/20")
                        
                        with col_c:
                            matieres = st.multiselect(
                                "Matières",
                                ['Algorithme', 'BDD', 'Réseaux'],
                                key=f"mat_{student['id']}"
                            )
                        
                        st.markdown("---")
            else:
                st.success("✅ Aucun étudiant en rattrapage")
        
        with col2:
            st.markdown("### Planification rattrapage")
            
            with st.form("rattrapage_form"):
                date_rattrapage = st.date_input("Date du rattrapage", 
                                              min_value=datetime.now())
                heure_debut = st.time_input("Heure de début", value=datetime(2024, 1, 1, 9, 0))
                heure_fin = st.time_input("Heure de fin", value=datetime(2024, 1, 1, 12, 0))
                salle = st.text_input("Salle", value="Amphi A")
                
                if st.form_submit_button("📅 Planifier la session"):
                    st.success(f"✅ Session de rattrapage planifiée le {date_rattrapage.strftime('%d/%m/%Y')}")
    
    with tab5:
        st.subheader("📄 Relevés de Notes")
        
        # Sélection de l'étudiant
        students_list = st.session_state.students['cne'] + " - " + \
                       st.session_state.students['nom'] + " " + \
                       st.session_state.students['prenom']
        
        selected_student = st.selectbox("Sélectionner un étudiant", students_list.tolist())
        
        if selected_student:
            cne = selected_student.split(" - ")[0]
            student = st.session_state.students[st.session_state.students['cne'] == cne].iloc[0]
            student_grades = st.session_state.grades[st.session_state.grades['cne'] == cne]
            
            # Aperçu du relevé
            st.subheader(f"📋 Relevé de notes - {student['nom']} {student['prenom']}")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("CNE", student['cne'])
            
            with col2:
                st.metric("Classe", student['classe'])
            
            with col3:
                st.metric("Moyenne générale", f"{student['moyenne_generale']}/20")
            
            with col4:
                statut = "✅ Validé" if student['valide'] else "❌ Non validé"
                st.metric("Statut", statut)
            
            # Détail des notes
            if not student_grades.empty:
                st.subheader("📊 Détail des notes par matière")
                
                # Calculer la moyenne par matière
                matieres_detail = student_grades.groupby('module').agg({
                    'note': ['mean', 'count'],
                    'coefficient': 'sum'
                }).round(2)
                
                matieres_detail.columns = ['Moyenne matière', 'Nombre notes', 'Coefficient total']
                
                st.dataframe(matieres_detail, use_container_width=True)
                
                # Graphique des notes
                fig = px.bar(student_grades, x='module', y='note', color='examen',
                            title="Notes par matière et type d'examen",
                            barmode='group')
                st.plotly_chart(fig, use_container_width=True)
                
                # Bouton d'export
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("📄 Générer PDF", use_container_width=True):
                        st.success("✅ Relevé PDF généré")
                        st.download_button(
                            label="📥 Télécharger PDF",
                            data="Simulation PDF",
                            file_name=f"releve_{cne}_{datetime.now().strftime('%Y%m%d')}.pdf",
                            mime="application/pdf"
                        )
                
                with col2:
                    if st.button("📊 Générer Excel", use_container_width=True):
                        st.success("✅ Relevé Excel généré")
                        st.download_button(
                            label="📥 Télécharger Excel",
                            data="Simulation Excel",
                            file_name=f"releve_{cne}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                
                with col3:
                    if st.button("📧 Envoyer par email", use_container_width=True):
                        st.success("✅ Relevé envoyé par email")
            else:
                st.info("Aucune note disponible pour cet étudiant")

def show_timetable_system():
    """Système complet de gestion des emplois du temps"""
    st.markdown("<h1 class='main-header'>🕒 Système de Gestion des Emplois du Temps</h1>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📅 Planning Interactif", "🏫 Gestion des Salles", "⚠️ Conflits", "📤 Export", "🔔 Notifications"])
    
    with tab1:
        st.subheader("📅 Planning Interactif")
        
        # Filtres
        col1, col2, col3 = st.columns(3)
        
        with col1:
            jour_selection = st.selectbox("Jour", 
                                        ["Tous"] + st.session_state.timetable['jour'].unique().tolist())
        
        with col2:
            classe_selection = st.selectbox("Classe", 
                                          ["Toutes"] + st.session_state.timetable['classe'].unique().tolist())
        
        with col3:
            professeur_selection = st.selectbox("Professeur", 
                                              ["Tous"] + st.session_state.timetable['professeur'].unique().tolist())
        
        # Appliquer les filtres
        filtered_timetable = st.session_state.timetable.copy()
        
        if jour_selection != "Tous":
            filtered_timetable = filtered_timetable[filtered_timetable['jour'] == jour_selection]
        
        if classe_selection != "Toutes":
            filtered_timetable = filtered_timetable[filtered_timetable['classe'] == classe_selection]
        
        if professeur_selection != "Tous":
            filtered_timetable = filtered_timetable[filtered_timetable['professeur'] == professeur_selection]
        
        # Vue planning
        st.subheader("🗓️ Vue Planning")
        
        if not filtered_timetable.empty:
            # Organiser par jour et heure
            jours = filtered_timetable['jour'].unique()
            
            for jour in sorted(jours):
                jour_data = filtered_timetable[filtered_timetable['jour'] == jour]
                
                st.markdown(f"### 📅 {jour}")
                
                for _, seance in jour_data.sort_values('heure').iterrows():
                    with st.expander(f"{seance['heure']} - {seance['module']}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"**Professeur:** {seance['professeur']}")
                            st.markdown(f"**Classe:** {seance['classe']}")
                            st.markdown(f"**Groupe:** {seance['groupe']}")
                        
                        with col2:
                            st.markdown(f"**Salle:** {seance['salle']}")
                            st.markdown(f"**Type:** {seance['type_cours']}")
                            st.markdown(f"**Effectif:** {seance['effectif']} étudiants")
                            st.markdown(f"**Présence:** {seance['presence_reelle']}/{seance['effectif']} ({seance['taux_presence']}%)")
                        
                        # Actions rapides
                        col_a, col_b, col_c = st.columns(3)
                        
                        with col_a:
                            if st.button("✏️ Modifier", key=f"edit_{seance['id']}"):
                                st.info("Fonctionnalité de modification")
                        
                        with col_b:
                            if st.button("❌ Annuler", key=f"cancel_{seance['id']}"):
                                st.warning("Séance annulée")
                        
                        with col_c:
                            if st.button("📝 Présence", key=f"pres_{seance['id']}"):
                                st.info("Saisie des présences")
        else:
            st.info("Aucune séance trouvée avec les critères sélectionnés")
        
        # Vue calendrier
        st.subheader("📆 Vue Calendrier")
        
        # Créer un calendrier interactif
        calendar_data = []
        for _, seance in filtered_timetable.iterrows():
            # Convertir l'heure en format datetime pour le calendrier
            heure_debut = seance['heure'].split('-')[0]
            heure_fin = seance['heure'].split('-')[1]
            
            calendar_data.append({
                'title': f"{seance['module']} - {seance['classe']}",
                'start': f"2024-01-01 {heure_debut}",
                'end': f"2024-01-01 {heure_fin}",
                'resource': seance['salle'],
                'color': '#3498db' if seance['type_cours'] == 'Cours' else 
                        '#2ecc71' if seance['type_cours'] == 'TD' else '#e74c3c'
            })
        
        # Afficher sous forme de tableau
        if calendar_data:
            calendar_df = pd.DataFrame(calendar_data)
            st.dataframe(calendar_df[['title', 'start', 'end', 'resource']], use_container_width=True)
    
    with tab2:
        st.subheader("🏫 Gestion des Salles et Ressources")
        
        # Liste des salles avec capacités
        salles_info = {
            'A101': {'Capacité': 30, 'Type': 'Salle de cours', 'Équipement': 'Vidéoprojecteur, Tableau'},
            'A102': {'Capacité': 30, 'Type': 'Salle de cours', 'Équipement': 'Vidéoprojecteur, Tableau'},
            'A201': {'Capacité': 50, 'Type': 'Amphithéâtre', 'Équipement': 'Vidéoprojecteur, Micro'},
            'A202': {'Capacité': 50, 'Type': 'Amphithéâtre', 'Équipement': 'Vidéoprojecteur, Micro'},
            'B101': {'Capacité': 20, 'Type': 'Salle TP', 'Équipement': 'Ordinateurs, Tableau'},
            'B102': {'Capacité': 20, 'Type': 'Salle TP', 'Équipement': 'Ordinateurs, Tableau'}
        }
        
        # Affichage des salles
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Liste des Salles")
            
            salles_df = pd.DataFrame(salles_info).T.reset_index()
            salles_df.columns = ['Salle', 'Capacité', 'Type', 'Équipement']
            
            st.dataframe(salles_df, use_container_width=True)
        
        with col2:
            st.subheader("📊 Occupation des Salles")
            
            # Calculer l'occupation
            occupation_data = []
            for salle in salles_info.keys():
                seances_salle = st.session_state.timetable[
                    st.session_state.timetable['salle'] == salle
                ]
                capacite = salles_info[salle]['Capacité']
                occupation = len(seances_salle)
                
                occupation_data.append({
                    'Salle': salle,
                    'Capacité': capacite,
                    'Occupation': occupation,
                    'Taux occupation': (occupation / 20 * 100) if occupation > 0 else 0  # 20 créneaux max/semaine
                })
            
            occupation_df = pd.DataFrame(occupation_data)
            occupation_df['Taux occupation'] = occupation_df['Taux occupation'].round(1)
            
            # Graphique d'occupation
            fig = px.bar(occupation_df, x='Salle', y='Taux occupation',
                        title="Taux d'occupation des salles",
                        color='Taux occupation',
                        color_continuous_scale='RdYlGn')
            st.plotly_chart(fig, use_container_width=True)
        
        # Réservation de salle
        st.subheader("📅 Réservation de Salle")
        
        with st.form("reservation_form"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                nouvelle_salle = st.selectbox("Salle", list(salles_info.keys()))
                type_cours = st.selectbox("Type de cours", ['Cours', 'TD', 'TP', 'Réunion'])
            
            with col2:
                jour_reservation = st.selectbox("Jour", 
                                              ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi'])
                heure_reservation = st.selectbox("Heure", 
                                               ['08:00-10:00', '10:15-12:15', '14:00-16:00', '16:15-18:15'])
            
            with col3:
                module_reservation = st.text_input("Module")
                professeur_reservation = st.text_input("Professeur")
                effectif_prev
                effectif_prev = st.number_input("Effectif prévu", min_value=1, max_value=100, value=25)
            
            # Vérifier la disponibilité
            conflits = st.session_state.timetable[
                (st.session_state.timetable['salle'] == nouvelle_salle) &
                (st.session_state.timetable['jour'] == jour_reservation) &
                (st.session_state.timetable['heure'] == heure_reservation)
            ]
            
            if not conflits.empty:
                st.error(f"⚠️ Salle déjà occupée par: {conflits.iloc[0]['module']} ({conflits.iloc[0]['professeur']})")
            elif effectif_prev > salles_info[nouvelle_salle]['Capacité']:
                st.error(f"⚠️ Effectif trop important! Capacité max: {salles_info[nouvelle_salle]['Capacité']}")
            else:
                st.success("✅ Salle disponible")
            
            if st.form_submit_button("✅ Réserver la salle"):
                if not conflits.empty:
                    st.warning("Impossible de réserver - Conflit détecté")
                else:
                    # Ajouter la réservation
                    new_seance = {
                        'id': f"SE{len(st.session_state.timetable):04d}",
                        'jour': jour_reservation,
                        'heure': heure_reservation,
                        'salle': nouvelle_salle,
                        'module': module_reservation,
                        'professeur': professeur_reservation,
                        'classe': "À définir",
                        'groupe': "Groupe unique",
                        'type_cours': type_cours,
                        'semestre': "S3",
                        'effectif': effectif_prev,
                        'presence_reelle': 0,
                        'taux_presence': 0.0
                    }
                    
                    new_df = pd.DataFrame([new_seance])
                    st.session_state.timetable = pd.concat([st.session_state.timetable, new_df], ignore_index=True)
                    
                    st.success(f"✅ Salle {nouvelle_salle} réservée avec succès!")
                    st.balloons()
    
    with tab3:
        st.subheader("⚠️ Détection des Conflits")
        
        # Détecter les conflits
        conflits_data = []
        
        # Conflits salle/heure
        for _, seance in st.session_state.timetable.iterrows():
            autres_seances = st.session_state.timetable[
                (st.session_state.timetable['salle'] == seance['salle']) &
                (st.session_state.timetable['jour'] == seance['jour']) &
                (st.session_state.timetable['heure'] == seance['heure']) &
                (st.session_state.timetable['id'] != seance['id'])
            ]
            
            if not autres_seances.empty:
                for _, autre in autres_seances.iterrows():
                    conflits_data.append({
                        'Type': 'Salle double',
                        'Conflit': f"{seance['professeur']} et {autre['professeur']}",
                        'Détails': f"Salle {seance['salle']} - {seance['jour']} {seance['heure']}",
                        'Sévérité': 'Haute'
                    })
        
        # Conflits professeur/heure
        for _, seance in st.session_state.timetable.iterrows():
            autres_cours = st.session_state.timetable[
                (st.session_state.timetable['professeur'] == seance['professeur']) &
                (st.session_state.timetable['jour'] == seance['jour']) &
                (st.session_state.timetable['heure'] == seance['heure']) &
                (st.session_state.timetable['id'] != seance['id'])
            ]
            
            if not autres_cours.empty:
                for _, autre in autres_cours.iterrows():
                    conflits_data.append({
                        'Type': 'Professeur double',
                        'Conflit': f"{seance['professeur']}",
                        'Détails': f"Deux cours en même temps: {seance['module']} et {autre['module']}",
                        'Sévérité': 'Moyenne'
                    })
        
        # Afficher les conflits
        if conflits_data:
            conflits_df = pd.DataFrame(conflits_data).drop_duplicates()
            
            st.subheader(f"⚠️ {len(conflits_df)} Conflits Détectés")
            st.dataframe(conflits_df, use_container_width=True)
            
            # Graphique des conflits
            fig = px.bar(conflits_df['Type'].value_counts().reset_index(),
                        x='index', y='Type',
                        title="Répartition des types de conflits",
                        labels={'index': 'Type de conflit', 'Type': 'Nombre'})
            st.plotly_chart(fig, use_container_width=True)
            
            # Résolution des conflits
            st.subheader("🔄 Résolution des Conflits")
            
            for idx, conflit in conflits_df.iterrows():
                with st.expander(f"{conflit['Type']}: {conflit['Conflit']}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Détails:** {conflit['Détails']}")
                        st.write(f"**Sévérité:** {conflit['Sévérité']}")
                    
                    with col2:
                        action = st.selectbox("Action corrective", 
                                            ["Ignorer", "Déplacer", "Supprimer", "Réaffecter"],
                                            key=f"action_{idx}")
                        
                        if st.button("Appliquer", key=f"apply_{idx}"):
                            if action == "Déplacer":
                                st.info("Fonctionnalité de déplacement à implémenter")
                            elif action == "Supprimer":
                                st.warning("Séance supprimée")
                            elif action == "Réaffecter":
                                st.info("Réaffectation en cours...")
        else:
            st.success("✅ Aucun conflit détecté dans l'emploi du temps")
    
    with tab4:
        st.subheader("📤 Export des Emplois du Temps")
        
        # Options d'export
        export_type = st.radio("Type d'export", 
                             ["Par classe", "Par professeur", "Par salle", "Complet"],
                             horizontal=True)
        
        # Filtres selon le type
        if export_type == "Par classe":
            classe_export = st.selectbox("Sélectionner la classe", 
                                       st.session_state.timetable['classe'].unique())
            data_export = st.session_state.timetable[
                st.session_state.timetable['classe'] == classe_export
            ]
        elif export_type == "Par professeur":
            prof_export = st.selectbox("Sélectionner le professeur", 
                                     st.session_state.timetable['professeur'].unique())
            data_export = st.session_state.timetable[
                st.session_state.timetable['professeur'] == prof_export
            ]
        elif export_type == "Par salle":
            salle_export = st.selectbox("Sélectionner la salle", 
                                      st.session_state.timetable['salle'].unique())
            data_export = st.session_state.timetable[
                st.session_state.timetable['salle'] == salle_export
            ]
        else:
            data_export = st.session_state.timetable.copy()
        
        # Aperçu des données
        st.subheader("👁️ Aperçu des données")
        st.dataframe(data_export[['jour', 'heure', 'salle', 'module', 'professeur', 'classe']], 
                    use_container_width=True)
        
        # Formats d'export
        st.subheader("📄 Format d'export")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📅 Export iCal", use_container_width=True):
                # Générer un fichier iCal simulé
                ical_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Université//Emploi du Temps//FR
BEGIN:VEVENT
SUMMARY:Emploi du temps {export_type}
DTSTART:20240101T080000
DTEND:20240101T180000
DESCRIPTION:Export {export_type}
END:VEVENT
END:VCALENDAR"""
                
                st.download_button(
                    label="📥 Télécharger iCal",
                    data=ical_content,
                    file_name=f"emploi_du_temps_{export_type.lower()}.ics",
                    mime="text/calendar",
                    use_container_width=True
                )
        
        with col2:
            if st.button("📊 Export Excel", use_container_width=True):
                # Créer un fichier Excel
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    data_export.to_excel(writer, index=False, sheet_name='Emploi du temps')
                    
                    # Ajouter un résumé
                    summary = pd.DataFrame({
                        'Statistique': ['Nombre de séances', 'Nombre de classes', 'Nombre de professeurs'],
                        'Valeur': [len(data_export), 
                                  data_export['classe'].nunique(), 
                                  data_export['professeur'].nunique()]
                    })
                    summary.to_excel(writer, index=False, sheet_name='Résumé')
                
                output.seek(0)
                
                st.download_button(
                    label="📥 Télécharger Excel",
                    data=output,
                    file_name=f"emploi_du_temps_{export_type.lower()}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
        
        with col3:
            if st.button("📱 Export PDF", use_container_width=True):
                st.success("✅ PDF généré")
                st.download_button(
                    label="📥 Télécharger PDF",
                    data="Simulation PDF",
                    file_name=f"emploi_du_temps_{export_type.lower()}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
    
    with tab5:
        st.subheader("🔔 Système de Notifications")
        
        # Configuration des notifications
        st.subheader("⚙️ Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔔 Types de notifications")
            
            notif_types = {
                "Changements emploi du temps": st.checkbox("Changements ED", value=True),
                "Absences professeurs": st.checkbox("Absences profs", value=True),
                "Conflits détectés": st.checkbox("Conflits", value=True),
                "Réservations salles": st.checkbox("Réservations", value=True),
                "Rappels séances": st.checkbox("Rappels", value=True)
            }
        
        with col2:
            st.markdown("### 📱 Canaux de notification")
            
            channels = {
                "Email": st.checkbox("Email", value=True),
                "SMS": st.checkbox("SMS", value=False),
                "Application": st.checkbox("Application", value=True),
                "Web Push": st.checkbox("Web Push", value=True)
            }
            
            frequency = st.selectbox("Fréquence", 
                                   ["Immédiate", "Quotidienne", "Hebdomadaire"])
        
        # Historique des notifications
        st.subheader("📜 Historique des notifications")
        
        # Simuler des notifications
        notifications = [
            {"Date": "2024-01-15 09:30", "Type": "Changement", "Message": "Cours d'Algorithme déplacé en A201", "Statut": "✅ Lu"},
            {"Date": "2024-01-14 14:15", "Type": "Absence", "Message": "Prof. Dupont absent - Cours annulé", "Statut": "✅ Lu"},
            {"Date": "2024-01-14 10:00", "Type": "Rappel", "Message": "TP Réseaux à 14h en B102", "Statut": "✅ Lu"},
            {"Date": "2024-01-13 16:45", "Type": "Conflit", "Message": "Conflit détecté: Salle A101 double", "Statut": "⚠️ Non lu"},
            {"Date": "2024-01-13 08:30", "Type": "Réservation", "Message": "Salle A202 réservée pour réunion", "Statut": "✅ Lu"}
        ]
        
        st.dataframe(pd.DataFrame(notifications), use_container_width=True)
        
        # Test de notification
        st.subheader("🧪 Test de notification")
        
        with st.form("test_notif_form"):
            test_message = st.text_area("Message de test", 
                                      value="Ceci est un message de test du système de notification")
            test_type = st.selectbox("Type", ["Info", "Alerte", "Urgent"])
            
            if st.form_submit_button("📤 Envoyer notification test"):
                st.success("✅ Notification de test envoyée!")
                
                # Afficher un aperçu
                with st.expander("👁️ Aperçu de la notification"):
                    st.info(f"**Type:** {test_type}")
                    st.info(f"**Message:** {test_message}")
                    st.info(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
                    st.info("**Canaux:** Email, Application, Web Push")

def show_professor_dashboard():
    """Dashboard complet pour les professeurs"""
    prof_details = st.session_state.user_info['details']
    
    st.markdown(f"<h1 class='main-header'>👨‍🏫 Dashboard Professeur - {prof_details['name']}</h1>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Mes Informations", "📚 Mes Matières", "👨‍🎓 Mes Étudiants", "📊 Mes Statistiques", "💬 Communication"])
    
    with tab1:
        # Informations personnelles
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📋 Profil Professionnel")
            
            # Afficher les informations
            info_data = {
                "Nom complet": prof_details['name'],
                "Email": prof_details['email'],
                "Téléphone": prof_details.get('phone', 'Non spécifié'),
                "Spécialité": prof_details.get('specialite', 'Non spécifié'),
                "Expérience": f"{prof_details.get('experience', 0)} années",
                "Statut": prof_details.get('statut', 'Non spécifié'),
                "Date d'embauche": prof_details.get('date_embauche', 'Non spécifié'),
                "Heures/semaine": f"{prof_details.get('heures_semaine', 0)} heures",
                "Classes assignées": prof_details.get('classes_assigned', 0)
            }
            
            for key, value in info_data.items():
                st.markdown(f"**{key}:** {value}")
            
            # Matières enseignées
            if 'matieres' in prof_details:
                st.subheader("📚 Matières enseignées")
                matieres_list = prof_details['matieres']
                if isinstance(matieres_list, str):
                    matieres_list = [m.strip() for m in matieres_list.split(',')]
                
                for matiere in matieres_list:
                    st.markdown(f"- {matiere}")
        
        with col2:
            # Photo et actions
            st.markdown("### 🖼️ Photo de profil")
            st.image("https://via.placeholder.com/200x200/3498db/ffffff?text=PROF", width=200)
            
            st.markdown("### ⚡ Actions rapides")
            
            if st.button("✏️ Modifier mon profil", use_container_width=True):
                st.info("Fonctionnalité de modification à implémenter")
            
            if st.button("📅 Mon emploi du temps", use_container_width=True):
                st.session_state.selected_page = "🕒 Emploi du Temps"
                st.rerun()
            
            if st.button("📝 Saisir des notes", use_container_width=True):
                st.session_state.selected_page = "📝 Système de Notes"
                st.rerun()
    
    with tab2:
        st.subheader("📚 Mes Matières et Classes")
        
        # Simuler les matières du professeur
        prof_matieres = ['Algorithme', 'Base de données'] if 'Algorithme' in prof_details.get('matieres', '') else ['Mathématiques', 'Physique']
        prof_classes = ['INFO-3', 'INFO-4', 'MASTER-1']
        
        # Vue par matière
        for matiere in prof_matieres:
            with st.expander(f"📘 {matiere}", expanded=True):
                # Statistiques de la matière
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Étudiants", "45")
                
                with col2:
                    st.metric("Moyenne", "14.2/20")
                
                with col3:
                    st.metric("Taux réussite", "85%")
                
                with col4:
                    st.metric("Heures/semaine", "6h")
                
                # Classes pour cette matière
                st.markdown("**Classes:**")
                for classe in prof_classes:
                    col_a, col_b, col_c = st.columns([2, 2, 1])
                    
                    with col_a:
                        st.write(f"🎓 {classe}")
                    
                    with col_b:
                        st.write("📅 Lundi 10:15-12:15")
                    
                    with col_c:
                        if st.button("📊 Voir", key=f"voir_{matiere}_{classe}"):
                            st.info(f"Statistiques pour {matiere} - {classe}")
                
                st.markdown("---")
        
        # Ajouter une nouvelle matière
        with st.expander("➕ Ajouter une nouvelle matière"):
            with st.form("new_matiere_form"):
                new_matiere = st.text_input("Nom de la matière")
                new_classe = st.selectbox("Classe", prof_classes)
                heures = st.number_input("Heures/semaine", 1, 10, 3)
                semestre = st.selectbox("Semestre", ["S1", "S2", "S3", "S4", "S5", "S6"])
                
                if st.form_submit_button("➕ Ajouter la matière"):
                    if new_matiere:
                        st.success(f"Matière {new_matiere} ajoutée pour la classe {new_classe}")
    
    with tab3:
        st.subheader("👨‍🎓 Mes Étudiants")
        
        # Filtres
        col1, col2 = st.columns(2)
        
        with col1:
            matiere_filter = st.selectbox("Filtrer par matière", 
                                        ["Toutes"] + prof_matieres)
        
        with col2:
            classe_filter = st.selectbox("Filtrer par classe", 
                                       ["Toutes"] + prof_classes)
        
        # Simuler les étudiants du professeur
        students_data = []
        for i in range(25):
            students_data.append({
                'Nom': f'Étudiant{i}',
                'Prénom': f'Prénom{i}',
                'Classe': np.random.choice(prof_classes),
                'Matière': np.random.choice(prof_matieres),
                'Moyenne': round(np.random.uniform(8, 18), 2),
                'Absence': f"{np.random.randint(0, 30)}%",
                'Statut': np.random.choice(['✅ Bon', '⚠️ Moyen', '❌ Faible'], p=[0.6, 0.3, 0.1])
            })
        
        students_df = pd.DataFrame(students_data)
        
        # Appliquer les filtres
        if matiere_filter != "Toutes":
            students_df = students_df[students_df['Matière'] == matiere_filter]
        
        if classe_filter != "Toutes":
            students_df = students_df[students_df['Classe'] == classe_filter]
        
        # Affichage
        st.dataframe(students_df, use_container_width=True)
        
        # Actions sur les étudiants
        st.subheader("⚡ Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📧 Contacter la classe", use_container_width=True):
                st.info("Fonctionnalité de contact à implémenter")
        
        with col2:
            if st.button("📊 Statistiques détaillées", use_container_width=True):
                with st.expander("📈 Statistiques"):
                    st.metric("Nombre d'étudiants", len(students_df))
                    st.metric("Moyenne générale", f"{students_df['Moyenne'].mean():.2f}/20")
                    st.metric("Taux d'absence moyen", f"{students_df['Absence'].str.rstrip('%').astype(float).mean():.1f}%")
        
        with col3:
            if st.button("📄 Exporter la liste", use_container_width=True):
                csv = students_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Télécharger CSV",
                    data=csv,
                    file_name="mes_etudiants.csv",
                    mime="text/csv"
                )
    
    with tab4:
        st.subheader("📊 Mes Statistiques de Performance")
        
        # KPIs
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class='kpi-card'>
                <div class='kpi-title'>ÉTUDIANTS</div>
                <div class='kpi-value'>85</div>
                <div>Total cette année</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='kpi-card-secondary'>
                <div class='kpi-title'>TAUX RÉUSSITE</div>
                <div class='kpi-value'>78.5%</div>
                <div>Moyenne des matières</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class='kpi-card-tertiary'>
                <div class='kpi-title'>SATISFACTION</div>
                <div class='kpi-value'>4.2/5</div>
                <div>Évaluations étudiants</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class='kpi-card-employee'>
                <div class='kpi-title'>HEURES</div>
                <div class='kpi-value'>18</div>
                <div>Par semaine</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Graphiques
        col1, col2 = st.columns(2)
        
        with col1:
            # Évolution des résultats
            months = ['Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb']
            success_rates = [72, 75, 76, 78, 79, 78.5]
            
            fig = px.line(x=months, y=success_rates, markers=True,
                         title="Évolution du taux de réussite",
                         color_discrete_sequence=['#2ecc71'])
            fig.update_layout(xaxis_title="Mois", yaxis_title="Taux de réussite (%)")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Comparaison avec département
            matieres = ['Algorithme', 'BDD', 'Réseaux']
            moyennes_prof = [14.2, 13.8, 15.1]
            moyennes_dept = [12.8, 12.5, 13.2]
            
            fig = go.Figure(data=[
                go.Bar(name='Département', x=matieres, y=moyennes_dept),
                go.Bar(name='Mes résultats', x=matieres, y=moyennes_prof)
            ])
            
            fig.update_layout(
                title="Comparaison avec la moyenne départementale",
                barmode='group',
                xaxis_title="Matière",
                yaxis_title="Moyenne (/20)"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Tableau des évaluations
        st.subheader("📝 Mes Évaluations")
        
        evaluations = [
            {"Semestre": "2023-S1", "Matière": "Algorithme", "Note": 4.5, "Commentaire": "Excellent pédagogie"},
            {"Semestre": "2023-S1", "Matière": "Base de données", "Note": 4.2, "Commentaire": "Très bon cours"},
            {"Semestre": "2023-S2", "Matière": "Algorithme", "Note": 4.3, "Commentaire": "Continuez ainsi"},
            {"Semestre": "2023-S2", "Matière": "Réseaux", "Note": 4.0, "Commentaire": "Bon enseignement"}
        ]
        
        st.dataframe(pd.DataFrame(evaluations), use_container_width=True)
    
    with tab5:
        st.subheader("💬 Communication avec les Étudiants")
        
        # Messagerie
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 📨 Nouveau message")
            
            with st.form("message_form"):
                destinataire = st.selectbox("Destinataire", 
                                          ["Tous mes étudiants", "Par classe", "Par matière", "Étudiant spécifique"])
                
                if destinataire == "Par classe":
                    classe_msg = st.selectbox("Sélectionner la classe", prof_classes)
                elif destinataire == "Par matière":
                    matiere_msg = st.selectbox("Sélectionner la matière", prof_matieres)
                elif destinataire == "Étudiant spécifique":
                    etudiant_msg = st.selectbox("Sélectionner l'étudiant", 
                                              ["Étudiant1", "Étudiant2", "Étudiant3"])
                
                sujet = st.text_input("Sujet", placeholder="Ex: Informations sur le prochain contrôle")
                message = st.text_area("Message", height=150)
                
                piece_jointe = st.file_uploader("Pièce jointe (optionnel)", 
                                              type=['pdf', 'docx', 'ppt', 'jpg'])
                
                col_a, col_b = st.columns(2)
                
                with col_a:
                    envoyer = st.form_submit_button("📤 Envoyer", use_container_width=True)
                
                with col_b:
                    programmer = st.form_submit_button("⏰ Programmer", use_container_width=True)
                
                if envoyer or programmer:
                    if message:
                        st.success("✅ Message envoyé avec succès!")
                    else:
                        st.warning("Veuillez saisir un message")
        
        with col2:
            st.markdown("### 📨 Messages reçus")
            
            messages_recus = [
                {"De": "Étudiant Martin", "Sujet": "Question sur l'examen", "Date": "15/01", "Lu": "✅"},
                {"De": "Administration", "Sujet": "Réunion département", "Date": "14/01", "Lu": "✅"},
                {"De": "Étudiant Dupont", "Sujet": "Absence justifiée", "Date": "13/01", "Lu": "⚠️"},
                {"De": "Direction", "Sujet": "Nouvelles consignes", "Date": "12/01", "Lu": "✅"}
            ]
            
            for msg in messages_recus:
                with st.container():
                    st.write(f"**{msg['De']}**")
                    st.write(f"{msg['Sujet']}")
                    st.write(f"📅 {msg['Date']} {msg['Lu']}")
                    st.markdown("---")
            
            if st.button("📥 Voir tous les messages", use_container_width=True):
                st.info("Fonctionnalité de messagerie complète")

def show_professor_subjects():
    """Page dédiée aux matières du professeur"""
    prof_details = st.session_state.user_info['details']
    
    st.markdown(f"<h1 class='main-header'>📚 Mes Matières - {prof_details['name']}</h1>", unsafe_allow_html=True)
    
    # Simuler les matières avec plus de détails
    subjects_data = [
        {
            "Matière": "Algorithme",
            "Classe": "INFO-3",
            "Semestre": "S3",
            "Heures": "6h/semaine",
            "Étudiants": 45,
            "Moyenne": 14.2,
            "Progression": "+2.5%",
            "Statut": "✅ En cours"
        },
        {
            "Matière": "Base de données",
            "Classe": "INFO-4",
            "Semestre": "S4",
            "Heures": "4h/semaine",
            "Étudiants": 42,
            "Moyenne": 13.8,
            "Progression": "+1.8%",
            "Statut": "✅ En cours"
        },
        {
            "Matière": "Réseaux",
            "Classe": "MASTER-1",
            "Semestre": "S5",
            "Heures": "5h/semaine",
            "Étudiants": 38,
            "Moyenne": 15.1,
            "Progression": "+3.2%",
            "Statut": "✅ En cours"
        }
    ]
    
    # Vue d'ensemble
    st.subheader("📊 Vue d'ensemble de mes matières")
    
    total_students = sum([s["Étudiants"] for s in subjects_data])
    avg_grade = sum([s["Moyenne"] for s in subjects_data]) / len(subjects_data)
    total_hours = sum([int(s["Heures"].split('h')[0]) for s in subjects_data])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total étudiants", total_students)
    
    with col2:
        st.metric("Moyenne générale", f"{avg_grade:.1f}/20")
    
    with col3:
        st.metric("Heures totales", f"{total_hours}h/semaine")
    
    # Détail par matière
    for subject in subjects_data:
        with st.expander(f"📘 {subject['Matière']} - {subject['Classe']} ({subject['Semestre']})", expanded=True):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Étudiants", subject['Étudiants'])
            
            with col2:
                st.metric("Moyenne", f"{subject['Moyenne']}/20")
            
            with col3:
                st.metric("Progression", subject['Progression'])
            
            with col4:
                st.metric("Statut", subject['Statut'])
            
            # Onglets pour chaque matière
            tab1, tab2, tab3, tab4 = st.tabs(["📁 Contenu", "📝 Évaluations", "👨‍🎓 Étudiants", "📊 Statistiques"])
            
            with tab1:
                st.subheader("📁 Contenu pédagogique")
                
                # Plan du cours
                st.markdown("### 📋 Plan du cours")
                chapitres = [
                    "Introduction et complexité",
                    "Structures de données",
                    "Algorithmes de tri",
                    "Algorithmes de recherche",
                    "Graphes et parcours",
                    "Programmation dynamique"
                ]
                
                for chap in chapitres:
                    st.checkbox(chap)
                
                # Ressources
                st.markdown("### 📚 Ressources pédagogiques")
                
                ressources = [
                    {"Type": "📄 Syllabus", "Fichier": "syllabus_algo.pdf", "Date": "01/09/2023"},
                    {"Type": "📊 Présentation", "Fichier": "cours1_algo.pptx", "Date": "05/09/2023"},
                    {"Type": "💻 TP", "Fichier": "tp1_algo.zip", "Date": "12/09/2023"},
                    {"Type": "📝 Contrôle", "Fichier": "controle1_algo.pdf", "Date": "10/10/2023"}
                ]
                
                for res in ressources:
                    col_a, col_b, col_c = st.columns([1, 3, 2])
                    
                    with col_a:
                        st.write(res["Type"])
                    
                    with col_b:
                        st.write(res["Fichier"])
                    
                    with col_c:
                        st.write(res["Date"])
                        if st.button("📥", key=f"dl_{res['Fichier']}"):
                            st.info(f"Téléchargement de {res['Fichier']}")
            
            with tab2:
                st.subheader("📝 Évaluations et notes")
                
                # Types d'évaluation
                evaluations = [
                    {"Type": "Contrôle 1", "Date": "10/10/2023", "Coefficient": 1, "Moyenne": 13.5, "Statut": "✅ Corrigé"},
                    {"Type": "Contrôle 2", "Date": "05/12/2023", "Coefficient": 1, "Moyenne": "À venir", "Statut": "⏳ En cours"},
                    {"Type": "Projet", "Date": "15/12/2023", "Coefficient": 2, "Moyenne": "À venir", "Statut": "📅 Planifié"},
                    {"Type": "Examen final", "Date": "20/01/2024", "Coefficient": 3, "Moyenne": "À venir", "Statut": "📅 Planifié"}
                ]
                
                st.dataframe(pd.DataFrame(evaluations), use_container_width=True)
                
                # Ajouter une évaluation
                with st.expander("➕ Ajouter une évaluation"):
                    with st.form("new_eval_form"):
                        eval_type = st.text_input("Type d'évaluation")
                        eval_date = st.date_input("Date")
                        eval_coef = st.number_input("Coefficient", 1, 5, 1)
                        eval_description = st.text_area("Description")
                        
                        if st.form_submit_button("➕ Ajouter"):
                            st.success(f"Évaluation {eval_type} ajoutée")
            
            with tab3:
                st.subheader("👨‍🎓 Liste des étudiants")
                
                # Simuler des étudiants
                students = []
                for i in range(1, 11):
                    students.append({
                        "Nom": f"Étudiant{i}",
                        "Prénom": f"Prénom{i}",
                        "Moyenne": round(np.random.uniform(8, 18), 1),
                        "Absences": np.random.randint(0, 5),
                        "Statut": np.random.choice(["✅ Excellent", "👍 Bon", "⚠️ Moyen", "❌ Faible"], p=[0.2, 0.5, 0.2, 0.1])
                    })
                
                st.dataframe(pd.DataFrame(students), use_container_width=True)
                
                # Actions
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("📧 Contacter la classe", use_container_width=True):
                        st.info("Fonctionnalité de contact")
                
                with col2:
                    if st.button("📄 Exporter la liste", use_container_width=True):
                        st.success("Liste exportée")
            
            with tab4:
                st.subheader("📊 Statistiques détaillées")
                
                # Graphiques pour la matière
                col1, col2 = st.columns(2)
                
                with col1:
                    # Distribution des notes
                    notes_simulees = np.random.normal(subject['Moyenne'], 2, 100)
                    notes_simulees = np.clip(notes_simulees, 0, 20)
                    
                    fig = px.histogram(x=notes_simulees, nbins=15,
                                      title=f"Distribution des notes - {subject['Matière']}",
                                      color_discrete_sequence=['#3498db'])
                    fig.add_vline(x=10, line_dash="dash", line_color="red")
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Évolution historique
                    annees = ['2019', '2020', '2021', '2022', '2023']
                    moyennes_hist = [12.5, 13.0, 13.5, 14.0, subject['Moyenne']]
                    
                    fig = px.line(x=annees, y=moyennes_hist, markers=True,
                                 title="Évolution de la moyenne sur 5 ans",
                                 color_discrete_sequence=['#2ecc71'])
                    fig.update_layout(xaxis_title="Année", yaxis_title="Moyenne (/20)")
                    st.plotly_chart(fig, use_container_width=True)

def show_student_dashboard():
    """Espace étudiant complet"""
    student_details = st.session_state.user_info['details']
    
    st.markdown(f"<h1 class='main-header'>👨‍🎓 Mon Espace Étudiant - {student_details['name']}</h1>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Mon Profil", "📚 Mes Notes", "📅 Mon Emploi du Temps", "📈 Ma Progression", "🔔 Mes Alertes"])
    
    with tab1:
        # Profil étudiant
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📋 Mes Informations Personnelles")
            
            # Informations de base
            info_data = {
                "Nom complet": student_details['name'],
                "CNE": student_details.get('cne', 'Non spécifié'),
                "Email": student_details.get('email', 'Non spécifié'),
                "Téléphone": student_details.get('phone', 'Non spécifié'),
                "Date de naissance": student_details.get('date_naissance', 'Non spécifié'),
                "Ville": student_details.get('ville', 'Non spécifié')
            }
            
            for key, value in info_data.items():
                st.markdown(f"**{key}:** {value}")
            
            # Informations académiques
            st.subheader("🎓 Mes Informations Académiques")
            
            academic_data = {
                "Filière": student_details.get('filiere', 'Non spécifié'),
                "Spécialité": student_details.get('specialite', 'Non spécifié'),
                "Niveau": student_details.get('niveau', 'Non spécifié'),
                "Classe": student_details.get('classe', 'Non spécifié'),
                "Année universitaire": student_details.get('annee_universitaire', 'Non spécifié'),
                "Statut": student_details.get('statut', 'Non spécifié'),
                "Date d'inscription": student_details.get('date_inscription', 'Non spécifié')
            }
            
            for key, value in academic_data.items():
                st.markdown(f"**{key}:** {value}")
        
        with col2:
            # Photo et stats
            st.markdown("### 🖼️ Photo de profil")
            st.image("https://via.placeholder.com/200x200/2ecc71/ffffff?text=ETU", width=200)
            
            # KPIs rapides
            moyenne = student_details.get('moyenne_generale', 0)
            absence = student_details.get('taux_absence', 0)
            
            st.markdown(f"""
            <div class='kpi-card'>
                <div class='kpi-title'>MA MOYENNE</div>
                <div class='kpi-value'>{moyenne:.2f}/20</div>
                <div>{"✅ Validé" if moyenne >= 10 else "❌ Non validé"}</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class='kpi-card-secondary'>
                <div class='kpi-title'>MON ABSENCE</div>
                <div class='kpi-value'>{absence}%</div>
                <div>{"✅ Normal" if absence <= 20 else "⚠️ Élevé"}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Actions rapides
            st.markdown("### ⚡ Actions")
            
            if st.button("✏️ Modifier mon profil", use_container_width=True):
                st.info("Fonctionnalité à implémenter")
            
            if st.button("📄 Mes documents", use_container_width=True):
                st.info("Accès aux documents")
    
    with tab2:
        st.subheader("📚 Mes Notes par Matière")
        
        # Simuler les notes de l'étudiant
        matieres_notes = [
            {
                "Matière": "Algorithme",
                "Contrôle 1": 14.5,
                "Contrôle 2": 15.0,
                "Examen": 16.0,
                "Moyenne": 15.2,
                "Coefficient": 4,
                "Crédits": "✅ 5",
                "Professeur": "Prof. Dupont"
            },
            {
                "Matière": "Base de données",
                "Contrôle 1": 12.0,
                "Contrôle 2": 13.5,
                "Examen": 14.0,
                "Moyenne": 13.2,
                "Coefficient": 3,
                "Crédits": "✅ 5",
                "Professeur": "Prof. Martin"
            },
            {
                "Matière": "Réseaux",
                "Contrôle 1": 15.5,
                "Contrôle 2": 16.0,
                "Examen": 17.0,
                "Moyenne": 16.2,
                "Coefficient": 4,
                "Crédits": "✅ 5",
                "Professeur": "Prof. Leroy"
            },
            {
                "Matière": "Mathématiques",
                "Contrôle 1": 10.0,
                "Contrôle 2": 11.5,
                "Examen": "À venir",
                "Moyenne": 10.8,
                "Coefficient": 3,
                "Crédits": "⏳ En cours",
                "Professeur": "Prof. Bernard"
            }
        ]
        
        # Afficher les notes
        for matiere in matieres_notes:
            with st.expander(f"📘 {matiere['Matière']} - Moyenne: {matiere['Moyenne']}/20", expanded=True):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Contrôle 1", f"{matiere['Contrôle 1']}/20")
                    st.metric("Contrôle 2", f"{matiere['Contrôle 2']}/20")
                
                with col2:
                    st.metric("Examen", f"{matiere['Examen']}/20" if isinstance(matiere['Examen'], (int, float)) else matiere['Examen'])
                    st.metric("Coefficient", matiere['Coefficient'])
                
                with col3:
                    st.metric("Crédits", matiere['Crédits'])
                    st.metric("Professeur", matiere['Professeur'].split()[-1])
                
                # Graphique d'évolution
                if isinstance(matiere['Examen'], (int, float)):
                    notes = [matiere['Contrôle 1'], matiere['Contrôle 2'], matiere['Examen']]
                    examens = ['Contrôle 1', 'Contrôle 2', 'Examen']
                    
                    fig = px.line(x=examens, y=notes, markers=True,
                                 title=f"Évolution des notes - {matiere['Matière']}",
                                 color_discrete_sequence=['#3498db'])
                    fig.add_hline(y=10, line_dash="dash", line_color="red")
                    fig.update_layout(xaxis_title="Évaluation", yaxis_title="Note (/20)")
                    st.plotly_chart(fig, use_container_width=True)
        
        # Relevé de notes
        st.subheader("📄 Mon Relevé de Notes")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Générer mon relevé", use_container_width=True):
                st.success("✅ Relevé généré")
                st.download_button(
                    label="📥 Télécharger PDF",
                    data="Simulation PDF",
                    file_name=f"releve_{student_details.get('cne', 'etudiant')}.pdf",
                    mime="application/pdf"
                )
        
        with col2:
            if st.button("📧 Envoyer par email", use_container_width=True):
                st.success("✅ Relevé envoyé par email")
        
        with col3:
            if st.button("🖨️ Imprimer", use_container_width=True):
                st.info("🖨️ Impression lancée")

def show_student_timetable():
    """Emploi du temps étudiant"""
    student_details = st.session_state.user_info['details']
    
    st.markdown(f"<h1 class='main-header'>📅 Mon Emploi du Temps - {student_details['name']}</h1>", unsafe_allow_html=True)
    
    # Simuler l'emploi du temps de l'étudiant
    student_classe = student_details.get('classe', 'INFO-3')
    
    # Créer un emploi du temps simulé
    timetable_data = []
    jours = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi']
    creneaux = {
        'Lundi': [
            {"heure": "08:00-10:00", "matière": "Algorithme", "type": "Cours", "salle": "A201", "prof": "Dupont"},
            {"heure": "10:15-12:15", "matière": "Base de données", "type": "TD", "salle": "B102", "prof": "Martin"},
            {"heure": "14:00-16:00", "matière": "Mathématiques", "type": "Cours", "salle": "A101", "prof": "Bernard"}
        ],
        'Mardi': [
            {"heure": "08:00-10:00", "matière": "Réseaux", "type": "Cours", "salle": "A202", "prof": "Leroy"},
            {"heure": "10:15-12:15", "matière": "Algorithme", "type": "TP", "salle": "B101", "prof": "Dupont"}
        ],
        'Mercredi': [
            {"heure": "08:00-12:15", "matière": "Projet informatique", "type": "Projet", "salle": "Labo Info", "prof": "Dupont"},
            {"heure": "14:00-16:00", "matière": "Anglais", "type": "TD", "salle": "C201", "prof": "Smith"}
        ],
        'Jeudi': [
            {"heure": "10:15-12:15", "matière": "Base de données", "type": "TP", "salle": "B102", "prof": "Martin"},
            {"heure": "14:00-16:00", "matière": "Économie", "type": "Cours", "salle": "A101", "prof": "Petit"}
        ],
        'Vendredi': [
            {"heure": "08:00-10:00", "matière": "Réseaux", "type": "TD", "salle": "B201", "prof": "Leroy"},
            {"heure": "10:15-12:15", "matière": "Mathématiques", "type": "TD", "salle": "A102", "prof": "Bernard"}
        ]
    }
    
    # Vue par jour
    st.subheader(f"🗓️ Mon Emploi du Temps - Classe {student_classe}")
    
    selected_day = st.selectbox("Sélectionner un jour", jours)
    
    if selected_day in creneaux:
        st.markdown(f"### 📅 {selected_day}")
        
        cours_du_jour = creneaux[selected_day]
        
        for cours in cours_du_jour:
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 3, 2, 1])
                
                with col1:
                    st.markdown(f"**{cours['heure']}**")
                
                with col2:
                    st.markdown(f"**{cours['matière']}**")
                    st.caption(f"{cours['type']}")
                
                with col3:
                    st.markdown(f"📍 {cours['salle']}")
                    st.caption(f"👨‍🏫 {cours['prof']}")
                
                with col4:
                    if st.button("📍", key=f"map_{selected_day}_{cours['heure']}"):
                        st.info(f"Carte pour {cours['salle']}")
                
                st.markdown("---")
        
        # Résumé du jour
        total_heures = len(cours_du_jour) * 2  # Chaque créneau = 2h
        st.metric(f"Total heures le {selected_day}", f"{total_heures}h")
    
    # Vue semaine complète
    st.subheader("📆 Vue Semaine Complète")
    
    # Créer un tableau de la semaine
    week_data = []
    for jour in jours:
        if jour in creneaux:
            for cours in creneaux[jour]:
                week_data.append({
                    'Jour': jour,
                    'Heure': cours['heure'],
                    'Matière': cours['matière'],
                    'Type': cours['type'],
                    'Salle': cours['salle'],
                    'Professeur': cours['prof']
                })
    
    week_df = pd.DataFrame(week_data)
    
    # Pivot table pour affichage tabulaire
    if not week_df.empty:
        pivot_table = week_df.pivot_table(
            index='Heure',
            columns='Jour',
            values='Matière',
            aggfunc=lambda x: ', '.join(x)
        ).fillna('-')
        
        # Réorganiser les colonnes
        pivot_table = pivot_table.reindex(columns=jours, fill_value='-')
        
        st.dataframe(pivot_table, use_container_width=True)
    
    # Export et fonctionnalités
    st.subheader("⚡ Fonctionnalités")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📅 Export iCal", use_container_width=True):
            st.success("✅ iCal généré")
            st.download_button(
                label="📥 Télécharger",
                data="BEGIN:VCALENDAR...END:VCALENDAR",
                file_name="mon_emploi_du_temps.ics",
                mime="text/calendar"
            )
    
    with col2:
        if st.button("📱 Synchroniser", use_container_width=True):
            st.info("📱 Synchronisation avec Google Calendar/Outlook")
    
    with col3:
        if st.button("🔔 Notifications", use_container_width=True):
            st.info("🔔 Configurer les rappels de cours")

def show_student_progression():
    """Progression académique de l'étudiant"""
    student_details = st.session_state.user_info['details']
    
    st.markdown(f"<h1 class='main-header'>📈 Ma Progression Académique - {student_details['name']}</h1>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Vue d'ensemble", "📈 Évolution", "🎯 Objectifs", "💡 Recommandations"])
    
    with tab1:
        # KPIs de progression
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            moyenne = student_details.get('moyenne_generale', 0)
            st.markdown(f"""
            <div class='kpi-card'>
                <div class='kpi-title'>MA MOYENNE</div>
                <div class='kpi-value'>{moyenne:.2f}/20</div>
                <div>{"🎉 Excellente" if moyenne >= 14 else "✅ Bonne" if moyenne >= 12 else "⚠️ Moyenne" if moyenne >= 10 else "❌ Insuffisante"}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            credits_obtenus = student_details.get('credits_obtenus', 0)
            credits_totaux = student_details.get('credits_totaux', 180)
            progression = (credits_obtenus / credits_totaux * 100) if credits_totaux > 0 else 0
            
            st.markdown(f"""
            <div class='kpi-card-secondary'>
                <div class='kpi-title'>MES CRÉDITS</div>
                <div class='kpi-value'>{credits_obtenus}/{credits_totaux}</div>
                <div>{progression:.1f}% acquis</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            absence = student_details.get('taux_absence', 0)
            st.markdown(f"""
            <div class='kpi-card-tertiary'>
                <div class='kpi-title'>MON ABSENCE</div>
                <div class='kpi-value'>{absence}%</div>
                <div>{"✅ Normal" if absence <= 15 else "⚠️ Attention" if absence <= 25 else "❌ Critique"}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            # Classement simulé
            rang = np.random.randint(1, 50)
            total = np.random.randint(100, 200)
            
            st.markdown(f"""
            <div class='kpi-card-employee'>
                <div class='kpi-title'>MON CLASSEMENT</div>
                <div class='kpi-value'>{rang}/{total}</div>
                <div>Dans ma filière</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Graphique de progression
        st.subheader("📈 Ma Progression Semestrielle")
        
        # Simuler des données de progression
        semestres = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6']
        moyennes_semestres = [10.5, 11.2, 12.0, 12.8, 13.5, student_details.get('moyenne_generale', 14.0)]
        credits_semestres = [25, 50, 80, 105, 135, credits_obtenus]
        
        fig = go.Figure()
        
        # Ajouter la courbe des moyennes
        fig.add_trace(go.Scatter(
            x=semestres,
            y=moyennes_semestres,
            mode='lines+markers',
            name='Moyenne',
            yaxis='y',
            line=dict(color='#3498db', width=3)
        ))
        
        # Ajouter la courbe des crédits
        fig.add_trace(go.Scatter(
            x=semestres,
            y=[c/10 for c in credits_semestres],  # Normaliser pour l'échelle
            mode='lines+markers',
            name='Crédits (÷10)',
            yaxis='y2',
            line=dict(color='#2ecc71', width=3)
        ))
        
        fig.update_layout(
            title="Évolution de ma moyenne et de mes crédits",
            xaxis_title="Semestre",
            yaxis=dict(title="Moyenne (/20)", range=[0, 20]),
            yaxis2=dict(title="Crédits accumulés", overlaying='y', side='right'),
            hovermode='x unified'
        )
        
        # Ligne de seuil
        fig.add_hline(y=10, line_dash="dash", line_color="red", annotation_text="Seuil validation")
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("📊 Évolution Détailée")
        
        # Simulation de données historiques
        months = ['Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun']
        notes_evolution = [10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.2, 13.5, 13.8, student_details.get('moyenne_generale', 14.0)]
        absence_evolution = [20, 18, 16, 15, 14, 13, 12, 11, 10, student_details.get('taux_absence', 9)]
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Évolution des notes
            fig = px.line(x=months, y=notes_evolution, markers=True,
                         title="Évolution de ma moyenne mensuelle",
                         color_discrete_sequence=['#3498db'])
            fig.add_hline(y=10, line_dash="dash", line_color="red")
            fig.add_hrect(y0=14, y1=20, fillcolor="green", opacity=0.1)
            fig.add_hrect(y0=12, y1=14, fillcolor="lightgreen", opacity=0.1)
            fig.add_hrect(y0=10, y1=12, fillcolor="yellow", opacity=0.1)
            fig.add_hrect(y0=0, y1=10, fillcolor="red", opacity=0.1)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Évolution de l'absence
            fig = px.line(x=months, y=absence_evolution, markers=True,
                         title="Évolution de mon taux d'absence",
                         color_discrete_sequence=['#e74c3c'])
            fig.add_hline(y=15, line_dash="dash", line_color="orange", annotation_text="Seuil alerte")
            fig.add_hline(y=25, line_dash="dash", line_color="red", annotation_text="Seuil critique")
            fig.add_hrect(y0=0, y1=15, fillcolor="green", opacity=0.1)
            fig.add_hrect(y0=15, y1=25, fillcolor="orange", opacity=0.1)
            fig.add_hrect(y0=25, y1=100, fillcolor="red", opacity=0.1)
            st.plotly_chart(fig, use_container_width=True)
        
        # Analyse de tendance
        st.subheader("📈 Analyse des Tendances")
        
        if len(notes_evolution) > 1:
            # Calculer la tendance
            x = list(range(len(notes_evolution)))
            z = np.polyfit(x, notes_evolution, 1)
            trend = z[0] * len(notes_evolution)  # Projection sur la période
            
            col1, col2 = st.columns(2)
            
            with col1:
                if trend > 0:
                    st.success(f"📈 Tendance positive: +{trend:.2f} points sur la période")
                    st.metric("Amélioration moyenne", f"+{trend/len(months)*12:.2f} points/an")
                else:
                    st.warning(f"📉 Tendance négative: {trend:.2f} points sur la période")
            
            with col2:
                # Prévision
                future_months = 6
                projection = notes_evolution[-1] + (trend / len(months)) * future_months
                st.metric("Projection 6 mois", f"{projection:.2f}/20")
                
                if projection >= 10:
                    st.success("✅ Bonne probabilité de validation")
                else:
                    st.warning("⚠️ Risque de non-validation")
    
    with tab3:
        st.subheader("🎯 Mes Objectifs Académiques")
        
        # Objectifs personnels
        st.markdown("### 🎯 Définir mes objectifs")
        
        with st.form("objectifs_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                objectif_moyenne = st.number_input("Objectif moyenne (/20)", 
                                                  min_value=0.0, max_value=20.0, 
                                                  value=max(10.0, student_details.get('moyenne_generale', 0) + 1))
                objectif_absence = st.number_input("Objectif absence max (%)", 
                                                  min_value=0.0, max_value=100.0, 
                                                  value=max(5.0, student_details.get('taux_absence', 0) - 5))
            
            with col2:
                objectif_credits = st.number_input("Objectif crédits ce semestre", 
                                                  min_value=0, max_value=60, value=30)
                date_objectif = st.date_input("Date cible", 
                                            value=datetime.now() + timedelta(days=90))
            
            notes_objectifs = st.text_area("Notes personnelles", 
                                         placeholder="Mes stratégies pour atteindre ces objectifs...")
            
            if st.form_submit_button("💾 Enregistrer mes objectifs"):
                st.success("✅ Objectifs enregistrés !")
        
        # Suivi des objectifs
        st.markdown("### 📊 Suivi de mes objectifs")
        
        objectifs_data = [
            {"Objectif": "Moyenne ≥ 14", "Valeur actuelle": f"{student_details.get('moyenne_generale', 0):.2f}/20", "Progression": "85%", "Statut": "🟡 En cours"},
            {"Objectif": "Absence < 10%", "Valeur actuelle": f"{student_details.get('taux_absence', 0)}%", "Progression": "70%", "Statut": "🟡 En cours"},
            {"Objectif": "30 crédits ce semestre", "Valeur actuelle": f"{student_details.get('credits_obtenus', 0)%30}/30", "Progression": "40%", "Statut": "🔴 À améliorer"},
            {"Objectif": "Classement top 25%", "Valeur actuelle": "Top 35%", "Progression": "60%", "Statut": "🟡 En cours"}
        ]
        
        for obj in objectifs_data:
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                
                with col1:
                    st.write(f"**{obj['Objectif']}**")
                
                with col2:
                    st.write(obj["Valeur actuelle"])
                
                with col3:
                    # Barre de progression
                    progress = int(obj['Progression'].rstrip('%'))
                    st.progress(progress/100)
                    st.caption(obj['Progression'])
                
                with col4:
                    st.write(obj['Statut'])
                
                st.markdown("---")
    
    with tab4:
        st.subheader("💡 Recommandations Personnalisées")
        
        # Analyse et recommandations basées sur les données
        moyenne = student_details.get('moyenne_generale', 0)
        absence = student_details.get('taux_absence', 0)
        credits = student_details.get('credits_obtenus', 0)
        
        st.markdown("### 🎓 Analyse de votre situation")
        
        # Recommandations selon le profil
        recommendations = []
        
        if moyenne < 10:
            recommendations.append({
                "type": "❌ Critique",
                "titre": "Risque de non-validation",
                "message": "Votre moyenne est en dessous du seuil de validation. Recommandations:",
                "actions": [
                    "📚 Renforcez votre travail personnel",
                    "👨‍🏫 Consultez vos professeurs régulièrement",
                    "💻 Participez aux séances de rattrapage",
                    "📅 Établissez un planning de révision"
                ]
            })
        elif moyenne < 12:
            recommendations.append({
                "type": "⚠️ Attention",
                "titre": "Moyenne acceptable mais perfectible",
                "message": "Vous validez mais pourriez faire mieux. Suggestions:",
                "actions": [
                    "🎯 Fixez-vous des objectifs plus ambitieux",
                    "📊 Identifiez vos matières faibles",
                    "👥 Travaillez en groupe",
                    "📝 Améliorez vos méthodes de travail"
                ]
            })
        else:
            recommendations.append({
                "type": "✅ Bon",
                "titre": "Bon niveau académique",
                "message": "Continuez sur cette lancée! Pour aller plus loin:",
                "actions": [
                    "🏆 Visez l'excellence (moyenne ≥ 14)",
                    "💼 Développez vos compétences pratiques",
                    "🌍 Pensez aux échanges internationaux",
                    "🎓 Préparez votre projet professionnel"
                ]
            })
        
        if absence > 20:
            recommendations.append({
                "type": "⚠️ Important",
                "titre": "Absentéisme élevé",
                "message": f"Votre taux d'absence ({absence}%) est supérieur à la moyenne. Impacts:",
                "actions": [
                    "📅 Assurez une assiduité régulière",
                    "🏥 Justifiez vos absences si médicales",
                    "📞 Contactez le service social si besoin",
                    "🎯 Priorisez les cours importants"
                ]
            })
        
        # Afficher les recommandations
        for rec in recommendations:
            with st.expander(f"{rec['type']} {rec['titre']}", expanded=True):
                st.write(rec['message'])
                
                for action in rec['actions']:
                    st.checkbox(action)
                
                st.markdown("---")
        
        # Plan d'action personnalisé
        st.markdown("### 📋 Mon Plan d'Action")
        
        with st.form("action_plan_form"):
            actions_perso = st.text_area("Mes actions concrètes pour progresser",
                                       placeholder="Ex: Réviser 2h par jour, Participer en cours, etc.")
            echeance = st.date_input("Échéance de mon plan", 
                                   value=datetime.now() + timedelta(days=30))
            rappel = st.checkbox("Activer les rappels hebdomadaires")
            
            if st.form_submit_button("💾 Enregistrer mon plan d'action"):
                st.success("✅ Plan d'action enregistré !")
                if rappel:
                    st.info("🔔 Rappels activés - Vous recevrez un email hebdomadaire")

# Les autres fonctions restent similaires avec des implémentations complètes...

def show_advanced_statistics():
    """Statistiques avancées avec analytics"""
    st.markdown("<h1 class='main-header'>📈 Analytics Avancés</h1>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Analyses Prédictives", "👥 Segmentation", "🔗 Corrélations", "📋 Rapports"])
    
    with tab1:
        st.subheader("🎯 Analyses Prédictives")
        
        # Modèle de prédiction de réussite
        st.markdown("### 🤖 Prédiction du taux de réussite")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Inputs pour la prédiction
            moyenne_input = st.slider("Moyenne actuelle", 0.0, 20.0, 12.0, 0.5)
            absence_input = st.slider("Taux d'absence", 0.0, 50.0, 15.0, 1.0)
            heures_etude = st.slider("Heures d'étude/semaine", 0, 40, 15)
            participation = st.slider("Participation en cours (1-10)", 1, 10, 7)
        
        with col2:
            # Modèle de prédiction simple
            # Facteurs: moyenne (40%), absence (30%), étude (20%), participation (10%)
            score = (
                moyenne_input * 0.4 +  # 40% de la moyenne
                (20 - absence_input/2.5) * 0.3 +  # 30% de l'absence (inverse)
                heures_etude * 0.2 +  # 20% du temps d'étude
                participation * 0.1    # 10% de participation
            )
            
            # Normaliser entre 0 et 20
            prediction = max(0, min(20, score))
            
            # Probabilité de réussite
            if prediction >= 10:
                prob_reussite = min(95, 70 + (prediction - 10) * 5)
            else:
                prob_reussite = max(5, 30 + prediction * 5)
            
            st.metric("📊 Prédiction moyenne finale", f"{prediction:.2f}/20")
            st.metric("🎯 Probabilité de réussite", f"{prob_reussite:.0f}%")
            
            # Interprétation
            if prob_reussite >= 80:
                st.success("✅ Excellentes chances de réussite")
            elif prob_reussite >= 60:
                st.info("🟡 Bonnes chances de réussite")
            elif prob_reussite >= 40:
                st.warning("🟠 Chances modérées")
            else:
                st.error("🔴 Risque élevé d'échec")
        
        # Graphique de prédiction
        st.markdown("### 📈 Simulation d'amélioration")
        
        # Slider pour simuler l'impact des efforts
        effort_etude = st.slider("Effort supplémentaire d'étude (heures)", -5, 10, 0)
        reduction_absence = st.slider("Réduction d'absence (%)", -10, 10, 0)
        
        # Nouvelle prédiction avec efforts
        nouvelle_prediction = max(0, min(20, 
            prediction + 
            effort_etude * 0.1 +  # Chaque heure supplémentaire = +0.1 point
            (-reduction_absence) * 0.05  # Chaque % réduction = +0.05 point
        ))
        
        # Visualisation
        fig = go.Figure()
        
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=prediction,
            title={'text': "Situation actuelle"},
            domain={'x': [0, 0.45], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 20]},
                'bar': {'color': "#3498db"},
                'steps': [
                    {'range': [0, 10], 'color': "lightgray"},
                    {'range': [10, 20], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 10
                }
            }
        ))
        
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=nouvelle_prediction,
            title={'text': "Avec efforts"},
            domain={'x': [0.55, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 20]},
                'bar': {'color': "#2ecc71"},
                'steps': [
                    {'range': [0, 10], 'color': "lightgray"},
                    {'range': [10, 20], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 10
                }
            }
        ))
        
        fig.update_layout(
            title="Impact des efforts sur la prédiction",
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("👥 Segmentation des Étudiants")
        
        # Clustering des étudiants
        st.markdown("### 🎯 Segmentation par profils académiques")
        
        # Créer des clusters simulés
        students_cluster = st.session_state.students.copy()
        
        # Définir les clusters basés sur moyenne et absence
        conditions = [
            (students_cluster['moyenne_generale'] >= 15) & (students_cluster['taux_absence'] <= 10),
            (students_cluster['moyenne_generale'] >= 12) & (students_cluster['taux_absence'] <= 20),
            (students_cluster['moyenne_generale'] >= 10) & (students_cluster['taux_absence'] <= 30),
            (students_cluster['moyenne_generale'] < 10) | (students_cluster['taux_absence'] > 30)
        ]
        
        clusters = ['🎓 Excellents', '👍 Bons', '🟡 Moyens', '❌ À risque']
        colors = ['#2ecc71', '#3498db', '#f39c12', '#e74c3c']
        
        students_cluster['Cluster'] = np.select(conditions, clusters, default='Inconnu')
        students_cluster['Couleur'] = np.select(conditions, colors, default='gray')
        
        # Visualisation
        fig = px.scatter(students_cluster,
                        x='moyenne_generale',
                        y='taux_absence',
                        color='Cluster',
                        color_discrete_sequence=colors,
                        hover_data=['nom', 'prenom', 'specialite', 'niveau'],
                        title="Segmentation des étudiants par performance",
                        labels={
                            'moyenne_generale': 'Moyenne générale (/20)',
                            'taux_absence': 'Taux d\'absence (%)'
                        })
        
        # Ajouter des zones
        fig.add_hrect(y0=30, y1=100, line_width=0, fillcolor="red", opacity=0.1)
        fig.add_hrect(y0=20, y1=30, line_width=0, fillcolor="orange", opacity=0.1)
        fig.add_hrect(y0=0, y1=20, line_width=0, fillcolor="green", opacity=0.1)
        
        fig.add_vrect(x0=0, x1=10, line_width=0, fillcolor="red", opacity=0.1)
        fig.add_vrect(x0=10, x1=12, line_width=0, fillcolor="orange", opacity=0.1)
        fig.add_vrect(x0=12, x1=15, line_width=0, fillcolor="lightgreen", opacity=0.1)
        fig.add_vrect(x0=15, x1=20, line_width=0, fillcolor="green", opacity=0.1)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Statistiques par cluster
        st.markdown("### 📊 Caractéristiques des clusters")
        
        cluster_stats = students_cluster.groupby('Cluster').agg({
            'id': 'count',
            'moyenne_generale': ['mean', 'std'],
            'taux_absence': 'mean',
            'credits_obtenus': 'mean'
        }).round(2)
        
        cluster_stats.columns = ['Effectif', 'Moyenne', 'Écart-type', 'Absence moyenne', 'Crédits moyens']
        cluster_stats['% Total'] = (cluster_stats['Effectif'] / len(students_cluster) * 100).round(1)
        
        st.dataframe(cluster_stats, use_container_width=True)
        
        # Recommandations par cluster
        st.markdown("### 💡 Stratégies par segment")
        
        strategies = {
            '🎓 Excellents': [
                "Encourager l'excellence avec des projets avancés",
                "Proposer des options d'approfondissement",
                "Orienter vers la recherche ou l'entrepreneuriat"
            ],
            '👍 Bons': [
                "Maintenir la motivation avec des défis stimulants",
                "Renforcer les points forts",
                "Préparer à l'excellence"
            ],
            '🟡 Moyens': [
                "Identifier et combler les lacunes",
                "Renforcer le suivi personnalisé",
                "Améliorer les méthodes de travail"
            ],
            '❌ À risque': [
                "Mettre en place un suivi intensif",
                "Proposer du tutorat et soutien",
                "Établir un plan de rattrapage"
            ]
        }
        
        for cluster, actions in strategies.items():
            with st.expander(f"{cluster} - {len(students_cluster[students_cluster['Cluster']==cluster])} étudiants"):
                for action in actions:
                    st.checkbox(action)

def show_document_management():
    """Gestion des documents pour les employés"""
    employee_details = st.session_state.user_info['details']
    
    st.markdown(f"<h1 class='main-header'>📋 Gestion des Documents - {employee_details['name']}</h1>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📁 Mes Documents", "📤 Partage", "🗂️ Archivage", "📄 Modèles"])
    
    with tab1:
        st.subheader("📁 Mes Documents Personnels")
        
        # Upload de documents
        with st.expander("⬆️ Uploader un nouveau document"):
            uploaded_file = st.file_uploader(
                "Choisir un fichier",
                type=['pdf', 'docx', 'xlsx', 'pptx', 'jpg', 'png'],
                key="doc_upload"
            )
            
            if uploaded_file is not None:
                col1, col2 = st.columns(2)
                
                with col1:
                    nom_doc = st.text_input("Nom du document", 
                                          value=uploaded_file.name)
                    type_doc = st.selectbox("Type", 
                                          ["Administratif", "Pédagogique", "Comptabilité", "Autre"])
                
                with col2:
                    tags = st.multiselect("Tags", 
                                        ["Important", "Confidentiel", "À signer", "Archiver"])
                    dossier = st.selectbox("Dossier", 
                                         ["Courant", "Archives", "Partagé", "Personnel"])
                
                if st.button("💾 Enregistrer le document"):
                    # Simuler l'enregistrement
                    file_size = len(uploaded_file.getvalue()) / 1024  # KB
                    
                    st.success(f"✅ Document '{nom_doc}' enregistré avec succès!")
                    st.info(f"📏 Taille: {file_size:.1f} KB")
                    st.info(f"🏷️ Tags: {', '.join(tags) if tags else 'Aucun'}")
        
        # Liste des documents
        st.subheader("📋 Mes documents récents")
        
        # Simuler des documents
        mes_documents = [
            {
                "Nom": "Contrat étudiant Martin.pdf",
                "Type": "Administratif",
                "Taille": "245 KB",
                "Date": "15/01/2024",
                "Tags": ["Important", "À signer"],
                "Dossier": "Courant"
            },
            {
                "Nom": "Feuille présence Janvier.xlsx",
                "Type": "Administratif",
                "Taille": "128 KB",
                "Date": "14/01/2024",
                "Tags": ["Archiver"],
                "Dossier": "Courant"
            },
            {
                "Nom": "Notes réunion département.docx",
                "Type": "Pédagogique",
                "Taille": "89 KB",
                "Date": "12/01/2024",
                "Tags": ["Important"],
                "Dossier": "Partagé"
            },
            {
                "Nom": "Budget 2024.xlsx",
                "Type": "Comptabilité",
                "Taille": "512 KB",
                "Date": "10/01/2024",
                "Tags": ["Confidentiel", "Important"],
                "Dossier": "Personnel"
            }
        ]
        
        # Filtres
        col1, col2 = st.columns(2)
        
        with col1:
            type_filter = st.multiselect("Filtrer par type", 
                                       ["Administratif", "Pédagogique", "Comptabilité", "Autre"],
                                       default=["Administratif", "Pédagogique"])
        
        with col2:
            tag_filter = st.multiselect("Filtrer par tag", 
                                      ["Important", "Confidentiel", "À signer", "Archiver"])
        
        # Afficher les documents filtrés
        filtered_docs = [d for d in mes_documents if d['Type'] in type_filter]
        if tag_filter:
            filtered_docs = [d for d in filtered_docs if any(tag in d['Tags'] for tag in tag_filter)]
        
        for doc in filtered_docs:
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
                
                with col1:
                    st.write(f"**{doc['Nom']}**")
                    tags_display = " ".join([f"`{tag}`" for tag in doc['Tags']])
                    st.caption(tags_display)
                
                with col2:
                    st.write(doc['Type'])
                
                with col3:
                    st.write(doc['Taille'])
                
                with col4:
                    st.write(doc['Date'])
                
                with col5:
                    if st.button("📥", key=f"dl_{doc['Nom']}"):
                        st.info(f"Téléchargement de {doc['Nom']}")
                
                st.markdown("---")
        
        # Statistiques d'utilisation
        st.subheader("📊 Statistiques de stockage")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Documents totaux", len(mes_documents))
        
        with col2:
            total_size = sum([float(d['Taille'].split()[0]) for d in mes_documents])
            st.metric("Espace utilisé", f"{total_size:.1f} KB")
        
        with col3:
            important_docs = len([d for d in mes_documents if 'Important' in d['Tags']])
            st.metric("Documents importants", important_docs)

def show_help_support():
    """Système d'aide et support complet"""
    st.markdown("<h1 class='main-header'>❓ Aide & Support</h1>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📖 Documentation", "🎥 Tutoriels", "❓ FAQ", "🐛 Support", "💡 Suggestions"])
    
    with tab1:
        st.subheader("📖 Documentation Complète")
        
        # Documentation par module
        modules_docs = {
            "👨‍🎓 Module Étudiants": {
                "description": "Gestion complète des étudiants: ajout, modification, suppression, consultation des dossiers, statistiques individuelles.",
                "sections": [
                    "Fiche étudiant complète",
                    "Historique académique",
                    "Suivi des absences",
                    "Notes et moyennes",
                    "Statistiques personnelles"
                ]
            },
            "👨‍🏫 Module Professeurs": {
                "description": "Dashboard professeur, gestion des notes, suivi des classes, analyse des performances pédagogiques.",
                "sections": [
                    "Dashboard personnalisé",
                    "Gestion des notes",
                    "Suivi des classes",
                    "Analyses pédagogiques",
                    "Rapports d'activité"
                ]
            },
            "👔 Module Employés": {
                "description": "Gestion administrative, documents, support technique, gestion des services.",
                "sections": [
                    "Gestion des documents",
                    "Support administratif",
                    "Gestion des services",
                    "Rapports administratifs",
                    "Coordination"
                ]
            },
            "📊 Analytics": {
                "description": "Analyses statistiques avancées, prédictions, segmentation, rapports personnalisés.",
                "sections": [
                    "Statistiques descriptives",
                    "Analyses prédictives",
                    "Segmentation",
                    "Rapports automatisés",
                    "Visualisations"
                ]
            }
        }
        
        for module, info in modules_docs.items():
            with st.expander(module, expanded=True):
                st.write(info["description"])
                st.markdown("**Fonctionnalités clés:**")
                for section in info["sections"]:
                    st.markdown(f"- {section}")
        
        # Recherche dans la documentation
        st.subheader("🔍 Recherche dans la documentation")
        
        search_query = st.text_input("Rechercher un terme, une fonctionnalité...")
        
        if search_query:
            # Simuler des résultats
            results = [
                "Comment ajouter un étudiant ?",
                "Comment générer un relevé de notes ?",
                "Configurer les notifications",
                "Exporter des données en Excel",
                "Gérer les conflits d'emploi du temps"
            ]
            
            st.info(f"Résultats pour: '{search_query}'")
            for result in results:
                if search_query.lower() in result.lower():
                    with st.expander(result):
                        st.write("Explication détaillée de la fonctionnalité...")
    
    with tab2:
        st.subheader("🎥 Tutoriels Vidéo")
        
        # Catalogue de tutoriels
        tutorials = [
            {
                "id": 1,
                "titre": "Premiers pas avec le système",
                "durée": "5:24",
                "niveau": "Débutant",
                "description": "Découverte de l'interface et navigation de base",
                "vues": "1,245"
            },
            {
                "id": 2,
                "titre": "Saisie des notes efficace",
                "durée": "8:45",
                "niveau": "Professeur",
                "description": "Toutes les astuces pour une saisie rapide et précise",
                "vues": "876"
            },
            {
                "id": 3,
                "titre": "Analyses statistiques avancées",
                "durée": "12:30",
                "niveau": "Avancé",
                "description": "Exploitation des données pour la prise de décision",
                "vues": "543"
            },
            {
                "id": 4,
                "titre": "Gestion des documents",
                "durée": "7:15",
                "niveau": "Employé",
                "description": "Organisation et partage des documents administratifs",
                "vues": "321"
            }
        ]
        
        # Filtres
        col1, col2 = st.columns(2)
        
        with col1:
            niveau_filter = st.multiselect("Niveau", 
                                         ["Débutant", "Intermédiaire", "Avancé", "Professeur", "Employé"])
        
        with col2:
            duree_filter = st.slider("Durée max (minutes)", 0, 30, 15)
        
        # Afficher les tutoriels filtrés
        filtered_tutos = tutorials.copy()
        
        if niveau_filter:
            filtered_tutos = [t for t in filtered_tutos if t['niveau'] in niveau_filter]
        
        filtered_tutos = [t for t in filtered_tutos if float(t['durée'].replace(':', '.')) <= duree_filter]
        
        for tuto in filtered_tutos:
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            
            with col1:
                st.markdown(f"**{tuto['titre']}**")
                st.caption(tuto['description'])
            
            with col2:
                st.markdown(f"⏱️ {tuto['durée']}")
            
            with col3:
                st.markdown(f"📊 {tuto['niveau']}")
            
            with col4:
                if st.button("▶️ Regarder", key=f"watch_{tuto['id']}"):
                    st.info(f"🎥 Lancement du tutoriel: {tuto['titre']}")
                    # Simuler la lecture
                    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")  # URL exemple
            
            st.markdown("---")
        
        # Recommandations personnalisées
        st.subheader("⭐ Recommandé pour vous")
        
        user_role = st.session_state.user_info['role']
        
        if user_role == 'professeur':
            st.info("""
            **Pour les professeurs:**
            - Comment saisir et gérer les notes
            - Utiliser le dashboard professeur
            - Analyser les performances des étudiants
            - Communiquer avec les étudiants
            """)
        elif user_role == 'employee':
            st.info("""
            **Pour les employés:**
            - Gestion des documents administratifs
            - Suivi des procédures
            - Rapports et statistiques
            - Communication inter-services
            """)
        elif user_role == 'etudiant':
            st.info("""
            **Pour les étudiants:**
            - Consulter ses notes et résultats
            - Utiliser l'emploi du temps
            - Suivre sa progression
            - Gérer son profil
            """)

# Fonction principale
def main():
    if not st.session_state.authenticated:
        login_page()
    else:
        main_app()

if __name__ == "__main__":
    main()




             