<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Atelier Generator API</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    
    <style>
        /* Base styles */
        :root {
            --background: #09090b;
            --foreground: #fafafa;
            --muted: #27272a;
            --muted-foreground: #a1a1aa;
            --border: #27272a;
            --ring: #18181b;
            --primary: #fafafa;
            --primary-foreground: #18181b;
            --secondary: #27272a;
            --card: #09090b;
            --card-foreground: #fafafa;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--background);
            color: var(--foreground);
            line-height: 1.5;
            padding: 1rem;
        }

        /* Components */
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }

        .card {
            background-color: var(--card);
            border: 1px solid var(--border);
            border-radius: 0.5rem;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            text-align: center;
        }

        .button {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 0.375rem;
            font-weight: 500;
            padding: 0.5rem 1rem;
            transition: all 150ms;
            cursor: pointer;
            border: 1px solid var(--border);
        }

        .button-primary {
            background-color: var(--primary);
            color: var(--primary-foreground);
        }

        .button-secondary {
            background-color: var(--secondary);
            color: var(--foreground);
        }

        .input {
            width: 100%;
            padding: 0.5rem;
            background-color: var(--muted);
            border: 1px solid var(--border);
            border-radius: 0.375rem;
            color: var(--foreground);
            font-size: 0.875rem;
        }

        /* Modal */
        .modal-backdrop {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(4px);
            z-index: 50;
            display: none;
        }

        .modal {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: var(--card);
            border: 1px solid var(--border);
            border-radius: 0.5rem;
            padding: 1.5rem;
            width: 90%;
            max-width: 800px;
            z-index: 51;
        }

        /* Grid */
        .grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
            margin: 1rem 0;
        }

        .grid-item {
            aspect-ratio: 1;
            background-color: var(--muted);
            border-radius: 0.375rem;
            position: relative;
            overflow: hidden;
        }

        /* Table */
        .table-container {
            overflow-x: auto;
            border: 1px solid var(--border);
            border-radius: 0.5rem;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.875rem;
        }

        th, td {
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }

        th {
            background-color: var(--muted);
            font-weight: 500;
            color: var(--muted-foreground);
        }

        /* Loader */
        .loader {
            width: 2.5rem;
            height: 2.5rem;
            border: 3px solid var(--muted-foreground);
            border-bottom-color: transparent;
            border-radius: 50%;
            display: none;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            to { transform: translate(-50%, -50%) rotate(360deg); }
        }

        .grid-item.loading .loader {
            display: block;
        }

        .grid-item img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: none;
        }

        .warning {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: #fda4af;
            font-size: 0.875rem;
            font-weight: 500;
            text-align: center;
        }

        .warning svg {
            width: 1.25rem;
            height: 1.25rem;
            stroke: currentColor;
        }

                
        .download-button {
            position: absolute;
            bottom: 8px;
            right: 8px;
            background-color: var(--secondary);
            border-radius: 0.375rem;
            padding: 0.5rem;
            cursor: pointer;
            opacity: 0;
            transition: opacity 0.2s;
            z-index: 10;
            border: none;
        }

        .grid-item:hover .download-button {
            opacity: 1;
        }

        .download-button svg {
            width: 1.25rem;
            height: 1.25rem;
            stroke: var(--foreground);
        }

        .grid-item.loading .download-button,
        .grid-item:not(:has(img[src])) .download-button {
            display: none;
        }

        .tabs {
            display: flex;
            gap: 0.5rem;
            margin-bottom: 1rem;
            place-content: center;
        }

        .tab {
            padding: 0.5rem 1rem;
            background-color: var(--secondary);
            border: 1px solid var(--border);
            border-radius: 0.375rem;
            color: var(--muted-foreground);
            cursor: pointer;
            transition: all 150ms;
        }

        .tab.active {
            background-color: var(--primary);
            color: var(--primary-foreground);
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1 style="font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem;">Atelier Generator API Server</h1>
            <p style="color: var(--muted-foreground);">Copyright (C) 2025 Ikmal Said. All rights reserved</p>
            <button onclick="openTestDialog()" class="button button-primary" style="margin-top: 1rem;">
                Test Image Generation
            </button>
        </div>

        <!-- Modal Dialog -->
        <div id="testDialog" class="modal-backdrop">
            <div class="modal">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; place-content: center;">
                    <h2 style="font-size: 1.25rem; font-weight: 600;">Test Image Generation</h2>
                </div>

                <div style="display: flex; gap: 0.5rem; margin-bottom: 1rem;">
                    <input type="text" id="prompt" placeholder="Enter your prompt" class="input">
                    <button onclick="generateImages()" class="button button-primary">Generate</button>
                </div>

                <div class="grid">
                    <div class="grid-item" id="image0">
                        <div class="loader"></div>
                        <img>
                        <button class="download-button" onclick="downloadImage(this)">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" />
                            </svg>
                        </button>
                    </div>
                    <div class="grid-item" id="image1">
                        <div class="loader"></div>
                        <img>
                        <button class="download-button" onclick="downloadImage(this)">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" />
                            </svg>
                        </button>
                    </div>
                    <div class="grid-item" id="image2">
                        <div class="loader"></div>
                        <img>
                        <button class="download-button" onclick="downloadImage(this)">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" />
                            </svg>
                        </button>
                    </div>
                    <div class="grid-item" id="image3">
                        <div class="loader"></div>
                        <img>
                        <button class="download-button" onclick="downloadImage(this)">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" />
                            </svg>
                        </button>
                    </div>
                </div>

                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1rem; place-content: center;">
                    <button onclick="closeTestDialog()" class="button button-secondary">Close</button>
                </div>
            </div>
        </div>

        <!-- API Documentation -->
        <div class="card">
            <h2 style="font-size: 1.25rem; font-weight: 600; margin-bottom: 1rem;">API Documentation</h2>
            
            <div class="tabs">
                <button class="tab active" onclick="switchTab('inference')">Inference Endpoints</button>
                <button class="tab" onclick="switchTab('data')">Data Endpoints</button>
            </div>
        
            <div id="inference-tab" class="tab-content active">
                <div class="table-container">
                <table>
                    <tr>
                        <th>POST Endpoints</th>
                        <th>Description</th>
                        <th>Parameters</th>
                    </tr>
                    <tr>
                        <td>/v1/api/image/generate</td>
                        <td>Generate images from text prompts</td>
                        <td>
                            <ul>
                                <li><code>prompt</code> (required): Text prompt</li>
                                <li><code>negative_prompt</code>: Negative prompt</li>
                                <li><code>model_name</code>: Model name (default: "flux-turbo")</li>
                                <li><code>image_size</code>: Size ratio (default: "1:1")</li>
                                <li><code>lora_svi</code>: LoRA SVI preset</li>
                                <li><code>lora_flux</code>: LoRA Flux preset</li>
                                <li><code>image_seed</code>: Generation seed</li>
                                <li><code>style_name</code>: Style preset</li>
                            </ul>
                        </td>
                    </tr>
                    <tr>
                        <td>/v1/api/image/variation</td>
                        <td>Create variations of existing images</td>
                        <td>
                            <ul>
                                <li><code>image</code> (required): Source image</li>
                                <li><code>prompt</code> (required): Text prompt</li>
                                <li><code>negative_prompt</code>: Negative prompt</li>
                                <li><code>model_name</code>: Model name (default: "flux-turbo")</li>
                                <li><code>image_size</code>: Size ratio (default: "1:1")</li>
                                <li><code>strength</code>: Variation strength</li>
                                <li><code>lora_svi</code>: LoRA SVI preset</li>
                                <li><code>lora_flux</code>: LoRA Flux preset</li>
                                <li><code>image_seed</code>: Generation seed</li>
                                <li><code>style_name</code>: Style preset</li>
                            </ul>
                        </td>
                    </tr>
                    <tr>
                        <td>/v1/api/image/structure</td>
                        <td>Apply structural guidance to images</td>
                        <td>
                            <ul>
                                <li><code>image</code> (required): Source image</li>
                                <li><code>prompt</code> (required): Text prompt</li>
                                <li><code>negative_prompt</code>: Negative prompt</li>
                                <li><code>model_name</code>: Model name (default: "svi-realistic")</li>
                                <li><code>image_size</code>: Size ratio (default: "1:1")</li>
                                <li><code>strength</code>: Guidance strength</li>
                                <li><code>lora_svi</code>: LoRA SVI preset</li>
                                <li><code>image_seed</code>: Generation seed</li>
                                <li><code>style_name</code>: Style preset</li>
                            </ul>
                        </td>
                    </tr>
                    <tr>
                        <td>/v1/api/image/facial</td>
                        <td>Apply facial guidance to images</td>
                        <td>
                            <ul>
                                <li><code>image</code> (required): Source image</li>
                                <li><code>prompt</code> (required): Text prompt</li>
                                <li><code>negative_prompt</code>: Negative prompt</li>
                                <li><code>model_name</code>: Model name (default: "svi-realistic")</li>
                                <li><code>image_size</code>: Size ratio (default: "1:1")</li>
                                <li><code>strength</code>: Guidance strength</li>
                                <li><code>lora_svi</code>: LoRA SVI preset</li>
                                <li><code>image_seed</code>: Generation seed</li>
                                <li><code>style_name</code>: Style preset</li>
                            </ul>
                        </td>
                    </tr>
                    <tr>
                        <td>/v1/api/image/style</td>
                        <td>Apply style guidance to images</td>
                        <td>
                            <ul>
                                <li><code>image</code> (required): Source image</li>
                                <li><code>prompt</code> (required): Text prompt</li>
                                <li><code>negative_prompt</code>: Negative prompt</li>
                                <li><code>model_name</code>: Model name (default: "svi-realistic")</li>
                                <li><code>image_size</code>: Size ratio (default: "1:1")</li>
                                <li><code>strength</code>: Style strength</li>
                                <li><code>lora_svi</code>: LoRA SVI preset</li>
                                <li><code>image_seed</code>: Generation seed</li>
                                <li><code>style_name</code>: Style preset</li>
                            </ul>
                        </td>
                    </tr>
                    <tr>
                        <td>/v1/api/image/outpaint</td>
                        <td>Extend images beyond their borders</td>
                        <td>
                            <ul>
                                <li><code>image</code> (required): Source image</li>
                                <li><code>image_size</code>: Size ratio (default: "16:9")</li>
                            </ul>
                        </td>
                    </tr>
                    <tr>
                        <td>/v1/api/realtime/canvas</td>
                        <td>Real-time canvas processing</td>
                        <td>
                            <ul>
                                <li><code>image</code> (required): Source image</li>
                                <li><code>prompt</code> (required): Text prompt</li>
                                <li><code>negative_prompt</code>: Negative prompt</li>
                                <li><code>lora_rt</code>: LoRA RT preset</li>
                                <li><code>strength</code>: Creativity level (default: 0.9)</li>
                                <li><code>image_seed</code>: Generation seed</li>
                                <li><code>style_name</code>: Style preset</li>
                            </ul>
                        </td>
                    </tr>
                    <tr>
                        <td>/v1/api/realtime/generate</td>
                        <td>Real-time image generation</td>
                        <td>
                            <ul>
                                <li><code>prompt</code> (required): Text prompt</li>
                                <li><code>negative_prompt</code>: Negative prompt</li>
                                <li><code>image_size</code>: Size ratio (default: "1:1")</li>
                                <li><code>lora_rt</code>: LoRA RT preset</li>
                                <li><code>image_seed</code>: Generation seed</li>
                                <li><code>style_name</code>: Style preset</li>
                            </ul>
                        </td>
                    </tr>
                    <tr>
                        <td>/v1/api/image/inpaint</td>
                        <td>Fill masked areas in images</td>
                        <td>
                            <ul>
                                <li><code>image</code> (required): Source image</li>
                                <li><code>mask</code> (required): Mask image</li>
                                <li><code>prompt</code> (required): Text prompt</li>
                                <li><code>negative_prompt</code>: Negative prompt</li>
                                <li><code>strength</code>: Inpainting strength (default: 0.5)</li>
                                <li><code>cfg</code>: Prompt scale (default: 9.0)</li>
                                <li><code>style_name</code>: Style preset</li>
                            </ul>
                        </td>
                    </tr>
                    <tr>
                        <td>/v1/api/image/erase</td>
                        <td>Remove content from masked areas</td>
                        <td>
                            <ul>
                                <li><code>image</code> (required): Source image</li>
                                <li><code>mask</code> (required): Mask image</li>
                                <li><code>cfg</code>: Prompt scale (default: 9.0)</li>
                            </ul>
                        </td>
                    </tr>
                    <tr>
                        <td>/v1/api/image/enhance</td>
                        <td>Enhance image quality</td>
                        <td>
                            <ul>
                                <li><code>image</code> (required): Source image</li>
                                <li><code>prompt</code>: Text prompt</li>
                                <li><code>negative_prompt</code>: Negative prompt</li>
                                <li><code>creativity</code>: Creativity level (default: 0.3)</li>
                                <li><code>resemblance</code>: Resemblance level (default: 1)</li>
                                <li><code>hdr</code>: HDR strength (default: 0)</li>
                                <li><code>style_name</code>: Style preset</li>
                            </ul>
                        </td>
                    </tr>
                    <tr>
                        <td>/v1/api/image/controlnet</td>
                        <td>Apply ControlNet guidance</td>
                        <td>
                            <ul>
                                <li><code>image</code> (required): Source image</li>
                                <li><code>prompt</code> (required): Text prompt</li>
                                <li><code>negative_prompt</code>: Negative prompt</li>
                                <li><code>model_name</code>: Model name (default: "sd-toon")</li>
                                <li><code>controlnet</code>: Control type (default: "scribble")</li>
                                <li><code>strength</code>: Control strength (default: 70)</li>
                                <li><code>cfg</code>: Prompt scale (default: 9.0)</li>
                                <li><code>image_seed</code>: Generation seed</li>
                                <li><code>style_name</code>: Style preset</li>
                            </ul>
                        </td>
                    </tr>
                    <tr>
                        <td>/v1/api/face/gfpgan</td>
                        <td>Face restoration using GFPGAN</td>
                        <td>
                            <ul>
                                <li><code>image</code> (required): Source image</li>
                                <li><code>model_version</code>: Model version (default: "1.3")</li>
                            </ul>
                        </td>
                    </tr>
                    <tr>
                        <td>/v1/api/face/codeformer</td>
                        <td>Face restoration using CodeFormer</td>
                        <td>
                            <ul>
                                <li><code>image</code> (required): Source image</li>
                            </ul>
                        </td>
                    </tr>
                    <tr>
                        <td>/v1/api/image/upscale</td>
                        <td>Upscale image resolution</td>
                        <td>
                            <ul>
                                <li><code>image</code> (required): Source image</li>
                            </ul>
                        </td>
                    </tr>
                    <tr>
                        <td>/v1/api/image/bgremove</td>
                        <td>Remove image background</td>
                        <td>
                            <ul>
                                <li><code>image</code> (required): Source image</li>
                            </ul>
                        </td>
                    </tr>
                    <tr>
                        <td>/v1/api/image/caption</td>
                        <td>Generate image captions</td>
                        <td>
                            <ul>
                                <li><code>image</code> (required): Source image</li>
                            </ul>
                        </td>
                    </tr>
                    <tr>
                        <td>/v1/api/image/prompt</td>
                        <td>Generate prompts from images</td>
                        <td>
                            <ul>
                                <li><code>image</code> (required): Source image</li>
                            </ul>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div id="data-tab" class="tab-content">
            <div class="table-container">
                <table>
                    <tr>
                        <th>GET Endpoints</th>
                        <th>Description</th>
                        <th>Response</th>
                    </tr>
                    <tr>
                        <td>/v1/api/get/models</td>
                        <td>List all available models</td>
                        <td>
                            <ul>
                                <li><code>models</code>: List of model names</li>
                            </ul>
                        </td>
                    </tr>
                    <tr>
                        <td>/v1/api/get/models/guide</td>
                        <td>List guidance models</td>
                        <td>
                            <ul>
                                <li><code>models</code>: List of guidance model names</li>
                            </ul>
                        </td>
                    </tr>
                    <tr>
                        <td>/v1/api/get/models/flux</td>
                        <td>List Flux models</td>
                        <td>
                            <ul>
                                <li><code>models</code>: List of Flux model names</li>
                            </ul>
                        </td>
                    </tr>
                    <tr>
                        <td>/v1/api/get/models/svi</td>
                        <td>List SVI models</td>
                        <td>
                            <ul>
                                <li><code>models</code>: List of SVI model names</li>
                            </ul>
                        </td>
                    </tr>
                    <tr>
                        <td>/v1/api/get/models/sdxl</td>
                        <td>List SDXL models</td>
                        <td>
                            <ul>
                                <li><code>models</code>: List of SDXL model names</li>
                            </ul>
                        </td>
                    </tr>
                    <tr>
                        <td>/v1/api/get/lora/flux</td>
                        <td>List Flux LoRA presets</td>
                        <td>
                            <ul>
                                <li><code>models</code>: List of Flux LoRA presets</li>
                            </ul>
                        </td>
                    </tr>
                    <tr>
                        <td>/v1/api/get/lora/svi</td>
                        <td>List SVI LoRA presets</td>
                        <td>
                            <ul>
                                <li><code>models</code>: List of SVI LoRA presets</li>
                            </ul>
                        </td>
                    </tr>
                    <tr>
                        <td>/v1/api/get/lora/rt</td>
                        <td>List RT LoRA presets</td>
                        <td>
                            <ul>
                                <li><code>models</code>: List of RT LoRA presets</li>
                            </ul>
                        </td>
                    </tr>
                    <tr>
                        <td>/v1/api/get/styles</td>
                        <td>List style presets</td>
                        <td>
                            <ul>
                                <li><code>styles</code>: List of style presets</li>
                            </ul>
                        </td>
                    </tr>
                    <tr>
                        <td>/v1/api/get/controlnets</td>
                        <td>List ControlNet types</td>
                        <td>
                            <ul>
                                <li><code>controlnets</code>: List of ControlNet types</li>
                            </ul>
                        </td>
                    </tr>
                    <tr>
                        <td>/v1/api/get/gfpgan</td>
                        <td>List GFPGAN versions</td>
                        <td>
                            <ul>
                                <li><code>gfpgan</code>: List of GFPGAN versions</li>
                            </ul>
                        </td>
                    </tr>
                    <tr>
                        <td>/v1/api/get/models/remix</td>
                        <td>List Remix models</td>
                        <td>
                            <ul>
                                <li><code>remix</code>: List of Remix model names</li>
                            </ul>
                        </td>
                    </tr>
                    <tr>
                        <td>/v1/api/get/size</td>
                        <td>List available size ratios</td>
                        <td>
                            <ul>
                                <li><code>size</code>: List of size ratios</li>
                            </ul>
                        </td>
                    </tr>
                    <tr>
                        <td>/v1/api/get/guide/variation</td>
                        <td>List variation strength ranges</td>
                        <td>
                            <ul>
                                <li><code>variation</code>: Variation strength range</li>
                            </ul>
                        </td>
                    </tr>
                    <tr>
                        <td>/v1/api/get/guide/structure</td>
                        <td>List structure guidance ranges</td>
                        <td>
                            <ul>
                                <li><code>structure</code>: Structure guidance range</li>
                            </ul>
                        </td>
                    </tr>
                    <tr>
                        <td>/v1/api/get/guide/facial</td>
                        <td>List facial guidance ranges</td>
                        <td>
                            <ul>
                                <li><code>facial</code>: Facial guidance range</li>
                            </ul>
                        </td>
                    </tr>
                    <tr>
                        <td>/v1/api/get/guide/style</td>
                        <td>List style guidance ranges</td>
                        <td>
                            <ul>
                                <li><code>style</code>: Style guidance range</li>
                            </ul>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
    </div>

    <script>
        function switchTab(tabName) {
            // Update tab buttons
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
                if (tab.textContent.toLowerCase().includes(tabName)) {
                    tab.classList.add('active');
                }
            });

            // Update tab content
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            document.getElementById(`${tabName}-tab`).classList.add('active');
        }

        function openTestDialog() {
            document.getElementById('testDialog').style.display = 'block';
            updateCurlExample();
        }

        function closeTestDialog() {
            document.getElementById('testDialog').style.display = 'none';
            // Reset the grid
            for (let i = 0; i < 4; i++) {
                const container = document.getElementById(`image${i}`);
                container.classList.remove('loading');
                container.querySelector('img').style.display = 'none';
                container.querySelector('img').src = '';
            }
        }
        
        function downloadImage(button) {
                const img = button.parentElement.querySelector('img');
                if (!img.src) return;

                const link = document.createElement('a');
                link.href = img.src;
                link.download = `generated-image-${Date.now()}.png`;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
        }

        async function generateImages() {
            const prompt = document.getElementById('prompt').value;
            if (!prompt) {
                alert('Please enter a prompt');
                return;
            }

            // Reset and show loading for all containers
            for (let i = 0; i < 4; i++) {
                const container = document.getElementById(`image${i}`);
                container.classList.add('loading');
                container.querySelector('img').style.display = 'none';
            }

            // Send 4 parallel requests
            const requests = Array(4).fill().map(() => {
                const formData = new FormData();
                formData.append('prompt', prompt);
                return fetch('/v1/api/realtime/generate', {
                    method: 'POST',
                    body: formData
                }).then(response => response.json());
            });

            // Add helper function for warning message
            function showWarning(container) {
                container.classList.remove('loading');
                container.style.backgroundColor = 'rgb(127, 29, 29)';
                const warning = document.createElement('div');
                warning.className = 'warning';
                warning.innerHTML = `
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
                        <line x1="12" y1="9" x2="12" y2="13"/>
                        <line x1="12" y1="17" x2="12.01" y2="17"/>
                    </svg>
                    <span>Generation failed</span>
                `;
                container.appendChild(warning);
            }

            // Update the error handling in your promises
            requests.forEach((promise, index) => {
                promise.then(data => {
                    const container = document.getElementById(`image${index}`);
                    const img = container.querySelector('img');
                    
                    if (data.success) {
                        img.src = data.result;
                        img.onload = () => {
                            container.classList.remove('loading');
                            img.style.display = 'block';
                        };
                    } else {
                        showWarning(container);
                    }
                }).catch(() => {
                    const container = document.getElementById(`image${index}`);
                    showWarning(container);
                });
            });
        }
    </script>
</body>
</html> 