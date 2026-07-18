from pathlib import Path
from datetime import datetime


def export_notes(notes, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"notes_export_{datetime.now():%Y%m%d_%H%M%S}.txt"
    with path.open("w", encoding="utf-8") as f:
        f.write("STUDYDESK NOT DIŞA AKTARIMI\n")
        f.write("=" * 50 + "\n\n")
        for note in notes:
            f.write(f"Başlık: {note['title']}\n")
            f.write(f"Ders/Konu: {note['subject_name'] or '-'} / {note['topic_title'] or '-'}\n")
            f.write(f"Tarih: {note['created_at']}\n")
            f.write(f"Not: {note['content']}\n")
            f.write("-" * 50 + "\n")
    return path
