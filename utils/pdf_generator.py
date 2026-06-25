from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet


def generate_report(filename, data):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph("Talk2Mind Mental Wellness Report", styles["Title"])
    )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            f"Wellness Score: {data['wellness_score']}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Risk Level: {data['risk_level']}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Depression Level: {data['depression_level']}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Anxiety Level: {data['anxiety_level']}",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 10))

    content.append(
        Paragraph(
            f"Face Emotion: {data['face_emotion']} ({data['face_confidence']}%)",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Voice Emotion: {data['voice_emotion']} ({data['voice_confidence']}%)",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 10))

    content.append(
        Paragraph(
            "Recommendations",
            styles["Heading2"]
        )
    )

    for rec in data["recommendations"]:
        content.append(
            Paragraph(f"• {rec}", styles["Normal"])
        )

    doc.build(content)