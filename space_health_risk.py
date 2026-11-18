"""
ASTROCARE - Spaceflight Health Risk Assessment Engine

Purpose:
Screen astronaut-entered health measurements and generate
alerts for medical review.

This is a prototype screening system, NOT a diagnostic tool.
"""


def assess_space_health(data):

    alerts = []
    results = []

    # --------------------------------
    # 1. EXTRACT INPUT MEASUREMENTS
    # --------------------------------

    try:
        heart_rate = float(data["heart_rate"])
        temperature = float(data["temperature"])
        glucose = float(data["glucose"])
        systolic = float(data["systolic"])
        diastolic = float(data["diastolic"])
        sleep_hours = float(data["sleep_hours"])

        mood = str(data["mood"]).strip().lower()
        glucose_type = str(data["glucose_type"]).strip().lower()
        hours_since_meal = float(data["hours_since_meal"])

    except (KeyError, TypeError, ValueError):
        return {
            "status": "Invalid input",
            "alerts": ["Please provide all measurements correctly."],
            "results": []
        }

    # --------------------------------
    # 2. INPUT VALIDATION
    # --------------------------------

    if not 30 <= heart_rate <= 220:
        return {
            "status": "Invalid input",
            "alerts": ["Check heart-rate value and enter it in bpm."],
            "results": []
        }

    if not 25 <= temperature <= 45:
        return {
            "status": "Invalid input",
            "alerts": ["Check temperature and enter it in Celsius."],
            "results": []
        }

    if not 10 <= glucose <= 1000:
        return {
            "status": "Invalid input",
            "alerts": ["Check glucose value and enter it in mg/dL."],
            "results": []
        }

    if not 40 <= systolic <= 300 or not 20 <= diastolic <= 200:
        return {
            "status": "Invalid input",
            "alerts": ["Check blood pressure values and enter them in mmHg."],
            "results": []
        }

    if systolic <= diastolic:
        return {
            "status": "Invalid input",
            "alerts": [
                "Systolic pressure must be greater than diastolic pressure."
            ],
            "results": []
        }

    if not 0 <= sleep_hours <= 24:
        return {
            "status": "Invalid input",
            "alerts": ["Sleep hours must be between 0 and 24."],
            "results": []
        }

    if glucose_type not in ["before food", "after food"]:
        return {
            "status": "Invalid input",
            "alerts": ["Please select Before food or After food."],
            "results": []
        }

    if not 0 <= hours_since_meal <= 24:
        return {
            "status": "Invalid input",
            "alerts": ["Invalid hours since last meal."],
            "results": []
        }

    # --------------------------------
    # 3. HEART RATE ASSESSMENT
    # --------------------------------

    if heart_rate < 60:

        results.append({
            "category": "Heart Rate",
            "status": "Outside typical adult resting range",
            "observation": "Low resting heart rate recorded.",
            "recommendation": "Review symptoms, fitness level and previous readings."
        })

    elif heart_rate > 100:

        results.append({
            "category": "Heart Rate",
            "status": "Outside typical adult resting range",
            "observation": "Elevated resting heart rate recorded.",
            "recommendation": "Repeat measurement at rest and seek medical review if persistent."
        })

    else:

        results.append({
            "category": "Heart Rate",
            "status": "Within typical adult resting range",
            "observation": "No unusual resting heart-rate value identified."
        })

    # --------------------------------
    # 4. BODY TEMPERATURE ASSESSMENT
    # --------------------------------

    if temperature > 37.3:

        results.append({
            "category": "Body Temperature",
            "status": "Above typical range",
            "observation": "Body temperature is elevated compared with the typical adult range.",
            "recommendation": "Repeat measurement and consider medical evaluation."
        })

    elif temperature < 36.5:

        results.append({
            "category": "Body Temperature",
            "status": "Below typical range",
            "observation": "Body temperature is below the typical adult range.",
            "recommendation": "Repeat measurement and seek medical review if persistent."
        })

    else:

        results.append({
            "category": "Body Temperature",
            "status": "Within typical range",
            "observation": "Temperature is within the typical adult reference range."
        })

    # --------------------------------
    # 5. BLOOD GLUCOSE ASSESSMENT
    # --------------------------------

    if glucose < 70:

        results.append({
            "category": "Blood Glucose",
            "status": "Low glucose alert",
            "observation": "Blood glucose is below 70 mg/dL.",
            "recommendation": "Follow the medical team's low-glucose protocol."
        })

    elif glucose_type == "before food":

        if hours_since_meal >= 8:

            if glucose >= 126:

                results.append({
                    "category": "Blood Glucose",
                    "status": "Medical evaluation recommended",
                    "observation": "Fasting glucose meets the ADA threshold for diabetes evaluation.",
                    "recommendation": "Arrange appropriate laboratory confirmation."
                })

            elif glucose >= 100:

                results.append({
                    "category": "Blood Glucose",
                    "status": "Further evaluation recommended",
                    "observation": "Fasting glucose is above the usual normal range.",
                    "recommendation": "Discuss repeat testing with a healthcare professional."
                })

            else:

                results.append({
                    "category": "Blood Glucose",
                    "status": "Within usual fasting range",
                    "observation": "Fasting glucose is below 100 mg/dL."
                })

        else:

            results.append({
                "category": "Blood Glucose",
                "status": "Insufficient fasting duration",
                "observation": "Less than 8 hours have passed since the last meal.",
                "recommendation": "Do not interpret this as a fasting glucose result."
            })

    else:

        results.append({
            "category": "Blood Glucose",
            "status": "Post-meal reading",
            "observation": "Glucose was measured after food.",
            "recommendation": "Interpret using meal timing and clinical context."
        })

    # --------------------------------
    # 6. BLOOD PRESSURE ASSESSMENT
    # --------------------------------

    if systolic > 180 or diastolic > 120:

        results.append({
            "category": "Blood Pressure",
            "status": "Severely elevated",
            "observation": "Blood pressure exceeds the AHA severe-range threshold.",
            "recommendation": "Contact the medical team promptly for assessment."
        })

    elif systolic >= 140 or diastolic >= 90:

        results.append({
            "category": "Blood Pressure",
            "status": "Stage 2 range",
            "observation": "Blood pressure is in the AHA Stage 2 range.",
            "recommendation": "Arrange medical evaluation and repeat measurements."
        })

    elif systolic >= 130 or diastolic >= 80:

        results.append({
            "category": "Blood Pressure",
            "status": "Stage 1 range",
            "observation": "Blood pressure is in the AHA Stage 1 range.",
            "recommendation": "Repeat measurements and discuss with a healthcare professional."
        })

    elif systolic < 90 or diastolic < 60:

        results.append({
            "category": "Blood Pressure",
            "status": "Below typical range",
            "observation": "Blood pressure is below the usual adult reference range.",
            "recommendation": "Review symptoms and seek medical evaluation if persistent."
        })

    elif systolic >= 120 and diastolic < 80:

        results.append({
            "category": "Blood Pressure",
            "status": "Elevated range",
            "observation": "Systolic pressure is in the AHA elevated range.",
            "recommendation": "Continue monitoring and discuss persistent elevation with a healthcare professional."
        })

    else:

        results.append({
            "category": "Blood Pressure",
            "status": "Normal range",
            "observation": "Blood pressure is within the AHA normal category."
        })

    # --------------------------------
    # 7. MOOD ASSESSMENT
    # --------------------------------

    if mood in ["sad", "anxious", "stressed"]:

        results.append({
            "category": "Mental Wellbeing",
            "status": "Wellbeing check recommended",
            "observation": "Astronaut reports a negative mood state.",
            "recommendation": "Offer a confidential wellbeing check-in and appropriate support."
        })

    elif mood in ["good", "happy", "okay", "neutral"]:

        results.append({
            "category": "Mental Wellbeing",
            "status": "No concern reported",
            "observation": "Astronaut reports a generally positive or neutral mood."
        })

    else:

        results.append({
            "category": "Mental Wellbeing",
            "status": "Review required",
            "observation": "Mood entry was not recognised.",
            "recommendation": "Use good, happy, okay, neutral, sad, anxious or stressed."
        })

    # --------------------------------
    # 8. SLEEP ASSESSMENT
    # --------------------------------

    if sleep_hours < 7:

        results.append({
            "category": "Sleep Health",
            "status": "Insufficient sleep reported",
            "observation": "Sleep duration is below the general adult recommendation.",
            "recommendation": "Monitor sleep patterns and discuss persistent sleep difficulties with the medical team."
        })

    else:

        results.append({
            "category": "Sleep Health",
            "status": "Sleep duration meets general adult recommendation",
            "observation": "Sleep duration is at least seven hours."
        })

    # --------------------------------
    # 9. GENERATE ALERT LIST
    # --------------------------------

    normal_statuses = [
        "Within typical adult resting range",
        "Within typical range",
        "Within usual fasting range",
        "Normal range",
        "No concern reported",
        "Sleep duration meets general adult recommendation"
    ]

    for result in results:

        if result["status"] not in normal_statuses:

            alerts.append(
                result["category"] + ": " + result["observation"]
            )

    # --------------------------------
    # 10. FINAL ASSESSMENT
    # --------------------------------

    if alerts:

        overall_status = "Medical review or monitoring recommended"

    else:

        overall_status = "No unusual findings in the entered measurements"

    return {
        "status": overall_status,
        "results": results,
        "alerts": alerts,
        "disclaimer": (
            "This is an experimental screening system. "
            "It does not diagnose diseases or replace medical evaluation."
        )
    }