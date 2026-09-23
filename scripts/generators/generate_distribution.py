from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 15)
        self.cell(0, 10, 'Group TYG19: Individual Work Distribution', border=False, new_x="LMARGIN", new_y="NEXT", align='C')
        self.ln(5)

    def chapter_title(self, title):
        self.set_font('helvetica', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 8, title, border=False, new_x="LMARGIN", new_y="NEXT", fill=True)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('helvetica', '', 11)
        self.multi_cell(0, 6, body)
        self.ln(6)

pdf = PDF()
pdf.add_page()

# 1. Harsh
pdf.chapter_title('1. Harsh Manjramkar (Team Lead & Core Architect)')
body1 = """Primary Folders Owned: src/gateway/ , src/hitl/ , and static/
Harsh handled the core infrastructure, backend architecture, and full-stack integration.

- Core Proxy Architecture: Designed and implemented the main Transparent Proxy gateway using FastAPI (src/gateway/router.py) to flawlessly intercept JSON-RPC traffic.
- Asynchronous HITL Manager: Engineered the complex Human-in-the-Loop workflow (src/hitl/manager.py) using asyncio.Event() to securely pause and resume execution in server memory.
- Frontend Logic & AI Integration: Developed the JavaScript architecture for the Visual E2E Flow Simulator and the Live Custom Terminal (static/index.html), and handled the live integrations with Claude Desktop, Cursor IDE, and Antigravity.
"""
pdf.chapter_body(body1)

# 2. Vedant
pdf.chapter_title('2. Vedant Gaidhani (Security Engineer - Threat Detection)')
body2 = """Primary Folders Owned: src/risk/
Vedant owned the inbound payload inspection and prompt injection defense mechanisms.

- Regex Detection Engine: Built the comprehensive regex signature database (src/risk/detectors.py) to instantly identify and block prompt injections, DAN jailbreaks, and SQL injection vectors.
- Dynamic Heuristics: Implemented the wildcard heuristic engine (src/risk/heuristics.py) to dynamically flag dangerous tool executions (like 'delete', 'drop', or 'execute').
- Risk Router: Co-developed the evaluator.py logic to accurately assign LOW, MEDIUM, or HIGH risk severity to incoming AI payloads.
"""
pdf.chapter_body(body2)

# 3. Vineet
pdf.chapter_title('3. Vineet Wagh (Security Engineer - Data Privacy)')
body3 = """Primary Folders Owned: src/sanitizer/ and static/
Vineet owned the outbound data inspection, sanitization, and UI/UX design.

- PII Sanitization Engine: Developed the recursive JSON parsing algorithm (src/sanitizer/pii_engine.py) that actively intercepts returning payloads from the MCP server.
- Redaction Logic: Created the regex patterns (src/sanitizer/patterns.py) to detect and scrub sensitive data like Aadhaar numbers, PAN cards, and API keys without corrupting the JSON schema.
- Dashboard UI/UX: Wrote the advanced CSS styling and animations (static/index.html) for the interactive dashboard and data-packet simulation.
"""
pdf.chapter_body(body3)

# 4. Arjun
pdf.chapter_title('4. Arjun Joshi (QA & Integration Testing Engineer)')
body4 = """Primary Folders Owned: tests/ and tests/integration/
Arjun owned the massive testing suite to ensure the proxy was enterprise-ready.

- Enterprise Target Mocking: Designed the Mock Target Hub that correctly simulates the exact JSON-RPC schemas of 15 Enterprise MCPs (GitHub, PostgreSQL, Slack, Docker, etc.).
- Automated Test Suite: Wrote and maintained all 57 automated pytest integration tests (tests/integration/test_15_real_mcp_servers.py), proving the proxy never corrupts safe payloads.
- Documentation & DevOps: Handled the generation of the PDF demonstration guides, project documentation, and repository structure cleanup.
"""
pdf.chapter_body(body4)

pdf.output("Work_Distribution.pdf")
print("Work_Distribution.pdf Generated successfully.")
