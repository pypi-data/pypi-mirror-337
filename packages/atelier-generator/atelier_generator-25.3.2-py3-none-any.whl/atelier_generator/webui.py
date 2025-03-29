import gradio as gr
from datetime import datetime
from gradio_modal import Modal

def AtelierWebUI(client, host: str = None, port: int = None, browser: bool = False, upload_size: str = "4MB",
                 public: bool = False, limit: int = 10, quiet: bool = False):
    """ 
    Start Atelier Generator Web UI with all features.
    
    Parameters:
    - client (Client): Atelier Generator instance
    - host (str): Server host
    - port (int): Server port
    - browser (bool): Launch browser automatically
    - upload_size (str): Maximum file size for uploads
    - public (bool): Enable public URL mode
    - limit (int): Maximum number of concurrent requests
    """
    try:
        ime_size         = client.list_atr_size
        ime_remix_model  = client.list_atr_remix_model
        ime_controlnets  = client.list_atr_controlnets
        ime_lora         = client.list_atr_lora_rt
        atr_models       = client.list_atr_models
        atr_models_guide = client.list_atr_models_guide
        atr_models_svi   = client.list_atr_models_svi
        atr_lora_svi     = client.list_atr_lora_svi
        atr_lora_flux    = client.list_atr_lora_flux
        atr_size         = client.list_atr_size
        atr_g_variation  = client.list_atr_g_variation
        atr_g_structure  = client.list_atr_g_structure
        atr_g_facial     = client.list_atr_g_facial
        atr_g_style      = client.list_atr_g_style
        sty_styles       = client.list_atr_styles

        system_theme = gr.themes.Default(
            primary_hue=gr.themes.colors.rose,
            secondary_hue=gr.themes.colors.rose,
            neutral_hue=gr.themes.colors.zinc
        )

        css = '''
        ::-webkit-scrollbar {
            display: none;
        }

        ::-webkit-scrollbar-button {
            display: none;
        }

        body {
            background-color: #000000;
            background-image: linear-gradient(45deg, #111111 25%, #000000 25%, #000000 50%, #111111 50%, #111111 75%, #000000 75%, #000000 100%);
            background-size: 40px 40px;
            -ms-overflow-style: none;
        }

        gradio-app {
            --body-background-fill: None;
        }
        footer {
            display: none !important;
        }

        .app.svelte-182fdeq.svelte-182fdeq {
            padding: 0px;
        }

        .grid-wrap.svelte-hpz95u.svelte-hpz95u {
            overflow-y: auto;
        }


        .image-frame.svelte-rrgd5g img {
            object-fit: contain;
        }

        .image-container.svelte-1l6wqyv {
            height: 100%;
        }

        .grid-container.svelte-eynlr2.svelte-eynlr2 {
            grid-template-rows: repeat(auto-fit, minmax(200px, 1fr));
            grid-template-columns: repeat(auto-fit, minmax(200px, 0.505fr));
        }

        .wrap.svelte-1sbaaot {
            align-items: inherit;
        }

        .wrap.svelte-z7cif2.svelte-z7cif2 {
            z-index: 100;
            max-height: 100%;
        }

        .stage-wrap.svelte-1sbaaot {
            transform: translate(0px, 266px);
        }

        button.svelte-1uw5tnk {
            margin-bottom: 8px;
            width: 192px;
            padding: 8px;
            border-radius: var(--container-radius);
        }

        .selected.svelte-1uw5tnk {
            background: var(--button-cancel-background-fill);
            color: var(--button-cancel-text-color);
            border-radius: 10px;
            border: none;
            position: relative;
            overflow: hidden;
        }

        .tab-nav.svelte-1uw5tnk {
            justify-content: space-evenly;
            border: 0px;
        }

        div.svelte-19hvt5v {
            border-radius: 10px;
            margin-top: 12px;
            border: 1px solid var(--border-color-primary);
        }

        input[type=range].svelte-pc1gm4 {
            background-image: linear-gradient(var(--color-accent), var(--color-accent));
        }

        .thumbnails.svelte-eynlr2.svelte-eynlr2 {
            align-items: center;
            gap: 10px;
            padding-left: 10px;
            padding-right: 10px;
        }

        .icon.svelte-1oiin9d {
            display: none;
        }

        .caption-label.svelte-eynlr2.svelte-eynlr2 {
            display: none;
        }

        input[type=number].svelte-pjtc3.svelte-pjtc3 {
            line-height: 0px;
        }
        
        /* Touch device optimizations */
        @media (hover: none) {
            button, input, select {
                min-height: 44px;
            }
        }

        /* Prevent zoom on input focus for iOS */
        @media screen and (-webkit-min-device-pixel-ratio: 0) { 
            select,
            textarea,
            input {
                font-size: 16px;
            }
        }
        '''

        def Markdown(name:str):
            return gr.Markdown(f"{name}")

        def Textbox(name:str, lines:int=1, max_lines:int=4):
            return gr.Textbox(placeholder=f"{name}", lines=lines, max_lines=max_lines, container=False)

        def Slider(min:int, max:int, step:float, value:int, label:str=None):
            return gr.Number(value=value, minimum=min, maximum=max, step=step, label=label)

        def Dropdown(choices:list, value:str, label:str=None):
            return gr.Dropdown(choices=choices, value=value, label=label, container=False if label is None else True)

        def Checkbox(name:str, value:bool):
            return gr.Checkbox(value=value, label=name, min_width=96)

        def Button(name:str, variant:str='secondary'):
            return gr.Button(name, variant=variant, min_width=96)

        def Number(name:str, value:int, min:int, step:float=0.01):
            return gr.Number(value=value, minimum=min, step=step, label=name)

        def Image(name:str, sources:list, height:int):
            return gr.Image(type="filepath", height=height, sources=sources, label=name)

        def Gallery(height:int):
            return gr.Gallery(height=height, object_fit="contain", container=False, show_share_button=False)

        def State(name:list):
            return gr.State(name)

        def ImageMask():
            return gr.ImageMask(
                            height="80%",
                            type="pil",
                            layers=False,
                            container=False,
                            transforms=[],
                            sources=["upload"],
                            brush=gr.Brush(default_size=24, colors=["#ffffff"], color_mode="fixed"),
                            eraser=gr.Eraser(default_size=24),
                        )

        def Paint():
            return gr.ImageEditor(
                            height="80%",
                            type="pil",
                            container=False,
                            transforms=['crop'],
                            sources=['upload', 'webcam', 'clipboard'],
                            crop_size='1:1',
                            brush=gr.Brush(default_size=24, color_mode="defaults"),
                            eraser=gr.Eraser(default_size=24),
                            layers=False
                        )
        
        def truncate_prompt(prompt, max_length=50):
            if prompt is None or prompt == "":
                return "No Prompt"
            return (prompt[:max_length] + '...') if len(prompt) > max_length else prompt        
        
        js_func = """
        function refresh() {
            const url = new URL(window.location);
            url.searchParams.set('__theme', url.searchParams.get('__theme') === 'dark' || !url.searchParams.get('__theme') ? 'light' : 'dark');
            window.location.href = url.href;
        }
        """
                
        with gr.Blocks(title=f"Atelier Generator", css=css, analytics_enabled=False, theme=system_theme, fill_height=True).queue(default_concurrency_limit=limit) as demo:
            
            with gr.Row():
                with gr.Column(scale=1):
                    Markdown(f"## <br><center>Atelier Generator Web UI")
                    Markdown(f"<center>Copyright (C) {datetime.now().year} Ikmal Said. All rights reserved")
                
                # with gr.Column(scale=0):
                #     ToggleDM = Button("Toggle Dark Mode")
                #     ToggleDM.click(fn=None, inputs=None, outputs=None, js=js_func)

            with gr.Tab("Image Generator"):
                
                def f15a_preprocess(f15a_pro, f15a_neg, f15a_mod, f15a_siz, f15a_svi, f15a_flux, f15a_sed, f15a_sty, f15a_ram):
                    caption = f"{truncate_prompt(f15a_pro)} | Model: {f15a_mod} | Size: {f15a_siz} | Style: {f15a_sty} | SVI LoRA: {f15a_svi} | Flux LoRA: {f15a_flux} | Seed: {f15a_sed}"
                    results = client.image_generate(f15a_pro, f15a_neg, f15a_mod, f15a_siz, f15a_svi, f15a_flux, f15a_sed, f15a_sty)
                    if results is not None:
                        f15a_ram.insert(0, (results, caption))
                    return f15a_ram
                
                with gr.Row(equal_height=False):
                    with gr.Column(variant="panel", scale=1) as menu:
                        Markdown("## <center>Image Generator")
                        Markdown("<center>Basic Settings")
                        f15a_pro = Textbox("Prompt for image...")
                        f15a_neg = Textbox("Negative prompt...")
                        
                        Markdown("<center>Advanced Settings")
                        with gr.Row():
                            f15a_mod = Dropdown(atr_models, atr_models[0], label="Model Selection")
                            f15a_siz = Dropdown(atr_size, atr_size[0], label="Image Size")
                        with gr.Row():
                            f15a_svi = Dropdown(atr_lora_svi, atr_lora_svi[0], label="SVI LoRA")
                            f15a_flux = Dropdown(atr_lora_flux, atr_lora_flux[0], label="Flux LoRA")
                        
                        f15a_sed = Number("Seed (0 Random | -1 CPU)", 0, -1, 1)

                        Markdown("<center>Style Presets")
                        f15a_sty = Dropdown(sty_styles, sty_styles[0])
                        
                        with gr.Row():
                            f15a_sub = Button("Generate", "stop")
                        
                    with gr.Column(variant="panel", scale=3) as result:
                        f15a_res = Gallery(885.938)
                        f15a_ram = State([])
                        f15a_sub.click(
                            show_progress='minimal',
                            show_api=False,
                            scroll_to_output=True,
                            fn=f15a_preprocess,
                            inputs=[f15a_pro, f15a_neg, f15a_mod, f15a_siz, f15a_svi, f15a_flux, f15a_sed, f15a_sty, f15a_ram],
                            outputs=[f15a_res]
                        )    

            with gr.Tab("Image Variation"):
                def f15b_preprocess(f15b_img, f15b_pro, f15b_neg, f15b_mod, f15b_siz, f15b_gst, f15b_svi, f15b_flux, f15b_sed, f15b_sty, f15b_ram):
                    caption = f"{truncate_prompt(f15b_pro)} | Model: {f15b_mod} | Size: {f15b_siz} | Style: {f15b_sty}"
                    results = client.image_variation(f15b_img, f15b_pro, f15b_neg, f15b_mod, f15b_siz, 
                                            f15b_gst, f15b_svi, f15b_flux, f15b_sed, f15b_sty)
                    if results is not None:
                        f15b_ram.insert(0, (results, caption))
                    return f15b_ram
                
                with gr.Row(equal_height=False):
                    with gr.Column(variant="panel", scale=1) as menu:
                        Markdown("## <center>Image Variation")
                        Markdown("<center>Basic Settings")
                        f15b_img = Image("Upload Image", ["upload"], 150)
                        f15b_pro = Textbox("Prompt for image...")
                        f15b_neg = Textbox("Negative prompt...")

                        Markdown("<center>Advanced Settings")
                        with gr.Group():
                            with gr.Row():
                                f15b_mod = Dropdown(atr_models_guide, atr_models_guide[0], label="Model Selection")
                                f15b_siz = Dropdown(atr_size, atr_size[0], label="Image Size")
                            f15b_gst = Dropdown(atr_g_variation, atr_g_variation[0], label="Guide Strength")
                            with gr.Row():
                                f15b_svi = Dropdown(atr_lora_svi, atr_lora_svi[0], label="SVI LoRA")
                                f15b_flux = Dropdown(atr_lora_flux, atr_lora_flux[0], label="Flux LoRA")
                        
                        f15b_sed = Number("Seed (0 Random | -1 CPU)", 0, -1, 1)

                        Markdown("<center>Style Presets")
                        f15b_sty = Dropdown(sty_styles, sty_styles[0])
                        f15b_sub = Button("Generate", "stop")
                        
                    with gr.Column(variant="panel", scale=3) as result:
                        f15b_res = Gallery(961.344)
                        f15b_ram = State([])
                        f15b_sub.click(
                            show_progress='minimal',
                            show_api=False,
                            scroll_to_output=True,
                            fn=f15b_preprocess,
                            inputs=[f15b_img, f15b_pro, f15b_neg, f15b_mod, f15b_siz, f15b_gst, f15b_svi, f15b_flux, f15b_sed, f15b_sty, f15b_ram],
                            outputs=[f15b_res]
                        )

            with gr.Tab("Image Structure"):
                def f15c_preprocess(f15c_img, f15c_pro, f15c_neg, f15c_mod, f15c_siz, f15c_gst, f15c_svi, f15c_sed, f15c_sty, f15c_ram):
                    caption = f"{truncate_prompt(f15c_pro)} | Model: {f15c_mod} | Size: {f15c_siz} | Style: {f15c_sty}"
                    results = client.image_structure(f15c_img, f15c_pro, f15c_neg, f15c_mod, f15c_siz,
                                            f15c_gst, f15c_svi, f15c_sed, f15c_sty)
                    if results is not None:
                        f15c_ram.insert(0, (results, caption))
                    return f15c_ram
                
                with gr.Row(equal_height=False):
                    with gr.Column(variant="panel", scale=1) as menu:
                        Markdown("## <center>Image Structure")
                        Markdown("<center>Basic Settings")
                        f15c_img = Image("Upload Image", ["upload"], 150)
                        f15c_pro = Textbox("Prompt for image...")
                        f15c_neg = Textbox("Negative prompt...")

                        Markdown("<center>Advanced Settings")
                        with gr.Group():
                            with gr.Row():
                                f15c_mod = Dropdown(atr_models_svi, atr_models_svi[0], label="Model Selection")
                                f15c_siz = Dropdown(atr_size, atr_size[0], label="Image Size")
                            with gr.Row():
                                f15c_gst = Dropdown(atr_g_structure, atr_g_structure[0], label="Guide Strength")
                                f15c_svi = Dropdown(atr_lora_svi, atr_lora_svi[0], label="SVI LoRA")
                        
                        f15c_sed = Number("Seed (0 Random | -1 CPU)", 0, -1, 1)

                        Markdown("<center>Style Presets")
                        f15c_sty = Dropdown(sty_styles, sty_styles[0])
                        f15c_sub = Button("Generate", "stop")
                        
                    with gr.Column(variant="panel", scale=3) as result:
                        f15c_res = Gallery(961.344)
                        f15c_ram = State([])
                        f15c_sub.click(
                            show_progress='minimal',
                            show_api=False,
                            scroll_to_output=True,
                            fn=f15c_preprocess,
                            inputs=[f15c_img, f15c_pro, f15c_neg, f15c_mod, f15c_siz, f15c_gst, f15c_svi, f15c_sed, f15c_sty, f15c_ram],
                            outputs=[f15c_res]
                        )

            with gr.Tab("Image Facial"):
                def f15d_preprocess(f15d_img, f15d_pro, f15d_neg, f15d_mod, f15d_siz, f15d_gst, f15d_svi, f15d_sed, f15d_sty, f15d_ram):
                    caption = f"{truncate_prompt(f15d_pro)} | Model: {f15d_mod} | Size: {f15d_siz} | Style: {f15d_sty}"
                    results = client.image_facial(f15d_img, f15d_pro, f15d_neg, f15d_mod, f15d_siz,
                                        f15d_gst, f15d_svi, f15d_sed, f15d_sty)
                    if results is not None:
                        f15d_ram.insert(0, (results, caption))
                    return f15d_ram
                
                with gr.Row(equal_height=False):
                    with gr.Column(variant="panel", scale=1) as menu:
                        Markdown("## <center>Image Facial")
                        Markdown("<center>Basic Settings")
                        f15d_img = Image("Upload Image", ["upload"], 150)
                        f15d_pro = Textbox("Prompt for image...")
                        f15d_neg = Textbox("Negative prompt...")

                        Markdown("<center>Advanced Settings")
                        with gr.Group():
                            with gr.Row():
                                f15d_mod = Dropdown(atr_models_svi, atr_models_svi[0], label="Model Selection")
                                f15d_siz = Dropdown(atr_size, atr_size[0], label="Image Size")
                            with gr.Row():
                                f15d_gst = Dropdown(atr_g_facial, atr_g_facial[0], label="Guide Strength")
                                f15d_svi = Dropdown(atr_lora_svi, atr_lora_svi[0], label="SVI LoRA")
                        
                        f15d_sed = Number("Seed (0 Random | -1 CPU)", 0, -1, 1)

                        Markdown("<center>Style Presets")
                        f15d_sty = Dropdown(sty_styles, sty_styles[0])
                        f15d_sub = Button("Generate", "stop")
                        
                    with gr.Column(variant="panel", scale=3) as result:
                        f15d_res = Gallery(961.344)
                        f15d_ram = State([])
                        f15d_sub.click(
                            show_progress='minimal',
                            show_api=False,
                            scroll_to_output=True,
                            fn=f15d_preprocess,
                            inputs=[f15d_img, f15d_pro, f15d_neg, f15d_mod, f15d_siz, f15d_gst, f15d_svi, f15d_sed, f15d_sty, f15d_ram],
                            outputs=[f15d_res]
                        )

            with gr.Tab("Image Style"):
                def f15e_preprocess(f15e_img, f15e_pro, f15e_neg, f15e_mod, f15e_siz, f15e_gst, f15e_svi, f15e_sed, f15e_sty, f15e_ram):
                    caption = f"{truncate_prompt(f15e_pro)} | Model: {f15e_mod} | Size: {f15e_siz} | Style: {f15e_sty}"
                    results = client.image_style(f15e_img, f15e_pro, f15e_neg, f15e_mod, f15e_siz,
                                        f15e_gst, f15e_svi, f15e_sed, f15e_sty)
                    if results is not None:
                        f15e_ram.insert(0, (results, caption))
                    return f15e_ram
                
                with gr.Row(equal_height=False):
                    with gr.Column(variant="panel", scale=1) as menu:
                        Markdown("## <center>Image Style")
                        Markdown("<center>Basic Settings")
                        f15e_img = Image("Upload Image", ["upload"], 150)
                        f15e_pro = Textbox("Prompt for image...")
                        f15e_neg = Textbox("Negative prompt...")

                        Markdown("<center>Advanced Settings")
                        with gr.Group():
                            with gr.Row():
                                f15e_mod = Dropdown(atr_models_svi, atr_models_svi[0], label="Model Selection")
                                f15e_siz = Dropdown(atr_size, atr_size[0], label="Image Size")
                            with gr.Row():
                                f15e_gst = Dropdown(atr_g_style, atr_g_style[0], label="Guide Strength")
                                f15e_svi = Dropdown(atr_lora_svi, atr_lora_svi[0], label="SVI LoRA")
                        
                        f15e_sed = Number("Seed (0 Random | -1 CPU)", 0, -1, 1)

                        Markdown("<center>Style Presets")
                        f15e_sty = Dropdown(sty_styles, sty_styles[0])
                        f15e_sub = Button("Generate", "stop")
                        
                    with gr.Column(variant="panel", scale=3) as result:
                        f15e_res = Gallery(961.344)
                        f15e_ram = State([])
                        f15e_sub.click(
                            show_progress='minimal',
                            show_api=False,
                            scroll_to_output=True,
                            fn=f15e_preprocess,
                            inputs=[f15e_img, f15e_pro, f15e_neg, f15e_mod, f15e_siz, f15e_gst, f15e_svi, f15e_sed, f15e_sty, f15e_ram],
                            outputs=[f15e_res]
                        )

            with gr.Tab("Image Controlnet"):
                
                def f2_preprocess(f2_img, f2_pro, f2_neg, f2_mod, f2_con, f2_str, f2_sca, f2_sed, f2_sty, f2_ram):
                    caption = f"{truncate_prompt(f2_pro)} | Model: {f2_mod} | Control: {f2_con} | Style: {f2_sty}"
                    results = client.image_controlnet(f2_img, f2_pro, f2_neg, f2_mod, f2_con, f2_str, f2_sca, f2_sed, f2_sty)
                    if results is not None:
                        f2_ram.insert(0, (results, caption))
                    return f2_ram

                with gr.Row(equal_height=False):
                    with gr.Column(variant="panel", scale=1) as menu:
                        Markdown("## <center>Image Controlnet")
                        Markdown("<center>Basic Settings")
                        f2_img = Image("Upload Image", ["upload"], 199)
                        f2_pro = Textbox("Prompt for image...")
                        f2_neg = Textbox("Negative prompt...")
                    
                        Markdown("<center>Advanced Settings")
                        with gr.Row():
                            f2_mod = Dropdown(ime_remix_model, ime_remix_model[0], label="Model Selection")
                            f2_con = Dropdown(ime_controlnets, ime_controlnets[0], label="Control Type")
                        with gr.Row():
                            f2_str = Slider(0, 100, 1, 70, "Controlnet Strength")
                            f2_sca = Slider(3, 15, 0.5, 9, "Prompt Scale")
                            
                        f2_sed = Number("Seed (0 Random | -1 CPU)", 0, -1, 1)
                        
                        Markdown("<center>Style Presets")
                        f2_sty = Dropdown(sty_styles, sty_styles[0])
                        f2_sub = Button("Generate", "stop")
                        
                    with gr.Column(variant="panel", scale=3) as result:
                        f2_res = Gallery(898.344)
                        f2_ram = State([])
                        
                        f2_sub.click(
                            show_progress='minimal',
                            show_api=False,
                            scroll_to_output=True,
                            fn=f2_preprocess,
                            inputs=[f2_img, f2_pro, f2_neg, f2_mod, f2_con, f2_str, f2_sca, f2_sed, f2_sty, f2_ram],
                            outputs=[f2_res]
                        )    
                        
            with gr.Tab("Image Toolkit"):
                
                def f4_preprocess(f4_img, f4_ram):
                    caption = "Upscaled Image"
                    results = client.image_upscale(f4_img)
                    if results is not None:
                        f4_ram.insert(0, (results, caption))
                    return f4_ram
                
                def f4a_preprocess(f4_img, f4_ram):
                    caption = "Restored Image"
                    results = client.face_codeformer(f4_img)
                    if results is not None:
                        f4_ram.insert(0, (results, caption))
                    return f4_ram
                
                def f5_preprocess(f4_img, f4_ram):
                    caption = "Background Removed"
                    results = client.image_bgremove(f4_img)
                    if results is not None:
                        f4_ram.insert(0, (results, caption))
                    return f4_ram

                def f4d_preprocess(f4_img, f4d_typ, f4_ram):
                    caption = f"Face Restored | Model: {f4d_typ}"
                    results = client.face_gfpgan(f4_img, f4d_typ)
                    if results is not None:
                        f4_ram.insert(0, (results, caption))
                    return f4_ram
                
                with gr.Row(equal_height=False):
                    with gr.Column(variant="panel", scale=1) as menu:
                        Markdown("## <center>Image Toolkit")
                        f4_img = Image("Upload Image", ["upload"], 199)
                        
                        Markdown("<center>Face Restoration")
                        f4d_typ = Dropdown(client.list_atr_gfpgan, client.list_atr_gfpgan[0], label="Model Selection")
                        f4d_sub = Button("Restore Face", "stop")
                        
                        Markdown("<center>Available Tools")
                        f5_sub = Button("Remove Background")
                        f4a_sub = Button("Upscale Image")
                        f4b_sub = Button("Restore Image")
                        f4c_sub = Button("Caption Image")
                        f6_sub = Button("Prompt Image")

                    with gr.Column(variant="panel", scale=3) as result:
                        f4_ram = State([])
                        f4_res = Gallery(606.406)
                        f6_res = Textbox("Upload an image to get a caption...", 5, 5)
                        f6a_res = Textbox("Upload an image to get a prompt...", 5, 5)
                        
                        f4a_sub.click(
                            show_progress='minimal',
                            show_api=False,
                            scroll_to_output=True,
                            fn=f4_preprocess,
                            inputs=[f4_img, f4_ram],
                            outputs=[f4_res] 
                        )
                        
                        f4b_sub.click(
                            show_progress='minimal',
                            show_api=False,
                            scroll_to_output=True,
                            fn=f4a_preprocess,
                            inputs=[f4_img, f4_ram],
                            outputs=[f4_res] 
                        )
                        
                        f4c_sub.click(
                            show_progress='minimal',
                            show_api=False,
                            scroll_to_output=True,
                            fn=client.image_caption,
                            inputs=[f4_img],
                            outputs=[f6_res] 
                        ) 
                        
                        f5_sub.click(
                            show_progress='minimal',
                            show_api=False,
                            scroll_to_output=True,
                            fn=f5_preprocess,
                            inputs=[f4_img, f4_ram],
                            outputs=[f4_res] 
                        )
                        
                        f6_sub.click(
                            show_progress='minimal',
                            show_api=False,
                            scroll_to_output=True,
                            fn=client.image_prompt,
                            inputs=[f4_img],
                            outputs=[f6a_res] 
                        )
                        
                        f4d_sub.click(
                            show_progress='minimal',
                            show_api=False,
                            scroll_to_output=True,
                            fn=f4d_preprocess,
                            inputs=[f4_img, f4d_typ, f4_ram],
                            outputs=[f4_res]
                        )      
                
            with gr.Tab("Image Enhance"):
                
                def f7_preprocess(f7_img, f7_pro, f7_neg, f7_cre, f7_rsm, f7_hdr, f7_sty, f7_ram):
                    caption = f"{truncate_prompt(f7_pro)} | Creativity: {f7_cre:.2f} | Resemblance: {f7_rsm:.2f} | Style: {f7_sty}"
                    results = client.image_enhance(f7_img, f7_pro, f7_neg, f7_cre, f7_rsm, f7_hdr, f7_sty)
                    if results is not None:
                        f7_ram.insert(0, (results, caption))
                    return f7_ram
                
                with gr.Row(equal_height=False):
                    with gr.Column(variant="panel", scale=1) as menu:
                        Markdown("## <center>Image Enhance")
                        Markdown("<center>Basic Settings")
                        f7_img = Image("Upload Image", ["upload"], 199)
                        f7_pro = Textbox("Prompt for image...", lines=1)
                        f7_neg = Textbox("Negative prompt...", lines=1)
                    
                        Markdown("<center>Advanced Settings")
                        with gr.Row():
                            f7_cre = Slider(0.2, 1.0, 0.05, 0.3, "Creativity Strength")
                            f7_rsm = Slider(0.0, 1.0, 0.05, 1.0, "Resemblance Strength")
                        with gr.Row():
                            f7_hdr = Slider(0.0, 1.0, 0.05, 0.0, "HDR Strength")
                        
                        Markdown("<center>Style Presets")
                        f7_sty = Dropdown(sty_styles, sty_styles[0])
                        f7_sub = Button("Generate", "stop")

                    with gr.Column(variant="panel", scale=3) as result:
                        f7_res = Gallery(885.938)
                        f7_ram = State([])
                        f7_sub.click(
                            show_progress='minimal',
                            show_api=False,
                            scroll_to_output=True,
                            fn=f7_preprocess,
                            inputs=[f7_img, f7_pro, f7_neg, f7_cre, f7_rsm, f7_hdr, f7_sty, f7_ram],
                            outputs=[f7_res]
                        )            
                
            with gr.Tab("Object Eraser"):
                
                def f8_preprocess(f8_mas, f8_ram):
                    caption = f"Object Erased"
                    results = client.image_erase(f8_mas)
                    if results is not None:
                        f8_ram.insert(0, (results, caption))
                    return f8_ram
                
                with gr.Row(equal_height=False):
                    with gr.Column(variant="panel", scale=1) as menu:
                        Markdown("## <center>Object Eraser")
                        
                        f8_img = Image("Canvas Image", [], 250)
                        with Modal(visible=False) as f8_m1:
                            f8_mas = ImageMask()
                            f8_mas.change(fn=lambda x: x["composite"], inputs=f8_mas, outputs=f8_img)
                            f8_clo = Button("Close Canvas").click(lambda: Modal(visible=False), None, f8_m1)
                        f8_ope = Button("Open Canvas").click(lambda: Modal(visible=True), None, f8_m1)
                    
                        f8_sub = Button("Erase Object", "stop")
                    
                    with gr.Column(variant="panel", scale=3) as result:
                        f8_res = Gallery(885.938)
                        f8_ram = State([])
                        f8_sub.click(
                            show_progress='minimal',
                            show_api=False,
                            scroll_to_output=True,
                            fn=f8_preprocess,
                            inputs=[f8_mas, f8_ram],
                            outputs=[f8_res]
                        ) 
                                
            with gr.Tab("Generative Fill"):
                
                def f9_preprocess(f9_mas, f9_pro, f9_sty, f9_ram):
                    caption = f"{truncate_prompt(f9_pro)} | Style: {f9_sty}"
                    results = client.image_inpaint(f9_mas, f9_pro, None, f9_sty)
                    if results is not None:
                        f9_ram.insert(0, (results, caption))
                    return f9_ram
                
                with gr.Row(equal_height=False):
                    with gr.Column(variant="panel", scale=1) as menu:
                        Markdown("## <center>Generative Fill")
                        Markdown("<center>Basic Settings")
                                
                        f9_img = Image("Canvas Image", [], 199)
                        with Modal(visible=False) as f9_m1:
                            f9_mas = ImageMask()
                            f9_mas.change(fn=lambda x: x["composite"], inputs=f9_mas, outputs=f9_img)
                            f9_clo = Button("Close Canvas").click(lambda: Modal(visible=False), None, f9_m1)
                        f9_ope = Button("Open Canvas").click(lambda: Modal(visible=True), None, f9_m1)
                        
                        f9_pro = Textbox("Prompt for image...")

                        Markdown("<center>Style Presets")
                        f9_sty = Dropdown(sty_styles, sty_styles[0])
                        f9_sub = Button("Inpaint Image", "stop")
                        
                    with gr.Column(variant="panel", scale=3) as result:
                        f9_res = Gallery(885.938)
                        f9_ram = State([])
                        f9_sub.click(
                            show_progress='minimal',
                            show_api=False,
                            scroll_to_output=True,
                            fn=f9_preprocess,
                            inputs=[f9_mas, f9_pro, f9_sty, f9_ram],
                            outputs=[f9_res]
                        )

            with gr.Tab("RT Generator"):
                
                def f10_preprocess(f10_pro, f10_neg, f10_siz, f10_lra, f10_sed, f10_sty, f10_ram):
                    caption = f"{truncate_prompt(f10_pro)} | Size: {f10_siz} | LoRA: {f10_lra} | Style: {f10_sty}"
                    results = client.realtime_generate(f10_pro, f10_neg, f10_siz, f10_lra, f10_sed, f10_sty)
                    if results is not None:
                        f10_ram.insert(0, (results, caption))
                    return f10_ram
                
                with gr.Row(equal_height=False):
                    with gr.Column(variant="panel", scale=1) as menu:
                        Markdown("## <center>RT Image Generator")
                        Markdown("<center>Basic Settings")
                        f10_pro = Textbox("Prompt for image...")
                        f10_neg = Textbox("Negative prompt...")
                        
                        Markdown("<center>Advanced Settings")
                        with gr.Row():
                            f10_lra = Dropdown(ime_lora, ime_lora[0], label="LoRA Model")
                            f10_siz = Dropdown(ime_size, ime_size[0], label="Image Size")
                        
                        f10_sed = Number("Seed (0 Random | -1 CPU)", 0, -1, 1)
                        
                        Markdown("<center>Style Presets")
                        f10_sty = Dropdown(sty_styles, sty_styles[0])
                        f10_sub = Button("Generate", "stop")

                    with gr.Column(variant="panel", scale=3) as result:
                        f10_res = Gallery(885.938)
                        f10_ram = State([])
                        f10_sub.click(
                            show_progress='minimal',
                            show_api=False,
                            scroll_to_output=True,
                            fn=f10_preprocess,
                            inputs=[f10_pro, f10_neg, f10_siz, f10_lra, f10_sed, f10_sty, f10_ram],
                            outputs=[f10_res]
                        )

            with gr.Tab("RT Canvas"):
                
                def f11_preprocess(f11_img, f11_pro, f11_neg, f11_lra, f11_str, f11_sed, f11_sty, f11_ram):
                    caption = f"{truncate_prompt(f11_pro)} | LoRA: {f11_lra} | Strength: {f11_str:.2f} | Style: {f11_sty}"
                    results = client.realtime_canvas(f11_img, f11_pro, f11_neg, f11_lra, f11_str, f11_sed, f11_sty)
                    if results is not None:
                        f11_ram.insert(0, (results, caption))
                    return f11_ram
                
                with gr.Row(equal_height=False):
                    with gr.Column(variant="panel", scale=1) as menu:
                        Markdown("## <center>RT Canvas")
                        Markdown("<center>Basic Settings")
                        
                        f11_img = Image("Canvas Image", ['upload'], 199)
                        with Modal(visible=False) as f11_m1:
                            f11_can = Paint()
                            f11_can.change(fn=lambda x: x["composite"], inputs=f11_can, outputs=f11_img)
                            f11_clo = Button("Close Canvas").click(lambda: Modal(visible=False), None, f11_m1)
                        f11_ope = Button("Open Canvas").click(lambda: Modal(visible=True), None, f11_m1)
                        
                        f11_pro = Textbox("Prompt for image...", lines=1)
                        f11_neg = Textbox("Negative prompt...", lines=1)
                        
                        Markdown("<center>Advanced Settings")
                        with gr.Row():
                            f11_lra = Dropdown(ime_lora, ime_lora[0], label="LoRA Model")
                            f11_str = Slider(0.0, 1.0, 0.1, 1, "Creativity Strength")
                        
                        f11_sed = Number("Seed (0 Random | -1 CPU)", 0, -1, 1)
                        
                        Markdown("<center>Style Presets")
                        f11_sty = Dropdown(sty_styles, sty_styles[0])
                        f11_sub = Button("Generate", "stop")
                    
                    with gr.Column(variant="panel", scale=3) as result:
                        f11_res = Gallery(885.938)
                        f11_ram = State([])
                        
                        f11_sub.click(
                            show_progress='minimal',
                            show_api=False,
                            scroll_to_output=True,
                            fn=f11_preprocess,
                            inputs=[f11_img, f11_pro, f11_neg, f11_lra, f11_str, f11_sed, f11_sty, f11_ram],
                            outputs=[f11_res]
                        )  

            with gr.Tab("Image Outpaint"):
                def f12_preprocess(f12_img, f12_siz, f12_ram):
                    caption = f"Image Outpaint | Size: {f12_siz}"
                    results = client.image_outpaint(f12_img, f12_siz)
                    if results is not None:
                        f12_ram.insert(0, (results, caption))
                    return f12_ram
                
                with gr.Row(equal_height=False):
                    with gr.Column(variant="panel", scale=1) as menu:
                        Markdown("## <center>Image Outpaint")
                        Markdown("<center>Basic Settings")
                        f12_img = Image("Upload Image", ["upload"], 199)
                    
                        Markdown("<center>Advanced Settings")
                        f12_siz = Dropdown(atr_size, atr_size[0], label="Image Size")
                        f12_sub = Button("Generate", "stop")
                        
                    with gr.Column(variant="panel", scale=3) as result:
                        f12_res = Gallery(885.938)
                        f12_ram = State([])
                        f12_sub.click(
                            show_progress='minimal',
                            show_api=False,
                            scroll_to_output=True,
                            fn=f12_preprocess,
                            inputs=[f12_img, f12_siz, f12_ram],
                            outputs=[f12_res]
                        )
            
            Markdown("<center>Atelier can make mistakes. Check important info. Request errors will return None.")
            Markdown("<center>")

        demo.launch(
            server_name=host,
            server_port=port,
            inbrowser=browser,
            max_file_size=upload_size,
            share=public,
            quiet=quiet
        )
        
    except Exception as e:
        client.logger.error(f"{str(e)}")
        raise