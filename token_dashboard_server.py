# token_dashboard_server.py
import http.server
import socketserver
import json
import os
import sys
import re
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from datetime import datetime, timezone

sys.stdout.reconfigure(encoding='utf-8')

PORT = 8888
TRACE_FILE = Path("trace_logs.jsonl")
HTML_FILE = Path("token_dashboard.html")

def parse_trace_logs():
    """Reads trace_logs.jsonl and calculates real-time analytics."""
    if not TRACE_FILE.exists():
        return {
            "total_calls": 0,
            "total_input": 0,
            "total_output": 0,
            "total_tokens": 0,
            "avg_duration": 0.0,
            "total_duration": 0.0,
            "agents_map": {},
            "models_map": {},
            "timeline_map": {},
            "logs": [],
            "last_updated": datetime.now(timezone.utc).isoformat()
        }

    total_calls = 0
    total_input = 0
    total_output = 0
    total_tokens = 0
    total_duration = 0.0
    agents_map = {}
    models_map = {}
    timeline_map = {}
    logs = []

    with open(TRACE_FILE, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                data = json.loads(line)
                total_calls += 1
                
                inp = data.get("gen_ai.usage.input_tokens") or 0
                outp = data.get("gen_ai.usage.output_tokens") or 0
                tot = data.get("gen_ai.usage.total_tokens") or (inp + outp)
                dur = float(data.get("duration_seconds") or 0.0)
                
                total_input += inp
                total_output += outp
                total_tokens += tot
                total_duration += dur
                
                agent = data.get("agent_name") or "Unknown Agent"
                if agent not in agents_map:
                    agents_map[agent] = {"tokens": 0, "calls": 0, "input": 0, "output": 0}
                agents_map[agent]["tokens"] += tot
                agents_map[agent]["calls"] += 1
                agents_map[agent]["input"] += inp
                agents_map[agent]["output"] += outp
                
                model = data.get("gen_ai.response.model") or data.get("gen_ai.request.model") or "gemini-3.6-flash"
                models_map[model] = models_map.get(model, 0) + tot
                
                ts_str = data.get("timestamp", "")
                if ts_str:
                    hour_key = ts_str[:13] + ":00"
                    if hour_key not in timeline_map:
                        timeline_map[hour_key] = {"input": 0, "output": 0, "total": 0, "calls": 0}
                    timeline_map[hour_key]["input"] += inp
                    timeline_map[hour_key]["output"] += outp
                    timeline_map[hour_key]["total"] += tot
                    timeline_map[hour_key]["calls"] += 1
                
                logs.append({
                    "timestamp": ts_str,
                    "agent_name": agent,
                    "session_id": data.get("session_id", ""),
                    "lesson_id": data.get("lesson_id", ""),
                    "model": model,
                    "duration_seconds": round(dur, 2),
                    "input_tokens": inp,
                    "output_tokens": outp,
                    "total_tokens": tot,
                    "prompt_summary": (data.get("prompt_summary") or "")[:200],
                    "response_summary": (data.get("response_summary") or "")[:200]
                })
            except Exception:
                continue

    avg_duration = round(total_duration / total_calls, 2) if total_calls > 0 else 0.0

    # Sort timeline keys chronologically
    sorted_timeline = dict(sorted(timeline_map.items()))
    
    # Estimate Cost ($) for Gemini 3.6 Flash / High
    # Approx: Input $0.075 / 1M tokens, Output $0.30 / 1M tokens
    est_cost = (total_input / 1_000_000 * 0.075) + (total_output / 1_000_000 * 0.30)

    return {
        "total_calls": total_calls,
        "total_input": total_input,
        "total_output": total_output,
        "total_tokens": total_tokens,
        "avg_duration": avg_duration,
        "total_duration": round(total_duration, 1),
        "est_cost_usd": round(est_cost, 4),
        "agents_map": agents_map,
        "models_map": models_map,
        "timeline": sorted_timeline,
        "recent_logs": logs[-100:][::-1], # latest 100 logs reverse order
        "last_updated": datetime.now(timezone.utc).isoformat()
    }


class TokenDashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        if path in ["/", "/index.html", "/dashboard"]:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            if HTML_FILE.exists():
                with open(HTML_FILE, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.wfile.write(b"<h1>Dashboard HTML file not found.</h1>")
            return

        if path == "/api/stats":
            stats = parse_trace_logs()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(stats, ensure_ascii=False).encode("utf-8"))
            return

        if path == "/api/logs":
            params = parse_qs(parsed_url.query)
            limit = int(params.get("limit", [50])[0])
            agent_filter = params.get("agent", [""])[0].lower()
            
            stats = parse_trace_logs()
            filtered_logs = stats["recent_logs"]
            if agent_filter:
                filtered_logs = [l for l in filtered_logs if agent_filter in l["agent_name"].lower()]
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(filtered_logs[:limit], ensure_ascii=False).encode("utf-8"))
            return

        # Fallback to static files
        super().do_GET()


def run_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", PORT), TokenDashboardHandler) as httpd:
        print(f"=========================================================")
        print(f"🟢 REALTIME TOKEN DASHBOARD SERVER STARTED AT:")
        print(f"   http://127.0.0.1:{PORT}")
        print(f"   Reading live trace data from: {TRACE_FILE.resolve()}")
        print(f"=========================================================")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
