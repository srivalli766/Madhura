def assess_health(data):

    alerts = []
    recommendations = []

    # Heart Rate
    if data['heart_rate'] < 50 or data['heart_rate'] > 120:
        alerts.append("Heart rate requires medical review.")
        recommendations.append(
            "Repeat the measurement and consult the flight surgeon."
        )

    # Blood Pressure
    if data['systolic'] >= 140 or data['diastolic'] >= 90:
        alerts.append("Blood pressure is elevated.")
        recommendations.append(
            "Repeat the measurement and report the result to medical staff."
        )

    # Temperature
    if data['temperature'] < 35 or data['temperature'] >= 38:
        alerts.append("Temperature requires attention.")
        recommendations.append(
            "Repeat the measurement and contact the flight surgeon."
        )

    # Blood Glucose
    if data['glucose'] < 70 or data['glucose'] >= 200:
        alerts.append("Blood glucose requires clinical review.")
        recommendations.append(
            "Confirm the measurement and follow the mission medical protocol."
        )

    # Sleep
    if data['sleep'] < 7:
        alerts.append("Sleep duration is below the recommended target.")
        recommendations.append(
            "Review sleep schedule and discuss persistent sleep difficulties."
        )

    # Mood
    if data['mood'] in ['Stressed', 'Low']:
        alerts.append("Mental wellness support may be helpful.")
        recommendations.append(
            "Consider a confidential check-in with the behavioral health team."
        )

    if not alerts:
        alerts.append("No predefined alert criteria were triggered.")
        recommendations.append(
            "Continue routine monitoring and follow mission medical protocols."
        )

    return {
        "alerts": alerts,
        "recommendations": recommendations
    }