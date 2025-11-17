from app import app
from models import db, HospitalUser, DiseaseReport

# Create demo hospitals
hospitals_data = [
    {"hospital_name": "Lagos General Hospital", "email": "lagos@hospital.ng", "password": "password123"},
    {"hospital_name": "Dar es Salaam Medical Center", "email": "dar@hospital.tz", "password": "password123"},
    {"hospital_name": "Ahmedabad City Hospital", "email": "ahmedabad@hospital.in", "password": "password123"},
    {"hospital_name": "Mumbai Public Health Unit", "email": "mumbai@hospital.in", "password": "password123"},
    {"hospital_name": "Accra Regional Clinic", "email": "accra@hospital.gh", "password": "password123"},
]

# Create reports linked to hospitals
reports_data = [
    # Lagos (hospital_id=1)
    ("P001", "malaria", "Lagos", 1, "Patient: Amina | Age: 28 | Artemisinin prescribed", 1),
    ("P002", "cholera", "Lagos", 2, "Patient: Tunde | Severe dehydration", 1),
    ("P003", "dengue fever", "Lagos", 1, "Patient: Chioma | Low platelets", 1),
    ("P004", "malaria", "Lagos", 0, "Patient: Emeka | Admitted", 1),
    ("P005", "typhoid", "Lagos", 3, "Patient: Folake | Ciprofloxacin", 1),

    # Dar es Salaam (hospital_id=2)
    ("P006", "malaria", "Dar es Salaam", 2, "Patient: Zawadi | RDT positive", 2),
    ("P007", "cholera", "Dar es Salaam", 1, "Patient: Jabari | IV rehydration", 2),
    ("P008", "malaria", "Dar es Salaam", 4, "Patient: Aisha | Pregnant, careful treatment", 2),
    ("P009", "dengue fever", "Dar es Salaam", 2, "Patient: Rashid | Fever + rash", 2),
    ("P010", "typhoid", "Dar es Salaam", 5, "Patient: Fatuma | Blood culture +", 2),

    # Ahmedabad (hospital_id=3)
    ("P011", "cholera", "Ahmedabad-Ward5", 1, "Patient: Raj | Contaminated well", 3),
    ("P012", "typhoid", "Ahmedabad-Ward5", 2, "Patient: Meera | Salmonella confirmed", 3),
    ("P013", "cholera", "Ahmedabad-Ward5", 0, "Patient: Vikram | Hospitalized", 3),
    ("P014", "hepatitis A", "Ahmedabad-Ward7", 3, "Patient: Anjali | Jaundice", 3),
    ("P015", "dysentery", "Ahmedabad-Ward7", 2, "Patient: Sanjay | Stool pending", 3),

    # Mumbai (hospital_id=4)
    ("P016", "dengue fever", "Mumbai-Dharavi", 1, "Patient: Aman | Platelets low", 4),
    ("P017", "malaria", "Mumbai-Dharavi", 3, "Patient: Sunita | P. falciparum", 4),
    ("P018", "cholera", "Mumbai-Dharavi", 2, "Patient: Farhan | Severe dehydration", 4),
    ("P019", "dengue fever", "Mumbai-Dharavi", 0, "Patient: Leela | Admitted", 4),
    ("P020", "typhoid", "Mumbai-Andheri", 4, "Patient: Neha | Food handler", 4),

    # Accra (hospital_id=5)
    ("P021", "malaria", "Accra", 2, "Patient: Kwame | Treated outpatient", 5),
    ("P022", "yellow fever", "Accra", 5, "Patient: Efua | Vaccination status unknown", 5),
    ("P023", "cholera", "Accra", 1, "Patient: Kofi | Community outbreak", 5),
    ("P024", "malaria", "Accra", 3, "Patient: Ama | Recurrent", 5),
    ("P025", "typhoid", "Accra", 6, "Patient: Yaw | School-linked", 5),
]

if __name__ == '__main__':
    with app.app_context():
        # Clear old data (optional)
        db.drop_all()
        db.create_all()

        # Create hospitals
        hospital_map = {}
        for h in hospitals_data:
            user = HospitalUser(hospital_name=h["hospital_name"], email=h["email"])
            user.set_password(h["password"])
            db.session.add(user)
            db.session.flush()  # Get ID before commit
            hospital_map[h["email"]] = user.id
        db.session.commit()

        # Create reports
        for pid, disease, loc, days, notes, hid in reports_data:
            report = DiseaseReport(
                patient_id=pid,
                disease=disease.lower().strip(),
                location=loc.strip(),
                days_ago=days,
                hospital_id=hid  # ← Link to hospital
            )
            if notes:
                report.set_encrypted_notes(notes)
            db.session.add(report)

        db.session.commit()
        print("✅ Database seeded with 5 hospitals and 25 reports.")