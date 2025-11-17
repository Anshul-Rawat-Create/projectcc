from app import app, db
from db_utils import add_disease_report

demo_data = [
    ("P001", "malaria", "Lagos", 1),
    ("P002", "dengue fever", "Lagos", 2),
    ("P003", "cholera", "Lagos", 1),
    ("P004", "malaria", "Lagos", 3),
    ("P005", "typhoid", "Lagos", 2),
    ("P006", "malaria", "Lagos", 0),
    ("P007", "malaria", "Lagos", 1),
    ("P008", "dengue fever", "Lagos", 4),
    ("P009", "measles", "Kano", 5),
    ("P010", "tuberculosis", "Kano", 6),
    ("P011", "malaria", "Kano", 7),
    ("P012", "cholera", "Kano", 10),
    ("P013", "malaria", "Accra", 2),
    ("P014", "yellow fever", "Accra", 3),
    ("P015", "malaria", "Accra", 1),
    ("P016", "influenza", "Nairobi", 5),
    ("P017", "malaria", "Nairobi", 6),
    ("P018", "dengue fever", "Nairobi", 4),
    ("P019", "malaria", "Kampala", 2),
    ("P020", "typhoid", "Kampala", 3),
    ("P021", "cholera", "Kampala", 1),
    ("P022", "measles", "Kampala", 8),
    ("P023", "malaria", "Dar es Salaam", 1),
    ("P024", "malaria", "Dar es Salaam", 2),
    ("P025", "dengue fever", "Dar es Salaam", 3),
    ("P026", "tuberculosis", "Dar es Salaam", 12),
    ("P027", "malaria", "Dar es Salaam", 0),
    ("P028", "malaria", "Dar es Salaam", 1),
    ("P029", "cholera", "Dar es Salaam", 2),
    ("P030", "malaria", "Dar es Salaam", 4),
]

if __name__ == '__main__':
    with app.app_context():
        for pid, disease, loc, days in demo_data:
            try:
                add_disease_report(pid, disease, loc, days)
                print(f"✅ Added: {disease} in {loc}")
            except Exception as e:
                print(f"❌ Failed: {e}")
    print("🎉 Demo data seeded successfully!")