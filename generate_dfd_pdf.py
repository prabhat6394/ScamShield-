import os
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# Define output file paths
OUTPUT_DIR = r"d:\Scamm"
PDF_PATH = os.path.join(OUTPUT_DIR, "ScamShield_DFD_Diagrams_All_Levels.pdf")
IMG_DIR = os.path.join(OUTPUT_DIR, "scratch_dfd_imgs")
os.makedirs(IMG_DIR, exist_ok=True)

# Set styling constants
COLOR_PRIMARY = "#0F172A"    # Slate 900
COLOR_SECONDARY = "#0EA5E9"  # Cyan 500
COLOR_ACCENT = "#F59E0B"     # Amber 500
COLOR_DANGER = "#EF4444"     # Red 500
COLOR_SUCCESS = "#10B981"    # Emerald 500
COLOR_BG_LIGHT = "#F8FAFC"   # Slate 50
COLOR_CARD_BG = "#F1F5F9"    # Slate 100

# Helper function to create standard diagrams with matplotlib
def draw_rounded_rect(ax, x, y, width, height, text, bg_color="#0EA5E9", text_color="white", fontsize=9, shape="rect"):
    if shape == "circle":
        circle = patches.Circle((x + width/2, y + height/2), radius=height/2, facecolor=bg_color, edgecolor="#1E293B", linewidth=1.5, zorder=3)
        ax.add_patch(circle)
        ax.text(x + width/2, y + height/2, text, color=text_color, fontsize=fontsize, weight='bold', ha='center', va='center', zorder=4, wrap=True)
    elif shape == "datastore":
        # Draw open ended rectangle for DFD Data Store
        rect = patches.Rectangle((x, y), width, height, facecolor="#FEF3C7", edgecolor="#B45309", linewidth=1.5, zorder=3)
        ax.add_patch(rect)
        # Left bar double line
        ax.plot([x + width*0.18, x + width*0.18], [y, y + height], color="#B45309", linewidth=1.5, zorder=4)
        ax.text(x + width*0.58, y + height/2, text, color="#78350F", fontsize=fontsize, weight='bold', ha='center', va='center', zorder=5)
    elif shape == "entity":
        # Draw box for External Entity
        rect = patches.Rectangle((x, y), width, height, facecolor="#E0F2FE", edgecolor="#0369A1", linewidth=1.5, zorder=3)
        ax.add_patch(rect)
        ax.text(x + width/2, y + height/2, text, color="#0C4A6E", fontsize=fontsize, weight='bold', ha='center', va='center', zorder=4)
    else: # Process box
        rect = patches.FancyBboxPatch((x, y), width, height, boxstyle="round,pad=0.03,rounding_size=0.15",
                                      facecolor=bg_color, edgecolor="#1E293B", linewidth=1.5, zorder=3)
        ax.add_patch(rect)
        ax.text(x + width/2, y + height/2, text, color=text_color, fontsize=fontsize, weight='bold', ha='center', va='center', zorder=4)

def draw_arrow(ax, start, end, label="", label_pos=0.5, color="#475569", curvature=0.0):
    if curvature == 0:
        ax.annotate('', xy=end, xytext=start,
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.5, mutation_scale=12), zorder=2)
        mid_x = start[0] + (end[0] - start[0]) * label_pos
        mid_y = start[1] + (end[1] - start[1]) * label_pos
    else:
        ax.annotate('', xy=end, xytext=start,
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.5, mutation_scale=12,
                                    connectionstyle=f"arc3,rad={curvature}"), zorder=2)
        mid_x = start[0] + (end[0] - start[0]) * label_pos
        mid_y = start[1] + (end[1] - start[1]) * label_pos + curvature * 0.5
    
    if label:
        ax.text(mid_x, mid_y, label, fontsize=7.5, color="#1E293B", weight='bold', ha='center', va='center',
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="#CBD5E1", alpha=0.9), zorder=5)

# ==============================================================================
# DIAGRAM GENERATORS
# ==============================================================================

def create_level_0_diagram():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    # Title
    ax.text(5, 5.7, "DFD Level 0: Context Diagram (ScamShield Platform)", fontsize=14, weight='bold', color="#0F172A", ha='center')
    
    # Central Process 0.0
    draw_rounded_rect(ax, 3.8, 2.0, 2.4, 2.0, "0.0\nScamShield\nDigital Scam\nChecker System", bg_color="#0EA5E9", shape="circle", fontsize=10)
    
    # External Entities
    # Top Left: Web / PWA User
    draw_rounded_rect(ax, 0.5, 4.0, 2.0, 1.0, "User\n(Web Browser / PWA)", shape="entity", fontsize=8.5)
    # Bottom Left: Mobile App User
    draw_rounded_rect(ax, 0.5, 0.8, 2.0, 1.0, "Mobile User\n(Android Client App)", shape="entity", fontsize=8.5)
    # Top Right: External OCR & AI APIs
    draw_rounded_rect(ax, 7.5, 4.0, 2.0, 1.0, "External Services\n(Cloud OCR & AI API)", shape="entity", fontsize=8.5)
    # Bottom Right: Cybercrime Authorities
    draw_rounded_rect(ax, 7.5, 0.8, 2.0, 1.0, "National Cybercrime\nPortal (1930 / Gov)", shape="entity", fontsize=8.5)
    
    # Data Flows
    # Web User -> System
    draw_arrow(ax, (2.5, 4.6), (4.2, 3.7), "SMS, URL, Screenshot, Audio", label_pos=0.5, curvature=0.1)
    # System -> Web User
    draw_arrow(ax, (4.0, 3.0), (2.5, 4.1), "Scam Risk Score & Guidance", label_pos=0.5, curvature=0.1)
    
    # Mobile User -> System
    draw_arrow(ax, (2.5, 1.2), (4.1, 2.2), "Scan Requests & SMS Body", label_pos=0.5, curvature=-0.1)
    # System -> Mobile User
    draw_arrow(ax, (4.5, 2.1), (2.5, 1.6), "Real-time Push Risk Alert", label_pos=0.5, curvature=-0.1)
    
    # System -> External OCR/AI
    draw_arrow(ax, (5.8, 3.7), (7.5, 4.6), "Image Stream & Prompt Data", label_pos=0.5, curvature=0.1)
    # External OCR/AI -> System
    draw_arrow(ax, (7.5, 4.1), (5.9, 3.0), "Extracted Text & Classification", label_pos=0.5, curvature=0.1)
    
    # System -> Cybercrime Portal
    draw_arrow(ax, (5.8, 2.2), (7.5, 1.3), "Escalated Fraud Report Log", label_pos=0.5, curvature=-0.1)

    plt.tight_layout()
    img_path = os.path.join(IMG_DIR, "dfd_level_0.png")
    plt.savefig(img_path, bbox_inches='tight', dpi=300)
    plt.close()
    return img_path

def create_level_1_diagram():
    fig, ax = plt.subplots(figsize=(11, 7.5), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    ax.text(6, 7.6, "DFD Level 1: System Level Data Flow Diagram", fontsize=14, weight='bold', color="#0F172A", ha='center')
    
    # External Entities (Left)
    draw_rounded_rect(ax, 0.4, 5.2, 1.8, 0.9, "User\n(Web / App)", shape="entity", fontsize=8)
    draw_rounded_rect(ax, 0.4, 1.8, 1.8, 0.9, "External APIs\n(OCR / AI)", shape="entity", fontsize=8)
    
    # Level 1 Processes (Middle)
    draw_rounded_rect(ax, 3.2, 6.2, 2.0, 1.0, "1.0 Data Ingestion\n& Sanitization", bg_color="#0EA5E9", shape="rect", fontsize=8)
    draw_rounded_rect(ax, 3.2, 4.2, 2.0, 1.0, "2.0 Multi-Modal\nFeature Extraction", bg_color="#0EA5E9", shape="rect", fontsize=8)
    draw_rounded_rect(ax, 3.2, 2.2, 2.0, 1.0, "3.0 Scam Risk\nEngine Assessment", bg_color="#0EA5E9", shape="rect", fontsize=8)
    draw_rounded_rect(ax, 3.2, 0.4, 2.0, 1.0, "4.0 Result Formatter\n& Highlight Engine", bg_color="#0EA5E9", shape="rect", fontsize=8)
    
    draw_rounded_rect(ax, 7.2, 5.2, 2.0, 1.0, "5.0 Persistence &\nHistory Manager", bg_color="#0284C7", shape="rect", fontsize=8)
    draw_rounded_rect(ax, 7.2, 2.2, 2.0, 1.0, "6.0 Security Analytics\n& Simulator Engine", bg_color="#0284C7", shape="rect", fontsize=8)
    
    # Data Stores (Right)
    draw_rounded_rect(ax, 9.8, 6.2, 2.0, 0.8, "DS1: Scans DB\n(SQLite / D1)", shape="datastore", fontsize=7.5)
    draw_rounded_rect(ax, 9.8, 4.4, 2.0, 0.8, "DS4: Upload Stream\n(R2 / Memory)", shape="datastore", fontsize=7.5)
    draw_rounded_rect(ax, 9.8, 2.6, 2.0, 0.8, "DS3: Threat Patterns\n(Rule Engine)", shape="datastore", fontsize=7.5)
    draw_rounded_rect(ax, 9.8, 0.8, 2.0, 0.8, "DS2: Quiz & Stats DB\n(User Score)", shape="datastore", fontsize=7.5)

    # Connections
    # Entity -> 1.0
    draw_arrow(ax, (2.2, 5.7), (3.2, 6.6), "Raw Request Payload", label_pos=0.5)
    # 1.0 -> 2.0
    draw_arrow(ax, (4.2, 6.2), (4.2, 5.2), "Cleaned Input", label_pos=0.5)
    # 2.0 <-> External APIs
    draw_arrow(ax, (3.2, 4.5), (2.2, 2.5), "Bytes Stream", label_pos=0.5, curvature=0.1)
    draw_arrow(ax, (2.2, 2.1), (3.2, 4.3), "Extracted Text", label_pos=0.5, curvature=0.1)
    # 2.0 -> 3.0
    draw_arrow(ax, (4.2, 4.2), (4.2, 3.2), "Extracted Features", label_pos=0.5)
    # 3.0 <-> DS3 Threat Patterns
    draw_arrow(ax, (5.2, 2.5), (9.8, 2.9), "Query Regex & Rules", label_pos=0.5, curvature=0.1)
    # 3.0 -> 4.0
    draw_arrow(ax, (4.2, 2.2), (4.2, 1.4), "Raw Risk Weights", label_pos=0.5)
    # 4.0 -> User
    draw_arrow(ax, (3.2, 0.9), (1.2, 5.2), "Risk Score & Red Flags", label_pos=0.5, curvature=-0.2)
    # 4.0 -> 5.0 Persistence
    draw_arrow(ax, (5.2, 0.9), (7.2, 5.5), "Final Scan Log Record", label_pos=0.5, curvature=0.2)
    # 5.0 -> DS1 Scans DB
    draw_arrow(ax, (9.2, 5.7), (9.8, 6.5), "Write Scan Row", label_pos=0.5)
    # 6.0 <-> DS2 Quiz DB
    draw_arrow(ax, (9.2, 2.4), (9.8, 1.2), "Quiz Result & Score", label_pos=0.5)
    
    plt.tight_layout()
    img_path = os.path.join(IMG_DIR, "dfd_level_1.png")
    plt.savefig(img_path, bbox_inches='tight', dpi=300)
    plt.close()
    return img_path

def create_level_2_feature_extraction_diagram():
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    ax.text(5, 5.6, "DFD Level 2.1: Multi-Modal Feature Extraction Subsystem (Process 2.0)", fontsize=12, weight='bold', color="#0F172A", ha='center')
    
    # Input Data (Left)
    draw_rounded_rect(ax, 0.4, 2.2, 1.8, 1.6, "Ingested Data\n(Process 1.0)", shape="entity", fontsize=8)
    
    # Level 2.1 Subprocesses
    draw_rounded_rect(ax, 3.2, 4.4, 2.2, 0.9, "2.1 Message & Text\nPattern Extractor", bg_color="#0EA5E9", shape="rect", fontsize=7.5)
    draw_rounded_rect(ax, 3.2, 3.1, 2.2, 0.9, "2.2 URL Structure &\nDomain Parser", bg_color="#0EA5E9", shape="rect", fontsize=7.5)
    draw_rounded_rect(ax, 3.2, 1.8, 2.2, 0.9, "2.3 Image OCR Text\nExtractor", bg_color="#0EA5E9", shape="rect", fontsize=7.5)
    draw_rounded_rect(ax, 3.2, 0.5, 2.2, 0.9, "2.4 Audio Transcriber &\nSpeech Processor", bg_color="#0EA5E9", shape="rect", fontsize=7.5)
    
    # Data Store & External Service (Right)
    draw_rounded_rect(ax, 7.2, 4.0, 2.2, 0.8, "DS4: Media Storage\n(Upload Streams)", shape="datastore", fontsize=7.5)
    draw_rounded_rect(ax, 7.2, 1.2, 2.2, 0.9, "External OCR / AI\nAPIs", shape="entity", fontsize=8)
    
    # Arrows
    draw_arrow(ax, (2.2, 3.2), (3.2, 4.8), "Text Body", label_pos=0.5)
    draw_arrow(ax, (2.2, 3.0), (3.2, 3.5), "URL String", label_pos=0.5)
    draw_arrow(ax, (2.2, 2.8), (3.2, 2.2), "Screenshot File", label_pos=0.5)
    draw_arrow(ax, (2.2, 2.6), (3.2, 0.9), "Audio Recording", label_pos=0.5)
    
    draw_arrow(ax, (5.4, 2.2), (7.2, 4.2), "Save Image Bytes", label_pos=0.5)
    draw_arrow(ax, (5.4, 0.9), (7.2, 1.6), "Audio Stream", label_pos=0.5)
    
    plt.tight_layout()
    img_path = os.path.join(IMG_DIR, "dfd_level_2_1.png")
    plt.savefig(img_path, bbox_inches='tight', dpi=300)
    plt.close()
    return img_path

def create_level_2_risk_engine_diagram():
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    ax.text(5, 5.6, "DFD Level 2.2: Risk Assessment & Classification Subsystem (Process 3.0)", fontsize=12, weight='bold', color="#0F172A", ha='center')
    
    # Input
    draw_rounded_rect(ax, 0.4, 2.2, 1.8, 1.4, "Extracted Features\n(Process 2.0)", shape="entity", fontsize=8)
    
    # Processes
    draw_rounded_rect(ax, 3.2, 3.8, 2.4, 1.0, "3.1 Indicator Weight\nAccumulator Engine", bg_color="#0EA5E9", shape="rect", fontsize=8)
    draw_rounded_rect(ax, 3.2, 2.0, 2.4, 1.0, "3.2 Primary Scam\nCategory Classifier", bg_color="#0EA5E9", shape="rect", fontsize=8)
    draw_rounded_rect(ax, 3.2, 0.3, 2.4, 1.0, "3.3 Context Explanation &\nAction Generator", bg_color="#0EA5E9", shape="rect", fontsize=8)
    
    # Data Store & Output
    draw_rounded_rect(ax, 7.2, 3.8, 2.2, 0.9, "DS3: Threat Dictionary\n(Regex & Patterns)", shape="datastore", fontsize=7.5)
    draw_rounded_rect(ax, 7.2, 0.5, 2.2, 1.4, "Processed Risk Payload\n(Process 4.0)", shape="entity", fontsize=8)

    # Arrows
    draw_arrow(ax, (2.2, 3.0), (3.2, 4.3), "Tokens & Metadata", label_pos=0.5)
    draw_arrow(ax, (5.6, 4.3), (7.2, 4.3), "Lookup Rules", label_pos=0.5)
    draw_arrow(ax, (4.4, 3.8), (4.4, 3.0), "Weight Scores", label_pos=0.5)
    draw_arrow(ax, (4.4, 2.0), (4.4, 1.3), "Category & Level", label_pos=0.5)
    draw_arrow(ax, (5.6, 0.8), (7.2, 1.0), "Risk JSON Payload", label_pos=0.5)

    plt.tight_layout()
    img_path = os.path.join(IMG_DIR, "dfd_level_2_2.png")
    plt.savefig(img_path, bbox_inches='tight', dpi=300)
    plt.close()
    return img_path

def create_level_2_persistence_diagram():
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    ax.text(5, 5.6, "DFD Level 2.3: Data Persistence & History Subsystem (Process 5.0)", fontsize=12, weight='bold', color="#0F172A", ha='center')
    
    draw_rounded_rect(ax, 0.4, 2.2, 1.8, 1.4, "Formatted Result\n(Process 4.0)", shape="entity", fontsize=8)
    
    draw_rounded_rect(ax, 3.2, 3.8, 2.4, 1.0, "5.1 Scan Record\nDatabase Writer", bg_color="#0284C7", shape="rect", fontsize=8)
    draw_rounded_rect(ax, 3.2, 2.0, 2.4, 1.0, "5.2 History Search &\nFilter Engine", bg_color="#0284C7", shape="rect", fontsize=8)
    draw_rounded_rect(ax, 3.2, 0.3, 2.4, 1.0, "5.3 Record Deletion\nHandler", bg_color="#0284C7", shape="rect", fontsize=8)
    
    draw_rounded_rect(ax, 7.2, 2.2, 2.2, 1.0, "DS1: Scans DB\n(scans table)", shape="datastore", fontsize=7.5)
    
    draw_arrow(ax, (2.2, 3.0), (3.2, 4.3), "Scan Object", label_pos=0.5)
    draw_arrow(ax, (5.6, 4.3), (7.2, 3.0), "INSERT INTO scans", label_pos=0.5)
    draw_arrow(ax, (5.6, 2.5), (7.2, 2.5), "SELECT Query", label_pos=0.5)
    draw_arrow(ax, (5.6, 0.8), (7.2, 2.2), "DELETE Query", label_pos=0.5)

    plt.tight_layout()
    img_path = os.path.join(IMG_DIR, "dfd_level_2_3.png")
    plt.savefig(img_path, bbox_inches='tight', dpi=300)
    plt.close()
    return img_path

def create_level_2_analytics_diagram():
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    ax.text(5, 5.6, "DFD Level 2.4: Analytics & Simulator Subsystem (Process 6.0)", fontsize=12, weight='bold', color="#0F172A", ha='center')
    
    draw_rounded_rect(ax, 0.4, 2.2, 1.8, 1.4, "User / Simulator\nInterface", shape="entity", fontsize=8)
    
    draw_rounded_rect(ax, 3.2, 3.8, 2.4, 1.0, "6.1 Dashboard Metric\nAggregator", bg_color="#0284C7", shape="rect", fontsize=8)
    draw_rounded_rect(ax, 3.2, 2.0, 2.4, 1.0, "6.2 Interactive Quiz\nEvaluation Engine", bg_color="#0284C7", shape="rect", fontsize=8)
    draw_rounded_rect(ax, 3.2, 0.3, 2.4, 1.0, "6.3 Awareness Score\nCalculator", bg_color="#0284C7", shape="rect", fontsize=8)
    
    draw_rounded_rect(ax, 7.2, 2.2, 2.2, 1.0, "DS2: Quiz & Stats DB\n(user_stats)", shape="datastore", fontsize=7.5)
    
    draw_arrow(ax, (2.2, 3.0), (3.2, 4.3), "Get Stats Request", label_pos=0.5)
    draw_arrow(ax, (2.2, 2.7), (3.2, 2.5), "Submit Quiz Answers", label_pos=0.5)
    draw_arrow(ax, (5.6, 2.5), (7.2, 2.7), "Save Score", label_pos=0.5)
    draw_arrow(ax, (5.6, 0.8), (7.2, 2.3), "Update Score", label_pos=0.5)

    plt.tight_layout()
    img_path = os.path.join(IMG_DIR, "dfd_level_2_4.png")
    plt.savefig(img_path, bbox_inches='tight', dpi=300)
    plt.close()
    return img_path


# ==============================================================================
# REPORTLAB PDF GENERATOR
# ==============================================================================

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Skip cover page header/footer
        
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header
        self.drawString(54, 750, "ScamShield™ Complete Data Flow Diagram (DFD) Specification")
        self.drawRightString(612 - 54, 750, "Levels 0, 1 & 2")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.75)
        self.line(54, 742, 612 - 54, 742)
        
        # Footer
        self.line(54, 48, 612 - 54, 48)
        self.setFont("Helvetica", 8)
        self.drawString(54, 34, "CONFIDENTIAL & PROPRIETARY — SCAMSHIELD CYBER SAFETY ARCHITECTURE")
        self.drawRightString(612 - 54, 34, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()


def build_pdf():
    print("[1/2] Rendering DFD diagrams...")
    img_l0 = create_level_0_diagram()
    img_l1 = create_level_1_diagram()
    img_l2_1 = create_level_2_feature_extraction_diagram()
    img_l2_2 = create_level_2_risk_engine_diagram()
    img_l2_3 = create_level_2_persistence_diagram()
    img_l2_4 = create_level_2_analytics_diagram()

    print("[2/2] Generating PDF Document...")
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=26,
        leading=32,
        textColor=colors.HexColor("#0F172A"),
        alignment=0,
        spaceAfter=12
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#0EA5E9"),
        alignment=0,
        spaceAfter=24
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=14,
        spaceAfter=10,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#0284C7"),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#334155"),
        spaceAfter=8
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
        alignment=0
    )

    table_body_style = ParagraphStyle(
        'TableBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#1E293B")
    )

    story = []

    # ==========================================================================
    # PAGE 1: COVER PAGE
    # ==========================================================================
    story.append(Spacer(1, 40))
    story.append(Paragraph("ScamShield™ Cyber Safety Platform", subtitle_style))
    story.append(Paragraph("Complete Data Flow Diagram (DFD)<br/>Specification Document", title_style))
    story.append(HRFlowable(width="100%", thickness=4, color=colors.HexColor("#0EA5E9"), spaceAfter=20))
    
    story.append(Paragraph(
        "<b>Comprehensive Multi-Level DFD Documentation (Level 0, Level 1, Level 2.1 - 2.4)</b><br/>"
        "This specification details the structural data flow, external entity interfaces, process decompositions, "
        "and data store schemas for the ScamShield digital scam check system.",
        body_style
    ))
    story.append(Spacer(1, 25))

    meta_data = [
        [Paragraph("<b>Document Version:</b>", body_style), Paragraph("v2.4 (Production Grade)", body_style)],
        [Paragraph("<b>Target Platform:</b>", body_style), Paragraph("ScamShield Web, PWA & Android Ecosystem", body_style)],
        [Paragraph("<b>Notation Standard:</b>", body_style), Paragraph("Gane & Sarson DFD Methodology", body_style)],
        [Paragraph("<b>Engine Components:</b>", body_style), Paragraph("Python Flask, Cloudflare D1 SQL, Multi-Tier OCR, Risk Engine", body_style)],
        [Paragraph("<b>Security Controls:</b>", body_style), Paragraph("In-Memory Processing, Sanitized Input Summaries, CORS Guards", body_style)],
        [Paragraph("<b>Release Date:</b>", body_style), Paragraph("August 2026", body_style)],
    ]
    t_meta = Table(meta_data, colWidths=[150, 350])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('PADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 30))

    story.append(Paragraph("<b>Table of Contents:</b>", h2_style))
    toc_data = [
        [Paragraph("1. Executive Summary & DFD Methodology", body_style), Paragraph("Page 2", body_style)],
        [Paragraph("2. Level 0 Context Diagram (Process 0.0)", body_style), Paragraph("Page 3", body_style)],
        [Paragraph("3. Level 1 System Level Data Flow Diagram", body_style), Paragraph("Page 4", body_style)],
        [Paragraph("4. Level 2 Subsystem Decompositions (2.1 & 2.2)", body_style), Paragraph("Page 5", body_style)],
        [Paragraph("5. Level 2 Subsystem Decompositions (2.3 & 2.4)", body_style), Paragraph("Page 6", body_style)],
        [Paragraph("6. Data Store Specifications & SQL Schemas", body_style), Paragraph("Page 7", body_style)],
        [Paragraph("7. Data Security, Privacy & Boundary Governance", body_style), Paragraph("Page 8", body_style)],
    ]
    t_toc = Table(toc_data, colWidths=[400, 100])
    t_toc.setStyle(TableStyle([
        ('PADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 2: METHODOLOGY & SYSTEM ARCHITECTURE
    # ==========================================================================
    story.append(Paragraph("1. Executive Summary & DFD Methodology", h1_style))
    story.append(Paragraph(
        "ScamShield is an AI-powered cybersecurity platform designed to protect non-technical users from digital "
        "scams, financial fraud, phishing, KYC traps, and impersonation attacks across SMS, WhatsApp, Emails, "
        "Web URLs, Screenshots, and Audio Call Recordings.",
        body_style
    ))
    story.append(Paragraph(
        "This document models how information moves into, through, and out of ScamShield using standard <b>Gane & Sarson DFD Notation</b>:",
        body_style
    ))

    notations = [
        [Paragraph("<b>Symbol Type</b>", table_header_style), Paragraph("<b>Gane & Sarson Shape</b>", table_header_style), Paragraph("<b>ScamShield System Mapping</b>", table_header_style)],
        [Paragraph("<b>External Entity</b>", table_body_style), Paragraph("Double Square Box", table_body_style), Paragraph("Users (Web/PWA/Android), External OCR/AI APIs, Cybercrime Authorities (1930 portal)", table_body_style)],
        [Paragraph("<b>Process</b>", table_body_style), Paragraph("Rounded Rectangle / Circle", table_body_style), Paragraph("Numbered routines (1.0 Data Ingestion, 3.0 Risk Engine, etc.) executing business logic", table_body_style)],
        [Paragraph("<b>Data Store</b>", table_body_style), Paragraph("Open-ended Rectangle", table_body_style), Paragraph("DS1 (Scans DB), DS2 (Quiz/Stats DB), DS3 (Threat Rules), DS4 (Upload Storage)", table_body_style)],
        [Paragraph("<b>Data Flow</b>", table_body_style), Paragraph("Labeled Directional Arrow", table_body_style), Paragraph("Data payloads (Raw Text, OCR tokens, Risk Scores 0-100, Highlighted HTML)", table_body_style)],
    ]
    t_not = Table(notations, colWidths=[110, 140, 254])
    t_not.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F172A")),
        ('PADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_not)
    story.append(Spacer(1, 15))

    story.append(Paragraph("High-Level Data Transformation Flow:", h2_style))
    story.append(Paragraph("• <b>Ingestion Phase:</b> User inputs raw content (Message text, URL string, Screenshot image, or Audio clip).", bullet_style))
    story.append(Paragraph("• <b>Feature Extraction:</b> Images undergo multi-tier OCR; audio undergoes speech transcription; text and URLs are tokenized.", bullet_style))
    story.append(Paragraph("• <b>Risk Calculation:</b> Pattern matching evaluates indicator weights against DS3 Threat Dictionary. Total weight is capped at 100.", bullet_style))
    story.append(Paragraph("• <b>Result Delivery:</b> Formatted risk level (LIKELY SAFE, SUSPICIOUS, HIGH RISK), warning signs, and suspicious phrase highlights are returned to the user.", bullet_style))
    story.append(Paragraph("• <b>Audit & Persistence:</b> Sanitized scan record is saved to DS1 (Scans DB) for user history and dashboard analytics.", bullet_style))
    
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 3: LEVEL 0 CONTEXT DIAGRAM
    # ==========================================================================
    story.append(Paragraph("2. Level 0: Context Diagram (Process 0.0)", h1_style))
    story.append(Paragraph(
        "The Level 0 Context Diagram establishes the highest-level operational boundary of the ScamShield system, "
        "identifying all external actors and primary data interactions.",
        body_style
    ))
    story.append(Spacer(1, 5))
    story.append(Image(img_l0, width=504, height=302))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Level 0 Data Dictionary Table:", h2_style))
    l0_dict = [
        [Paragraph("<b>Flow Name</b>", table_header_style), Paragraph("<b>Source</b>", table_header_style), Paragraph("<b>Destination</b>", table_header_style), Paragraph("<b>Data Payload Description</b>", table_header_style)],
        [Paragraph("Raw Input Payload", table_body_style), Paragraph("User (Web / PWA)", table_body_style), Paragraph("Process 0.0", table_body_style), Paragraph("SMS text, URL string, Screenshot image stream, Audio recording bytes", table_body_style)],
        [Paragraph("Scam Risk Report", table_body_style), Paragraph("Process 0.0", table_body_style), Paragraph("User (Web / PWA)", table_body_style), Paragraph("Risk score (0-100), risk level, warning signs, highlighted HTML text, guidance", table_body_style)],
        [Paragraph("Scan & Push Alert", table_body_style), Paragraph("Process 0.0", table_body_style), Paragraph("Mobile App User", table_body_style), Paragraph("Real-time danger rating & SMS scam category alert", table_body_style)],
        [Paragraph("OCR & AI Prompts", table_body_style), Paragraph("Process 0.0", table_body_style), Paragraph("External Services", table_body_style), Paragraph("Image byte stream, audio buffer, LLM classification prompt", table_body_style)],
        [Paragraph("Extracted Response", table_body_style), Paragraph("External Services", table_body_style), Paragraph("Process 0.0", table_body_style), Paragraph("Parsed OCR text, speech transcript, AI risk category", table_body_style)],
        [Paragraph("Fraud Escalation Log", table_body_style), Paragraph("Process 0.0", table_body_style), Paragraph("Cybercrime Portal", table_body_style), Paragraph("Escalation template with complaint metadata for official 1930 portal reporting", table_body_style)],
    ]
    t_l0 = Table(l0_dict, colWidths=[100, 95, 95, 214])
    t_l0.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F172A")),
        ('PADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_l0)
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 4: LEVEL 1 SYSTEM DFD
    # ==========================================================================
    story.append(Paragraph("3. Level 1: System Level Data Flow Diagram", h1_style))
    story.append(Paragraph(
        "The Level 1 DFD decomposes Process 0.0 into 6 core functional processes, showing how data moves "
        "between ingestion, feature extraction, risk calculation, formatting, storage, and analytics.",
        body_style
    ))
    story.append(Spacer(1, 5))
    story.append(Image(img_l1, width=504, height=343))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Level 1 Process Decomposition Directory:", h2_style))
    l1_dir = [
        [Paragraph("<b>Proc ID</b>", table_header_style), Paragraph("<b>Process Name</b>", table_header_style), Paragraph("<b>Input Flows</b>", table_header_style), Paragraph("<b>Output Flows</b>", table_header_style)],
        [Paragraph("<b>1.0</b>", table_body_style), Paragraph("Data Ingestion & Sanitization", table_body_style), Paragraph("Raw Form / File Uploads", table_body_style), Paragraph("Sanitized Input Payload", table_body_style)],
        [Paragraph("<b>2.0</b>", table_body_style), Paragraph("Multi-Modal Feature Extraction", table_body_style), Paragraph("Sanitized Payload, OCR Bytes", table_body_style), Paragraph("Extracted Text & URL Features", table_body_style)],
        [Paragraph("<b>3.0</b>", table_body_style), Paragraph("Scam Risk Assessment Engine", table_body_style), Paragraph("Extracted Features, DS3 Rules", table_body_style), Paragraph("Indicator Score Weights & Category", table_body_style)],
        [Paragraph("<b>4.0</b>", table_body_style), Paragraph("Result Formatter & Highlight Engine", table_body_style), Paragraph("Raw Weights & Level", table_body_style), Paragraph("Formatted HTML Result, Final Log Record", table_body_style)],
        [Paragraph("<b>5.0</b>", table_body_style), Paragraph("Persistence & History Manager", table_body_style), Paragraph("Final Scan Log Record", table_body_style), Paragraph("DS1 SQL Insert / Query", table_body_style)],
        [Paragraph("<b>6.0</b>", table_body_style), Paragraph("Security Analytics & Simulator", table_body_style), Paragraph("Quiz Submission, Analytics Query", table_body_style), Paragraph("DS2 Score Updates, Dashboard Metrics", table_body_style)],
    ]
    t_l1 = Table(l1_dir, colWidths=[45, 135, 140, 184])
    t_l1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F172A")),
        ('PADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_l1)
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 5: LEVEL 2 DECOMPOSITIONS (2.1 & 2.2)
    # ==========================================================================
    story.append(Paragraph("4. Level 2 Subsystem Decompositions (2.1 & 2.2)", h1_style))
    
    story.append(Paragraph("Subsystem 2.1: Multi-Modal Feature Extraction (Decomposition of Process 2.0)", h2_style))
    story.append(Image(img_l2_1, width=504, height=277))
    story.append(Paragraph(
        "• <b>2.1 Text Extractor:</b> Tokenizes text messages and extracts suspicious regex keywords (e.g. 'blocked', 'urgent', 'winner').<br/>"
        "• <b>2.2 URL Parser:</b> Resolves shortened URLs (bit.ly, tinyurl), checks domain age, IP address usage, and phishing keywords.<br/>"
        "• <b>2.3 Screenshot OCR:</b> Converts uploaded screenshot images to text using in-memory Pytesseract / Cloud OCR.<br/>"
        "• <b>2.4 Audio Transcriber:</b> Processes audio clips into text transcripts for scam keyword detection.",
        body_style
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Subsystem 2.2: Risk Assessment & Classification (Decomposition of Process 3.0)", h2_style))
    story.append(Image(img_l2_2, width=504, height=277))
    story.append(Paragraph(
        "• <b>3.1 Indicator Weight Accumulator:</b> Queries DS3 Threat Dictionary and sums risk weights for all detected indicators (capped at 100).<br/>"
        "• <b>3.2 Primary Category Classifier:</b> Determines primary scam type (e.g. KYC Scam, UPI Scam, Banking Scam, Phishing, Job Scam).<br/>"
        "• <b>3.3 Explanation & Action Generator:</b> Builds human-understandable risk explanations and recommended safety actions based on risk tier.",
        body_style
    ))
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 6: LEVEL 2 DECOMPOSITIONS (2.3 & 2.4)
    # ==========================================================================
    story.append(Paragraph("5. Level 2 Subsystem Decompositions (2.3 & 2.4)", h1_style))

    story.append(Paragraph("Subsystem 2.3: Data Persistence & History (Decomposition of Process 5.0)", h2_style))
    story.append(Image(img_l2_3, width=504, height=277))
    story.append(Paragraph(
        "• <b>5.1 Scan Record Writer:</b> Serializes risk scores, category, warning signs JSON, and input summary into DS1 (`scans` table).<br/>"
        "• <b>5.2 History Search & Filter:</b> Executes filtered SELECT queries on DS1 by search term, risk level, or date sorting.<br/>"
        "• <b>5.3 Record Deletion Handler:</b> Performs secure deletion of individual scan records upon user request.",
        body_style
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Subsystem 2.4: Security Analytics & Simulator (Decomposition of Process 6.0)", h2_style))
    story.append(Image(img_l2_4, width=504, height=277))
    story.append(Paragraph(
        "• <b>6.1 Dashboard Metric Aggregator:</b> Calculates total scans, threat category distribution, and average risk score for `/dashboard`.<br/>"
        "• <b>6.2 Interactive Quiz Evaluator:</b> Scores user responses in the 'Spot the Scam' simulator.<br/>"
        "• <b>6.3 Awareness Score Calculator:</b> Updates overall cyber awareness index score in DS2 (`user_stats` table).",
        body_style
    ))
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 7: DATA STORE SPECIFICATIONS
    # ==========================================================================
    story.append(Paragraph("6. Data Store Specifications & SQL Schemas", h1_style))
    story.append(Paragraph(
        "ScamShield utilizes Cloudflare D1 serverless SQL database with local SQLite fallback. "
        "Below are the complete schema definitions for all system data stores.",
        body_style
    ))

    story.append(Paragraph("DS1: Scans Database (`scans` Table Schema)", h2_style))
    ds1_data = [
        [Paragraph("<b>Field Name</b>", table_header_style), Paragraph("<b>Data Type</b>", table_header_style), Paragraph("<b>Constraints</b>", table_header_style), Paragraph("<b>Description / Content</b>", table_header_style)],
        [Paragraph("`id`", table_body_style), Paragraph("INTEGER", table_body_style), Paragraph("PRIMARY KEY AUTOINCREMENT", table_body_style), Paragraph("Unique scan identifier", table_body_style)],
        [Paragraph("`created_at`", table_body_style), Paragraph("TIMESTAMP", table_body_style), Paragraph("DEFAULT CURRENT_TIMESTAMP", table_body_style), Paragraph("Scan execution timestamp", table_body_style)],
        [Paragraph("`scan_type`", table_body_style), Paragraph("TEXT", table_body_style), Paragraph("NOT NULL", table_body_style), Paragraph("'message', 'url', 'screenshot', 'call'", table_body_style)],
        [Paragraph("`risk_score`", table_body_style), Paragraph("INTEGER", table_body_style), Paragraph("NOT NULL (0-100)", table_body_style), Paragraph("Calculated scam risk score", table_body_style)],
        [Paragraph("`risk_level`", table_body_style), Paragraph("TEXT", table_body_style), Paragraph("NOT NULL", table_body_style), Paragraph("'LIKELY SAFE', 'NEEDS VERIFICATION', 'SUSPICIOUS', 'HIGH RISK'", table_body_style)],
        [Paragraph("`scam_category`", table_body_style), Paragraph("TEXT", table_body_style), Paragraph("NOT NULL", table_body_style), Paragraph("'Banking Scam', 'UPI Scam', 'KYC Scam', 'Phishing', etc.", table_body_style)],
        [Paragraph("`warning_signs_json`", table_body_style), Paragraph("TEXT (JSON)", table_body_style), Paragraph("NULLABLE", table_body_style), Paragraph("JSON array of detected red flags", table_body_style)],
        [Paragraph("`explanation`", table_body_style), Paragraph("TEXT", table_body_style), Paragraph("NULLABLE", table_body_style), Paragraph("Contextual risk explanation paragraph", table_body_style)],
        [Paragraph("`input_summary`", table_body_style), Paragraph("TEXT", table_body_style), Paragraph("NULLABLE", table_body_style), Paragraph("Sanitized, truncated summary of analyzed content", table_body_style)],
    ]
    t_ds1 = Table(ds1_data, colWidths=[110, 80, 140, 174])
    t_ds1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F172A")),
        ('PADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_ds1)
    story.append(Spacer(1, 15))

    story.append(Paragraph("DS2: Quiz & User Stats Database (`quiz_results` & `user_stats` Schemas)", h2_style))
    ds2_data = [
        [Paragraph("<b>Table</b>", table_header_style), Paragraph("<b>Field</b>", table_header_style), Paragraph("<b>Type</b>", table_header_style), Paragraph("<b>Description</b>", table_header_style)],
        [Paragraph("`quiz_results`", table_body_style), Paragraph("`score`, `total_questions`", table_body_style), Paragraph("INTEGER", table_body_style), Paragraph("Number of correct answers and total questions in quiz run", table_body_style)],
        [Paragraph("`quiz_results`", table_body_style), Paragraph("`accuracy`", table_body_style), Paragraph("REAL", table_body_style), Paragraph("Accuracy percentage (0.0 to 100.0)", table_body_style)],
        [Paragraph("`user_stats`", table_body_style), Paragraph("`awareness_score`", table_body_style), Paragraph("INTEGER", table_body_style), Paragraph("Aggregated user cyber safety awareness score (default 85)", table_body_style)],
        [Paragraph("`user_stats`", table_body_style), Paragraph("`total_scans`", table_body_style), Paragraph("INTEGER", table_body_style), Paragraph("Total number of scans completed across all channels", table_body_style)],
    ]
    t_ds2 = Table(ds2_data, colWidths=[90, 120, 80, 214])
    t_ds2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F172A")),
        ('PADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_ds2)
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 8: SECURITY & GOVERNANCE
    # ==========================================================================
    story.append(Paragraph("7. Data Security, Privacy & Boundary Governance", h1_style))
    story.append(Paragraph(
        "To ensure compliance with cybersecurity best practices and protect sensitive user data, "
        "ScamShield enforces strict data boundary controls across all DFD processes:",
        body_style
    ))

    story.append(Paragraph("<b>1. Ephemeral In-Memory File Processing (Zero Disk Dependency)</b>", h2_style))
    story.append(Paragraph(
        "Screenshots and audio recordings uploaded to Process 1.0/2.0 are converted into in-memory byte streams "
        "(`io.BytesIO`) during OCR and audio transcription. No persistent files are written to ephemeral disk storage in production.",
        body_style
    ))

    story.append(Paragraph("<b>2. Input Sanitization & Privacy Truncation</b>", h2_style))
    story.append(Paragraph(
        "Before persisting scan logs to DS1 (`scans` table), input strings undergo HTML escaping and sanitization. "
        "Full message contents are truncated to safe summaries (`input_summary`), ensuring credentials, OTPs, or passwords "
        "accidentally submitted by users are not logged.",
        body_style
    ))

    story.append(Paragraph("<b>3. HTTP Security Headers & Cross-Origin Resource Sharing (CORS)</b>", h2_style))
    story.append(Paragraph(
        "All API endpoints enforce mandatory security headers (`X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, "
        "`X-XSS-Protection: 1; mode=block`). Requests from unauthorized origins are blocked.",
        body_style
    ))

    story.append(Paragraph("<b>4. Escalation Protocol & Helpline Integration</b>", h2_style))
    story.append(Paragraph(
        "High-risk scans (Score >= 75) trigger direct emergency recommendations guiding users to immediately dial "
        "the <b>National Cyber Crime Helpline (1930)</b> or file complaints at <b>cybercrime.gov.in</b>.",
        body_style
    ))

    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceAfter=15))
    story.append(Paragraph(
        "<b>Document Sign-off:</b><br/>"
        "Architect: <i>ScamShield Engineering Team</i><br/>"
        "Status: <i>Approved & Verified</i>",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] DFD Specification PDF successfully generated at: {PDF_PATH}")

if __name__ == "__main__":
    build_pdf()
