from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 14)
        self.cell(0, 10, 'AgentShield: FF 180 Major Project Synopsis', border=False, new_x="LMARGIN", new_y="NEXT", align='C')
        self.ln(5)

    def section_title(self, title):
        self.set_font('helvetica', 'B', 12)
        self.set_fill_color(220, 230, 250)
        self.cell(0, 8, title, border=False, new_x="LMARGIN", new_y="NEXT", fill=True)
        self.ln(2)
        
    def sub_title(self, title):
        self.set_font('helvetica', 'B', 10)
        self.cell(0, 6, title, border=False, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body_text(self, body):
        self.set_font('helvetica', '', 10)
        self.multi_cell(0, 5, body)
        self.ln(4)
        
    def bullet(self, text):
        self.set_font('helvetica', '', 10)
        self.multi_cell(0, 5, f"- {text}")
        self.ln(1)

pdf = PDF()
pdf.add_page()

# 1. Environment
pdf.section_title('1. Environment')
pdf.body_text("AgentShield considers environmental sustainability by directly reducing wasteful GPU and cloud computing overhead caused by autonomous AI agents. When AI agents fail a task, they frequently enter 'hallucination loops,' continuously firing redundant API calls to external tools.")
pdf.body_text("AgentShield implements a sliding-window rate limiter and quarantine protocol that detects and halts these runaway loops, significantly reducing API traffic, GPU token generation, and cloud energy consumption. Furthermore, AgentShield uses a deterministic, rule-based security engine rather than a heavy Machine Learning model, resulting in an ultra-low carbon footprint.")
pdf.sub_title("Environmental Impact & Compute Optimization Example:")
pdf.bullet("API Calls: 100+ calls/min (Without Proxy) vs Capped at 10 calls/5sec (With AgentShield)")
pdf.bullet("Token Waste: ~50,000+ wasted tokens/min vs Cut off instantly (Zero waste)")
pdf.bullet("Security Compute: Heavy LLM API calls vs Local Regex/Heuristics (Sub-2ms)")
pdf.bullet("Memory Usage: Heavy vs < 50 MB RAM")
pdf.ln(4)

# 2. Sustainability
pdf.section_title('2. Sustainability')
pdf.body_text("Sustainability addresses both technical and operational longevity. AgentShield is designed as a modular, protocol-agnostic system that supports long-term technical sustainability. Because it strictly adheres to the official JSON-RPC 2.0 standard for the Model Context Protocol (MCP), it guarantees compatibility with future AI models and enterprise tools without requiring codebase rewrites.")
pdf.sub_title("AgentShield Project-Specific Considerations:")
pdf.bullet("Modular: Separated logically into Gateway, Risk Engine, Sanitizer, and HITL Manager.")
pdf.bullet("Extensible: New attack vectors and PII patterns can be added by simply appending new Regex rules without touching core routing logic.")
pdf.bullet("Vendor-Agnostic: Compatible with any future AI client (e.g., Claude, GPT) or MCP server.")
pdf.sub_title("Example of Extensibility:")
pdf.body_text("The PII Sanitizer currently redacts: Aadhaar -> PAN -> AWS API Keys.\nLater, new compliance requirements can be added: Credit Cards -> Health Records -> Internal IP Addresses simply by updating src/sanitizer/patterns.py.")
pdf.ln(4)

# 3. Safety and Security
pdf.section_title('3. Safety and Security')
pdf.body_text("AgentShield is fundamentally a cybersecurity project. It ensures the safety of enterprise infrastructure by providing multi-tiered runtime guardrails between unpredictable AI agents and sensitive corporate tools.")
pdf.sub_title("AgentShield Project-Specific Safety Considerations:")
pdf.bullet("Prompt Injection Defense: Blocks malicious jailbreaks (e.g., <system_override>, DAN modes) before they reach the execution environment.")
pdf.bullet("Destructive Action Prevention: Uses dynamic wildcards to flag dangerous tools (e.g., containing 'delete', 'drop', 'execute').")
pdf.bullet("Human-in-the-Loop (HITL): Pauses high-risk commands in server memory and waits for explicit human administrator approval via the dashboard.")
pdf.bullet("Fail-Closed Architecture: If an administrator does not approve a HITL request within 60 seconds, the request is automatically destroyed.")
pdf.sub_title("Example:")
pdf.body_text("If an AI agent attempts to call the 'github_delete_repo' tool, AgentShield does not automatically reject or accept it. Instead, it assigns a HIGH RISK score, holds the JSON payload asynchronously, and pushes an alert to the Admin Dashboard for manual verification.")
pdf.ln(4)

pdf.add_page()
# 4. Ethical Considerations
pdf.section_title('4. Ethical Considerations')
pdf.body_text("AgentShield inherently enforces Ethical AI practices by guaranteeing data privacy, system transparency, and human oversight. Because MCP allows AI to read local enterprise files and databases, there is a massive risk of sensitive corporate data being sent to external LLM providers.")
pdf.sub_title("Important Ethical Considerations Addressed:")
pdf.bullet("Data Privacy (DLP): The Outbound PII Sanitizer recursively scrubs returning payloads, replacing sensitive personal information with '[REDACTED]' before it is transmitted back to the AI.")
pdf.bullet("Accountability & Transparency: Every single intercepted request, risk score, and action is logged asynchronously to agentshield_audit.db. If an AI makes a mistake, there is a perfect, tamper-proof audit trail.")
pdf.bullet("Human Agency: By implementing HITL, AgentShield ensures that AI cannot take autonomous, destructive actions without human consent, aligning with global Responsible AI guidelines.")
pdf.ln(4)

# 5. Cost and Economic Feasibility
pdf.section_title('5. Cost and Economic Feasibility')
pdf.body_text("The economic feasibility of AgentShield is exceptionally high. It is built entirely on open-source technologies, incurring zero commercial licensing fees, and its deterministic risk engine runs locally, eliminating the need to pay for external LLM API calls for security checks.")
pdf.body_text("Potential Economic Benefits: The system prevents catastrophic financial losses associated with AI-driven data breaches, accidental database deletions, and runaway API token costs.")
pdf.sub_title("Cost Assessment (Without AgentShield vs. With AgentShield):")
pdf.bullet("Security Licensing: Expensive API gateways vs Rs. 0 (100% Open Source)")
pdf.bullet("AI Token Waste: High (Prone to infinite loops) vs Negligible (Quarantines rogue agents)")
pdf.bullet("Data Breach Risk: High (Raw data sent to LLM providers) vs Low (Automated PII Redaction)")
pdf.bullet("Incident Auditing: Manual log parsing vs Automated SQLite JSONB tracking")
pdf.bullet("Infrastructure Req.: High (if using ML) vs Minimal (<50MB RAM, sub-2ms latency)")
pdf.ln(4)

# 6. SDG Project Mapping
pdf.section_title('6. SDG Project Mapping')
pdf.sub_title("Goal 9: Industry, Innovation, and Infrastructure")
pdf.body_text("Explanation: By building a resilient, low-latency security proxy, AgentShield allows enterprises to safely adopt cutting-edge AI technologies without risking their existing infrastructure. It fosters innovation by removing the security roadblocks associated with autonomous AI deployment.")
pdf.sub_title("Goal 16: Peace, Justice, and Strong Institutions")
pdf.body_text("Explanation: AgentShield enforces accountability and transparency in AI systems. Through its exhaustive audit logging and Human-in-the-Loop approval gates, it ensures that corporate institutions maintain strong, governed oversight over how AI interacts with their private data, promoting digital trust.")

pdf.output("docs/midsem_materials/AgentShield_FF180_Synopsis.pdf")
print("PDF Generated successfully.")
