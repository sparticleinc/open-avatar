# Open Avatar

An AI-powered 2D digital human avatar with intelligent clothing replacement using Live2D and Google Gemini API.

## Try it yourself (2 steps live demo)
1. https://avatar.gbase.ai/ → name, style, (optional) company URL for auto-branding → Generate (live preview)
2. Connect a knowledge base so it can actually talk (we use GBase; use whatever)

## Features

- 🎨 **AI-Powered Clothing Replacement**: Upload clothing images or use text descriptions to automatically replace avatar clothing
- 🤖 **Intelligent Recognition**: Uses Gemini Vision API to understand clothing details from photos
- 🎭 **Live2D Integration**: Built on Live2D runtime for smooth 2D character animation
- 🔄 **Easy Restoration**: One-click restore to original texture
- 📸 **Multiple Input Methods**: Support both image upload and text description

## Project Structure

```
openavatar/
├── index.html              # Main HTML page for displaying the avatar
├── generate_texture.py     # AI-powered texture generation tool
├── requirements.txt        # Python dependencies
├── lib/
│   └── local_main.js       # JavaScript loader for Live2D runtime
└── runtime/
    ├── anime_runtime.js    # Live2D runtime library
    └── motion/             # Animation motion files
```

## Installation

### Prerequisites

- Python 3.8 or higher
- A Google Gemini API key (get one from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Setup

1. Clone the repository:
```bash
git clone git@github.com-mikeyang-spar:sparticleinc/open-avatar.git
cd open-avatar
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your Gemini API key:
```bash
export GEMINI_API_KEY='your_gemini_api_key_here'
```

## Usage

### Running the Avatar Viewer

Simply open `index.html` in a web browser. The Live2D avatar will be displayed with animations.

For local development, you may need to serve the files through a web server:
```bash
# Using Python
python -m http.server 8000

# Using Node.js
npx serve
```

Then open `http://localhost:8000` in your browser.

### Changing Avatar Clothing

Run the texture generation tool:
```bash
python generate_texture.py
```

The tool provides three modes:

1. **Image Upload Mode**: Provide a path to a clothing image
   ```
   Input > /path/to/your/tshirt.jpg
   ```
   The AI will analyze the image and generate a 2D cartoon version.

2. **Text Description Mode**: Describe the clothing directly
   ```
   Input > red hoodie with white logo on front
   ```

3. **Restore Original**: Revert to the original texture
   ```
   Input > restore
   ```

4. **Quit**: Exit the program
   ```
   Input > quit
   ```

### Example Workflow

```bash
$ python generate_texture.py
==================================================
Avatar Clothing Change Tool - AI Smart Replacement
==================================================
✨ Feature: AI automatically identifies clothing position, keeps other parts unchanged

Usage:
  1. Upload clothing photo: Enter the file path of a real clothing image
  2. Text description: Directly enter the clothing description
  3. Restore original: Enter 'restore'
  4. Quit program: Enter 'quit'

Input > red t-shirt with blue jeans
📝 Using text description: red t-shirt with blue jeans
🔄 AI is intelligently replacing clothing part...
✓ New texture saved to: runtime/haru_greeter_t05.2048/texture_01.png
✅ Clothing change complete! Texture updated
   💡 Please refresh browser to see the effect
```

After generating a new texture, refresh your browser to see the updated avatar.

## How It Works

1. **Clothing Analysis** (Image Mode): When you upload a clothing image, Gemini Vision API analyzes the clothing details including:
   - Clothing type (T-shirt, hoodie, jacket, etc.)
   - Colors and color scheme
   - Patterns or logos
   - Special design elements
   - Overall style

2. **Intelligent Replacement**: The AI understands the Live2D texture layout and:
   - Identifies the torso/clothing area automatically
   - Keeps all other parts unchanged (hair, face, arms, legs, etc.)
   - Generates new clothing in 2D cartoon style matching the original
   - Maintains the exact layout and positions

3. **Texture Update**: The new texture is saved as `texture_00.png`, replacing the original while keeping a backup.

## Configuration

### API Configuration

The tool uses Google Gemini API. You need to set the API key as an environment variable:

```bash
export GEMINI_API_KEY='your_api_key_here'
```


## Troubleshooting

### API Request Failed
- Verify your `GEMINI_API_KEY` is correctly set
- Check your network connection
- Ensure your API key has proper permissions

### Generated Texture Not Expected
- Try more detailed descriptions
- Use the `restore` command to revert
- Upload a clearer clothing image

### Import Errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (3.8+ required)

### Live2D Model Not Loading
- Ensure all runtime files are in the correct directories
- Check browser console for errors
- Verify file paths in `lib/local_main.js`

## Technical Details
- **Model Format**: Live2D Cubism 3.0 (`.moc3`, `.model3.json`)
- **Texture Size**: 2048x2048 pixels
- **AI Models Used**:
  - `gemini-2.0-flash-exp` for image understanding
  - `gemini-2.5-flash-image` for texture generation

## Contributing
We welcome contributions to Open Avatar! 
