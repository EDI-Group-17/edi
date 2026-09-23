from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 15)
        self.cell(0, 10, 'AgentShield: Knowledge Transfer & Glossary', border=False, new_x="LMARGIN", new_y="NEXT", align='C')
        self.set_font('helvetica', 'I', 10)
        self.cell(0, 6, 'Internal Team Study Guide for Mid-Sem Review', border=False, new_x="LMARGIN", new_y="NEXT", align='C')
        self.ln(5)

    def term(self, word, definition):
        self.set_font('helvetica', 'B', 11)
        self.set_text_color(20, 40, 120)
        self.cell(0, 8, f"{word}:", new_x="LMARGIN", new_y="NEXT")
        
        self.set_font('helvetica', '', 10)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 6, definition)
        self.ln(4)

pdf = PDF()
pdf.add_page()

pdf.set_font('helvetica', 'B', 12)
pdf.set_fill_color(200, 220, 255)
pdf.cell(0, 8, '1. Core Architecture Concepts', border=False, new_x="LMARGIN", new_y="NEXT", fill=True)
pdf.ln(4)

pdf.term("Model Context Protocol (MCP)", "An open standard created by Anthropic that allows AI models (like Claude) to securely connect to external tools, databases, and APIs. Think of it as a universal plug that gives AI hands to interact with local enterprise systems.")
pdf.term("JSON-RPC 2.0", "A Remote Procedure Call protocol encoded in JSON. It is the language that the AI and the MCP server use to talk to each other. It contains a 'method' (what to do) and 'params' (the arguments).")
pdf.term("Transparent Proxy", "A server that sits in the middle of a connection without modifying the sender or receiver. In our project, the AI thinks it's talking to the target server, and the target server thinks it's talking to the AI. Neither knows AgentShield is secretly in the middle inspecting the traffic.")
pdf.term("Asynchronous (Async/Await) & FastAPI", "Modern Python frameworks (like FastAPI) use 'async' to avoid freezing. When our proxy pauses a request to wait for human approval, it doesn't freeze the whole server. It efficiently puts that single request to sleep while continuing to serve other AI requests.")

pdf.set_font('helvetica', 'B', 12)
pdf.set_fill_color(200, 220, 255)
pdf.cell(0, 8, '2. Inbound Security (The Risk Engine)', border=False, new_x="LMARGIN", new_y="NEXT", fill=True)
pdf.ln(4)

pdf.term("Prompt Injection / DAN Jailbreak", "A cyberattack where a user tricks the AI by injecting malicious instructions (e.g., 'Ignore all previous rules' or 'Do Anything Now (DAN)'). Our proxy scans for these and blocks them before they reach the enterprise system.")
pdf.term("SQLi (SQL Injection)", "An attack where malicious SQL statements are inserted into an input field (e.g., 'DROP TABLE users'). Our proxy detects these in the tool arguments.")
pdf.term("Regex (Regular Expressions)", "A sequence of characters that specifies a search pattern. We use Regex to look for exact malicious shapes (like '<system_override>') in the AI's payload.")
pdf.term("Heuristics (Wildcards)", "Instead of looking for exact strings, heuristics use logic/rules of thumb. For example, instead of blocking the exact tool 'github_delete_repo', our heuristic engine flags ANY tool containing the wildcard word 'delete', 'drop', or 'remove'.")
pdf.term("Human-in-the-Loop (HITL)", "A security mechanism where an automated process pauses a high-risk action (like deleting a database) and holds it in memory until a human administrator clicks 'Approve' or 'Deny'.")

pdf.add_page()
pdf.set_font('helvetica', 'B', 12)
pdf.set_fill_color(200, 220, 255)
pdf.cell(0, 8, '3. Outbound Security (The Sanitizer)', border=False, new_x="LMARGIN", new_y="NEXT", fill=True)
pdf.ln(4)

pdf.term("PII (Personally Identifiable Information)", "Highly sensitive user data that can identify a specific person or compromise security (e.g., Aadhaar Numbers, PAN Cards, AWS API Keys, Passwords).")
pdf.term("Recursive JSON Sanitization", "When the MCP server returns a response, it might be deeply nested (a dictionary inside a list inside a dictionary). Our 'recursive' algorithm crawls down into every single layer of the JSON to ensure no PII is hiding anywhere, replacing it with '[REDACTED]'.")
pdf.term("Data Exfiltration", "The unauthorized transfer or theft of data. By scrubbing PII, we prevent a hacked AI from exfiltrating sensitive enterprise data back to the attacker.")

pdf.set_font('helvetica', 'B', 12)
pdf.set_fill_color(200, 220, 255)
pdf.cell(0, 8, '4. Testing & QA Terminologies', border=False, new_x="LMARGIN", new_y="NEXT", fill=True)
pdf.ln(4)

pdf.term("PyTest", "A robust Python testing framework used to write and run automated test code.")
pdf.term("Integration Testing", "Testing the entire system working together (e.g., the AI, the Proxy, and the Target MCP). This proves that our proxy doesn't accidentally break or corrupt the JSON-RPC traffic when it forwards it.")
pdf.term("Enterprise Schema Mocking", "We created fake (mock) versions of 15 real-world corporate MCP servers (like GitHub or PostgreSQL). We tested our proxy against these fake servers to scientifically prove it works on real-world enterprise data structures.")

pdf.output("Knowledge_Transfer.pdf")
print("Knowledge_Transfer.pdf Generated successfully.")
