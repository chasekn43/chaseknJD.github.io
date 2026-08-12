import os
import sys
import json
import subprocess
from datetime import datetime

# Script directory
script_dir = r"c:\Users\Charwiz43\\.gemini\antigravity\scratch\Affirm\regulatory-archive-2026"
artifact_dir = r"C:\Users\Charwiz43\.gemini\antigravity\brain\4a7c38ce-5405-4d8c-aa94-238ed4b5146d"
report_filename = "rank_progress_report.md"

def run_sweep():
    print("Running verification sweep...")
    try:
        # Run run_verification_batch.py
        result = subprocess.run(
            [sys.executable, "run_verification_batch.py"],
            cwd=script_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("Sweep complete. Return code:", result.returncode)
        if result.stdout.strip():
            print("--- Subprocess Stdout ---")
            print(result.stdout)
        if result.stderr.strip():
            print("--- Subprocess Stderr ---")
            print(result.stderr)
            
        if result.returncode != 0:
            return False
        return True
    except Exception as e:
        print("Failed to run sweep:", e)
        return False

def generate_report():
    json_path = os.path.join(script_dir, "query_verification_run.json")
    if not os.path.exists(json_path):
        print(f"Error: JSON file not found at {json_path}")
        return
        
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        timestamp = data.get("timestamp", datetime.now().isoformat())
        engine_summary = data.get("engine_summary", {})
        detailed_results = data.get("detailed_results", {})
        
        # Calculate overall hits
        total_queries = data.get("queries_executed", 0)
        total_hits = sum(stats.get("total_hits", 0) for stats in engine_summary.values())
        
        # Start markdown
        md = []
        md.append(f"# 🔍 GRC Search Indexing & Rank Tracking Report")
        md.append(f"\n> **Last Updated**: {timestamp} (Checked every 15 minutes)")
        md.append(f"> **Target Domain**: `chasekn43.github.io/regulatory-archive-2026/`\n")
        
        md.append("## 📊 Engine Performance Summary")
        md.append("| Search Engine | Queries Executed | Avg Latency | Total Results | Target Hits | Hit Rate | Errors |")
        md.append("| :--- | :---: | :---: | :---: | :---: | :---: | :---: |")
        
        for engine, stats in engine_summary.items():
            avg_time = round(stats.get("total_time_ms", 0) / stats.get("queries", 1), 2) if stats.get("queries", 0) > 0 else 0
            hit_rate = round((stats.get("total_hits", 0) / stats.get("queries", 1)) * 100, 2) if stats.get("queries", 0) > 0 else 0
            md.append(f"| **{engine}** | {stats.get('queries')} | {avg_time:.1f}ms | {stats.get('total_results')} | {stats.get('total_hits')} | {hit_rate:.1f}% | {stats.get('errors')} |")
            
        md.append(f"\n**Total Target Hits Across All Engines**: `{total_hits}`")
        
        md.append("\n## 🎯 Target Search Results & Keyword Matches")
        md.append("Below are the queries that successfully returned search hits pointing to your public regulatory archive or GitHub repository:")
        
        matches_found = False
        md.append("| Query String | Engine | Matched URL / Title |")
        md.append("| :--- | :--- | :--- |")
        
        for query, engines in detailed_results.items():
            for engine, res in engines.items():
                hit_details = res.get("hit_details", [])
                if hit_details:
                    matches_found = True
                    for hit in hit_details:
                        title = hit.get("title", "No Title")
                        url = hit.get("url", "#")
                        md.append(f"| `{query}` | **{engine}** | [{title}]({url}) |")
                        
        if not matches_found:
            md.append("| *No matches detected in this sweep* | - | - |")
            
        # Write detailed failure check
        md.append("\n## 🛠️ Bot Mitigation & Diagnostics")
        md.append("Monitoring search engine crawl challenges (CAPTCHAs/JS loops):")
        for engine, stats in engine_summary.items():
            status = "🟢 OPERATIONAL"
            if stats.get("errors", 0) > 0:
                status = f"🔴 ERROR ({stats.get('errors')} failures)"
            elif stats.get("total_results", 0) == 0 and engine in ["Google", "Bing"]:
                status = "🟡 BLOCKED (JavaScript Challenge / Redirect)"
            md.append(f"- **{engine}**: {status}")
            
        # Write report to artifact folder
        report_path = os.path.join(artifact_dir, report_filename)
        with open(report_path, "w", encoding="utf-8") as rf:
            rf.write("\n".join(md))
            
        print(f"Progress report generated at {report_path}")
        
    except Exception as e:
        print("Failed to generate report:", e)

if __name__ == "__main__":
    if run_sweep():
        generate_report()
