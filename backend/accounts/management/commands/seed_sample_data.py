"""
Seed the database with a realistic sample dataset: doctors, patients,
appointments, prescriptions, and medical reports (with generated placeholder
report images so the AI report summarizer has real files to work against).

Usage:
    python manage.py seed_sample_data            # add sample data
    python manage.py seed_sample_data --flush    # wipe previously seeded sample
                                                  # data first, then reseed

This is dev/demo tooling only — it creates plain-text default passwords and
is not meant to run against a production database.
"""

import io
import random
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction
from PIL import Image, ImageDraw

from appointments.models import Appointment
from doctors.models import Doctor
from patients.models import Patient
from prescriptions.models import Prescription
from reports.models import MedicalReport

User = get_user_model()

DEFAULT_PASSWORD = "demo1234"

# Covers every specialization the frontend already expects (see
# frontend/src/mock/mockData.js) so BookAppointment always has a doctor to
# show for every department in the demo.
DOCTORS = [
    {"first": "Anil", "last": "Sharma", "specialization": "Cardiologist", "experience": 14,
     "qualification": "MBBS, MD (Cardiology)", "available_days": ["Mon", "Wed", "Fri"],
     "visiting_hours": "9:00 AM - 2:00 PM"},
    {"first": "Neha", "last": "Verma", "specialization": "Dermatologist", "experience": 8,
     "qualification": "MBBS, MD (Dermatology)", "available_days": ["Tue", "Thu"],
     "visiting_hours": "11:00 AM - 4:00 PM"},
    {"first": "Ramesh", "last": "Iyer", "specialization": "General Physician", "experience": 20,
     "qualification": "MBBS, MD (General Medicine)",
     "available_days": ["Mon", "Tue", "Wed", "Thu", "Fri"], "visiting_hours": "9:00 AM - 1:00 PM"},
    {"first": "Priya", "last": "Nair", "specialization": "Orthopedic", "experience": 11,
     "qualification": "MBBS, MS (Orthopedics)", "available_days": ["Mon", "Thu"],
     "visiting_hours": "2:00 PM - 6:00 PM"},
    {"first": "Karan", "last": "Mehta", "specialization": "Endocrinologist", "experience": 9,
     "qualification": "MBBS, DM (Endocrinology)", "available_days": ["Wed", "Fri"],
     "visiting_hours": "10:00 AM - 1:00 PM"},
    {"first": "Farah", "last": "Khan", "specialization": "Pediatrician", "experience": 13,
     "qualification": "MBBS, MD (Pediatrics)", "available_days": ["Mon", "Wed", "Fri"],
     "visiting_hours": "10:00 AM - 3:00 PM"},
    {"first": "Suresh", "last": "Reddy", "specialization": "Neurologist", "experience": 17,
     "qualification": "MBBS, DM (Neurology)", "available_days": ["Tue", "Thu"],
     "visiting_hours": "1:00 PM - 5:00 PM"},
    {"first": "Meenal", "last": "Gupta", "specialization": "Gynecologist", "experience": 15,
     "qualification": "MBBS, MS (Obstetrics & Gynecology)", "available_days": ["Mon", "Wed", "Fri"],
     "visiting_hours": "9:00 AM - 12:00 PM"},
    {"first": "Vivek", "last": "Bhatt", "specialization": "ENT Specialist", "experience": 10,
     "qualification": "MBBS, MS (ENT)", "available_days": ["Tue", "Thu", "Sat"],
     "visiting_hours": "3:00 PM - 6:00 PM"},
    {"first": "Alia", "last": "Malhotra", "specialization": "Psychiatrist", "experience": 12,
     "qualification": "MBBS, MD (Psychiatry)", "available_days": ["Wed", "Fri"],
     "visiting_hours": "11:00 AM - 2:00 PM"},
    {"first": "Rajat", "last": "Joshi", "specialization": "Dentist", "experience": 7,
     "qualification": "BDS, MDS", "available_days": ["Mon", "Tue", "Wed", "Thu", "Fri"],
     "visiting_hours": "10:00 AM - 4:00 PM"},
    {"first": "Divya", "last": "Rao", "specialization": "Ophthalmologist", "experience": 16,
     "qualification": "MBBS, MS (Ophthalmology)", "available_days": ["Mon", "Thu", "Sat"],
     "visiting_hours": "9:00 AM - 1:00 PM"},
]

PATIENTS = [
    {"first": "Riya", "last": "Kapoor", "gender": "F", "blood_group": "O+", "age": 24,
     "allergies": "Penicillin", "past_diseases": ["Mild Anemia (2026)"]},
    {"first": "Arjun", "last": "Mehta", "gender": "M", "blood_group": "B+", "age": 38,
     "allergies": "None known", "past_diseases": ["Borderline High Cholesterol (2026)"]},
    {"first": "Sana", "last": "Sheikh", "gender": "F", "blood_group": "A-", "age": 29,
     "allergies": "Sulfa drugs", "past_diseases": []},
    {"first": "Vikram", "last": "Rao", "gender": "M", "blood_group": "AB+", "age": 52,
     "allergies": "None known", "past_diseases": ["Type 2 Diabetes (2023)", "Hypertension (2025)"]},
    {"first": "Ananya", "last": "Ghosh", "gender": "F", "blood_group": "B-", "age": 31,
     "allergies": "Peanuts", "past_diseases": []},
    {"first": "Farhan", "last": "Ahmed", "gender": "M", "blood_group": "O-", "age": 45,
     "allergies": "Ibuprofen", "past_diseases": ["Coronary Artery Disease (2024)"]},
    {"first": "Meera", "last": "Pillai", "gender": "F", "blood_group": "A+", "age": 19,
     "allergies": "None known", "past_diseases": []},
    {"first": "Rohit", "last": "Desai", "gender": "M", "blood_group": "B+", "age": 60,
     "allergies": "Aspirin", "past_diseases": ["Osteoarthritis (2022)", "Type 2 Diabetes (2021)"]},
    {"first": "Ishaan", "last": "Kapoor", "gender": "M", "blood_group": "O+", "age": 8,
     "allergies": "None known", "past_diseases": []},
    {"first": "Zara", "last": "Sheikh", "gender": "F", "blood_group": "A+", "age": 6,
     "allergies": "Eggs", "past_diseases": ["Mild Asthma (2025)"]},
    {"first": "Kabir", "last": "Chatterjee", "gender": "M", "blood_group": "B-", "age": 34,
     "allergies": "None known", "past_diseases": []},
    {"first": "Naina", "last": "Bose", "gender": "F", "blood_group": "AB-", "age": 27,
     "allergies": "Latex", "past_diseases": ["Migraine (2024)"]},
    {"first": "Aditya", "last": "Kulkarni", "gender": "M", "blood_group": "O+", "age": 67,
     "allergies": "None known", "past_diseases": ["Hypertension (2018)", "Coronary Artery Disease (2022)"]},
    {"first": "Priyanka", "last": "Iyer", "gender": "F", "blood_group": "B+", "age": 42,
     "allergies": "Sulfa drugs", "past_diseases": ["Hypothyroidism (2020)"]},
    {"first": "Dev", "last": "Patel", "gender": "M", "blood_group": "A+", "age": 55,
     "allergies": "None known", "past_diseases": ["Type 2 Diabetes (2019)"]},
    {"first": "Ritu", "last": "Sinha", "gender": "F", "blood_group": "O-", "age": 15,
     "allergies": "None known", "past_diseases": []},
    {"first": "Manav", "last": "Choudhury", "gender": "M", "blood_group": "AB+", "age": 71,
     "allergies": "Aspirin", "past_diseases": ["Osteoarthritis (2015)", "Hypertension (2017)"]},
    {"first": "Alisha", "last": "Menon", "gender": "F", "blood_group": "B+", "age": 33,
     "allergies": "Penicillin", "past_diseases": []},
    {"first": "Yusuf", "last": "Ansari", "gender": "M", "blood_group": "A-", "age": 48,
     "allergies": "None known", "past_diseases": ["Fatty Liver (2023)"]},
    {"first": "Tara", "last": "Krishnan", "gender": "F", "blood_group": "O+", "age": 39,
     "allergies": "None known", "past_diseases": ["Anxiety Disorder (2022)"]},
]

# Report templates cover the panels report_summarizer.py + lab_reference_ranges.json
# know how to parse. Value ranges deliberately span both normal and abnormal so
# some (not all) seeded reports come back flagged -- a mix is more realistic
# and more useful for a demo than either "everything flagged" or "everything
# clean".
REPORT_TEMPLATES = [
    {
        "report_type": "Blood Test (CBC)",
        "raw_text": ("Complete Blood Count\nHemoglobin: {hb} g/dL\nWBC Count: {wbc} /uL\n"
                     "Platelet Count: {plt} /uL\nFasting Blood Sugar: {sugar} mg/dL"),
        "values": lambda: {
            "hb": round(random.uniform(9.5, 15.5), 1),
            "wbc": random.randint(3500, 12000),
            "plt": random.randint(140000, 420000),
            "sugar": random.randint(80, 160),
        },
    },
    {
        "report_type": "Lipid Profile",
        "raw_text": ("Lipid Profile\nTotal Cholesterol: {tc} mg/dL\nLDL: {ldl} mg/dL\n"
                     "HDL: {hdl} mg/dL\nTriglycerides: {tg} mg/dL"),
        "values": lambda: {
            "tc": random.randint(150, 260),
            "ldl": random.randint(80, 190),
            "hdl": random.randint(35, 65),
            "tg": random.randint(90, 250),
        },
    },
    {
        "report_type": "ECG",
        "raw_text": ("ECG Report\nHeart Rate: {hr} bpm\nRhythm: {rhythm}\nPR Interval: {pr} ms"),
        "values": lambda: {
            "hr": random.randint(58, 105),
            "rhythm": random.choice(["Normal sinus rhythm", "Sinus tachycardia", "Normal sinus rhythm"]),
            "pr": random.randint(120, 200),
        },
    },
    {
        "report_type": "Liver Function Test",
        "raw_text": ("Liver Function Test\nALT: {alt} U/L\nAST: {ast} U/L"),
        "values": lambda: {
            "alt": random.randint(15, 95),
            "ast": random.randint(10, 70),
        },
    },
    {
        "report_type": "Thyroid Profile",
        "raw_text": ("Thyroid Profile\nTSH: {tsh} mIU/L"),
        "values": lambda: {
            "tsh": round(random.uniform(0.2, 6.5), 1),
        },
    },
    {
        "report_type": "HbA1c (Diabetes Panel)",
        "raw_text": ("HbA1c Test\nHbA1c: {hba1c} %"),
        "values": lambda: {
            "hba1c": round(random.uniform(4.5, 8.2), 1),
        },
    },
]


def make_placeholder_image(title, lines, size=(600, 800)):
    """Render a simple placeholder 'report scan' image with the given text so
    seeded MedicalReport rows have a real file attached, without needing any
    external image downloads."""
    img = Image.new("RGB", size, color=(250, 250, 248))
    draw = ImageDraw.Draw(img)
    draw.rectangle([(0, 0), (size[0] - 1, 90)], fill=(30, 60, 90))
    draw.text((20, 30), title, fill=(255, 255, 255))
    y = 130
    for line in lines:
        draw.text((30, y), line, fill=(20, 20, 20))
        y += 30
    draw.rectangle([(0, 0), (size[0] - 1, size[1] - 1)], outline=(200, 200, 200))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf


class Command(BaseCommand):
    help = "Seed sample doctors, patients, appointments, prescriptions, and reports."

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush", action="store_true",
            help="Delete previously seeded sample users (and their related rows) before reseeding.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["flush"]:
            deleted, _ = User.objects.filter(username__startswith="demo_").delete()
            self.stdout.write(self.style.WARNING(f"Flushed {deleted} previously seeded rows."))

        doctors = self._seed_doctors()
        patients = self._seed_patients()
        self._seed_appointments(patients, doctors)
        self._seed_reports(patients)
        self._seed_prescriptions(patients, doctors)

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {len(doctors)} doctors and {len(patients)} patients "
            f"(default password for all: '{DEFAULT_PASSWORD}')."
        ))

    def _seed_doctors(self):
        created = []
        for d in DOCTORS:
            username = f"demo_dr_{d['last'].lower()}"
            user, _ = User.objects.get_or_create(
                username=username,
                defaults={
                    "first_name": d["first"], "last_name": d["last"],
                    "email": f"{username}@demo.hms", "role": "doctor",
                    "phone": f"+91 9{random.randint(100000000, 999999999)}",
                },
            )
            user.set_password(DEFAULT_PASSWORD)
            user.save()
            doctor, _ = Doctor.objects.get_or_create(
                user=user,
                defaults={
                    "specialization": d["specialization"], "experience": d["experience"],
                    "qualification": d["qualification"], "available_days": d["available_days"],
                    "visiting_hours": d["visiting_hours"], "rating": round(random.uniform(4.3, 4.9), 1),
                },
            )
            created.append(doctor)
        return created

    def _seed_patients(self):
        created = []
        for p in PATIENTS:
            username = f"demo_pt_{p['last'].lower()}_{p['first'].lower()}"
            user, _ = User.objects.get_or_create(
                username=username,
                defaults={
                    "first_name": p["first"], "last_name": p["last"],
                    "email": f"{username}@demo.hms", "role": "patient",
                    "phone": f"+91 9{random.randint(100000000, 999999999)}",
                },
            )
            user.set_password(DEFAULT_PASSWORD)
            user.save()
            dob = date.today() - timedelta(days=p["age"] * 365)
            patient, _ = Patient.objects.get_or_create(
                user=user,
                defaults={
                    "dob": dob, "gender": p["gender"], "blood_group": p["blood_group"],
                    "address": "Delhi, India", "insurance": "Star Health",
                    "allergies": p["allergies"], "emergency_contact": f"+91 9{random.randint(100000000, 999999999)}",
                    "past_diseases": p["past_diseases"],
                },
            )
            created.append(patient)
        return created

    def _seed_appointments(self, patients, doctors):
        for patient in patients:
            for _ in range(random.randint(1, 3)):
                doctor = random.choice(doctors)
                offset = random.randint(-45, 20)
                appt_date = date.today() + timedelta(days=offset)
                if offset < 0:
                    # A small fraction of past appointments were cancelled --
                    # more realistic than every past visit being completed.
                    status = "cancelled" if random.random() < 0.1 else "completed"
                else:
                    status = "upcoming"
                Appointment.objects.create(
                    patient=patient, doctor=doctor, date=appt_date,
                    time=random.choice(["9:00 AM", "9:30 AM", "10:00 AM", "11:00 AM", "2:00 PM", "2:30 PM"]),
                    status=status,
                    reason=random.choice([
                        "General checkup", "Follow-up", "Fever and fatigue",
                        "Routine screening", "Vaccination", "Skin rash",
                        "Joint pain", "Annual physical",
                    ]),
                )

    def _seed_reports(self, patients):
        for patient in patients:
            num_reports = random.randint(1, 3)
            templates = random.sample(REPORT_TEMPLATES, k=min(num_reports, len(REPORT_TEMPLATES)))
            for template in templates:
                values = template["values"]()
                raw_text = template["raw_text"].format(**values)
                lines = raw_text.split("\n")[1:]  # drop title line for the image body
                img_buf = make_placeholder_image(template["report_type"], lines)
                report = MedicalReport(
                    patient=patient, report_type=template["report_type"],
                    hospital="City Care Hospital", raw_text=raw_text,
                )
                slug = template["report_type"].split(" ")[0].lower()
                filename = f"{slug}_{patient.patient_id}.png"
                report.file.save(filename, ContentFile(img_buf.read()), save=False)
                report.save()

    def _seed_prescriptions(self, patients, doctors):
        # Deliberately free of any pair listed in data/drug_interactions.csv --
        # these represent prescriptions a doctor already safely wrote, so a
        # dangerous combination here would be a data bug, not a demo feature.
        # To demo the live interaction check, use the Write Prescription form
        # in the app with e.g. "Aspirin" + "Warfarin".
        medicine_pool = [
            {"name": "Paracetamol", "dosage": "500mg", "frequency": "Twice daily"},
            {"name": "Ferrous Sulfate", "dosage": "325mg", "frequency": "Once daily"},
            {"name": "Metformin", "dosage": "500mg", "frequency": "Twice daily"},
            {"name": "Atorvastatin", "dosage": "10mg", "frequency": "Once at night"},
            {"name": "Cetirizine", "dosage": "10mg", "frequency": "Once at night"},
            {"name": "Amlodipine", "dosage": "5mg", "frequency": "Once daily"},
            {"name": "Azithromycin", "dosage": "500mg", "frequency": "Once daily for 3 days"},
            {"name": "Pantoprazole", "dosage": "40mg", "frequency": "Once daily before breakfast"},
            {"name": "Vitamin D3", "dosage": "60000 IU", "frequency": "Once weekly"},
            {"name": "Losartan", "dosage": "50mg", "frequency": "Once daily"},
            {"name": "Levothyroxine", "dosage": "50mcg", "frequency": "Once daily on empty stomach"},
            {"name": "Insulin Glargine", "dosage": "10 units", "frequency": "Once at night"},
        ]
        for patient in patients:
            doctor = random.choice(doctors)
            meds = random.sample(medicine_pool, k=random.randint(1, 2))
            Prescription.objects.create(
                patient=patient, doctor=doctor, medicines=meds,
                notes="Take after food. Follow up if symptoms persist.",
                followup_date=date.today() + timedelta(days=random.choice([15, 30, 60])),
            )