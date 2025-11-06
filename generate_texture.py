#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Avatar Clothing Change Tool
Upload clothing images, understand the content, and replace only the clothing part in the texture
Uses AI-powered intelligent recognition and replacement, no manual region definition needed
"""

import os
import requests
from pathlib import Path
import base64
import io
import json

# PIL is required for image processing
try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    print("❌ Pillow is not installed, it's a required dependency")
    print("Please run: pip install Pillow")
    exit(1)

# Configuration paths
TEXTURE_PATH = Path("runtime/mark_free_t04.2048/texture_00.png")
BACKUP_PATH = Path("runtime/mark_free_t04.2048/texture_00_backup.png")

def backup_texture():
    """Backup original texture file"""
    if TEXTURE_PATH.exists():
        import shutil
        shutil.copy2(TEXTURE_PATH, BACKUP_PATH)
        print(f"✓ Original texture backed up to: {BACKUP_PATH}")
        return True
    return False

def restore_texture():
    """Restore original texture file"""
    if BACKUP_PATH.exists():
        import shutil
        shutil.copy2(BACKUP_PATH, TEXTURE_PATH)
        print(f"✓ Original texture restored")
        return True
    return False

def load_and_encode_image(image_path):
    """Load image and convert to base64 encoding"""
    try:
        with open(image_path, "rb") as f:
            image_data = f.read()
        return base64.b64encode(image_data).decode('utf-8')
    except Exception as e:
        print(f"❌ Failed to read image: {e}")
        return None

def understand_clothing_image(image_path, api_key):
    """
    Use Gemini Vision API to understand uploaded clothing image
    Returns detailed description of the clothing
    """
    if not api_key:
        print("⚠️  GEMINI_API_KEY environment variable not set")
        return None

    image_b64 = load_and_encode_image(image_path)
    if not image_b64:
        return None

    model_name = "gemini-2.0-flash-exp"
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"

    payload = {
        "contents": [{
            "parts": [
                {
                    "text": (
                        "Please describe the clothing in the image in detail, including:\n"
                        "1. Clothing type (T-shirt, hoodie, jacket, etc.)\n"
                        "2. Main colors and color scheme\n"
                        "3. Patterns or logos (if any)\n"
                        "4. Special design elements (pockets, zippers, hood, etc.)\n"
                        "5. Overall style (casual, sporty, formal, etc.)\n\n"
                        "The description should be concise and clear, suitable for generating 2D cartoon-style Live2D character texture maps."
                    )
                },
                {
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": image_b64
                    }
                }
            ]
        }]
    }

    try:
        print("🔄 Analyzing uploaded clothing image...")
        response = requests.post(
            api_url,
            params={"key": api_key},
            json=payload,
            timeout=60
        )

        if response.status_code != 200:
            print(f"❌ API request failed, status code: {response.status_code}")
            return None

        data = response.json()
        text_content = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")

        if text_content:
            print(f"✓ Clothing analysis completed:")
            print(f"  {text_content[:200]}..." if len(text_content) > 200 else f"  {text_content}")
            return text_content
        else:
            print("❌ Failed to get image description")
            return None

    except Exception as e:
        print(f"❌ Error analyzing image: {e}")
        return None

def generate_new_texture_with_clothing(clothing_description, api_key):
    """
    Use Gemini Imagen to intelligently replace clothing parts while keeping other parts unchanged
    Let AI understand the original texture layout and automatically identify and replace only the TORSO area
    """
    if not api_key:
        print("⚠️  GEMINI_API_KEY environment variable not set")
        return False

    # Determine which file to use as the original texture
    if BACKUP_PATH.exists():
        source_texture = BACKUP_PATH
        print("✓ Using backup file as original texture")
    elif TEXTURE_PATH.exists():
        source_texture = TEXTURE_PATH
        print("✓ Using current texture file")
        # Create backup if it doesn't exist yet
        if not BACKUP_PATH.exists():
            backup_texture()
    else:
        print("❌ Texture file not found")
        return False

    try:
        # 1. Load and encode original texture
        original_texture_b64 = load_and_encode_image(str(source_texture))
        if not original_texture_b64:
            return False

        print("✓ Original texture loaded")

        # 2. Build intelligent prompt to tell Gemini to keep layout unchanged
        model_name = "gemini-2.5-flash-image"
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"

        enhanced_prompt = (
            f"Generate a new version of this Live2D character texture sheet. "
            f"CRITICAL: Keep the EXACT SAME layout, positions, and style. "
            f"ONLY modify the TORSO clothing area (the shirt/hoodie in the middle). "
            f"Keep ALL other parts COMPLETELY UNCHANGED:\n"
            f"- Hair (top row): KEEP EXACTLY THE SAME\n"
            f"- Face and expressions: KEEP EXACTLY THE SAME\n"
            f"- Arms and hands: KEEP EXACTLY THE SAME\n"
            f"- Legs and shoes: KEEP EXACTLY THE SAME\n"
            f"- Background: white, KEEP THE SAME\n"
            f"- Layout and positions: KEEP EXACTLY THE SAME\n"
            f"\n"
            f"ONLY CHANGE: The torso/clothing in the center to: {clothing_description}\n"
            f"\n"
            f"Style requirements:\n"
            f"- 2D cartoon anime style (same as original)\n"
            f"- Clean black outlines (same as original)\n"
            f"- Similar shading style\n"
            f"- Output: 2048x2048 pixels"
        )

        payload = {
            "contents": [{
                "parts": [
                    {"text": enhanced_prompt},
                    {
                        "inline_data": {
                            "mime_type": "image/png",
                            "data": original_texture_b64
                        }
                    }
                ]
            }],
            "generationConfig": {
                "responseModalities": ["IMAGE"]
            }
        }

        # 3. Call API to generate new texture
        print("🔄 AI is intelligently replacing clothing part...")
        print(f"   Target clothing: {clothing_description}")
        print("   (AI will automatically identify clothing area and keep other parts unchanged)")

        response = requests.post(
            api_url,
            params={"key": api_key},
            json=payload,
            timeout=120
        )

        if response.status_code != 200:
            print(f"❌ API request failed, status code: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error info: {error_data}")
            except:
                print(f"Response: {response.text}")
            return False

        data = response.json()
        candidates = data.get("candidates")
        if not candidates:
            print("❌ No image data received from Gemini")
            return False

        result = candidates[0].get("content", {})
        parts = result.get("parts", [])
        image_part = next(
            (part for part in parts if "inlineData" in part or "image" in part),
            None
        )

        if not image_part:
            print("❌ Missing image content in response")
            return False

        if "inlineData" in image_part:
            image_b64 = image_part["inlineData"].get("data")
        else:
            image_b64 = image_part["image"].get("base64Data")

        if not image_b64:
            print("❌ Unable to get image data")
            return False

        # 4. Save new texture
        image_data = base64.b64decode(image_b64)
        img = Image.open(io.BytesIO(image_data))

        # Ensure it's 2048x2048
        if img.size != (2048, 2048):
            print(f"⚠️  Resizing image from {img.size} to (2048, 2048)")
            img = img.resize((2048, 2048), Image.Resampling.LANCZOS)

        TEXTURE_PATH.parent.mkdir(parents=True, exist_ok=True)
        img.save(TEXTURE_PATH, "PNG")

        print(f"✓ New texture saved to: {TEXTURE_PATH}")
        print(f"  ✨ AI has intelligently replaced clothing part, other parts remain unchanged")
        return True

    except Exception as e:
        print(f"❌ Error generating new texture: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function"""
    print("=" * 50)
    print("Avatar Clothing Change Tool - AI Smart Replacement")
    print("=" * 50)
    print("✨ Feature: AI automatically identifies clothing position, keeps other parts unchanged")
    print()

    # Check API key
    gemini_key = os.getenv("GEMINI_API_KEY")

    if not gemini_key:
        print("⚠️  GEMINI_API_KEY not detected")
        print("Please set environment variable:")
        print("  export GEMINI_API_KEY='your_gemini_api_key'")
        print()
        return

    # Check if texture file exists
    if not TEXTURE_PATH.exists():
        print(f"❌ Texture file not found: {TEXTURE_PATH}")
        print("Please ensure the file exists before running")
        return

    # Ensure backup file exists
    if not BACKUP_PATH.exists():
        print("📋 First run, creating texture backup...")
        backup_texture()
        print()

    # Main loop
    print("\nUsage:")
    print("  1. Upload clothing photo: Enter the file path of a real clothing image")
    print("     Example: /path/to/your/tshirt.jpg")
    print("     (AI will understand the clothing in the photo and generate a 2D cartoon version)")
    print()
    print("  2. Text description: Directly enter the clothing description")
    print("     Example: red hoodie with white logo on front")
    print()
    print("  3. Restore original: Enter 'restore'")
    print("  4. Quit program: Enter 'quit'")
    print()

    while True:
        user_input = input("Input > ").strip()

        if not user_input:
            continue

        if user_input.lower() == 'quit':
            print("👋 Goodbye!")
            break

        if user_input.lower() == 'restore':
            restore_texture()
            continue

        # Determine if it's an image path or text description
        if os.path.isfile(user_input):
            # Image upload mode
            print(f"\n📸 Image file detected: {user_input}")

            # 1. Understand image
            clothing_description = understand_clothing_image(user_input, gemini_key)

            if not clothing_description:
                print("❌ Unable to analyze image, please try again")
                continue

            # 2. Ask user for confirmation
            print(f"\n📝 AI's understanding of clothing features:")
            print(f"   {clothing_description}")
            confirm = input("\nUse this description to generate clothing? (y/n) > ").strip().lower()

            if confirm != 'y':
                print("❌ Cancelled")
                continue

            # 3. Let AI intelligently replace clothing
            success = generate_new_texture_with_clothing(clothing_description, gemini_key)

            if success:
                print("\n✅ Clothing change complete! Texture updated")
                print("   💡 Please refresh browser to see the effect")
                print("   💡 If not satisfied, enter 'restore' to revert")
            else:
                print("\n❌ Clothing change failed")

        else:
            # Text description mode
            print(f"\n📝 Using text description: {user_input}")

            # Let AI intelligently replace clothing
            success = generate_new_texture_with_clothing(user_input, gemini_key)

            if success:
                print("\n✅ Clothing change complete! Texture updated")
                print("   💡 Please refresh browser to see the effect")
                print("   💡 If not satisfied, enter 'restore' to revert")
            else:
                print("\n❌ Clothing change failed")

if __name__ == "__main__":
    main()
