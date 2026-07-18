def minutes_from_text(value: str) -> int:
    try:
        minutes = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("Süre dakika cinsinden tam sayı olmalıdır.") from exc
    if minutes <= 0:
        raise ValueError("Süre 0'dan büyük olmalıdır.")
    return minutes
