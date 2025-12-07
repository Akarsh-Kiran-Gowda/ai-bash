#!/usr/bin/env python3
"""
Check available Gemini models for your API key.
Run this to see which models you can use.
"""

import os
import google.generativeai as genai

# Get API key from environment or .env file
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    try:
        with open(".env", "r") as f:
            for line in f:
                if line.startswith("GEMINI_API_KEY="):
                    api_key = line.split("=", 1)[1].strip()
                    break
    except FileNotFoundError:
        pass

if not api_key:
    print("❌ GEMINI_API_KEY not found!")
    print("Set it in .env file or as environment variable")
    exit(1)

print("Checking available Gemini models...\n")

genai.configure(api_key=api_key)

available_models = []
for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        available_models.append(m.name)
        print(f"✓ {m.name}")

if not available_models:
    print("❌ No models available for your API key!")
else:
    print(f"\n✓ Found {len(available_models)} available model(s)")
    print("\nRecommended for AI Bash:")
    if "models/gemini-1.5-flash" in available_models:
        print("  → gemini-1.5-flash (fast and efficient)")
    elif "models/gemini-1.5-pro" in available_models:
        print("  → gemini-1.5-pro (most capable)")
    elif "models/gemini-pro" in available_models:
        print("  → gemini-pro (standard)")
    else:
        print(f"  → {available_models[0].replace('models/', '')}")
