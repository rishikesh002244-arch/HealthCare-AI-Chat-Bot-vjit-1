# Medical data sourced from Mayo Clinic, CDC, WHO, WebMD
# Last updated: April 2026

DISEASE_REMEDIES = {
    "Fungal infection": [
        "Keep the infected area clean and completely dry — moisture promotes fungal growth (Mayo Clinic)",
        "Apply over-the-counter antifungal creams containing clotrimazole or miconazole as directed (CDC)",
        "Wear loose-fitting, breathable cotton clothing to reduce moisture buildup (WebMD)",
    ],
    "Allergy": [
        "Use a saline nasal rinse (neti pot) to flush allergens from nasal passages (Mayo Clinic)",
        "Take over-the-counter antihistamines such as cetirizine or loratadine for symptom relief (Mayo Clinic)",
        "Use HEPA air purifiers and keep windows closed during high pollen counts (CDC)",
    ],
    "GERD": [
        "Eat smaller, more frequent meals and avoid lying down for 3 hours after eating (Mayo Clinic)",
        "Elevate the head of your bed 6–8 inches using blocks or a wedge pillow (Mayo Clinic)",
        "Avoid trigger foods including citrus, tomato, chocolate, caffeine, and fatty foods (Mayo Clinic)",
    ],
    "Chronic cholestasis": [
        "Take ursodeoxycholic acid (UDCA) as prescribed to improve bile flow (Mayo Clinic)",
        "Apply fragrance-free moisturizers and take lukewarm oatmeal baths to relieve itching (WebMD)",
        "Follow a low-fat diet and take fat-soluble vitamin supplements (A, D, E, K) as directed (Mayo Clinic)",
    ],
    "Drug Reaction": [
        "Stop the suspected medication immediately and contact your healthcare provider (Mayo Clinic)",
        "Take diphenhydramine (Benadryl) for mild allergic reactions such as hives or itching (Mayo Clinic)",
        "For severe reactions (anaphylaxis), use epinephrine auto-injector and call emergency services (CDC)",
    ],
    "Peptic ulcer diseae": [
        "Take prescribed proton pump inhibitors (PPIs) like omeprazole to reduce stomach acid (Mayo Clinic)",
        "Avoid NSAIDs (ibuprofen, aspirin) which can worsen ulcers and cause bleeding (Mayo Clinic)",
        "Eat a balanced diet with fruits, vegetables, and whole grains; avoid spicy foods if they worsen symptoms (WebMD)",
    ],
    "AIDS": [
        "Adhere strictly to antiretroviral therapy (ART) — take medications at the same time daily (WHO)",
        "Eat a high-protein, nutrient-rich diet to support immune function and maintain weight (CDC)",
        "Get recommended vaccinations including influenza and pneumococcal vaccines (CDC)",
    ],
    "Diabetes ": [
        "Monitor blood glucose regularly and follow the DASH or Mediterranean eating pattern (Mayo Clinic)",
        "Get at least 150 minutes of moderate aerobic exercise per week such as brisk walking (Mayo Clinic)",
        "Maintain a healthy weight — losing 5–7% body weight significantly improves blood sugar control (CDC)",
    ],
    "Gastroenteritis": [
        "Drink oral rehydration solution (ORS) in small, frequent sips to prevent dehydration (WHO)",
        "Follow the BRAT diet (bananas, rice, applesauce, toast) when you can tolerate food (Mayo Clinic)",
        "Rest and gradually reintroduce bland, easy-to-digest foods as symptoms improve (CDC)",
    ],
    "Bronchial Asthma": [
        "Always carry your rescue inhaler (albuterol) and use it at the first sign of symptoms (Mayo Clinic)",
        "Identify and avoid personal triggers including dust mites, pet dander, smoke, and cold air (CDC)",
        "Use a peak flow meter daily to monitor lung function and detect worsening early (Mayo Clinic)",
    ],
    "Hypertension ": [
        "Follow the DASH diet — rich in fruits, vegetables, whole grains, and low-fat dairy (Mayo Clinic)",
        "Reduce sodium intake to less than 1,500 mg per day and increase potassium-rich foods (Mayo Clinic)",
        "Exercise at least 150 minutes per week — even a daily 30-minute brisk walk helps lower BP (Mayo Clinic)",
    ],
    "Migraine": [
        "Rest in a quiet, dark room and apply a cold compress to your forehead at onset (Mayo Clinic)",
        "Take OTC pain relievers (acetaminophen, ibuprofen) early — they work best at first sign (Mayo Clinic)",
        "Keep a headache diary to identify and avoid personal triggers like stress, certain foods, or poor sleep (Mayo Clinic)",
    ],
    "Cervical spondylosis": [
        "Apply heat or ice packs for 15–20 minutes to relieve neck pain and stiffness (Mayo Clinic)",
        "Do gentle neck stretches and range-of-motion exercises as recommended by a physical therapist (Mayo Clinic)",
        "Use a cervical pillow that supports the natural curve of your neck while sleeping (WebMD)",
    ],
    "Paralysis (brain hemorrhage)": [
        "Follow prescribed physical therapy and rehabilitation exercises consistently (Mayo Clinic)",
        "Keep blood pressure strictly within the range prescribed by your doctor (WHO)",
        "Install safety rails, grab bars, and remove trip hazards at home to prevent falls (CDC)",
    ],
    "Jaundice": [
        "Rest adequately and stay well-hydrated with water and clear fluids (Mayo Clinic)",
        "Avoid alcohol completely until liver function test results normalize (Mayo Clinic)",
        "Eat a balanced, low-fat diet and avoid medications that stress the liver without doctor approval (WebMD)",
    ],
    "Malaria": [
        "Take prescribed antimalarial medications exactly as directed — complete the full course (WHO)",
        "Stay well-hydrated and use acetaminophen (not aspirin) to manage fever (CDC)",
        "Sleep under insecticide-treated bed nets to prevent reinfection (WHO)",
    ],
    "Chicken pox": [
        "Apply calamine lotion to blisters and take lukewarm oatmeal baths to relieve itching (Mayo Clinic)",
        "Keep fingernails trimmed short and consider wearing cotton gloves at night to prevent scratching (CDC)",
        "Use acetaminophen for fever — never give aspirin to children due to Reye's syndrome risk (CDC)",
    ],
    "Dengue": [
        "Rest and drink plenty of fluids — water, ORS, and clear broths to prevent dehydration (WHO/CDC)",
        "Use only acetaminophen (paracetamol) for pain and fever — avoid aspirin and ibuprofen which increase bleeding risk (CDC)",
        "Monitor for warning signs: severe abdominal pain, persistent vomiting, or bleeding — seek emergency care immediately (WHO)",
    ],
    "Typhoid": [
        "Drink only boiled or purified water and complete the full course of prescribed antibiotics (WHO)",
        "Eat soft, high-calorie foods that are easy to digest, like porridge, boiled potatoes, and soups (CDC)",
        "Wash hands thoroughly with soap after using the restroom and before eating (CDC)",
    ],
    "hepatitis A": [
        "Get plenty of rest — fatigue is common and can last weeks to months (Mayo Clinic)",
        "Stay well-hydrated and eat small, frequent, low-fat meals to manage nausea (Mayo Clinic)",
        "Avoid alcohol completely during illness and for at least 6 months after recovery (CDC)",
    ],
    "Hepatitis B": [
        "Take prescribed antiviral medications consistently at the same time each day (Mayo Clinic)",
        "Avoid alcohol entirely as it accelerates liver damage (CDC)",
        "Get regular liver function tests and hepatocellular carcinoma screening as scheduled (WHO)",
    ],
    "Hepatitis C": [
        "Complete the full course of prescribed direct-acting antiviral (DAA) therapy (Mayo Clinic)",
        "Avoid alcohol and any hepatotoxic medications or supplements (CDC)",
        "Eat a balanced diet and drink coffee, which studies show has liver-protective benefits (Mayo Clinic)",
    ],
    "Hepatitis D": [
        "Continue hepatitis B antiviral treatment — HDV requires HBV to replicate (WHO)",
        "Take pegylated interferon as prescribed by your hepatologist (Mayo Clinic)",
        "Avoid alcohol and get regular liver imaging and blood tests (WHO)",
    ],
    "Hepatitis E": [
        "Rest and stay well-hydrated with clean, boiled water (WHO)",
        "Eat simple, easily digestible foods and avoid raw/undercooked meat and shellfish (CDC)",
        "Avoid alcohol during the entire recovery period (Mayo Clinic)",
    ],
    "Alcoholic hepatitis": [
        "Stop all alcohol consumption immediately — this is the most critical step (Mayo Clinic)",
        "Eat a high-calorie, high-protein diet to combat malnutrition common in this condition (Mayo Clinic)",
        "Take prescribed vitamin B-complex and folate supplements to address deficiencies (WebMD)",
    ],
    "Tuberculosis": [
        "Complete the full 6–9 month antibiotic course without missing doses — even if you feel better (WHO)",
        "Ensure good ventilation in living spaces and cover your mouth when coughing (CDC)",
        "Eat protein-rich foods and get adequate vitamin D through sunlight or supplements (WHO)",
    ],
    "Common Cold": [
        "Stay hydrated with warm fluids — honey-lemon water, broths, and herbal teas soothe the throat (Mayo Clinic)",
        "Gargle with warm salt water (1/4 to 1/2 teaspoon salt in 8 oz water) for sore throat relief (Mayo Clinic)",
        "Use a cool-mist humidifier and saline nasal drops to ease congestion (Mayo Clinic)",
    ],
    "Pneumonia": [
        "Complete all prescribed antibiotics even if you feel better — stopping early risks relapse (Mayo Clinic)",
        "Stay hydrated with warm fluids to help loosen mucus in the lungs (Mayo Clinic)",
        "Rest in a semi-upright position and do not suppress productive cough — it clears infection (WebMD)",
    ],
    "Dimorphic hemmorhoids(piles)": [
        "Take warm sitz baths for 15–20 minutes, 2–3 times daily to reduce pain and swelling (Mayo Clinic)",
        "Eat high-fiber foods (25–30g daily) and drink plenty of water to soften stools (Mayo Clinic)",
        "Apply over-the-counter witch hazel pads or hydrocortisone cream for symptom relief (Mayo Clinic)",
    ],
    "Heart attack": [
        "Call emergency services (ambulance) immediately — do not drive yourself (Mayo Clinic)",
        "Chew one regular aspirin (325mg) while waiting for emergency help unless allergic (Mayo Clinic)",
        "Lie down, stay calm, and loosen any tight clothing around chest and neck (CDC)",
    ],
    "Varicose veins": [
        "Elevate legs above heart level for 15 minutes several times daily to reduce swelling (Mayo Clinic)",
        "Wear graduated compression stockings during the day as recommended by your doctor (Mayo Clinic)",
        "Exercise regularly — walking and swimming improve calf muscle pump and circulation (Mayo Clinic)",
    ],
    "Hypothyroidism": [
        "Take levothyroxine on an empty stomach, 30–60 minutes before breakfast, at the same time daily (Mayo Clinic)",
        "Wait at least 4 hours before taking calcium or iron supplements which interfere with absorption (Mayo Clinic)",
        "Get TSH levels tested every 6–8 weeks when adjusting medication dose (Mayo Clinic)",
    ],
    "Hyperthyroidism": [
        "Take prescribed antithyroid medications (methimazole) exactly as directed (Mayo Clinic)",
        "Avoid excess iodine from supplements, seaweed, and iodinated contrast dyes (Mayo Clinic)",
        "Eat a calcium and vitamin D-rich diet to protect bone density affected by excess thyroid hormone (Mayo Clinic)",
    ],
    "Urinary tract infection": [
        "Drink 6–8 glasses of water daily to help flush bacteria from the urinary tract (Mayo Clinic)",
        "Complete the full course of prescribed antibiotics even if symptoms improve quickly (CDC)",
        "Urinate frequently — do not hold urine — and always wipe front to back (Mayo Clinic)",
    ],
    "Acne": [
        "Wash affected areas gently twice daily with a mild cleanser — avoid scrubbing (Mayo Clinic)",
        "Use non-comedogenic (oil-free) skincare products and sunscreen (Mayo Clinic)",
        "Apply over-the-counter benzoyl peroxide or salicylic acid treatments as directed (Mayo Clinic)",
    ],
    "Psoriasis": [
        "Apply thick moisturizers or emollients immediately after bathing to lock in moisture (Mayo Clinic)",
        "Use medicated shampoos containing coal tar or salicylic acid for scalp psoriasis (Mayo Clinic)",
        "Get controlled, brief sun exposure — UV light can slow skin cell turnover (Mayo Clinic)",
    ],
    "Impetigo": [
        "Gently wash sores with soap and water, then cover with gauze bandages (CDC)",
        "Apply prescribed mupirocin antibiotic ointment to affected areas as directed (Mayo Clinic)",
        "Wash the infected person's towels, linens, and clothing separately in hot water (CDC)",
    ],
    "Hypoglycemia": [
        "Consume 15g of fast-acting glucose immediately — juice, glucose tablets, or hard candy (Mayo Clinic)",
        "Recheck blood sugar after 15 minutes and eat a protein + carb snack once stabilized (Mayo Clinic)",
        "Always carry fast-acting sugar sources and wear a medical alert bracelet (CDC)",
    ],
    "Osteoarthristis": [
        "Do low-impact exercises like swimming, cycling, or walking to strengthen muscles around joints (Mayo Clinic)",
        "Apply heat for stiffness and cold packs for swelling — 15–20 minutes at a time (Mayo Clinic)",
        "Maintain a healthy weight — each pound lost removes 4 pounds of pressure from knees (CDC)",
    ],
    "Arthritis": [
        "Stay physically active with gentle exercises like tai chi, swimming, or yoga (CDC)",
        "Apply alternating hot and cold therapy to stiff or inflamed joints (Mayo Clinic)",
        "Consider omega-3 fatty acid supplements or eat fatty fish 2–3 times per week to reduce inflammation (Mayo Clinic)",
    ],
    "(vertigo) Paroymsal  Positional Vertigo": [
        "Perform the Epley maneuver as demonstrated by your doctor to reposition inner ear crystals (Mayo Clinic)",
        "Move slowly when changing positions — sit on the bed before standing up (Mayo Clinic)",
        "Sleep with your head slightly elevated on 2 pillows and avoid sudden head movements (WebMD)",
    ],
}

DISEASE_PRECAUTIONS = {
    "Fungal infection": [
        "Do not share towels, clothing, or personal items with others (CDC)",
        "Wear breathable cotton socks, change daily, and disinfect shoes regularly (Mayo Clinic)",
        "Dry skin folds thoroughly after bathing and apply antifungal powder to moisture-prone areas (CDC)",
    ],
    "Allergy": [
        "Identify specific allergens through professional allergy testing (Mayo Clinic)",
        "Carry an epinephrine auto-injector if you have a history of severe allergic reactions (CDC)",
        "Wash bedding weekly in hot water and keep indoor humidity below 50% to control dust mites (Mayo Clinic)",
    ],
    "GERD": [
        "Do not eat within 3 hours of lying down or going to bed (Mayo Clinic)",
        "Quit smoking — it weakens the lower esophageal sphincter (Mayo Clinic)",
        "Avoid tight belts and clothing that put pressure on the abdomen (Mayo Clinic)",
    ],
    "Chronic cholestasis": [
        "Monitor liver function tests every 3 months as directed by your doctor (Mayo Clinic)",
        "Avoid hepatotoxic drugs including high-dose acetaminophen without medical supervision (WebMD)",
        "Report any new yellowing of skin or eyes to your doctor immediately (Mayo Clinic)",
    ],
    "Drug Reaction": [
        "Inform all healthcare providers about your drug allergies before any treatment (Mayo Clinic)",
        "Wear a medical alert bracelet listing all medications that caused reactions (CDC)",
        "Keep a written record of drug reactions including the medication name, dose, and symptoms (Mayo Clinic)",
    ],
    "Peptic ulcer diseae": [
        "Avoid NSAIDs (ibuprofen, naproxen, aspirin) completely as they worsen ulcers (Mayo Clinic)",
        "Do not smoke — smoking delays ulcer healing and increases recurrence risk (Mayo Clinic)",
        "Complete the full H. pylori antibiotic course if prescribed — partial treatment causes resistance (CDC)",
    ],
    "AIDS": [
        "Take antiretroviral medications at the exact prescribed times every day (WHO)",
        "Disclose HIV status to sexual partners and practice safe sex consistently (CDC)",
        "Get regular CD4 count and viral load monitoring as scheduled by your doctor (WHO)",
    ],
    "Diabetes ": [
        "Inspect feet daily for cuts, blisters, or sores — diabetic neuropathy reduces sensation (Mayo Clinic)",
        "Never skip meals, especially if taking insulin or sulfonylureas (CDC)",
        "Schedule regular eye exams and kidney function tests annually (Mayo Clinic)",
    ],
    "Gastroenteritis": [
        "Wash hands with soap for at least 20 seconds, especially before eating and after toilet use (CDC)",
        "Do not prepare food for others while symptomatic and for 48 hours after recovery (CDC)",
        "Disinfect contaminated surfaces with bleach solution to prevent household spread (WHO)",
    ],
    "Bronchial Asthma": [
        "Create and follow a written asthma action plan developed with your doctor (Mayo Clinic)",
        "Get annual flu and pneumococcal vaccines — respiratory infections trigger severe attacks (CDC)",
        "Use spacer devices with metered-dose inhalers for better medication delivery (Mayo Clinic)",
    ],
    "Hypertension ": [
        "Monitor blood pressure at home twice daily and keep a log for your doctor (Mayo Clinic)",
        "Take prescribed medications at the same time every day — do not skip doses (Mayo Clinic)",
        "Quit smoking and limit alcohol to no more than 1 drink per day (CDC)",
    ],
    "Migraine": [
        "Maintain a consistent sleep schedule — even on weekends (Mayo Clinic)",
        "Stay hydrated throughout the day — dehydration is a common migraine trigger (Mayo Clinic)",
        "Limit screen time and use blue-light filtering glasses to reduce eye strain triggers (WebMD)",
    ],
    "Cervical spondylosis": [
        "Take regular breaks from screen work every 30 minutes to stretch your neck (Mayo Clinic)",
        "Use an ergonomic workstation with monitor at eye level (Mayo Clinic)",
        "Avoid carrying heavy loads on shoulders or head (WebMD)",
    ],
    "Paralysis (brain hemorrhage)": [
        "Control blood pressure strictly within the range prescribed by your doctor (WHO)",
        "Attend all physical, occupational, and speech therapy sessions without skipping (Mayo Clinic)",
        "Install safety rails in bathrooms and along stairs to prevent falls (CDC)",
    ],
    "Jaundice": [
        "Avoid alcohol completely until bilirubin levels and liver function normalize (Mayo Clinic)",
        "Do not take over-the-counter medications without your doctor's explicit approval (Mayo Clinic)",
        "Get tested for underlying causes like hepatitis or gallstones (Mayo Clinic)",
    ],
    "Malaria": [
        "Sleep under insecticide-treated mosquito nets in endemic areas (WHO)",
        "Take prescribed prophylactic antimalarials when traveling to endemic regions (CDC)",
        "Seek immediate medical attention for fever after travel to malaria-endemic areas (WHO)",
    ],
    "Chicken pox": [
        "Isolate the infected person until all blisters have crusted over — usually 5–7 days (CDC)",
        "Do not give aspirin to children with chickenpox — risk of Reye's syndrome (CDC)",
        "Avoid contact with pregnant women and immunocompromised individuals (CDC)",
    ],
    "Dengue": [
        "Eliminate standing water around your home to prevent mosquito breeding (WHO)",
        "Avoid aspirin and ibuprofen — they increase the risk of hemorrhage (CDC)",
        "Seek emergency medical care immediately if warning signs appear after fever breaks (WHO)",
    ],
    "Typhoid": [
        "Drink only boiled or bottled water and avoid street food during outbreaks (WHO)",
        "Wash hands with soap before eating and after using the toilet (CDC)",
        "Get the typhoid vaccine before traveling to endemic areas (CDC)",
    ],
    "hepatitis A": [
        "Practice strict hand washing with soap after restroom use and before food preparation (CDC)",
        "Avoid preparing food for others during acute infection (CDC)",
        "Get vaccinated if traveling to endemic areas — the vaccine is highly effective (CDC)",
    ],
    "Hepatitis B": [
        "Do not share razors, toothbrushes, or needles (CDC)",
        "Ensure sexual partners are tested and vaccinated against hepatitis B (WHO)",
        "Get regular liver cancer screening with ultrasound every 6–12 months (Mayo Clinic)",
    ],
    "Hepatitis C": [
        "Never share needles, syringes, or drug paraphernalia (CDC)",
        "Do not donate blood, organs, or tissue if infected (CDC)",
        "Avoid alcohol completely — it accelerates liver fibrosis and cirrhosis (Mayo Clinic)",
    ],
    "Hepatitis D": [
        "Continue hepatitis B antiviral treatment consistently — stopping allows HDV to worsen (WHO)",
        "Ensure household contacts are vaccinated against hepatitis B to prevent HDV co-infection (WHO)",
        "Do not share personal items that may have blood on them (CDC)",
    ],
    "Hepatitis E": [
        "Drink only boiled or purified water, especially in endemic areas (WHO)",
        "Pregnant women should seek immediate medical care — HEV is especially dangerous in pregnancy (WHO)",
        "Avoid raw or undercooked pork and shellfish which can harbor the virus (CDC)",
    ],
    "Alcoholic hepatitis": [
        "Abstain from all alcohol permanently — continued drinking is fatal (Mayo Clinic)",
        "Avoid acetaminophen and other liver-metabolized medications without doctor approval (Mayo Clinic)",
        "Enroll in a structured alcohol rehabilitation or counseling program (Mayo Clinic)",
    ],
    "Tuberculosis": [
        "Complete the full 6–9 month antibiotic course — never stop early even if feeling better (WHO)",
        "Use directly observed therapy (DOT) if available in your area (WHO)",
        "Ensure good ventilation in living and working spaces to reduce airborne transmission (CDC)",
    ],
    "Common Cold": [
        "Wash hands frequently with soap for at least 20 seconds (CDC)",
        "Avoid touching eyes, nose, and mouth with unwashed hands (CDC)",
        "Stay home during the first 2–3 days when you are most contagious (Mayo Clinic)",
    ],
    "Pneumonia": [
        "Get annual influenza and pneumococcal vaccines for prevention (CDC)",
        "Do not suppress productive cough — coughing helps clear the infection from lungs (Mayo Clinic)",
        "Avoid smoking and secondhand smoke which impair lung healing (Mayo Clinic)",
    ],
    "Dimorphic hemmorhoids(piles)": [
        "Do not strain during bowel movements — straining worsens hemorrhoids (Mayo Clinic)",
        "Respond to the urge to defecate promptly — delaying hardens stool (Mayo Clinic)",
        "Avoid sitting on the toilet for extended periods — limit to 5 minutes (WebMD)",
    ],
    "Heart attack": [
        "Take all prescribed medications (statins, blood thinners, beta-blockers) daily without skipping (Mayo Clinic)",
        "Learn to recognize warning signs: chest pain, jaw pain, arm numbness, shortness of breath (CDC)",
        "Quit smoking permanently and attend cardiac rehabilitation after discharge (Mayo Clinic)",
    ],
    "Varicose veins": [
        "Avoid sitting or standing in one position for more than 30 minutes (Mayo Clinic)",
        "Do not cross your legs while sitting — it restricts blood flow (WebMD)",
        "Exercise regularly — walking and swimming are ideal for vein health (Mayo Clinic)",
    ],
    "Hypothyroidism": [
        "Take thyroid medication at the same time daily on an empty stomach (Mayo Clinic)",
        "Do not switch between brand-name and generic levothyroxine without doctor approval (Mayo Clinic)",
        "Wait 4 hours before taking calcium, iron, or antacid supplements (Mayo Clinic)",
    ],
    "Hyperthyroidism": [
        "Monitor heart rate daily and report persistent rapid heartbeat to your doctor (Mayo Clinic)",
        "Avoid vigorous exercise until thyroid hormone levels are normalized (Mayo Clinic)",
        "Protect eyes from dryness with lubricating eye drops if Graves' disease is present (Mayo Clinic)",
    ],
    "Urinary tract infection": [
        "Always wipe from front to back after using the toilet (Mayo Clinic)",
        "Do not hold urine for extended periods — urinate when you feel the urge (CDC)",
        "Avoid irritating feminine products like douches and scented sprays (Mayo Clinic)",
    ],
    "Acne": [
        "Do not pick, squeeze, or pop pimples — it causes scarring and spreads bacteria (Mayo Clinic)",
        "Remove all makeup completely before sleeping every night (Mayo Clinic)",
        "Avoid excessive sun exposure which worsens post-inflammatory marks (WebMD)",
    ],
    "Psoriasis": [
        "Moisturize skin immediately after every bath to prevent dryness and flares (Mayo Clinic)",
        "Avoid skin injuries, cuts, and sunburns — they trigger new plaques (Koebner phenomenon) (Mayo Clinic)",
        "Manage stress through relaxation techniques — stress is a major flare trigger (Mayo Clinic)",
    ],
    "Impetigo": [
        "Keep the infected person's belongings separate from other family members (CDC)",
        "Do not send children to school until 24 hours after starting antibiotic treatment (CDC)",
        "Cut fingernails short to prevent scratching and spreading the infection (CDC)",
    ],
    "Hypoglycemia": [
        "Never skip meals or go more than 4 hours without eating (Mayo Clinic)",
        "Check blood sugar before driving — hypoglycemia impairs reaction time (Mayo Clinic)",
        "Inform coworkers and family about signs of low blood sugar and how to help (CDC)",
    ],
    "Osteoarthristis": [
        "Avoid high-impact activities like running and jumping that stress joints (Mayo Clinic)",
        "Use assistive devices like canes or walkers to reduce load on affected joints (Mayo Clinic)",
        "Maintain healthy weight — excess weight significantly accelerates joint deterioration (CDC)",
    ],
    "Arthritis": [
        "Balance activity with rest — avoid overexerting on days when symptoms feel better (CDC)",
        "Use ergonomic tools and jar openers to reduce strain on hand joints (Mayo Clinic)",
        "Protect joints from cold weather which worsens stiffness — keep them warm (Mayo Clinic)",
    ],
    "(vertigo) Paroymsal  Positional Vertigo": [
        "Move slowly when changing positions, especially in the morning (Mayo Clinic)",
        "Avoid tilting your head far back — squat instead of bending to pick things up (Mayo Clinic)",
        "Avoid activities with rapid head movement like rollercoasters until symptoms resolve (WebMD)",
    ],
}

SEARCH_NAME_MAP = {
    "GERD": "Gastroesophageal reflux disease",
    "(vertigo) Paroymsal  Positional Vertigo": "Benign paroxysmal positional vertigo",
    "Dimorphic hemmorhoids(piles)": "Hemorrhoids",
    "Peptic ulcer diseae": "Peptic ulcer disease",
    "Osteoarthristis": "Osteoarthritis",
    "hepatitis A": "Hepatitis A",
    "Diabetes ": "Diabetes mellitus",
    "Hypertension ": "Hypertension",
    "Chicken pox": "Chickenpox",
    "Paralysis (brain hemorrhage)": "Intracerebral hemorrhage",
    "Bronchial Asthma": "Asthma",
    "Drug Reaction": "Adverse drug reaction",
}
