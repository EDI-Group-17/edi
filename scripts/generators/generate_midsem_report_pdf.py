import os
from fpdf import FPDF

class MidSemReportPDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(100, 116, 139)
        self.cell(0, 8, 'AgentShield - Mid-Semester Project Presentation Dossier | VIT Pune (AY 2026-27)', 0, 0, 'L')
        self.cell(0, 8, f'Page {self.page_no()}', 0, 1, 'R')
        self.set_draw_color(226, 232, 240)
        self.line(12, 18, 198, 18)
        self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(148, 163, 184)
        self.cell(0, 10, 'Department of Computer Engineering | Group TYG19 | Guide: Prof. Sanyukta Deshmukh', 0, 0, 'C')

def create_report():
    pdf = MidSemReportPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(14, 14, 14)

    # ------------------ COVER PAGE ------------------
    pdf.add_page()
    pdf.ln(10)
    pdf.set_fill_color(15, 23, 42) # Dark Navy
    pdf.rect(14, 15, 182, 45, 'F')

    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 20)
    pdf.set_y(22)
    pdf.cell(0, 10, 'AgentShield: Mid-Sem Review Dossier', 0, 1, 'C')
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(148, 163, 184)
    pdf.cell(0, 7, 'Slide-by-Slide Presentation Guide, Research Backing & Evaluation Data', 0, 1, 'C')
    pdf.cell(0, 6, 'Aligned with VIT FF No. 180 Progress Review 1 Parameters', 0, 1, 'C')

    pdf.set_y(68)
    pdf.set_text_color(30, 41, 59)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 7, 'ACADEMIC & INSTITUTIONAL PROFILE', 0, 1, 'L')
    pdf.set_draw_color(14, 165, 233)
    pdf.set_line_width(0.5)
    pdf.line(14, 76, 196, 76)
    pdf.ln(4)

    pdf.set_font('Helvetica', '', 10)
    info_data = [
        ("Institution", "Vishwakarma Institute of Technology (VIT), Pune"),
        ("Department", "Department of Computer Engineering"),
        ("Academic Year", "2026-2027 | Semester: 5 | Group No.: TYG19"),
        ("Project Title", "AgentShield: A Dynamic Risk-Aware Security Framework for the Model Context Protocol"),
        ("Project Area", "Artificial Intelligence & Cybersecurity"),
        ("Faculty Guide", "Prof. Sanyukta Deshmukh (Contact: 9021907414, Sanyukta.deshmukh@vit.edu)"),
        ("Form Reference", "Issue 01 : Rev No. 00 : Dt. 05/02/26 (FF No. 180)"),
        ("Project Status", "100% of Epics 1-7 Implemented | 57/57 PyTest Unit & Integration Tests Passed")
    ]
    for k, v in info_data:
        pdf.set_font('Helvetica', 'B', 9)
        pdf.set_text_color(51, 65, 85)
        pdf.cell(38, 6, f"{k}:", 0, 0)
        pdf.set_font('Helvetica', '', 9)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(0, 6, v, 0, 1)

    pdf.ln(4)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 7, 'GROUP MEMBER ALLOCATION & ROLES', 0, 1, 'L')
    pdf.line(14, 137, 196, 137)
    pdf.ln(4)

    members = [
        ("1", "Harsh Manjramkar", "TY-G", "70", "12414557", "harsh.manjramkar24@vit.edu", "Lead Architect & Security Gateway Core"),
        ("2", "Vedant Gaidhani", "TY-G", "74", "12415020", "vedant.gaidhani242@vit.edu", "Dynamic Risk Engine & Heuristic Detectors"),
        ("3", "Vineet Wagh", "TY-G", "75", "12415021", "vineet.wagh241@vit.edu", "PII Redaction Engine & Rate Limit Quarantine"),
        ("4", "Arjun Joshi", "TY-G", "76", "12415022", "arjun.joshi241@vit.edu", "Async Audit Logging & Real-time Web Dashboard")
    ]

    pdf.set_fill_color(241, 245, 249)
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(10, 6, "Sr", 1, 0, 'C', True)
    pdf.cell(38, 6, "Name", 1, 0, 'L', True)
    pdf.cell(12, 6, "Div/Roll", 1, 0, 'C', True)
    pdf.cell(20, 6, "G.R. No.", 1, 0, 'C', True)
    pdf.cell(48, 6, "Email ID", 1, 0, 'L', True)
    pdf.cell(54, 6, "Key Technical Responsibility", 1, 1, 'L', True)

    pdf.set_font('Helvetica', '', 8)
    for sr, name, div, roll, gr, email, role in members:
        pdf.cell(10, 6, sr, 1, 0, 'C')
        pdf.cell(38, 6, name, 1, 0, 'L')
        pdf.cell(12, 6, f"{div}/{roll}", 1, 0, 'C')
        pdf.cell(20, 6, gr, 1, 0, 'C')
        pdf.cell(48, 6, email, 1, 0, 'L')
        pdf.cell(54, 6, role, 1, 1, 'L')

    pdf.ln(6)
    pdf.set_fill_color(238, 242, 255)
    pdf.set_draw_color(99, 102, 241)
    pdf.rect(14, 185, 182, 36, 'DF')
    pdf.set_xy(18, 188)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(49, 46, 129)
    pdf.cell(0, 6, 'MID-SEMESTER REVIEW EVALUATION CRITERIA (FF NO. 180)', 0, 1)
    pdf.set_font('Helvetica', '', 8.5)
    pdf.set_text_color(30, 41, 59)
    pdf.multi_cell(174, 4.5, 
        "- Completeness of Literature Survey & Identification of Novel Research Gaps.\n"
        "- Clarity of Problem Formulation & Theoretical Soundness of System Architecture.\n"
        "- Quality of Implementation, Real-time Interception, & Tool Verification.\n"
        "- Demonstration of Working Prototypes: Injection Interception, HITL, PII Redaction, Auditing.\n"
        "- Team Work Distribution & Technical Mastery across all functional modules."
    )

    # ------------------ SLIDE BY SLIDE DOSSIER ------------------
    slides = [
        {
            "num": "Slide 1",
            "title": "Title & Project Identification",
            "intent": "Professional formal introduction establishing identity, university credentials, and guide.",
            "points": [
                "Project Title: AgentShield: A Dynamic Risk-Aware Security Framework for the Model Context Protocol",
                "Project Area: Artificial Intelligence and Cybersecurity (Enterprise Governance)",
                "Group Details: Group TYG19 | Computer Engineering | AY 2026-27 | Semester 5",
                "Team Members: Harsh Manjramkar (70), Vedant Gaidhani (74), Vineet Wagh (75), Arjun Joshi (76)",
                "Internal Faculty Guide: Prof. Sanyukta Deshmukh (Department of Computer Engineering, VIT Pune)"
            ],
            "notes": "Good morning respected guide Prof. Sanyukta Deshmukh and evaluation committee. Today our team TYG19 presents the mid-semester progress review for our capstone research project, AgentShield."
        },
        {
            "num": "Slide 2",
            "title": "Introduction & Industrial Motivation",
            "intent": "Explain the explosive growth of AI Agents and why the Model Context Protocol requires runtime protection.",
            "points": [
                "The MCP Revolution: Anthropic's open Model Context Protocol has emerged as the universal standard connecting LLM agents (Claude, Cursor, OpenAI) to enterprise databases, internal APIs, and filesystem tools.",
                "The Core Security Vulnerability: By default, MCP provides open point-to-point connections with direct execution rights. AI agents act autonomously with high privileges.",
                "The Enterprise Risk: AI hallucinations, prompt injection attacks, or compromised tool arguments can lead to catastrophic data drops, unauthorized privilege escalation, or credentials theft.",
                "Why Perimeter Security Fails: Traditional WAFs and API gateways do not inspect semantic JSON-RPC payloads, nor can they detect LLM jailbreaks or control AI tool permissions dynamically."
            ],
            "notes": "Highlight that while MCP standardizes tool connectivity, it inherently trusts the agent. When an LLM hallucinates or gets manipulated by a prompt injection, there is no firewall between the model and the database."
        },
        {
            "num": "Slide 3",
            "title": "Problem Statement & Real-World Threat Vectors",
            "intent": "Formal problem definition as committed in FF No. 180 Section 3.",
            "points": [
                "Formal Problem Statement: Direct integration of autonomous AI agents with critical enterprise infrastructure lacks runtime interception, dynamic risk evaluation, human supervision, and response sanitization.",
                "Threat Vector 1 (Prompt Injection & Jailbreaks): Malicious users inject hidden system overrides (<system_override>) forcing the LLM to call privileged tools like delete_repo or execute_sql.",
                "Threat Vector 2 (Accidental Destruction): Agents hallucinating recursive file writes or issuing unconstrained DROP TABLE / rm -rf commands without human review.",
                "Threat Vector 3 (Confidential Data Exfiltration): Target servers returning raw records containing AWS keys, PAN cards, or Aadhaar numbers directly into the LLM context window.",
                "Threat Vector 4 (Execution Loops / DoS): Infinite recursive tool calls exhausting enterprise API limits and compute resources."
            ],
            "notes": "Frame the problem clearly: We need a centralized, transparent proxy that acts like an intelligent security guard stationed between the AI agent and the enterprise tools."
        },
        {
            "num": "Slide 4",
            "title": "Literature Review & Prior Art Analysis",
            "intent": "Directly cite the 5 papers analyzed in FF No. 180 Section 2.",
            "points": [
                "Paper 1: MCPShield - Dynamic Trust Evaluation for MCP Servers (2026): Analyzes historical server metadata; Limitation: Static pre-handshake evaluation only, no runtime request inspection or enforcement.",
                "Paper 2: MCPSec - Secure Communication Framework for MCP (2026): Protocol-level encryption and message integrity; Limitation: Secures channel transport but cannot evaluate semantic agent actions or tool arguments.",
                "Paper 3: ShieldMCP - Runtime Security Proxy for MCP (2026): Basic proxy interceptor; Limitation: Lacks dynamic contextual risk scoring, response-side PII sanitization, and centralized audit management.",
                "Paper 4: Enterprise Security Framework for MCP (2025): Architectural guidelines; Limitation: Purely conceptual recommendations without working runtime implementations.",
                "Paper 5: Security Threats and Attack Analysis for AI Agents (2026): Comprehensive taxonomy of agent risks; Limitation: Focuses on attack discovery rather than active runtime mitigation."
            ],
            "notes": "Show the committee that we thoroughly studied state-of-the-art literature published in 2025-2026. Every existing paper either focuses only on the transport protocol or on static server trust, leaving a critical runtime gap."
        },
        {
            "num": "Slide 5",
            "title": "Identified Research Gaps & Novelty",
            "intent": "Articulate why AgentShield is a novel academic and practical contribution.",
            "points": [
                "Gap 1: Detection vs. Prevention: Prior work identifies attacks post-mortem; AgentShield actively intercepts and blocks attacks before execution.",
                "Gap 2: Static Rules vs. Dynamic Contextual Risk: AgentShield evaluates method, tool sensitivity, argument payloads, and agent history simultaneously.",
                "Gap 3: Complete Absence of Human-in-the-Loop (HITL): High-impact destructive tools (e.g., github_delete_repo) execute unchecked in existing systems without admin oversight.",
                "Gap 4: Lack of Response-Side PII Cleansing: Data leaking from enterprise databases into LLM context windows is never redacted by traditional proxies.",
                "Gap 5: Zero-Modification Integration: AgentShield requires zero code changes on either the AI Agent client or the target MCP server."
            ],
            "notes": "Emphasize our novelty: Dynamic multi-tier risk evaluation coupled with synchronous HITL pauses and recursive response PII redaction."
        },
        {
            "num": "Slide 6",
            "title": "Project Objectives & Scope of Work",
            "intent": "Reiterate specific, measurable objectives from FF No. 180 Section 4.",
            "points": [
                "Objective 1: Develop an asynchronous, high-throughput JSON-RPC 2.0 interceptor proxy (/mcp/v1/proxy).",
                "Objective 2: Implement a Dynamic Risk Assessment Engine categorizing requests into LOW, MEDIUM, and HIGH risk.",
                "Objective 3: Build heuristic detectors for prompt injection, DAN jailbreaks, SQLi, and dangerous system commands (sudo, chmod, /etc/).",
                "Objective 4: Provide real-time Human-in-the-Loop (HITL) approval with fail-closed 60-second timeouts.",
                "Objective 5: Design a recursive multi-level PII Sanitization Engine masking API keys, Aadhaar numbers, and credit cards.",
                "Objective 6: Implement sliding-window rate limiting (60 req/min) and hallucination loop quarantine detection.",
                "Objective 7: Maintain an asynchronous batched PostgreSQL/SQLite audit log with SHA-256 payload hashing.",
                "Objective 8: Create a real-time Glassmorphism Web Dashboard with live WebSockets for admin control."
            ],
            "notes": "Walk the faculty through the 8 core objectives. Confirm that every single one of these has already been designed, coded, and tested."
        },
        {
            "num": "Slide 7",
            "title": "System Architecture & Engineering Flowchart",
            "intent": "Explain the architectural pipeline and component interactions as committed in FF No. 180 Section 5.",
            "points": [
                "Component 1: Inbound Request Interceptor (FastAPI ASGI) parsing JSON-RPC 2.0 frames.",
                "Component 2: Multi-Factor Risk Assessment Engine (Detectors + Argument Heuristics).",
                "Component 3: Decision Gate: LOW risk -> Forward; HIGH risk injection -> Immediate Block (-32002); Sensitive Tool -> HITL Pause (-32001).",
                "Component 4: Rate Limiter & Loop Quarantine: Sliding window counter + quarantine state table.",
                "Component 5: Outbound Forwarder: Non-blocking HTTPX client forwarding to target MCP server.",
                "Component 6: Response Transformer: Deep-nested JSON traversal sanitizing PII.",
                "Component 7: Background Audit Writer: Asynchronous Queue buffering logs without degrading request latency.",
                "Component 8: Real-Time WebSockets Dashboard: Live streaming metrics, pending HITL queues, and quarantine toggles."
            ],
            "notes": "Direct the audience to the architectural diagram from our synopsis. Highlight that AgentShield operates completely asynchronously using non-blocking Python asyncio."
        },
        {
            "num": "Slide 8",
            "title": "Proposed Technology Stack & Justification",
            "intent": "Defend the technology choices made during development.",
            "points": [
                "Backend Framework: Python FastAPI & Starlette - Delivers native asynchronous ASGI performance capable of handling thousands of concurrent JSON-RPC requests.",
                "Communication Protocol: JSON-RPC 2.0 over HTTP & WebSockets (/ws/traffic) - 100% compliant with Anthropic's Model Context Protocol specification.",
                "Database & ORM: PostgreSQL & SQLite via Async SQLAlchemy - Provides ACID-compliant immutable audit logs with JSONB payload storage.",
                "Caching & Rate Limiting: Sliding window memory state machine with Redis compatibility - Enforces granular per-agent throttling.",
                "Security Detectors: Pre-compiled regex automata & heuristic analyzers - Sub-millisecond inspection latency (<2ms).",
                "Admin Frontend: Single-Page Cyberpunk Glassmorphism UI - Native WebSockets, zero heavy build dependencies, instant live reload."
            ],
            "notes": "Justify why FastAPI was chosen over Flask: Async support was mandatory to prevent proxy bottlenecks during long-running tool executions and HITL holds."
        },
        {
            "num": "Slide 9",
            "title": "Mid-Sem Implementation Milestones Accomplished",
            "intent": "Demonstrate that 100% of planned user stories and epics are fully completed.",
            "points": [
                "Epic 1 (Proxy Foundation): Async router, target forwarder, standard JSON-RPC error builders completed.",
                "Epic 2 (Risk & Injection): 3-tier risk engine, DAN prompt, SQLi, subshell, and system directory heuristics implemented.",
                "Epic 3 (Rate Limiting & Quarantine): Sliding-window limiter and rapid-fire loop isolation engine built.",
                "Epic 4 (Human-in-the-Loop): Event-driven approval manager with async pub-sub and 60s fail-closed timeout operational.",
                "Epic 5 (Response PII Sanitizer): Recursive deep-nested dictionary/list sanitizer protecting AWS, OpenAI, PAN, and Aadhaar data.",
                "Epic 6 (Audit Persistence): Asynchronous Queue batch database persistence running in background tasks.",
                "Epic 7 (Admin Dashboard & API): Live WebSocket traffic monitoring, HITL interactive buttons, and quarantine release REST endpoints live."
            ],
            "notes": "State with confidence: As of this mid-semester review, all 7 epics and 15 user stories are completely implemented and operational in code."
        },
        {
            "num": "Slide 10",
            "title": "Comprehensive Testing & Verification Matrix",
            "intent": "Present rigorous test metrics proving industrial quality.",
            "points": [
                "Total Test Suite Size: 57 Automated Unit & Integration Tests.",
                "Test Pass Rate: 100% (57 Passed, 0 Failed, 0 Skipped).",
                "Execution Performance: Entire 57-test suite executes in ~0.89 seconds locally (or ~60s across simulated multi-transport integration).",
                "Coverage Breakdown: 13 Unit Test modules (Detectors, Evaluator, PII, HITL, Limiter) + 7 Integration Test modules (Proxy, Audit, WebSockets).",
                "Adversarial Code Review Audit: Conducted 4-layer adversarial review; patched DOM XSS escaping, shell pipeline regexes, serialization fallbacks, and memory caps."
            ],
            "notes": "Point out the 57 passing tests. This proves to the faculty that AgentShield is not just a theoretical concept or mockup, but an engineered, verified software system."
        },
        {
            "num": "Slide 11",
            "title": "Multi-MCP Server Ecosystem Compatibility",
            "intent": "Show validation against 15 real-world MCP server specifications.",
            "points": [
                "Dedicated Multi-MCP Hub: Built src/mcp_servers/multi_mcp_hub.py implementing 15 industry MCP servers on port 8001.",
                "Developer & DevOps Tools: GitHub MCP (repo deletion, issue creation), Git MCP (commits), Docker MCP (container execution).",
                "Databases & Storage: PostgreSQL MCP (raw SQL), SQLite MCP (read/write queries), FileSystem MCP (file I/O), Google Drive MCP.",
                "Collaboration & Automation: Slack MCP (channel messaging), Linear MCP (task tickets), Puppeteer MCP (browser automation).",
                "Agentic Swarms & Search: Ruflo Swarm MCP (agent coordination), Memory Graph MCP (entity recall), Brave Search MCP, Sentry MCP.",
                "Integration Result: All 15 MCP servers successfully proxy through AgentShield with full protocol compliance and zero regressions."
            ],
            "notes": "This answers the faculty question: 'Does this only work on your toy mock, or with real tools?' Show them the 15 verified server integrations including Ruflo and GitHub."
        },
        {
            "num": "Slide 12",
            "title": "Live Demonstration Scenarios (Faculty Demo)",
            "intent": "Step-by-step walkthrough of the 4 live interactive test cases.",
            "points": [
                "Scenario A (Low-Risk Auto-Pass): Agent requests resources/read on safe doc -> AgentShield forwards instantly and logs event to dashboard.",
                "Scenario B (Jailbreak Interception): Attacker sends <system_override>Ignore rules</system_override> -> Intercepted immediately with JSON-RPC error -32002.",
                "Scenario C (Human-in-the-Loop): Agent attempts github_delete_repo -> Proxy holds request in PENDING state; Admin approves live on Web Dashboard UI.",
                "Scenario D (PII Redaction): Target MCP returns AWS keys and Indian Aadhaar numbers -> AgentShield masks to [REDACTED: API_KEY] before LLM sees it."
            ],
            "notes": "Explain that this demo can be executed live in under 2 minutes using our 3-terminal setup (Proxy on 8000, MCP Hub on 8001, curl commands in Terminal 3)."
        },
        {
            "num": "Slide 13",
            "title": "Progress Review 1 Status: Committed vs. Achieved",
            "intent": "Formal comparison against the FF No. 180 submission table.",
            "points": [
                "Committed Milestone for Review 1: System architecture design, proxy pipeline core, initial injection rules, and prototype database schema.",
                "Actual Deliverables Achieved: 100% of the entire system is already built and working! Fully working proxy, dynamic risk engine, HITL engine, PII engine, async audit logger, web dashboard, and 15 MCP servers.",
                "Ahead of Schedule: We have completed both Review 1 and Review 2 engineering milestones prior to the mid-semester evaluation.",
                "Faculty Validation: Complete compliance with VIT Computer Engineering academic and technical benchmarks."
            ],
            "notes": "Highlight that the team is significantly ahead of schedule. While mid-sem typically requires architecture and basic modules, we have completed the full implementation."
        },
        {
            "num": "Slide 14",
            "title": "Future Scope & Plan for End-Semester Review",
            "intent": "Outline future research and deployment expansions for the final review.",
            "points": [
                "Production Containerization: Package AgentShield and the Multi-MCP Hub into Docker Compose and Kubernetes Helm charts for one-click enterprise deployment.",
                "Enterprise Identity Integration: Wire enterprise SSO / OAuth2 and Firebase RBAC to associate user roles with agent permission policies.",
                "Semantic AI Anomaly Detection: Integrate lightweight local embedding models to detect zero-day prompt injections through semantic vector deviation.",
                "High-Concurrency Performance Benchmarking: Conduct Locust / k6 load testing to measure latency overhead under 10,000 requests per second."
            ],
            "notes": "Close the technical section by demonstrating vision for the final semester: containerization, enterprise SSO, and high-load stress testing."
        },
        {
            "num": "Slide 15",
            "title": "Conclusion, References & Open Q&A",
            "intent": "Summarize key contributions, acknowledge guide, and invite questions.",
            "points": [
                "Summary: AgentShield establishes a robust, non-intrusive runtime security layer for autonomous AI agents operating in enterprise MCP environments.",
                "Key Achievements: Dynamic 3-tier risk evaluation, jailbreak defense, human oversight, confidential PII protection, and immutable auditability.",
                "Literature References: MCPShield (2026), MCPSec (2026), ShieldMCP (2026), Anthropic Model Context Protocol Specification.",
                "Acknowledgment: Sincere gratitude to our faculty guide, Prof. Sanyukta Deshmukh, and the Department of Computer Engineering.",
                "Open for Discussion: Respected committee members, we are now ready for questions and live demonstration."
            ],
            "notes": "Thank the guide and committee. Stand ready to demonstrate the live curl scenarios or answer technical questions on algorithms and code."
        }
    ]

    for s in slides:
        pdf.add_page()
        pdf.set_fill_color(15, 23, 42)
        pdf.rect(14, 15, 182, 14, 'F')
        pdf.set_xy(16, 17)
        pdf.set_font('Helvetica', 'B', 12)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(30, 10, s["num"] + ":", 0, 0)
        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_text_color(56, 189, 248)
        pdf.cell(0, 10, s["title"], 0, 1)

        pdf.set_y(33)
        pdf.set_fill_color(248, 250, 252)
        pdf.set_draw_color(203, 213, 225)
        pdf.rect(14, 32, 182, 12, 'DF')
        pdf.set_xy(16, 33)
        pdf.set_font('Helvetica', 'B', 8.5)
        pdf.set_text_color(71, 85, 105)
        pdf.cell(24, 10, "Slide Purpose:", 0, 0)
        pdf.set_font('Helvetica', 'I', 8.5)
        pdf.set_text_color(30, 41, 59)
        pdf.cell(0, 10, s["intent"], 0, 1)

        pdf.set_y(48)
        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(0, 6, "Key Content / Presentation Bullet Points:", 0, 1)
        pdf.line(14, 55, 196, 55)
        pdf.ln(3)

        pdf.set_font('Helvetica', '', 9)
        pdf.set_text_color(30, 41, 59)
        for pt in s["points"]:
            pdf.cell(4, 5, chr(149), 0, 0, 'R')
            pdf.multi_cell(178, 5, pt)
            pdf.ln(1.5)

        pdf.ln(4)
        pdf.set_fill_color(254, 243, 199) # Warm yellow
        pdf.set_draw_color(245, 158, 11)
        pdf.set_line_width(0.4)
        pdf.rect(14, pdf.get_y(), 182, 34, 'DF')
        
        box_y = pdf.get_y() + 2
        pdf.set_xy(18, box_y)
        pdf.set_font('Helvetica', 'B', 9)
        pdf.set_text_color(180, 83, 9)
        pdf.cell(0, 5, "SPEAKER NOTES & FACULTY EXAMINER TALKING POINTS:", 0, 1)
        
        pdf.set_xy(18, box_y + 6)
        pdf.set_font('Helvetica', '', 8.5)
        pdf.set_text_color(69, 26, 3)
        pdf.multi_cell(174, 4.5, s["notes"])

    os.makedirs('docs', exist_ok=True)
    out_path = 'docs/AgentShield_MidSem_Review_Report.pdf'
    pdf.output(out_path)
    print(f"Report generated successfully at: {out_path}")

if __name__ == '__main__':
    create_report()
