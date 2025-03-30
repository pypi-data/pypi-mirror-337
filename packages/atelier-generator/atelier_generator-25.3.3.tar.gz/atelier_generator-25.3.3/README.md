# atelier-generator

A comprehensive toolkit for state-of-the-art AI image generation compatible with all devices.

## Installation

```bash
pip install atelier-generator
```

## Key Features

- 🎨 **Image Generation**
  - Text-to-Image Generation
  - Image Variations
  - Structural & Facial Guidance
  - Style Transfer & ControlNet
- 🛠️ **Image Editing**
  - Face Enhancement (GFPGAN/CodeFormer)
  - Background Removal
  - Image Upscaling
  - Object Erasing & Inpainting
- ⚡ **Real-time Features**
  - RT Image Generation
  - Interactive Canvas
  - Image Outpainting
  - Image Analysis (Caption/Prompt)

## Usage

### Python Library

```python
from atelier_generator import AtelierGenerator

# Initialize
atelier = AtelierGenerator(
    mode="default", # Mode (default/webui/api)
    gradio=False, # Enable Gradio support
    timeout=180, # Request timeout (seconds)
    log_on=True, # Enable logging
    save_to="outputs", # Output directory
    save_as="webp" # Output format (png/webp/jpg/pil)
)

# Basic image generation
result = atelier.image_generate(
    prompt="a beautiful landscape",
    negative_prompt="", # Optional negative prompt
    model_name="flux-turbo", # Model selection
    image_size="1:1", # Output size ratio
    lora_svi=None, # LoRA SVI preset
    lora_flux=None, # LoRA Flux preset
    image_seed=0, # Generation seed
    style_name=None # Style preset
)

# Image variation
result = atelier.image_variation(
    image="source.jpg", # Source image
    prompt="convert to anime",
    negative_prompt="", # Optional negative prompt
    model_name="flux-turbo", # Model selection
    image_size="1:1", # Output size ratio
    strength="high", # Variation strength (low/medium/high)
    lora_svi=None, # LoRA SVI preset
    lora_flux=None, # LoRA Flux preset
    image_seed=0, # Generation seed
    style_name=None # Style preset
)

# Structural guidance
result = atelier.image_structure(
    image="structure.jpg", # Source image
    prompt="enhance details",
    negative_prompt="", # Optional negative prompt
    model_name="svi-realistic", # Model selection
    image_size="1:1", # Output size ratio
    strength="high", # Guide strength (low/medium/high)
    lora_svi=None,  # LoRA SVI preset
    image_seed=0, # Generation seed
    style_name=None # Style preset
)

# Face enhancement
result = atelier.face_gfpgan(
    image="face.jpg",
    model_version="1.3" # Model version (1.2/1.3)
)
result = atelier.face_codeformer(
    image="face.jpg"
)

# Image editing
result = atelier.image_enhance(
    image="photo.jpg",
    prompt="enhance quality", # Optional prompt
    negative_prompt="", # Optional negative prompt
    creativity=0.3, # Creativity level (0.0-1.0)
    resemblance=1.0, # Resemblance level (0.0-1.0)
    hdr=0.0, # HDR strength (0.0-1.0)
    style_name=None # Style preset
)

result = atelier.image_inpaint(
    image="image.jpg",
    mask="mask.jpg", # Mask image
    prompt="fill with trees",
    style_name=None # Style preset
)

result = atelier.image_erase(
    image="image.jpg",
    mask="mask.jpg" # Mask image
)

result = atelier.image_bgremove(
    image="photo.jpg"
)

result = atelier.image_upscale(
    image="small.jpg"
)

result = atelier.image_outpaint(
    image="image.jpg",
    image_size="16:9" # Output size ratio
)

# Real-time features
result = atelier.realtime_generate(
    prompt="quick sketch",
    negative_prompt="", # Optional negative prompt
    image_size="1:1", # Output size ratio
    lora_rt=None, # LoRA RT preset
    image_seed=0, # Generation seed
    style_name=None # Style preset
)

result = atelier.realtime_canvas(
    image="canvas.jpg", # Source image
    prompt="enhance drawing",
    negative_prompt="", # Optional negative prompt
    lora_rt=None, # LoRA RT preset
    strength=0.9, # Creativity level (0.0-1.0)
    image_seed=0, # Generation seed
    style_name=None # Style preset
)

# Image analysis
caption = atelier.image_caption(
    image="photo.jpg"
)
prompt = atelier.image_prompt(
    image="photo.jpg"
)

# ControlNet features
result = atelier.image_controlnet(
    image="sketch.jpg",
    prompt="convert to art",
    negative_prompt="", # Optional negative prompt
    model_name="sd-toon", # Model selection
    controlnet="scribble", # Control type (scribble/pose/line-art/depth/canny)
    strength=70, # Control strength (0-100)
    cfg=9.0, # Prompt guidance scale
    image_seed=0, # Generation seed
    style_name=None # Style preset
)
```

### Web UI

Start the Gradio web interface:

```python
atelier = AtelierGenerator(mode="webui")
# OR
atelier = AtelierGenerator()
atelier.start_wui(
    host="localhost", # Server host
    port=7860, # Server port
    browser=True, # Launch browser
    upload_size="4MB", # Max upload size
    public=False, # Enable public URL
    limit=10, # Max concurrent requests
    quiet=False # Quiet mode
)
```

### REST API

Start the Flask API server:

```python
atelier = AtelierGenerator(mode="api")
# OR
atelier = AtelierGenerator()
atelier.start_api(
    host="0.0.0.0", # Server host
    port=5000, # Server port
    debug=False # Enable debug mode
)
```

#### API Endpoints

Image Generation:
- `POST /v1/api/image/generate` - Generate images from text
- `POST /v1/api/image/variation` - Create image variations
- `POST /v1/api/image/structure` - Apply structural guidance
- `POST /v1/api/image/facial` - Apply facial guidance
- `POST /v1/api/image/style` - Apply style transfer
- `POST /v1/api/image/controlnet` - Apply ControlNet

Image Editing:
- `POST /v1/api/image/enhance` - Enhance image quality
- `POST /v1/api/image/inpaint` - Fill masked areas
- `POST /v1/api/image/erase` - Remove objects
- `POST /v1/api/image/upscale` - Upscale image
- `POST /v1/api/image/bgremove` - Remove background
- `POST /v1/api/image/outpaint` - Extend image borders

Face Enhancement:
- `POST /v1/api/face/gfpgan` - GFPGAN face restoration
- `POST /v1/api/face/codeformer` - CodeFormer face restoration

Real-time Features:
- `POST /v1/api/realtime/generate` - Real-time generation
- `POST /v1/api/realtime/canvas` - Interactive canvas

Image Analysis:
- `POST /v1/api/image/caption` - Generate image caption
- `POST /v1/api/image/prompt` - Convert image to prompt

Data Endpoints:
- `GET /v1/api/get/models` - List all available models
- `GET /v1/api/get/models/guide` - List guidance models
- `GET /v1/api/get/models/flux` - List Flux models
- `GET /v1/api/get/models/svi` - List SVI models
- `GET /v1/api/get/models/sdxl` - List SDXL models
- `GET /v1/api/get/models/remix` - List Remix models
- `GET /v1/api/get/lora/flux` - List Flux LoRA presets
- `GET /v1/api/get/lora/svi` - List SVI LoRA presets
- `GET /v1/api/get/lora/rt` - List RT LoRA presets
- `GET /v1/api/get/styles` - List style presets
- `GET /v1/api/get/controlnets` - List ControlNet types
- `GET /v1/api/get/gfpgan` - List GFPGAN versions
- `GET /v1/api/get/size` - List available image sizes
- `GET /v1/api/get/guide/variation` - List variation strength presets
- `GET /v1/api/get/guide/structure` - List structure guidance presets
- `GET /v1/api/get/guide/facial` - List facial guidance presets
- `GET /v1/api/get/guide/style` - List style guidance presets

## Configuration

### Output Formats
- `webp` (default) - High quality, small size
- `png` - Lossless quality
- `jpg` - Standard compressed
- `pil` - PIL Image object

### Available Models & Presets
```python
# Get available options
models = atelier.list_atr_models # All models
sizes = atelier.list_atr_size # Image sizes
styles = atelier.list_sty_styles # Style presets
svi_lora = atelier.list_atr_lora_svi # SVI LoRA models
flux_lora = atelier.list_atr_lora_flux # Flux LoRA models
rt_lora = atelier.list_atr_lora_rt # RT LoRA models
```

## License

See [LICENSE](LICENSE) for details.
