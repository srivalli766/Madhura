def analyze_trends(records):

    if len(records) < 2:
        return ["More records are needed for trend analysis."]

    trends = []

    measurements = [
        ('heart_rate', 'Heart Rate'),
        ('temperature', 'Temperature'),
        ('glucose', 'Blood Glucose'),
        ('systolic', 'Systolic Blood Pressure'),
        ('diastolic', 'Diastolic Blood Pressure')
    ]

    for key, name in measurements:

        values = [float(record[key]) for record in records]

        first_value = values[0]
        latest_value = values[-1]
        average_value = sum(values) / len(values)

        change = latest_value - first_value

        trends.append(
            f"{name}: First {first_value}, "
            f"Latest {latest_value}, "
            f"Average {average_value:.2f}, "
            f"Change {change:+.2f}"
        )

    return trends
