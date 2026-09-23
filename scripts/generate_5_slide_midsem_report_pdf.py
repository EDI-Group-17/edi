import os
from fpdf import FPDF

class FiveSlideReportPDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(100, 116, 139)
        self.cell(0, 8, 'AgentShield - Mid-Semester Presentation Dossier (5-Slide Executive Deck) | VIT Pune', 0, 0, 'L')
        self.cell(0, 8, f'Page {self.page_no()}', 0, 1, 'R')
        self.set_draw_color(226, 232, 240)
        self.line(14, 18, 196, 18)
        self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(148, 163, 184)
        self.cell(0, 10, 'Department of Computer Engineering | Group TYG19 | Guide: Prof. Sanyukta Deshmukh', 0, 0, 'C')

def create_report():
    pdf = FiveSlideReportPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=False)
    pdf.set_margins(14, 14, 14)

    # ==================== PAGE 1: COVER & FORMAL ASSESSMENT MAPPING ====================
    pdf.add_page()
    pdf.ln(5)
    pdf.set_fill_color(15, 23, 42) # Dark Navy
    pdf.rect(14, 14, 182, 42, 'F')

    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 18)
    pdf.set_y(19)
    pdf.cell(0, 9, 'AgentShield: Mid-Sem Review Presentation Dossier', 0, 1, 'C')
    pdf.set_font('Helvetica', '', 10.5)
    pdf.set_text_color(148, 163, 184)
    pdf.cell(0, 6, '5-Slide Executive Academic Deck & Evaluation Criteria Assessment', 0, 1, 'C')
    pdf.cell(0, 6, 'Aligned with VIT FF No. 180 Progress Review 1 Parameters', 0, 1, 'C')

    pdf.set_y(62)
    pdf.set_text_color(30, 41, 59)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 6, 'ACADEMIC & INSTITUTIONAL PROFILE', 0, 1, 'L')
    pdf.set_draw_color(14, 165, 233)
    pdf.set_line_width(0.5)
    pdf.line(14, 69, 196, 69)
    pdf.ln(3)

    info_data = [
        ("Institution", "Vishwakarma Institute of Technology (VIT), Pune"),
        ("Department", "Department of Computer Engineering (Academic Year 2026-27)"),
        ("Semester / Group", "Semester 5 | Group No.: TYG19 | Area: AI & Cybersecurity"),
        ("Project Title", "AgentShield: A Dynamic Risk-Aware Security Framework for the Model Context Protocol"),
        ("Faculty Guide", "Prof. Sanyukta Deshmukh (Contact: 9021907414, Sanyukta.deshmukh@vit.edu)"),
        ("Form Reference", "Issue 01 : Rev No. 00 : Dt. 05/02/26 (FF No. 180 Progress Review 1)")
    ]
    for k, v in info_data:
        pdf.set_font('Helvetica', 'B', 8.5)
        pdf.set_text_color(51, 65, 85)
        pdf.cell(34, 5.2, f"{k}:", 0, 0)
        pdf.set_font('Helvetica', '', 8.5)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(0, 5.2, v, 0, 1)

    pdf.ln(2)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 6, 'GROUP MEMBERS & INDIVIDUAL RESPONSIBILITIES', 0, 1, 'L')
    pdf.line(14, 110, 196, 110)
    pdf.ln(3)

    members = [
        ("1", "Harsh Manjramkar", "TY-G/70", "12414557", "harsh.manjramkar24@vit.edu", "Lead Architect, Async Proxy Gateway Core & JSON-RPC Routing"),
        ("2", "Vedant Gaidhani", "TY-G/74", "12415020", "vedant.gaidhani242@vit.edu", "Dynamic 3-Tier Risk Classifier & Heuristic Injection Detectors"),
        ("3", "Vineet Wagh", "TY-G/75", "12415021", "vineet.wagh241@vit.edu", "Response PII Redaction Engine & Rate Limit Loop Quarantine"),
        ("4", "Arjun Joshi", "TY-G/76", "12415022", "arjun.joshi241@vit.edu", "Async Batch Audit Logger & Real-time WebSockets Dashboard")
    ]

    pdf.set_fill_color(241, 245, 249)
    pdf.set_font('Helvetica', 'B', 7.5)
    pdf.cell(8, 5.5, "Sr", 1, 0, 'C', True)
    pdf.cell(34, 5.5, "Name", 1, 0, 'L', True)
    pdf.cell(16, 5.5, "Div/Roll", 1, 0, 'C', True)
    pdf.cell(18, 5.5, "G.R. No.", 1, 0, 'C', True)
    pdf.cell(46, 5.5, "Email ID", 1, 0, 'L', True)
    pdf.cell(60, 5.5, "Individual Technical Responsibility", 1, 1, 'L', True)

    pdf.set_font('Helvetica', '', 7.5)
    for sr, name, div, gr, email, role in members:
        pdf.cell(8, 5.2, sr, 1, 0, 'C')
        pdf.cell(34, 5.2, name, 1, 0, 'L')
        pdf.cell(16, 5.2, div, 1, 0, 'C')
        pdf.cell(18, 5.2, gr, 1, 0, 'C')
        pdf.cell(46, 5.2, email, 1, 0, 'L')
        pdf.cell(60, 5.2, role, 1, 1, 'L')

    pdf.ln(4)
    pdf.set_fill_color(238, 242, 255)
    pdf.set_draw_color(99, 102, 241)
    pdf.rect(14, 150, 182, 125, 'DF')
    pdf.set_xy(18, 153)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(49, 46, 129)
    pdf.cell(0, 5, 'EVALUATION PARAMETERS MAPPING TABLE (VIT ASSESSMENT SCHEME)', 0, 1)
    
    pdf.set_xy(18, 160)
    params_mapping = [
        ("1. Problem Definition, Related Work & Complexity", "Slide 1 & Slide 2", "Autonomous AI risk, prompt injection, lack of oversight, <5ms latency complexity."),
        ("2. Literature Review, Proposed Solution & Feasibility", "Slide 2", "5 foundational papers evaluated, runtime proxy solution, FastAPI ASGI feasibility."),
        ("3. Cost, Resources, Environment & Sustainability", "Slide 4", "100% open-source, edge-compatible, prevents wasteful LLM loops (green computing)."),
        ("4. Group Formation & Individual Responsibilities", "Slide 1 & Cover", "Clear task split across Gateway, Risk Engine, PII Sanitizer, and Audit/UI."),
        ("5. Objectives of the Project", "Slide 1", "8 specific measurable goals aligned with FF No. 180 Section 4."),
        ("6. System Architecture & Engineering Pipeline", "Slide 3", "10-stage sequential data pipeline (Interception -> Risk -> HITL -> Sanitizer -> DB)."),
        ("7. Methodology & Defense In-Depth Strategy", "Slide 3", "Regex automata, argument heuristics, sliding window limiter, recursive JSON cleansing."),
        ("8. Knowledge of Domain, Technology & Tools", "Slide 3 & Slide 5", "FastAPI, JSON-RPC 2.0, Async SQLAlchemy, WebSockets, 15 real MCP servers tested."),
        ("9. Progress Done Till Now vs. End-Sem Roadmap", "Slide 5", "Core proxy & security modules operational; public demo portal & containerization remaining."),
        ("10. EDI Guide Consultation Points", "Slide 5", "Enterprise RBAC, live public demo portal & package publishing as advised by Guide.")
    ]

    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(30, 41, 59)
    for p_name, s_loc, desc in params_mapping:
        pdf.set_x(18)
        pdf.set_font('Helvetica', 'B', 8)
        pdf.cell(75, 4.8, p_name, 0, 0)
        pdf.set_font('Helvetica', 'I', 8)
        pdf.set_text_color(79, 70, 229)
        pdf.cell(26, 4.8, f"[{s_loc}]", 0, 0)
        pdf.set_font('Helvetica', '', 7.8)
        pdf.set_text_color(51, 65, 85)
        pdf.cell(73, 4.8, desc, 0, 1)

    # ==================== SLIDES 1 TO 5 ====================
    slides_data = [
        {
            "num": "SLIDE 1 OF 5",
            "title": "Project Overview, Objectives, Team Responsibilities & Problem Complexity",
            "params": "Parameters Covered: Problem Definition, Related Work, Complexity, Group Formation, Project Objectives",
            "sections": [
                ("Project Context & Domain", [
                    "Title: AgentShield: A Dynamic Risk-Aware Security Framework for the Model Context Protocol.",
                    "Academic Profile: Group TYG19 | Computer Engineering | AY 2026-27 | Internal Guide: Prof. Sanyukta Deshmukh.",
                    "Team Roles: Harsh (Gateway/Routing), Vedant (Risk/Injection), Vineet (PII/RateLimit), Arjun (Audit/Dashboard)."
                ]),
                ("Problem Definition & Architectural Complexity", [
                    "Problem Statement: Direct point-to-point integration of AI agents with enterprise tools (databases, filesystems, shell) via MCP introduces critical runtime vulnerabilities due to hallucinations, prompt injections, and lack of human supervision.",
                    "Complexity: The security gateway must inspect bidirectional, deeply-nested JSON-RPC payloads in real time, evaluate multi-variable risk heuristics, and hold high-risk calls synchronously while maintaining sub-5 millisecond proxy latency."
                ]),
                ("Core Project Objectives (FF No. 180 Aligned)", [
                    "1. Intercept & inspect all JSON-RPC 2.0 communication transparently without modifying agent or server code.",
                    "2. Implement a Dynamic Risk Engine classifying requests into LOW, MEDIUM, and HIGH risk categories.",
                    "3. Detect prompt injections, DAN jailbreaks, SQLi, and sensitive command execution (sudo, chmod, /etc/).",
                    "4. Enforce real-time Human-in-the-Loop (HITL) approval gates with 60-second fail-closed timeouts.",
                    "5. Recursively sanitize target MCP responses to prevent PII (AWS keys, Aadhaar, PAN) from leaking into LLMs."
                ])
            ],
            "notes": "Good morning respected guide Prof. Sanyukta Deshmukh and committee. Slide 1 establishes our team allocation, formal problem definition, and objectives. MCP grants AI direct tool execution rights without a firewall. AgentShield provides the missing runtime guardrail without adding perceptible latency."
        },
        {
            "num": "SLIDE 2 OF 5",
            "title": "Literature Review, Related Work & Proposed Solution Feasibility",
            "params": "Parameters Covered: Literature Review, Related Work, Proposed Solution, Technical Approach, Feasibility",
            "sections": [
                ("Literature Survey & Critical Gaps (5 Foundational Papers)", [
                    "MCPShield (2026): Evaluates historical server trust; Limitation: Static pre-handshake checks only, lacks runtime inspection.",
                    "MCPSec (2026): Protocol-level encryption and message integrity; Limitation: Cannot inspect or govern semantic agent actions.",
                    "ShieldMCP (2026): Basic proxy interceptor; Limitation: Lacks dynamic contextual risk scoring, response PII sanitization, and audit.",
                    "Enterprise Security Framework (2025): Governance guidelines; Limitation: Conceptual policies without runtime implementation.",
                    "Security Threats Analysis (2026): Threat taxonomy; Limitation: Focuses on attack discovery rather than runtime mitigation."
                ]),
                ("Proposed Solution: Transparent Runtime Security Gateway", [
                    "Architecture: AgentShield acts as a smart reverse proxy between AI clients (OpenAI/Claude) and target MCP servers.",
                    "Dynamic Risk Governance: Replaces static rules with multi-factor risk assessment evaluating tools, arguments, and agent history.",
                    "Zero-Trust Human Oversight: Pauses dangerous commands for administrator sign-off before execution reaches enterprise systems."
                ]),
                ("Technical Approach & Engineering Feasibility", [
                    "Feasibility: Standard JSON-RPC 2.0 compliance means any client configuring proxy URL (http://proxy:8000/mcp/v1/proxy) works instantly.",
                    "Low-Latency Execution: Built on asynchronous ASGI (FastAPI + Starlette) with non-blocking I/O, ensuring negligible proxy overhead."
                ])
            ],
            "notes": "Slide 2 presents our literature study. Existing 2025-2026 research focuses purely on transport encryption or static server trust. AgentShield bridges this gap with an active runtime proxy that evaluates semantics, pauses for human approval, and sanitizes responses."
        },
        {
            "num": "SLIDE 3 OF 5",
            "title": "System Architecture, Methodology & Technology Stack",
            "params": "Parameters Covered: System Architecture, Methodology, Knowledge of Domain, Technology and Tools",
            "sections": [
                ("System Architecture & 10-Stage Request Lifecycle", [
                    "1. Inbound Interceptor -> Captures JSON-RPC 2.0 requests at /mcp/v1/proxy.",
                    "2. Dynamic Risk Classifier -> Analyzes method, tool name, and payload; assigns LOW, MEDIUM, or HIGH score.",
                    "3. Heuristic Detectors -> Scans arguments for injection tags (<system_override>), SQLi, and shell commands (sudo, chmod).",
                    "4. Decision Gate -> LOW: Forward immediately | INJECTION: Block (-32002) | SENSITIVE TOOL: Hold for HITL (-32001).",
                    "5. Rate Limiter / Quarantine -> Sliding-window tracker isolates looping agents (>10 calls in 5s) for 60s.",
                    "6. Outbound Forwarder -> Asynchronous HTTPX client forwards approved requests to target MCP servers on port 8001.",
                    "7. Response PII Sanitizer -> Deep recursive object walker redacts AWS keys, Aadhaar numbers, and credentials.",
                    "8. Async Audit Logger -> Non-blocking asyncio.Queue batches transaction records directly to PostgreSQL/SQLite.",
                    "9. WebSockets Broadcaster -> Streams real-time transaction events and pending approval popups to the Admin Dashboard."
                ]),
                ("Technology Stack & Toolchain Justification", [
                    "Backend: Python 3.10+, FastAPI, Starlette (Async ASGI for high concurrency and microsecond routing).",
                    "Database & ORM: PostgreSQL & SQLite via Async SQLAlchemy (ACID audit trails with JSONB payload indexing).",
                    "Frontend UI: Glassmorphism Single-Page Dashboard with native HTML5 WebSockets (/ws/traffic).",
                    "Verification Hub: Built multi_mcp_hub.py validating compatibility across 15 real MCP servers (GitHub, Ruflo, Docker, etc.)."
                ])
            ],
            "notes": "Slide 3 details our architecture. Every request passes through a 10-stage pipeline: interception, risk scoring, heuristic analysis, decision gating, rate limiting, forwarding, PII sanitization, background queue logging, and real-time dashboard broadcasting."
        },
        {
            "num": "SLIDE 4 OF 5",
            "title": "Cost, Resources, Environmental Relevance & Sustainability",
            "params": "Parameters Covered: Cost, Resources, Environmental Relevance, Sustainability",
            "sections": [
                ("Cost Efficiency & Zero SaaS Dependencies", [
                    "100% Open-Source Stack: Constructed using Python, FastAPI, SQLite, and PostgreSQL with zero commercial licensing fees.",
                    "Elimination of Third-Party API Costs: Regex automata and heuristic risk engines run locally in memory without querying costly external LLM APIs for guardrail checks, saving significant operational expenditure."
                ]),
                ("Resource Optimization & Minimal Hardware Footprint", [
                    "Lightweight Footprint: Consumes under 50 MB of memory and less than 2% CPU at idle, allowing deployment on micro-instances or edge VMs.",
                    "Microsecond Execution: Local pattern matching executes in sub-2ms, preventing processing bottlenecks."
                ]),
                ("Environmental Relevance & Green Computing (Loop Suppression)", [
                    "Preventing AI Token Waste: Autonomous agents frequently enter infinite hallucination loops, making hundreds of redundant LLM API calls and heavy database queries.",
                    "Compute & Energy Conservation: AgentShield's Loop Quarantine detector isolates rogue agents within 5 seconds, preventing wasted GPU cluster cycles, cloud carbon emissions, and excessive data center power draw."
                ]),
                ("Sustainability & Extensibility", [
                    "Standardized JSON-RPC 2.0 interface ensures AgentShield can govern any future MCP server release without vendor lock-in."
                ])
            ],
            "notes": "Slide 4 addresses sustainability and cost. By running local heuristic evaluation, AgentShield incurs zero API inspection fees. Crucially, our loop quarantine suppresses hallucination loops, saving massive amounts of GPU compute power, data center energy, and enterprise cost."
        },
        {
            "num": "SLIDE 5 OF 5",
            "title": "Progress Achieved Till Mid-Sem, Remaining Roadmap & EDI Guide Discussion",
            "params": "Parameters Covered: Progress Done Till Now, Remaining Work for End-Sem, Additional Guide Points",
            "sections": [
                ("Progress Accomplished Till Mid-Semester Review", [
                    "Core Security Gateway & Routing Engine operational with standard JSON-RPC 2.0 compliance.",
                    "3-Tier Risk Engine & Heuristics implemented (DAN prompts, SQLi, subshells, sensitive directories).",
                    "Sliding-window Rate Limiter & Hallucination Loop Quarantine engine active.",
                    "Real-time Human-in-the-Loop (HITL) approval manager with 60s fail-closed timeout built.",
                    "Recursive Response PII Sanitizer operational (protects AWS keys, Aadhaar numbers, PAN, credit cards).",
                    "Async batch audit logging pipeline and Glassmorphism Web Dashboard prototype functional.",
                    "Rigorous Verification: 57 automated PyTest unit & integration tests passing (100% pass rate)."
                ]),
                ("Remaining Roadmap for End-Semester Review", [
                    "1. Production Containerization: Packaging the gateway and MCP hub into Docker Compose & Kubernetes for one-click deployment.",
                    "2. Public Demonstration Web Portal: Developing a hosted interactive webpage allowing evaluators to test live AI agent prompts against live tools in real-time.",
                    "3. Open-Source Package Publishing: Publishing AgentShield as an installable Python package (pip install agentshield) for community integration.",
                    "4. Enterprise RBAC & OAuth2 Integration: Associating agent capabilities with organizational user roles as discussed with EDI Guide Prof. Sanyukta Deshmukh."
                ])
            ],
            "notes": "Slide 5 covers our progress and roadmap. The core proxy, risk engine, HITL approval, PII sanitizer, and 57 tests are complete. For the end-sem, as discussed with Prof. Deshmukh, we will focus on Docker deployment, publishing the package, building a public demo web portal, and enterprise RBAC."
        }
    ]

    for s in slides_data:
        pdf.add_page()
        # Slide Header Bar
        pdf.set_fill_color(15, 23, 42)
        pdf.rect(14, 14, 182, 14, 'F')
        pdf.set_xy(16, 16)
        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(32, 10, s["num"] + ":", 0, 0)
        pdf.set_font('Helvetica', 'B', 10.5)
        pdf.set_text_color(56, 189, 248)
        pdf.cell(0, 10, s["title"], 0, 1)

        # Assessment Parameters Pill
        pdf.set_y(30)
        pdf.set_fill_color(248, 250, 252)
        pdf.set_draw_color(203, 213, 225)
        pdf.rect(14, 30, 182, 9, 'DF')
        pdf.set_xy(16, 30.5)
        pdf.set_font('Helvetica', 'B', 7.5)
        pdf.set_text_color(71, 85, 105)
        pdf.cell(0, 8, s["params"], 0, 1)

        # Content Sections
        current_y = 42
        pdf.set_y(current_y)
        for sec_title, bullet_list in s["sections"]:
            pdf.set_font('Helvetica', 'B', 9)
            pdf.set_text_color(15, 23, 42)
            pdf.cell(0, 5, sec_title, 0, 1)
            pdf.set_draw_color(14, 165, 233)
            pdf.line(14, pdf.get_y(), 196, pdf.get_y())
            pdf.ln(1.5)

            pdf.set_font('Helvetica', '', 8.2)
            pdf.set_text_color(30, 41, 59)
            for bullet in bullet_list:
                pdf.cell(4, 4.2, chr(149), 0, 0, 'R')
                pdf.multi_cell(178, 4.2, bullet)
                pdf.ln(0.8)
            pdf.ln(2)

        # Speaker Notes Box at bottom
        notes_y = 232
        pdf.set_fill_color(254, 243, 199) # Warm yellow
        pdf.set_draw_color(245, 158, 11)
        pdf.set_line_width(0.4)
        pdf.rect(14, notes_y, 182, 44, 'DF')
        
        pdf.set_xy(18, notes_y + 2.5)
        pdf.set_font('Helvetica', 'B', 8.5)
        pdf.set_text_color(180, 83, 9)
        pdf.cell(0, 4.5, "SPEAKER NOTES & FACULTY EXAMINER TALKING POINTS:", 0, 1)
        
        pdf.set_xy(18, notes_y + 8)
        pdf.set_font('Helvetica', '', 8)
        pdf.set_text_color(69, 26, 3)
        pdf.multi_cell(174, 4.2, s["notes"])

    os.makedirs('docs', exist_ok=True)
    out_path = 'docs/AgentShield_MidSem_Review_Report.pdf'
    pdf.output(out_path)
    print(f"5-Slide Report generated successfully at: {out_path}")

if __name__ == '__main__':
    create_report()
