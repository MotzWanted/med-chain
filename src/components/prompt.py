import jinja2
import pydantic

MEDQA = [
    {
        "question": "A 22-year-old male marathon runner presents to the office with the complaint of right-sided rib pain when he runs long distances. Physical examination reveals normal heart and lung findings and an exhalation dysfunction at ribs 4-5 on the right. Which of the following muscles or muscle groups will be most useful in correcting this dysfunction utilizing a direct method?",
        "answers": ["Anterior scalene", "Latissimus dorsi", "Pectoralis minor", "quadratus lumborum"],
        "target": 2,
        "explanation": "We refer to Wikipedia articles on medicine for help. Among the options, only pectoralis minor muscle origins from the outer surfaces of the 3rd to 5th ribs.",
    },
    {
        "question": "A 36-year-old male presents to the office with a 3-week history of low back pain. He denies any recent trauma but says that he climbs in and out of his truck numerous times a day for his job. Examination of the patient in the prone position reveals a deep sacral sulcus on the left, a posterior inferior lateral angle on the right, and a lumbosacral junction that springs freely on compression. Which of the following is the most likely diagnosis?",
        "answers": [
            "Left-on-left sacral torsion",
            "Left-on-right sacral torsion",
            "Right unilateral sacral flexion",
            "Right-on-right sacral torsion",
        ],
        "target": 3,
        "explanation": "We refer to Wikipedia articles on medicine for help. The deep sulcus on the left, a posterior ILA on the right, with a negative spring test suggests a right-on-right sacral torsion. All other options have a deep sulcus on the right.",
    },
    {
        "question": "A 44-year-old man comes to the office because of a 3-day history of sore throat, nonproductive cough, runny nose, and frontal headache. He says the headache is worse in the morning and ibuprofen does provide some relief. He has not had shortness of breath. Medical history is unremarkable. He takes no medications other than the ibuprofen for pain. Vital signs are temperature 37.4°C (99.4°F), pulse 88/min, respirations 18/min, and blood pressure 120/84 mm Hg. Examination of the nares shows erythematous mucous membranes. Examination of the throat shows erythema and follicular lymphoid hyperplasia on the posterior oropharynx. There is no palpable cervical adenopathy. Lungs are clear to auscultation. Which of the following is the most likely cause of this patient's symptoms?",
        "answers": ["Allergic rhinitis", "Epstein-Barr virus", "Mycoplasma pneumonia", "Rhinovirus"],
        "target": 3,
        "explanation": "We refer to Wikipedia articles on medicine for help. The symptoms, especially the headache, suggest that the most likely cause is Rhinovirus. Epstein-Barr virus will cause swollen lymph nodes but there is no palpable cervical adenopathy. Lungs are clear to auscultation suggests it's not Mycoplasma pneumonia.",
    },
    {
        "question": "A previously healthy 32-year-old woman comes to the physician 8 months after her husband was killed in a car crash. Since that time, she has had a decreased appetite and difficulty falling asleep. She states that she is often sad and cries frequently. She has been rechecking the door lock five times before leaving her house and has to count exactly five pieces of toilet paper before she uses it. She says that she has always been a perfectionist but these urges and rituals are new. Pharmacotherapy should be targeted to which of the following neurotransmitters?",
        "answers": ["Dopamine", "Glutamate", "Norepinephrine", "Serotonin"],
        "target": 3,
        "explanation": "We refer to Wikipedia articles on medicine for help. The patient feels sad and among the options, only Dopamine and Serotonin can help increase positive emotions. Serotonin also affects digestion and metabolism, which can help the patient's decreased appetite and sleep difficulty.",
    },
    {
        "question": "A 42-year-old man comes to the office for preoperative evaluation prior to undergoing adrenalectomy scheduled in 2 weeks. One month ago, he received care in the emergency department for pain over his right flank following a motor vehicle collision. At that time, blood pressure was 160/100 mm Hg and CT scan of the abdomen showed an incidental 10-cm left adrenal mass. Results of laboratory studies, including complete blood count, serum electrolyte concentrations, and liver function tests, were within the reference ranges. The patient otherwise had been healthy and had never been told that he had elevated blood pressure. He takes no medications. A follow-up visit in the office 2 weeks ago disclosed elevated urinary normetanephrine and metanephrine and plasma aldosterone concentrations. The patient was referred to a surgeon, who recommended the adrenalectomy. Today, vital signs are temperature 36.6°C (97.9°F), pulse 100/min, respirations 14/min, and blood pressure 170/95 mm Hg. Physical examination discloses no significant findings. Initial preoperative preparation should include treatment with which of the following?",
        "answers": ["Labetalol", "A loading dose of potassium chloride", "Nifedipine", "Phenoxybenzamine"],
        "target": 3,
        "explanation": "We refer to Wikipedia articles on medicine for help. The symptoms and the adrenal mass suggested pheochromocytoma, and the blood pressure indicates hypertension. Phenoxybenzamine is used to treat hypertension caused by pheochromocytoma.",
    },
]


MEDMCQA = [
    {
        "question": "In Gaucher's diseases, there is deficiency of:",
        "answers": ["Glucocerebrosidase", "Glucokinase", "Sphingomyelinase", "G-6PD"],
        "target": 0,
        "explanation": "Gaucher's disease is a rare genetic disorder that results from a deficiency of the enzyme glucocerebrosidase. The disease is characterized by the accumulation of a type of fat called glucocerebroside in cells and organs, particularly in the liver, spleen, and bone marrow. As a result, affected individuals may experience enlargement of these organs, anemia, low platelet count, and bone pain or fractures.",
    },
    {
        "question": "Which muscle is an abductor of the vocal cords?",
        "answers": ["Transverse arytenoid", "Oblique arytenoid", "Lateral thyroarytenoid", "Posterior Cricoarytenoid"],
        "target": 3,
        "explanation": "The following movements are associated with specific muscles: elevation of the larynx is performed by the thyrohyoid and mylohyoid muscles, depression of the larynx is performed by the sternothyroid and sternohyoid muscles, opening the inlet of the larynx is performed by the thyroepiglottic muscle, and closing the inlet of the larynx is performed by the aryepiglottic muscle. The abductor of the vocal cords is the posterior cricoarytenoid muscle, while the lateral cricoarytenoid, transverse, and oblique arytenoid muscles are responsible for adducting the vocal cords.",
    },
    {
        "question": "Inner ear is present in which bone:",
        "answers": [
            "Parietal bone",
            "Petrous part of temporal bone",
            "Occipital bone",
            "Petrous part of squamous bone",
        ],
        "target": 1,
        "explanation": 'The inner ear is housed within a structure known as the bony labyrinth or otic capsule, which is a type of cartilaginous bone that forms from a cartilage model through endochondral bone formation. The bony labyrinth or otic capsule is located in the petrous part of the temporal bone. The petrous part is called "petrous" because it is one of the densest bones in the body, though not the strongest.',
    },
    {
        "question": "Blood flow in intervillous space at term:",
        "answers": ["150 ml", "250 ml", "350 ml", "450 ml"],
        "target": 0,
        "explanation": "The mature placenta has a total of 500 ml of blood. Out of this, 150 ml of blood is present in the intervillous space, while the remaining 350 ml of blood is present in the villi system.",
    },
    {
        "question": "Spuriously high BP is seen in A/E:",
        "answers": ["Auscultatory gap", "Small cuff", "Thick calcified vessels", "Obesity"],
        "answer": 0,
        "explanation": "Spuriously high blood pressure readings can be observed in various conditions. These include the auscultatory gap, which is a brief silence heard during measurement due to the disappearance of Korotkoff sounds, often found in hypertensive patients. Additionally, using a small cuff that is not appropriately sized for the patient can lead to falsely elevated readings. Obese individuals may also falsely experience high blood pressure due to the thick layer of fat that can dissipate cuff pressure, resulting in inaccurate readings. Lastly, patients with thick and calcified vessels may experience falsely high blood pressure readings.",
    },
]

FIXED_SHOTS = {
    "VodLM/medqa": MEDQA,
    "medmcqa": MEDMCQA,
}


def get_fixed_shots(user_template: str, assistant_template: str, dataset_name: str, k: int) -> list[dict[str, str]]:
    """Get fixed shots."""
    usr_temp = jinja2.Template(user_template)
    ass_temp = jinja2.Template(assistant_template)
    shot_samples = FIXED_SHOTS[dataset_name][:k]

    shots = []
    for sample in shot_samples:
        user_message = usr_temp.render(**sample)
        assistant_message = ass_temp.render(**sample)
        shots.append({"role": "user", "content": user_message})
        shots.append({"role": "assistant", "content": assistant_message})
    return shots


class FewshotConfig(pydantic.BaseModel):
    """Fewshot config."""

    assistant_template: str
    dataset_name: str
    k: int | None = 5


def get_messages(user_template: str, system_template: str | None, fewshot: dict | None = None) -> list[dict[str, str]]:
    """Get a list of messages for prompting LLM."""
    messages = []
    if system_template:
        messages.append({"role": "system", "content": system_template})
    if fewshot:
        config = FewshotConfig(**fewshot)
        shots = get_fixed_shots(user_template, **config.model_dump())
        messages.extend(shots)
    messages.append({"role": "user", "content": user_template})
    return messages
