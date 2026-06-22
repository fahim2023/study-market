"""
Management command to seed the StudyMarket database with realistic
fake data for development and demonstration purposes.

Usage:
    python manage.py seed_data
    python manage.py seed_data --documents 30

This command creates:
    - Subjects and Courses
    - Seller and buyer User accounts with Profiles
    - Published Documents with 100% accurate academic preview text, real PDFs, and tags
"""

import os
import random
import re
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from faker import Faker

# ReportLab imports organized at the top level
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from accounts.models import Profile
from courses.models import Course, Subject
from documents.models import Document, DocumentTag

fake = Faker("en_GB")


# --- Seed data constants ---------------------------------------------------

SUBJECTS = [
    (
        "Biology",
        [
            ("A-Level Biology", "a_level", "AQA"),
            ("GCSE Biology", "gcse", "Edexcel"),
            ("Undergraduate Biology", "undergraduate", ""),
        ],
    ),
    (
        "Mathematics",
        [
            ("A-Level Maths", "a_level", "Edexcel"),
            ("GCSE Maths", "gcse", "AQA"),
            ("A-Level Further Maths", "a_level", "OCR"),
        ],
    ),
    (
        "Economics",
        [
            ("A-Level Economics", "a_level", "AQA"),
            ("Undergraduate Economics", "undergraduate", ""),
        ],
    ),
    (
        "Law",
        [
            ("A-Level Law", "a_level", "OCR"),
            ("Introduction to Law", "undergraduate", ""),
        ],
    ),
    (
        "Psychology",
        [
            ("A-Level Psychology", "a_level", "AQA"),
            ("Cognitive Psychology", "undergraduate", ""),
        ],
    ),
    (
        "History",
        [
            ("GCSE History", "gcse", "AQA"),
            ("A-Level History", "a_level", "Edexcel"),
        ],
    ),
]

TAGS = [
    "Exam Prep",
    "Summary Notes",
    "Past Paper Solutions",
    "Revision Guide",
    "Lecture Notes",
    "Essay Plans",
    "Cheat Sheet",
    "Worked Examples",
]

INSTITUTIONS = [
    "University of Oxford",
    "University of Cambridge",
    "University of Edinburgh",
    "University of Manchester",
    "King's College London",
    "University of Bristol",
    "Durham University",
    "University of Warwick",
]

DOCUMENT_TITLE_TEMPLATES = [
    "Complete {topic} Revision Guide",
    "{topic} Summary Notes",
    "{topic} Exam Prep Pack",
    "Comprehensive {topic} Notes",
    "{topic} Past Paper Solutions",
    "{topic} Cheat Sheet",
    "{topic} Lecture Notes",
    "{topic} Essay Plans",
]

# --- Explicit Mapping to align Topics with their respective Parent Subjects ---
TOPIC_TO_SUBJECT_MAP = {
    "Cell Biology": "Biology",
    "Genetics": "Biology",
    "Ecosystems": "Biology",
    "Evolution": "Biology",
    "Calculus": "Mathematics",
    "Statistics": "Mathematics",
    "Pure Mathematics": "Mathematics",
    "Mechanics": "Mathematics",
    "Microeconomics": "Economics",
    "Macroeconomics": "Economics",
    "Market Structures": "Economics",
    "Contract Law": "Law",
    "Criminal Law": "Law",
    "Tort Law": "Law",
    "Cognitive Psychology": "Psychology",
    "Social Psychology": "Psychology",
    "Developmental Psychology": "Psychology",
    "Cold War": "History",
    "World War II": "History",
    "Industrial Revolution": "History",
}

TOPICS = list(TOPIC_TO_SUBJECT_MAP.keys())


class Command(BaseCommand):
    help = "Seeds the database with fake data for development"

    def add_arguments(self, parser):
        parser.add_argument(
            "--documents",
            type=int,
            default=30,
            help="Number of documents to create (default: 60)",
        )

    def handle(self, *args, **options):
        self.stdout.write("Seeding database...")

        # --- Step 1: Create tags ---
        self.stdout.write("Creating tags...")
        tags = []
        for tag_name in TAGS:
            tag, _ = DocumentTag.objects.get_or_create(name=tag_name)
            tags.append(tag)
        self.stdout.write(self.style.SUCCESS(f"  {len(tags)} tags ready"))

        # --- Step 2: Create subjects and courses ---
        self.stdout.write("Creating subjects and courses...")
        for subject_name, course_list in SUBJECTS:
            subject, _ = Subject.objects.get_or_create(name=subject_name)
            for course_name, level, exam_board in course_list:
                Course.objects.get_or_create(
                    subject=subject,
                    name=course_name,
                    level=level,
                    defaults={"exam_board": exam_board},
                )
        self.stdout.write(self.style.SUCCESS("  Subjects and courses ready"))

        # --- Step 3: Create seller accounts ---
        self.stdout.write("Creating seller accounts...")
        sellers = []
        for i in range(5):
            username = fake.user_name() + str(random.randint(10, 99))
            if User.objects.filter(username=username).exists():
                continue
            user = User.objects.create_user(
                username=username,
                email=fake.email(),
                password="testpass123",
                first_name=fake.first_name(),
                last_name=fake.last_name(),
            )
            user.profile.is_seller = True
            user.profile.institution = random.choice(INSTITUTIONS)
            user.profile.bio = f"Top achieving student at {user.profile.institution} offering premium structural study layouts."
            user.profile.save()
            sellers.append(user)
        self.stdout.write(self.style.SUCCESS(f"  {len(sellers)} sellers created"))

        # --- Step 4: Create buyer accounts ---
        self.stdout.write("Creating buyer accounts...")
        for i in range(5):
            username = "buyer_" + fake.user_name() + str(random.randint(10, 99))
            if User.objects.filter(username=username).exists():
                continue
            User.objects.create_user(
                username=username,
                email=fake.email(),
                password="testpass123",
            )
        self.stdout.write(self.style.SUCCESS("  5 buyers created"))

        # --- Step 5: Create documents ---
        self.stdout.write(f'Creating {options["documents"]} documents...')

        media_doc_dir = os.path.join(settings.MEDIA_ROOT, "documents")
        os.makedirs(media_doc_dir, exist_ok=True)

        if not sellers:
            self.stdout.write(
                self.style.WARNING(
                    "No sellers found — using superuser as fallback seller"
                )
            )
            sellers = list(User.objects.filter(is_superuser=True))

        # Core Academic content mapper definitions
        REAL_ACADEMIC_CONTENT = {
            "Cell Biology": "Mitochondria are double-membrane-bound organelles responsible for generating ATP through aerobic respiration. The inner membrane is deeply folded into cristae, maximizing surface area for electron transport chain enzymes. Plant cells differ from animal cells by possessing a cellulose cell wall, large central vacuole, and chloroplasts for photosynthesis.",
            "Genetics": "Monohybrid inheritance tracks a single gene with two alleles. Gregor Mendel's laws of inheritance demonstrate that alleles segregate during gamete formation. Phenotypic ratios typically follow a 3:1 pattern in a heterozygous cross, while genotypic profiles present as 1:2:1. Linkage occurs when distinct loci reside on the same chromosome.",
            "Ecosystems": "An ecosystem consists of biotic communities interacting with abiotic factors. Energy flows unidirectionally through trophic levels, with roughly 10% efficiency transferred upward between links, while nutrients cycle endlessly through biogeochemical pathways. Net primary productivity (NPP) measures biomass accumulation rate.",
            "Evolution": "Natural selection acts on phenotypical variations within a breeding population. Environmental selection pressures favor advantageous traits, leading to differential reproductive success. Over generations, these genetic allele shifts can culminate in speciation, as documented widely across fossil records.",
            "Calculus": "The fundamental theorem of calculus establishes a direct link between differentiation and integration. The derivative represents an instantaneous rate of change or tangent gradient, calculated via first principles. Integration computes the accumulated area under a curve, utilizing definite limits.",
            "Statistics": "The normal distribution forms a symmetric, bell-shaped probability curve centered entirely around the population mean. Standard deviation quantifies data dispersion margins. Under Chebyshev's rule, approximately 68% of data points fall within one standard deviation, and 95% fall within two.",
            "Pure Mathematics": "Proof by mathematical induction verifies propositions across infinite sets of integers. The process requires establishing a foundational base case, assuming validity for an arbitrary integer k, and demonstrating that validity holds true for k+1. Complex numbers extend this field via imaginary roots.",
            "Mechanics": "Newton's second law stipulates that the net force acting on an object is directly proportional to its mass and resultant acceleration vector ($F=ma$). Static equilibrium requires both net external forces and net torques to equal zero. Friction forces always oppose impending relative motion.",
            "Microeconomics": "Price elasticity of demand measures consumer responsiveness to price adjustments. Supply and demand curves intersect at the market-clearing equilibrium price. Monopolistic competition features low barriers to entry with highly differentiated products, distinct from perfect competition.",
            "Macroeconomics": "Gross Domestic Product (GDP) aggregates the total market value of finished goods produced within a nation over a specific timeframe. Inflationary pressures are monitored via the Consumer Price Index (CPI). Monetary policy tools utilize central interest rates to control liquidity.",
            "Market Structures": "Perfect competition features a high density of firms selling homogenous products, making individual businesses strict price takers. Oligopolies are characterized by strategic interdependence, where game theory configurations like the Nash Equilibrium predict pricing decisions.",
            "Contract Law": "A legally binding contract requires an offer, unequivocal acceptance, mutual consideration, and an intention to create legal relations. Breach of condition entitles the innocent party to terminate performance, whereas a breach of warranty only allows for claims regarding monetary damages.",
            "Criminal Law": "Criminal liability requires the simultaneous coexistence of actus reus (the prohibited physical act) and mens rea (the guilty mind or intent). The prosecution carries the burden of proof to demonstrate these elements beyond a reasonable doubt. Defenses include duress and self-defense.",
            "Tort Law": "The tort of negligence requires establishing that the defendant owed the claimant a duty of care, breached that standard, and directly caused foreseeable consequential damage. The foundational landmark case of Donoghue v Stevenson established the universal 'neighbor principle'.",
            "Cognitive Psychology": "The multi-store model of memory partitions cognitive processing into sensory memory, short-term memory (STM), and long-term memory (LTM). Working memory models expand on this by introducing a central executive system controlling phonological loops and visuospatial sketchpads.",
            "Social Psychology": "Milgram's obedience experiments demonstrated that individuals comply with destructive orders when directed by an perceived legitimate authority figure. Asch's conformity studies illustrated that group pressure can force individuals to provide obviously incorrect consensus answers.",
            "Developmental Psychology": "Piaget's stages of cognitive development propose that children progress sequentially through sensorimotor, preoperational, concrete operational, and formal operational periods. Vygotsky countered this by highlighting social interaction and the Zone of Proximal Development.",
            "Cold War": "The geopolitical standoff between the United States and the Soviet Union escalated through proxy conflicts rather than direct warfare. Key milestones include the Truman Doctrine, the structural division of Berlin, the Cuban Missile Crisis, and the eventual collapse of the Berlin Wall.",
            "World War II": "The conflict erupted following Germany's invasion of Poland in 1939, leading to a total mobilization of global alliances. Key strategic turning points included the Battle of Britain, the invasion of Stalingrad, and the D-Day landings, ending with unconditional surrender in 1945.",
            "Industrial Revolution": "The transition from agrarian economies to industrialized manufacturing began in 18th-century Britain. Technological innovations like steam engines, mechanized spinning jennies, and centralized textile factories triggered mass urbanization and structural economic shifts.",
        }

        # Extra boilerplate sentences to organically lengthen the dynamic previews
        UNIVERSAL_ACADEMIC_SENTENCES = [
            "This module contains rigorous explanations alongside clear, step-by-step sample parameters.",
            "Crucial definitions and foundational formulas are highlighted specifically for rapid examination review.",
            "Ideal for students looking to secure top marks and master challenging core modules.",
            "All content aligns directly with current syllabus guidelines and higher education criteria.",
            "Includes strategic exam insights, structured analytical breakdowns, and common mistakes to avoid.",
            "Designed systematically to reinforce classroom lectures and simplify sophisticated analytical concepts.",
            "Perfect for constructing robust long-term revision guides and optimizing independent study routines.",
        ]

        created = 0
        for i in range(options["documents"]):
            topic = random.choice(TOPICS)
            title_template = random.choice(DOCUMENT_TITLE_TEMPLATES)
            title = title_template.format(topic=topic)

            # Avoid duplicate records
            if Document.objects.filter(title=title).exists():
                continue

            # Intelligent Course Matching System
            target_subject_name = TOPIC_TO_SUBJECT_MAP[topic]
            matching_subject = Subject.objects.get(name=target_subject_name)
            eligible_courses = Course.objects.filter(subject=matching_subject)
            chosen_course = random.choice(list(eligible_courses))

            academic_notes = REAL_ACADEMIC_CONTENT.get(
                topic, "General revision notes covering syllabus requirements."
            )

            # Create a real physical PDF document
            local_filename = f"dummy_notes_{random.randint(1000, 9999)}_{i}.pdf"
            local_filepath = os.path.join(media_doc_dir, local_filename)

            doc = SimpleDocTemplate(local_filepath, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []

            # Write the authentic text inside the actual PDF
            story.append(Paragraph(f"Premium Study Content: {title}", styles["Title"]))
            story.append(Spacer(1, 12))
            story.append(Paragraph(academic_notes, styles["Normal"]))
            story.append(Spacer(1, 12))
            story.append(
                Paragraph(
                    "End of premium document sample. Purchase to unlock full breakdown.",
                    styles["Italic"],
                )
            )
            doc.build(story)

            # --- Fix: 100% Real Academic Sentences (No Lorem Ipsum) ---
            # 1. Start with the core dynamic introductory hook
            preview_sentences = [
                f"This comprehensive revision pack provides structured coverage for the topic of {topic}.",
                f"This resource breaks down complex theories surrounding {topic} into digestible, high-yield study frameworks.",
            ]
            chosen_intro = random.choice(preview_sentences)

            # 2. Extract the individual sentences from the topic's real content string
            topic_sentences = [
                s.strip() + "." for s in re.split(r"\.|\?", academic_notes) if s.strip()
            ]

            # 3. Pool the real topic sentences with the universal academic booster sentences
            sentence_pool = topic_sentences + UNIVERSAL_ACADEMIC_SENTENCES
            random.shuffle(sentence_pool)

            # 4. Pull out enough real sentences to build a solid 5-8 sentence paragraph
            target_count = (
                random.randint(5, 8) - 1
            )  # Subtract 1 because we already have our intro hook
            selected_body_sentences = sentence_pool
            selected_body_sentences = random.sample(
                sentence_pool, min(target_count, len(sentence_pool))
            )

            # 5. Assemble the final preview text
            preview_text = chosen_intro + " " + " ".join(selected_body_sentences)

            # 6. Build a real description from topic sentences
            description_sentences = [
                s.strip() + "." for s in re.split(r"\.|\?", academic_notes) if s.strip()
            ]
            description = (
                f"A comprehensive study resource covering {topic} for {chosen_course.name}. "
                + " ".join(description_sentences)
            )

            # Save clean record into database
            document = Document.objects.create(
                seller=random.choice(sellers),
                course=chosen_course,
                title=title,
                description=description,
                preview_text=preview_text,
                price=round(random.uniform(2.99, 14.99), 2),
                status="published",
            )

            # Assign file path and tags
            document.file.name = f"documents/{local_filename}"
            document.save()
            document.tags.set(random.sample(tags, k=random.randint(1, 3)))
            created += 1

        self.stdout.write(self.style.SUCCESS(f"  {created} documents created"))

        # --- Done ---
        self.stdout.write(
            self.style.SUCCESS(
                f"\nSeeding complete! "
                f"{Document.objects.count()} total documents in database."
            )
        )
