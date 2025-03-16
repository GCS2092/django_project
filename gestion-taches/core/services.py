from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from core.models import Project, Task
from datetime import datetime
from reportlab.pdfgen import canvas

def generate_task_report(response):
    response["Content-Disposition"] = "attachment; filename=rapport_taches.pdf"
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    y_position = height - 50

    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, y_position, "Rapport des Tâches")
    y_position -= 30

    p.setFont("Helvetica", 12)
    p.drawString(50, y_position, f"Généré le : {datetime.today().strftime('%Y-%m-%d %H:%M')}")
    y_position -= 30

    projects = Project.objects.all()
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y_position, f"Nombre total de projets : {projects.count()}")
    y_position -= 20

    for project in projects:
        if y_position < 100:
            p.showPage()
            p.setFont("Helvetica-Bold", 14)
            y_position = height - 50

        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y_position, f"Projet : {project.title}")
        y_position -= 20

        tasks = Task.objects.filter(project=project)
        if not tasks:
            p.setFont("Helvetica", 10)
            p.drawString(70, y_position, "Aucune tâche pour ce projet")
            y_position -= 20
        else:
            for task in tasks:
                p.setFont("Helvetica", 10)
                p.drawString(70, y_position, f"- {task.title} ({task.get_status_display()}) | Assigné à : {task.assigned_to.nom}")
                y_position -= 15

    p.showPage()
    p.save()
    return response

def generate_task_report(response):
    """Génère un rapport PDF basique"""
    p = canvas.Canvas(response)
    p.drawString(100, 750, "Rapport des Tâches")
    p.showPage()
    p.save()
    return response
