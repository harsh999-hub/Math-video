import os
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

pdf_path = "/Users/harsh283gmail.com/.gemini/antigravity/scratch/Math-video/Storyboard.pdf"
doc = SimpleDocTemplate(
    pdf_path,
    pagesize=landscape(letter),
    rightMargin=36,
    leftMargin=36,
    topMargin=36,
    bottomMargin=36
)

styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Heading1'],
    fontName='Helvetica-Bold',
    fontSize=18,
    leading=22,
    textColor=colors.HexColor('#0f172a'),
    alignment=1
)
subtitle_style = ParagraphStyle(
    'DocSubtitle',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=11,
    leading=15,
    textColor=colors.HexColor('#475569'),
    alignment=1
)
cell_title = ParagraphStyle(
    'CellTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=9,
    leading=12,
    textColor=colors.HexColor('#0f172a')
)
cell_body = ParagraphStyle(
    'CellBody',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=8.5,
    leading=11,
    textColor=colors.HexColor('#334155')
)
header_style = ParagraphStyle(
    'HeaderStyle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=9.5,
    leading=12,
    textColor=colors.white
)

elements = []

elements.append(Paragraph("M3 Internal Assessment — 6-Scene Animation Video Storyboard", title_style))
elements.append(Spacer(1, 4))
elements.append(Paragraph("<b>Topic:</b> Eigenvalues and Eigenvectors: Visualizing Invariant Directions & Matrix Scaling | <b>Format:</b> 1080p 16:9 | <b>Target Duration:</b> 5:00", subtitle_style))
elements.append(Paragraph("<b>One-Sentence Learning Objective:</b> <i>\"By the end of this video, the viewer will be able to geometrically identify invariant directions under a 2D linear transformation, solve the characteristic equation det(A - λI) = 0 to find eigenvalues, and compute the corresponding eigenvectors that form the transformation's natural coordinate system.\"</i>", subtitle_style))
elements.append(Spacer(1, 10))

table_data = [
    [
        Paragraph("Scene # & Time", header_style),
        Paragraph("Scene Title & Purpose", header_style),
        Paragraph("Visual & Animation Plan (1080p)", header_style),
        Paragraph("Narration & Mathematical Plan", header_style)
    ],
    [
        Paragraph("<b>Scene 1</b><br/>0:00 - 0:45<br/>(45 sec)", cell_title),
        Paragraph("<b>Hook / Context</b><br/>Spark curiosity & motivate why invariant directions matter in real systems.", cell_body),
        Paragraph("• Title card with Concept, Student Name & ID.<br/>• Animated 2D grid deforming under a random matrix.<br/>• Most vectors tilt and rotate away from their original lines.<br/>• A bright golden vector stays perfectly on its span.<br/>• Real-world icons: Bridge resonance, PageRank, PCA.", cell_body),
        Paragraph("Hook: When a matrix transforms space, almost every vector is knocked off course. But does any vector maintain its direction?<br/>Introduce the mystery of invariant directions and how Google PageRank and bridge engineers use them to analyze complex systems.", cell_body)
    ],
    [
        Paragraph("<b>Scene 2</b><br/>0:45 - 1:30<br/>(45 sec)", cell_title),
        Paragraph("<b>Concept Introduction</b><br/>Define the fundamental equation and clarify notation.", cell_body),
        Paragraph("• Formal definition highlighted in glowing cyan: <b>A v = λ v</b>.<br/>• Component breakdown: Matrix A (transform), vector v ≠ 0 (direction), scalar λ (stretch factor).<br/>• Rearrangement animation: (A - λ I) v = 0.<br/>• Definition of the zero vector exclusion.", cell_body),
        Paragraph("Define 'Eigen' (German for 'characteristic' or 'own'). Explain that matrix multiplication Av collapses into simple scalar multiplication λv.<br/>Explain why v cannot be the trivial zero vector and introduce the identity matrix I.", cell_body)
    ],
    [
        Paragraph("<b>Scene 3</b><br/>1:30 - 2:30<br/>(60 sec)", cell_title),
        Paragraph("<b>Visual Intuition</b><br/>Build geometric understanding through dynamic grid transformation.", cell_body),
        Paragraph("• Dynamic Cartesian coordinate grid [-4, 4] x [-4, 4].<br/>• Test vector sweeping 360 degrees.<br/>• Real-time angular deflection angle θ(v, Av) plotted.<br/>• At two specific angles (45° and 135°), the deflection drops to exactly 0°!<br/>• Grid stretches along these two perpendicular eigen-axes.", cell_body),
        Paragraph("Guide the viewer through rotating space: 'Watch how most vectors swing around. But look closely at the lines y = x and y = -x: along these special axes, vectors do not rotate at all! They only stretch.'", cell_body)
    ],
    [
        Paragraph("<b>Scene 4</b><br/>2:30 - 3:45<br/>(75 sec)", cell_title),
        Paragraph("<b>Worked Example</b><br/>Step-by-step algebraic derivation with clean 2x2 matrix.", cell_body),
        Paragraph("• Given matrix A = [[3, 1], [1, 3]].<br/>• Step 1: Characteristic equation det(A - λ I) = 0.<br/>• Matrix subtraction (3-λ, 1; 1, 3-λ).<br/>• Determinant: (3-λ)² - 1 = λ² - 6λ + 8 = (λ-4)(λ-2) = 0.<br/>• Step 2: Solve (A - 4I)v = 0 → v₁ = [1, 1]ᵀ.<br/>• Step 3: Solve (A - 2I)v = 0 → v₂ = [-1, 1]ᵀ.", cell_body),
        Paragraph("Walk step-by-step through the algebra without skipping steps. Explain why the determinant must equal zero: for non-zero v to exist in the nullspace, the matrix (A - λI) must compress space into a lower dimension.", cell_body)
    ],
    [
        Paragraph("<b>Scene 5</b><br/>3:45 - 4:30<br/>(45 sec)", cell_title),
        Paragraph("<b>Interpretation & Verification</b><br/>Connect algebra back to visual geometry and verify results.", cell_body),
        Paragraph("• Side-by-side verification:<br/>  A v₁ = [[3,1],[1,3]][1,1]ᵀ = [4,4]ᵀ = 4 v₁ (stretched 4x!).<br/>  A v₂ = [[3,1],[1,3]][-1,1]ᵀ = [-2,2]ᵀ = 2 v₂ (stretched 2x!).<br/>• Geometric animation: v₁ expanding along y = x by factor 4; v₂ expanding along y = -x by factor 2.<br/>• Comparison with a non-eigenvector [1, 0]ᵀ mapping to [3, 1]ᵀ.", cell_body),
        Paragraph("Verify the algebra geometrically: 'Notice that A quadrupled v₁ along the line y = x and doubled v₂ along y = -x. Any other vector, like [1, 0]ᵀ, gets rotated into [3, 1]ᵀ. The eigenvectors form the natural backbone of the transformation.'", cell_body)
    ],
    [
        Paragraph("<b>Scene 6</b><br/>4:30 - 5:00<br/>(30 sec)", cell_title),
        Paragraph("<b>Summary & Credits</b><br/>Reinforce 3 core takeaways, credits, and AI disclosure.", cell_body),
        Paragraph("• 3 Core Takeaways on screen:<br/>  1. Eigenvectors define invariant direction axes (no rotation).<br/>  2. Eigenvalues give the scaling factor along those axes.<br/>  3. Solved via det(A - λI) = 0 and nullspace (A - λI)v = 0.<br/>• References & textbook citations.<br/>• AI Tool Disclosure statement & Closing Frame.", cell_body),
        Paragraph("Summarize key concepts: Invariant direction, scaling factor, and algebraic solution method. Thank the viewer, cite M3 curriculum references, and display academic integrity disclosures.", cell_body)
    ]
]

t = Table(table_data, colWidths=[90, 140, 260, 230])
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e293b')),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
]))

elements.append(t)
doc.build(elements)
print("Storyboard PDF successfully created at:", pdf_path)
