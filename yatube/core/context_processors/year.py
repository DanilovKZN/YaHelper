from datetime import datetime


def year(request):
    """Добавляет переменную с текущим годом."""
    date_now = datetime.now()
    year = date_now.year
    return {
        "year": year,
    }
