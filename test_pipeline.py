#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from backend.pipeline import ResearchPipeline
import time

def test_pipeline():
    print("🧪 Testing ResearchPipeline directly...")
    start_time = time.time()

    try:
        pipeline = ResearchPipeline()
        print("✅ Pipeline initialized")

        query = "What is solar energy?"
        print(f"🔍 Running query: {query}")

        result = pipeline.run(query)
        elapsed = time.time() - start_time

        print(f"⏱️  Pipeline completed in {elapsed:.1f} seconds")
        print(f"📊 Result keys: {list(result.keys())}")

        if "report" in result:
            report = result["report"]
            print(f"📋 Report title: {report.get('title', 'N/A')}")
            print(f"📝 Key findings: {len(report.get('key_findings', []))}")
        else:
            print("❌ No report in result")

        return result

    except Exception as e:
        elapsed = time.time() - start_time
        print(f"💥 Exception after {elapsed:.1f} seconds: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_pipeline()