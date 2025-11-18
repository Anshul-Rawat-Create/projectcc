from app import app
from models import db, HospitalUser, DiseaseReport

# Define 6 hospitals (one per location group)
HOSPITALS = [
    {"name": "Ahmedabad General Hospital", "email": "ahmedabad.ward5@hospital.in"},
    {"name": "Ahmedabad Central Medical", "email": "ahmedabad.ward7@hospital.in"},
    {"name": "Mumbai Public Health Unit", "email": "mumbai.dharavi@hospital.in"},
    {"name": "Chennai City Hospital", "email": "chennai.tnagar@hospital.in"},
    {"name": "Kolkata Regional Clinic", "email": "kolkata.howrah@hospital.in"},
    {"name": "Delhi East Community Care", "email": "delhi.east@hospital.in"},
]

# 60 disease reports with notes and hospital_id
REPORTS = [
    # Ahmedabad-Ward5 → hospital_id=1
    ("P001", "cholera", "Ahmedabad-Ward5", 1, "Patient: Raj | Age: 38 | Source: contaminated well", 1),
    ("P002", "typhoid", "Ahmedabad-Ward5", 2, "Patient: Meera | Age: 29 | Salmonella confirmed", 1),
    ("P003", "cholera", "Ahmedabad-Ward5", 0, "Patient: Vikram | Age: 41 | Hospitalized", 1),
    ("P004", "hepatitis A", "Ahmedabad-Ward5", 3, "Patient: Anjali | Age: 24 | Jaundice observed", 1),
    ("P005", "cholera", "Ahmedabad-Ward5", 2, "Patient: Sanjay | Age: 55 | Elderly, high risk", 1),
    ("P006", "typhoid", "Ahmedabad-Ward5", 4, "Patient: Dev | Age: 32 | Full recovery", 1),
    ("P007", "dysentery", "Ahmedabad-Ward5", 1, "Patient: Priya | Age: 30 | Stool culture pending", 1),
    ("P008", "cholera", "Ahmedabad-Ward5", 5, "Patient: Manoj | Age: 44 | Recovered", 1),
    ("P009", "typhoid", "Ahmedabad-Ward5", 2, "Patient: Neha | Age: 27 | Prescribed antibiotics", 1),
    ("P010", "cholera", "Ahmedabad-Ward5", 1, "Patient: Suresh | Age: 50 | IV rehydration", 1),

    # Ahmedabad-Ward7 → hospital_id=2
    ("P011", "cholera", "Ahmedabad-Ward7", 1, "Patient: Arjun | Age: 28 | Recovered", 2),
    ("P012", "typhoid", "Ahmedabad-Ward7", 2, "Patient: Divya | Age: 33 | Blood culture +", 2),
    ("P013", "hepatitis A", "Ahmedabad-Ward7", 3, "Patient: Ravi | Age: 46 | Recovering at home", 2),
    ("P014", "cholera", "Ahmedabad-Ward7", 0, "Patient: Kavita | Age: 35 | Admitted", 2),
    ("P015", "dysentery", "Ahmedabad-Ward7", 2, "Patient: Amit | Age: 42 | Oral meds", 2),
    ("P016", "typhoid", "Ahmedabad-Ward7", 4, "Patient: Sneha | Age: 29 | Follow-up scheduled", 2),
    ("P017", "cholera", "Ahmedabad-Ward7", 1, "Patient: Ramesh | Age: 60 | High risk", 2),
    ("P018", "typhoid", "Ahmedabad-Ward7", 3, "Patient: Leena | Age: 31 | Treated", 2),
    ("P019", "cholera", "Ahmedabad-Ward7", 2, "Patient: Vijay | Age: 37 | Dehydrated", 2),
    ("P020", "hepatitis A", "Ahmedabad-Ward7", 5, "Patient: Anil | Age: 43 | Rest advised", 2),

    # Mumbai-Dharavi → hospital_id=3
    ("P021", "dengue fever", "Mumbai-Dharavi", 1, "Patient: Aman | Age: 25 | Low platelets", 3),
    ("P022", "malaria", "Mumbai-Dharavi", 3, "Patient: Sunita | Age: 37 | P. falciparum", 3),
    ("P023", "cholera", "Mumbai-Dharavi", 2, "Patient: Farhan | Age: 43 | Severe dehydration", 3),
    ("P024", "dengue fever", "Mumbai-Dharavi", 0, "Patient: Leela | Age: 22 | Hospitalized", 3),
    ("P025", "malaria", "Mumbai-Dharavi", 4, "Patient: Irfan | Age: 26 | Under observation", 3),
    ("P026", "dengue fever", "Mumbai-Dharavi", 2, "Patient: Zara | Age: 28 | Fever + rash", 3),
    ("P027", "cholera", "Mumbai-Dharavi", 1, "Patient: Karim | Age: 39 | IV fluids", 3),
    ("P028", "malaria", "Mumbai-Dharavi", 5, "Patient: Nisha | Age: 32 | Artemisinin", 3),
    ("P029", "dengue fever", "Mumbai-Dharavi", 3, "Patient: Sameer | Age: 30 | Rest advised", 3),
    ("P030", "cholera", "Mumbai-Dharavi", 2, "Patient: Rehana | Age: 41 | Recovering", 3),

    # Chennai-TNagar → hospital_id=4
    ("P031", "cholera", "Chennai-TNagar", 1, "Patient: Karthik | Age: 33 | Water source tested", 4),
    ("P032", "typhoid", "Chennai-TNagar", 2, "Patient: Deepa | Age: 28 | Antibiotics started", 4),
    ("P033", "hepatitis A", "Chennai-TNagar", 4, "Patient: Ravi | Age: 46 | Recovering", 4),
    ("P034", "cholera", "Chennai-TNagar", 0, "Patient: Maya | Age: 29 | Admitted", 4),
    ("P035", "typhoid", "Chennai-TNagar", 3, "Patient: Arun | Age: 35 | Prescribed cipro", 4),
    ("P036", "cholera", "Chennai-TNagar", 2, "Patient: Lakshmi | Age: 44 | Oral rehydration", 4),
    ("P037", "dysentery", "Chennai-TNagar", 1, "Patient: Gopal | Age: 31 | Stool pending", 4),
    ("P038", "typhoid", "Chennai-TNagar", 5, "Patient: Shanti | Age: 27 | Full course", 4),
    ("P039", "cholera", "Chennai-TNagar", 2, "Patient: Prakash | Age: 50 | Dehydrated", 4),
    ("P040", "hepatitis A", "Chennai-TNagar", 3, "Patient: Meena | Age: 25 | Jaundice", 4),

    # Kolkata-Howrah → hospital_id=5
    ("P041", "malaria", "Kolkata-Howrah", 2, "Patient: Amit | Age: 31 | Urban mosquito breeding", 5),
    ("P042", "dengue fever", "Kolkata-Howrah", 1, "Patient: Shreya | Age: 27 | Fever + rash", 5),
    ("P043", "cholera", "Kolkata-Howrah", 3, "Patient: Ranjit | Age: 50 | Public health alert", 5),
    ("P044", "malaria", "Kolkata-Howrah", 0, "Patient: Bina | Age: 28 | Artemether", 5),
    ("P045", "dengue fever", "Kolkata-Howrah", 4, "Patient: Dipak | Age: 33 | Low platelets", 5),
    ("P046", "cholera", "Kolkata-Howrah", 2, "Patient: Suchitra | Age: 42 | IV fluids", 5),
    ("P047", "malaria", "Kolkata-Howrah", 1, "Patient: Joy | Age: 26 | Outpatient", 5),
    ("P048", "typhoid", "Kolkata-Howrah", 3, "Patient: Ananya | Age: 30 | Blood +", 5),
    ("P049", "dengue fever", "Kolkata-Howrah", 2, "Patient: Rajesh | Age: 35 | Hospitalized", 5),
    ("P050", "cholera", "Kolkata-Howrah", 1, "Patient: Priyanka | Age: 29 | Recovering", 5),

    # Delhi-East → hospital_id=6
    ("P051", "typhoid", "Delhi-East", 1, "Patient: Rohan | Age: 24 | Travel history: none", 6),
    ("P052", "dengue fever", "Delhi-East", 2, "Patient: Nisha | Age: 35 | Vector control notified", 6),
    ("P053", "typhoid", "Delhi-East", 0, "Patient: Vikas | Age: 33 | Ciprofloxacin", 6),
    ("P054", "dengue fever", "Delhi-East", 3, "Patient: Meher | Age: 28 | Platelets low", 6),
    ("P055", "cholera", "Delhi-East", 2, "Patient: Ankit | Age: 40 | Dehydrated", 6),
    ("P056", "typhoid", "Delhi-East", 4, "Patient: Sonali | Age: 31 | Antibiotics", 6),
    ("P057", "dengue fever", "Delhi-East", 1, "Patient: Kabir | Age: 27 | Fever", 6),
    ("P058", "cholera", "Delhi-East", 3, "Patient: Neha | Age: 36 | Rehydration", 6),
    ("P059", "typhoid", "Delhi-East", 2, "Patient: Arjun | Age: 29 | Treated", 6),
    ("P060", "dengue fever", "Delhi-East", 0, "Patient: Zoya | Age: 25 | Admitted", 6),
]

if __name__ == '__main__':
    with app.app_context():
        # Optional: Clear old data
        db.drop_all()
        db.create_all()

        # Create hospitals
        hospitals = []
        for h in HOSPITALS:
            user = HospitalUser(hospital_name=h["name"], email=h["email"])
            user.set_password("securepassword123")  # All use same demo password
            db.session.add(user)
            db.session.flush()  # So we can get user.id
            hospitals.append(user)

        db.session.commit()

        # Create reports
        for pid, disease, loc, days, notes, hid in REPORTS:
            report = DiseaseReport(
                patient_id=pid,
                disease=disease.lower().strip(),
                location=loc.strip(),
                days_ago=days,
                hospital_id=hid
            )
            if notes:
                report.set_encrypted_notes(notes)
            db.session.add(report)

        db.session.commit()
        print("✅ Seeded 6 hospitals and 60 encrypted disease reports.")