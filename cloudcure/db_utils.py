from models import db, DiseaseReport

def add_disease_report(patient_id, disease, location, days_ago):
    report = DiseaseReport(
        patient_id=patient_id,
        disease=disease.lower().strip(),
        location=location.strip(),
        days_ago=int(days_ago)
    )
    db.session.add(report)
    db.session.commit()
    return report

def get_all_reports():
    return DiseaseReport.query.all()

def get_recent_reports(days=7):
    return DiseaseReport.query.filter(DiseaseReport.days_ago <= days).all()

def get_reports_grouped_by_location():
    reports = get_all_reports()
    grouped = {}
    for r in reports:
        grouped.setdefault(r.location, []).append(r.disease)
    return grouped