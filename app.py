from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

model    = joblib.load("disease_model.pkl")
symptoms = joblib.load("symptoms_list.pkl")
le       = joblib.load("label_encoder.pkl")

# ── Symptom categories ────────────────────────────────────────────────────────
CATEGORIES = {
    "Skin": ["itching","skin_rash","nodal_skin_eruptions","dischromic _patches","skin_peeling",
             "silver_like_dusting","small_dents_in_nails","inflammatory_nails","blister",
             "red_sore_around_nose","yellow_crust_ooze","pus_filled_pimples","blackheads","scurring"],
    "Digestive": ["stomach_pain","acidity","ulcers_on_tongue","vomiting","indigestion","nausea",
                  "loss_of_appetite","abdominal_pain","diarrhoea","constipation","belly_pain",
                  "passage_of_gases","internal_itching","stomach_bleeding","distention_of_abdomen",
                  "pain_during_bowel_movements","pain_in_anal_region","bloody_stool","irritation_in_anus"],
    "Respiratory": ["continuous_sneezing","cough","breathlessness","phlegm","throat_irritation",
                    "sinus_pressure","runny_nose","congestion","chest_pain","mucoid_sputum",
                    "rusty_sputum","blood_in_sputum"],
    "Neurological": ["headache","dizziness","loss_of_balance","lack_of_concentration","stiff_neck",
                     "depression","irritability","altered_sensorium","slurred_speech","spinning_movements",
                     "unsteadiness","weakness_of_one_body_side","loss_of_smell","visual_disturbances",
                     "blurred_and_distorted_vision","coma"],
    "Musculoskeletal": ["joint_pain","back_pain","neck_pain","knee_pain","hip_joint_pain","muscle_weakness",
                        "muscle_wasting","muscle_pain","swelling_joints","movement_stiffness",
                        "painful_walking","weakness_in_limbs","cramps"],
    "General": ["fatigue","weight_gain","weight_loss","anxiety","cold_hands_and_feets","mood_swings",
                "restlessness","lethargy","high_fever","mild_fever","sweating","dehydration","malaise",
                "shivering","chills","obesity","fast_heart_rate","swelled_lymph_nodes","toxic_look_(typhos)"],
    "Urinary": ["burning_micturition","spotting_ urination","dark_urine","yellow_urine","bladder_discomfort",
                "foul_smell_of urine","continuous_feel_of_urine","polyuria"],
    "Liver / Eyes": ["yellowish_skin","yellowing_of_eyes","acute_liver_failure","fluid_overload",
                     "swelling_of_stomach","fluid_overload.1","redness_of_eyes","watering_from_eyes",
                     "pain_behind_the_eyes","puffy_face_and_eyes"],
    "Metabolic": ["irregular_sugar_level","excessive_hunger","increased_appetite","sunken_eyes",
                  "dehydration","enlarged_thyroid","brittle_nails","swollen_extremeties",
                  "swollen_legs","swollen_blood_vessels","prominent_veins_on_calf","palpitations",
                  "abnormal_menstruation","patches_in_throat","red_spots_over_body"],
    "Other": ["extra_marital_contacts","receiving_blood_transfusion","receiving_unsterile_injections",
              "history_of_alcohol_consumption","family_history","drying_and_tingling_lips","bruising"]
}

# ── Disease info ──────────────────────────────────────────────────────────────
DISEASE_INFO = {
    "Fungal Infection":   {"desc":"A skin infection caused by fungi, commonly affecting moist areas of the body.","causes":["Warm/humid environment","Weakened immunity","Poor hygiene","Tight clothing"],"see_doctor":"If rash spreads, worsens after a week, or doesn't respond to OTC antifungals."},
    "Allergy":            {"desc":"An immune system reaction to a foreign substance that's not typically harmful.","causes":["Pollen, dust, pet dander","Certain foods","Insect stings","Medications"],"see_doctor":"If you experience difficulty breathing, swelling of throat, or severe reactions."},
    "GERD":               {"desc":"Stomach acid frequently flows back into the esophagus causing irritation.","causes":["Obesity","Hiatal hernia","Smoking","Fatty/spicy foods","Alcohol"],"see_doctor":"If symptoms occur more than twice a week or you have difficulty swallowing."},
    "Chronic Cholestasis":{"desc":"Reduced or stopped bile flow from the liver, causing bile buildup in the body.","causes":["Liver disease","Bile duct blockage","Certain medications","Pregnancy"],"see_doctor":"Immediately — this condition requires urgent medical evaluation."},
    "Drug Reaction":      {"desc":"An adverse immune or toxic response of the body to a medication.","causes":["Antibiotics","NSAIDs","Chemotherapy drugs","Genetic sensitivity"],"see_doctor":"Immediately if you have rash, swelling, or breathing difficulty after taking medication."},
    "Peptic Ulcer Disease":{"desc":"Open sores that develop on the inner lining of the stomach or small intestine.","causes":["H. pylori infection","Long-term NSAID use","Excess stomach acid","Smoking"],"see_doctor":"If you have severe stomach pain, black/tarry stools, or vomiting blood."},
    "AIDS":               {"desc":"Advanced stage of HIV infection that severely damages the immune system.","causes":["Unprotected sex","Contaminated needles","Blood transfusion","Mother to child"],"see_doctor":"Immediately — early antiretroviral therapy is critical."},
    "Diabetes":           {"desc":"A chronic condition affecting how the body processes blood sugar (glucose).","causes":["Genetics","Obesity","Sedentary lifestyle","Poor diet","Age"],"see_doctor":"If you have extreme thirst, frequent urination, blurred vision, or unexplained weight loss."},
    "Gastroenteritis":    {"desc":"Inflammation of the stomach and intestines, typically from infection.","causes":["Viral infection (norovirus)","Bacterial contamination","Contaminated food/water","Close contact with infected person"],"see_doctor":"If symptoms last more than 3 days, or you show signs of severe dehydration."},
    "Bronchial Asthma":   {"desc":"A condition causing airways to narrow, swell, and produce extra mucus.","causes":["Allergens","Air pollution","Exercise","Cold air","Respiratory infections"],"see_doctor":"If you have frequent attacks, symptoms worsen, or inhaler provides no relief."},
    "Hypertension":       {"desc":"Persistently elevated blood pressure that can lead to serious complications.","causes":["High salt diet","Obesity","Stress","Smoking","Genetics","Age"],"see_doctor":"If BP consistently reads above 140/90 or you have headaches, chest pain, or vision changes."},
    "Migraine":           {"desc":"A neurological condition causing intense, debilitating headaches often with nausea.","causes":["Hormonal changes","Stress","Certain foods","Sleep disruption","Bright lights"],"see_doctor":"If headaches are sudden/severe, or accompanied by fever, stiff neck, or neurological symptoms."},
    "Cervical Spondylosis":{"desc":"Age-related wear and tear of spinal disks in the neck.","causes":["Aging","Neck injuries","Repetitive neck movements","Sedentary lifestyle"],"see_doctor":"If you experience numbness, weakness in arms/hands, or loss of bladder/bowel control."},
    "Paralysis (brain hemorrhage)":{"desc":"Loss of muscle function due to bleeding in or around the brain.","causes":["High blood pressure","Head trauma","Blood vessel abnormalities","Blood thinners"],"see_doctor":"Emergency — call emergency services immediately."},
    "Jaundice":           {"desc":"Yellowing of skin and eyes caused by excess bilirubin in the blood.","causes":["Liver disease","Bile duct obstruction","Hemolytic anemia","Hepatitis"],"see_doctor":"Promptly — jaundice always requires medical investigation."},
    "Malaria":            {"desc":"A life-threatening disease caused by Plasmodium parasites transmitted by mosquitoes.","causes":["Anopheles mosquito bite","Travel to endemic regions","Contaminated blood transfusion"],"see_doctor":"Immediately — malaria can become life-threatening within hours."},
    "Chickenpox":         {"desc":"A highly contagious viral infection causing an itchy blister-like rash.","causes":["Varicella-zoster virus","Direct contact with infected person","Airborne droplets"],"see_doctor":"If rash spreads to eyes, or you develop high fever, confusion, or difficulty walking."},
    "Dengue":             {"desc":"A mosquito-borne viral infection causing severe flu-like illness.","causes":["Aedes mosquito bite","Travel to tropical regions"],"see_doctor":"Immediately if you have severe abdominal pain, persistent vomiting, or bleeding."},
    "Typhoid":            {"desc":"A bacterial infection caused by Salmonella typhi, spread through contaminated food/water.","causes":["Contaminated water","Contaminated food","Poor sanitation","Travel to endemic areas"],"see_doctor":"Promptly — typhoid requires antibiotic treatment."},
    "Hepatitis A":        {"desc":"A viral liver infection spread through contaminated food and water.","causes":["Contaminated food/water","Poor sanitation","Close contact with infected person"],"see_doctor":"If symptoms are severe or you have underlying liver disease."},
    "Hepatitis B":        {"desc":"A serious liver infection caused by the hepatitis B virus (HBV).","causes":["Unprotected sex","Contaminated needles","Mother to child at birth","Blood contact"],"see_doctor":"Promptly — chronic HBV can lead to liver failure and cancer."},
    "Hepatitis C":        {"desc":"A viral infection causing liver inflammation, sometimes leading to serious liver damage.","causes":["Contaminated needles","Blood transfusion (pre-1992)","Unprotected sex","Mother to child"],"see_doctor":"Promptly — effective antiviral treatments are available."},
    "Hepatitis D":        {"desc":"A liver infection that only occurs in people already infected with hepatitis B.","causes":["Co-infection with HBV","Contaminated needles","Blood contact"],"see_doctor":"Immediately — HDV with HBV causes more severe disease."},
    "Hepatitis E":        {"desc":"A liver disease caused by the hepatitis E virus, mainly spread through contaminated water.","causes":["Contaminated water","Undercooked pork/game meat","Travel to developing countries"],"see_doctor":"If you are pregnant or have underlying liver disease — can be severe."},
    "Alcoholic Hepatitis":{"desc":"Liver inflammation caused by drinking too much alcohol over time.","causes":["Heavy alcohol consumption","Malnutrition","Genetic factors"],"see_doctor":"Immediately — alcoholic hepatitis can be life-threatening."},
    "Tuberculosis":       {"desc":"A serious infectious disease that mainly affects the lungs, caused by Mycobacterium tuberculosis.","causes":["Airborne droplets from infected person","Weakened immune system","HIV infection","Malnutrition"],"see_doctor":"Immediately — TB requires a full course of antibiotics."},
    "Common Cold":        {"desc":"A viral infection of the upper respiratory tract, usually harmless.","causes":["Rhinovirus","Coronavirus","Close contact with infected person","Touching contaminated surfaces"],"see_doctor":"If symptoms last more than 10 days, or you develop high fever or severe headache."},
    "Pneumonia":          {"desc":"Infection that inflames air sacs in one or both lungs, which may fill with fluid.","causes":["Bacteria (Streptococcus)","Viruses","Fungi","Aspiration"],"see_doctor":"Immediately if you have difficulty breathing, chest pain, or high fever."},
    "Dimorphic Hemmorhoids (piles)":{"desc":"Swollen veins in the rectum or anus causing discomfort and bleeding.","causes":["Chronic constipation","Straining during bowel movements","Low-fiber diet","Pregnancy","Obesity"],"see_doctor":"If you have rectal bleeding, severe pain, or prolapsed hemorrhoids."},
    "Heart Attack":       {"desc":"Occurs when blood flow to part of the heart is blocked, causing heart muscle damage.","causes":["Coronary artery disease","High blood pressure","High cholesterol","Smoking","Diabetes"],"see_doctor":"Emergency — call emergency services immediately."},
    "Varicose Veins":     {"desc":"Enlarged, twisted veins usually appearing in the legs.","causes":["Prolonged standing/sitting","Pregnancy","Obesity","Age","Family history"],"see_doctor":"If you have severe pain, skin ulcers, or sudden swelling."},
    "Hypothyroidism":     {"desc":"A condition where the thyroid gland doesn't produce enough thyroid hormone.","causes":["Autoimmune disease (Hashimoto's)","Thyroid surgery","Radiation therapy","Iodine deficiency"],"see_doctor":"If you have extreme fatigue, unexplained weight gain, or depression."},
    "Hyperthyroidism":    {"desc":"A condition where the thyroid gland produces too much thyroid hormone.","causes":["Graves' disease","Thyroid nodules","Excess iodine","Thyroiditis"],"see_doctor":"If you have rapid heartbeat, tremors, or sudden weight loss."},
    "Hypoglycemia":       {"desc":"Abnormally low blood sugar levels, most common in people with diabetes.","causes":["Too much insulin","Skipping meals","Excessive exercise","Alcohol consumption"],"see_doctor":"If episodes are frequent, severe, or you lose consciousness."},
    "Osteoarthritis":     {"desc":"Degenerative joint disease causing breakdown of cartilage in joints.","causes":["Aging","Obesity","Joint injuries","Repetitive stress","Genetics"],"see_doctor":"If joint pain is severe, limits daily activities, or is accompanied by swelling."},
    "Arthritis":          {"desc":"Inflammation of one or more joints causing pain and stiffness.","causes":["Autoimmune response","Infection","Uric acid crystals","Wear and tear","Genetics"],"see_doctor":"If joint pain is persistent, severe, or accompanied by fever."},
    "Vertigo":            {"desc":"A sensation of feeling off balance or that the world is spinning around you.","causes":["Inner ear problems (BPPV)","Meniere's disease","Vestibular neuritis","Head injury"],"see_doctor":"If vertigo is sudden, severe, or accompanied by hearing loss, double vision, or weakness."},
    "Acne":               {"desc":"A skin condition that occurs when hair follicles become plugged with oil and dead skin cells.","causes":["Excess oil production","Bacteria","Hormonal changes","Certain medications","Diet"],"see_doctor":"If acne is severe, cystic, or causing significant scarring."},
    "Urinary Tract Infection":{"desc":"An infection in any part of the urinary system — kidneys, bladder, or urethra.","causes":["Bacteria (E. coli)","Sexual activity","Poor hygiene","Urinary tract abnormalities","Catheter use"],"see_doctor":"If you have fever, back pain, or symptoms don't improve within 2 days of treatment."},
    "Psoriasis":          {"desc":"A skin disease that causes red, itchy scaly patches, most commonly on knees, elbows, and scalp.","causes":["Immune system dysfunction","Genetics","Stress","Infections","Certain medications"],"see_doctor":"If plaques are widespread, severely itchy, or affecting your quality of life."},
    "Impetigo":           {"desc":"A highly contagious bacterial skin infection causing sores and blisters.","causes":["Staphylococcus aureus","Streptococcus pyogenes","Skin cuts or insect bites","Close contact"],"see_doctor":"Promptly — impetigo requires antibiotic treatment to prevent spread."},
}

# ── Feature importance from Random Forest ────────────────────────────────────
def get_symptom_importance(selected, input_vec):
    """Return top contributing symptoms using RF feature importances."""
    try:
        # CalibratedClassifierCV wraps VotingClassifier
        voting = model.estimator
        rf = dict(voting.estimators)['rf']
        importances = rf.feature_importances_
        # Only consider selected symptoms
        selected_indices = [i for i, v in enumerate(input_vec) if v == 1]
        scored = [(symptoms[i], float(round(importances[i] * 100, 2))) for i in selected_indices]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:5]
    except Exception:
        return []


@app.route('/')
def home():
    return render_template('index.html', symptoms=symptoms, categories=CATEGORIES)


@app.route('/predict', methods=['POST'])
def predict():
    selected_symptoms = request.form.getlist('symptoms')

    input_data = np.zeros(len(symptoms), dtype=int)
    for s in selected_symptoms:
        if s in symptoms:
            input_data[symptoms.index(s)] = 1

    proba    = model.predict_proba([input_data])[0]
    top_idx  = np.argsort(proba)[::-1][:3]
    top_diseases = [le.classes_[i] for i in top_idx]
    top_probs    = [float(np.round(proba[i], 3)) for i in top_idx]

    top1      = top_diseases[0]
    top1_prob = top_probs[0]

    info       = DISEASE_INFO.get(top1, {})
    importance = get_symptom_importance(selected_symptoms, input_data)

    return render_template(
        'result.html',
        disease=top1,
        disease_prob=top1_prob,
        top_diseases=list(zip(top_diseases, top_probs)),
        selected=selected_symptoms,
        info=info,
        importance=importance,
    )


if __name__ == "__main__":
    app.run(debug=True)
