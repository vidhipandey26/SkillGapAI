from reportlab.pdfgen import canvas
c = canvas.Canvas("test_resume.pdf")
c.drawString(100, 750, "John Doe Software Engineer")
c.drawString(100, 720, "Skills: Python, Machine Learning, SQL, Azure, Docker")
c.drawString(100, 690, "Experience: 3 years Data Science")
c.drawString(100, 660, "Tools: TensorFlow, PyTorch, Scikit-learn, Pandas")
c.drawString(100, 630, "Cloud: Azure ML, AWS, Kubernetes, Docker")
c.save()
print("Created")