from flask import Flask, request, jsonify, render_template
from io import BytesIO
import base64

def AtelierWebAPI(client, host: str = None, port: int = None, debug: bool = False):
    """
    Start Atelier Generator API server with all endpoints.
    
    Parameters:
    - client (Client): Atelier Generator instance
    - host (str): Host to run the server on
    - port (int): Port to run the server on
    - debug (bool): Enable Flask debug mode
    """
    try:
        app = Flask(__name__)

        def __data_url_processor(pil_image) -> str:
            """Convert PIL Image to base64 data URL."""
            try:
                img_io = BytesIO()
                pil_image.save(img_io, format='WEBP', quality=90)
                img_io.seek(0)
                img_base64 = base64.b64encode(img_io.getvalue()).decode()
                
                client.logger.info(f"Created data URL from PIL object!")
                return f"data:image/png;base64,{img_base64}"
            
            except Exception as e:
                client.logger.error(f"Error in data_url_processor: {e}")
                return None

        # Index Endpoint
        @app.route('/', methods=['GET'])
        def api_index():
            """Render the API documentation page"""
            try:
                return render_template('index.py')
            
            except Exception as e:
                client.logger.error(f"Error in api_index: {e}")
                return jsonify({"success": False, "error": str(e)}), 400

        # Data Endpoints
        @app.route('/v1/api/get/models', methods=['GET'])
        def list_models_api():
            """
            Handle model list requests.
            """
            try:
                return jsonify({"success": True, "models": client.list_atr_models})
            
            except Exception as e:
                client.logger.error(f"Error in list_models_api: {e}")
                return jsonify({"success": False, "error": str(e)}), 400
        
        @app.route('/v1/api/get/models/guide', methods=['GET'])
        def list_models_guide_api():
            """
            Handle guidance model list requests.
            """
            try:
                return jsonify({"success": True, "models": client.list_atr_models_guide})
            
            except Exception as e:
                client.logger.error(f"Error in list_models_guide_api: {e}")
                return jsonify({"success": False, "error": str(e)}), 400

        @app.route('/v1/api/get/models/flux', methods=['GET'])
        def list_models_flux_api():
            """
            Handle Flux model list requests.
            """
            try:
                return jsonify({"success": True, "models": client.list_atr_models_flux})
            
            except Exception as e:
                client.logger.error(f"Error in list_models_flux_api: {e}")
                return jsonify({"success": False, "error": str(e)}), 400

        @app.route('/v1/api/get/models/svi', methods=['GET'])
        def list_models_svi_api():
            """
            Handle SVI model list requests.
            """
            try:
                return jsonify({"success": True, "models": client.list_atr_models_svi})
            
            except Exception as e:
                client.logger.error(f"Error in list_models_svi_api: {e}")
                return jsonify({"success": False, "error": str(e)}), 400

        @app.route('/v1/api/get/models/sdxl', methods=['GET'])
        def list_models_sdxl_api():
            """
            Handle SDXL model list requests.
            """
            try:
                return jsonify({"success": True, "models": client.list_atr_models_sdxl})
            
            except Exception as e:
                client.logger.error(f"Error in list_models_sdxl_api: {e}")
                return jsonify({"success": False, "error": str(e)}), 400
        
        @app.route('/v1/api/get/lora/flux', methods=['GET'])
        def list_lora_flux_api():
            """
            Handle Flux LoRA list requests.
            """
            try:
                return jsonify({"success": True, "models": client.list_atr_lora_flux})
            
            except Exception as e:
                client.logger.error(f"Error in list_lora_flux_api: {e}")
                return jsonify({"success": False, "error": str(e)}), 400
        
        @app.route('/v1/api/get/lora/svi', methods=['GET'])
        def list_lora_svi_api():
            """
            Handle SVI LoRA list requests.
            """
            try:
                return jsonify({"success": True, "models": client.list_atr_lora_svi})
            
            except Exception as e:
                client.logger.error(f"Error in list_lora_svi_api: {e}")
                return jsonify({"success": False, "error": str(e)}), 400
        
        @app.route('/v1/api/get/lora/rt', methods=['GET'])
        def list_lora_rt_api():
            """
            Handle RT LoRA list requests.
            """
            try:
                return jsonify({"success": True, "models": client.list_atr_lora_rt})
            
            except Exception as e:
                client.logger.error(f"Error in list_lora_rt_api: {e}")
                return jsonify({"success": False, "error": str(e)}), 400
        
        @app.route('/v1/api/get/styles', methods=['GET'])
        def list_styles_api():
            """
            Handle style list requests.
            """
            try:
                return jsonify({"success": True, "styles": client.list_atr_styles})
            
            except Exception as e:
                client.logger.error(f"Error in list_styles_api: {e}")
                return jsonify({"success": False, "error": str(e)}), 400
        
        @app.route('/v1/api/get/controlnets', methods=['GET'])
        def list_controlnets_api():
            """
            Handle controlnet list requests.
            """
            try:
                return jsonify({"success": True, "controlnets": client.list_atr_controlnets})
            
            except Exception as e:
                client.logger.error(f"Error in list_controlnets_api: {e}")
                return jsonify({"success": False, "error": str(e)}), 400
        
        @app.route('/v1/api/get/gfpgan', methods=['GET'])
        def list_gfpgan_api():
            """
            Handle GFPGAN list requests.
            """
            try:
                return jsonify({"success": True, "gfpgan": client.list_atr_gfpgan})
            
            except Exception as e:
                client.logger.error(f"Error in list_gfpgan_api: {e}")
                return jsonify({"success": False, "error": str(e)}), 400
        
        @app.route('/v1/api/get/models/remix', methods=['GET'])
        def list_remix_model_api():
            """
            Handle Remix model list requests.
            """
            try:
                return jsonify({"success": True, "remix": client.list_atr_remix_model})
            
            except Exception as e:
                client.logger.error(f"Error in list_remix_model_api: {e}")
                return jsonify({"success": False, "error": str(e)}), 400

        @app.route('/v1/api/get/size', methods=['GET'])
        def list_size_api():
            """
            Handle size list requests.
            """
            try:
                return jsonify({"success": True, "size": client.list_atr_size})
            
            except Exception as e:
                client.logger.error(f"Error in list_size_api: {e}")
                return jsonify({"success": False, "error": str(e)}), 400

        # guide range
        @app.route('/v1/api/get/guide/variation', methods=['GET'])
        def list_guide_variation_api():
            """
            Handle guide variation range list requests.
            """
            try:
                return jsonify({"success": True, "variation": client.list_atr_g_variation})
            
            except Exception as e:
                client.logger.error(f"Error in list_guide_variation_api: {e}")
                return jsonify({"success": False, "error": str(e)}), 400
        
        @app.route('/v1/api/get/guide/structure', methods=['GET']) 
        def list_guide_structure_api():
            """
            Handle guide structure range list requests.
            """
            try:
                return jsonify({"success": True, "structure": client.list_atr_g_structure})
            
            except Exception as e:
                client.logger.error(f"Error in list_guide_structure_api: {e}")
                return jsonify({"success": False, "error": str(e)}), 400
        
        @app.route('/v1/api/get/guide/facial', methods=['GET'])
        def list_guide_facial_api():
            """
            Handle guide facial range list requests.
            """
            try:
                return jsonify({"success": True, "facial": client.list_atr_g_facial})
            
            except Exception as e:
                client.logger.error(f"Error in list_guide_facial_api: {e}")
                return jsonify({"success": False, "error": str(e)}), 400
        
        @app.route('/v1/api/get/guide/style', methods=['GET'])
        def list_guide_style_api():
            """
            Handle guide style range list requests.
            """
            try:
                return jsonify({"success": True, "style": client.list_atr_g_style})
            
            except Exception as e:
                client.logger.error(f"Error in list_guide_style_api: {e}")
                return jsonify({"success": False, "error": str(e)}), 400

        # Inference Endpoints
        @app.route('/v1/api/image/generate', methods=['POST'])
        def image_generate_api():
            """
            Handle image generation requests via form data.
            
            Form Parameters:
            - prompt (str, required): User's positive prompt
            - negative_prompt (str, optional): User's negative prompt
            - model_name (str, optional): Name of the model to use (default: "flux-turbo")
            - image_size (str, optional): Desired image size ratio (default: "1:1")
            - lora_svi (str, optional): Name of the LoRA SVI preset (default: "none")
            - lora_flux (str, optional): Name of the LoRA Flux preset (default: "none")
            - image_seed (int, optional): Seed for image generation (default: 0)
            - style_name (str, optional): Name of the style preset (default: "none")
            """
            try:
                data = {
                    'prompt': request.form.get('prompt'),
                    'negative_prompt': request.form.get('negative_prompt', ''),
                    'model_name': request.form.get('model_name', 'flux-turbo'),
                    'image_size': request.form.get('image_size', '1:1'),
                    'lora_svi': request.form.get('lora_svi', 'none'),
                    'lora_flux': request.form.get('lora_flux', 'none'),
                    'image_seed': request.form.get('image_seed', 0),
                    'style_name': request.form.get('style_name', 'none')
                }

                if not data['prompt']:
                    raise Exception("Missing prompt")

                result = client.image_generate(**data)
                if not result:
                    raise Exception("Generation failed")

                data_url = __data_url_processor(result)
                if not data_url:
                    raise Exception("Failed to process image")

                return jsonify({"success": True, "result": data_url})

            except Exception as e:
                client.logger.error(f"Error in image_generate_api: {e}")
                return jsonify({"success": False, "error": str(e)}), 400

        @app.route('/v1/api/image/variation', methods=['POST'])
        def image_variation_api():
            """
            Handle image variation requests via form data and files.
            
            Form Parameters:
            - prompt (str, required): User's positive prompt
            - negative_prompt (str, optional): User's negative prompt
            - model_name (str, optional): Name of the model to use (default: "flux-turbo")
            - image_size (str, optional): Desired image size ratio (default: "1:1")
            - strength (str|float, optional): Strength presets ('low' | 'medium' | 'high') or custom float (default: "medium")
            - lora_svi (str, optional): Name of the LoRA SVI preset (default: "none")
            - lora_flux (str, optional): Name of the LoRA Flux preset (default: "none")
            - image_seed (int, optional): Seed for image generation (default: 0)
            - style_name (str, optional): Name of the style preset (default: "none")
            
            Files:
            - image (file, required): Source image file
            """
            try:
                if 'image' not in request.files:
                    raise Exception("No image provided")

                data = {
                    'image': request.files['image'],
                    'prompt': request.form.get('prompt'),
                    'negative_prompt': request.form.get('negative_prompt', ''),
                    'model_name': request.form.get('model_name', 'flux-turbo'),
                    'image_size': request.form.get('image_size', '1:1'),
                    'strength': request.form.get('strength', 'medium'),
                    'lora_svi': request.form.get('lora_svi', 'none'),
                    'lora_flux': request.form.get('lora_flux', 'none'),
                    'image_seed': request.form.get('image_seed', 0),
                    'style_name': request.form.get('style_name', 'none')
                }

                if not data['prompt']:
                    raise Exception("Missing prompt")

                result = client.image_variation(**data)
                if not result:
                    raise Exception("Variation failed")

                data_url = __data_url_processor(result)
                if not data_url:
                    raise Exception("Failed to process image")

                return jsonify({"success": True, "result": data_url})

            except Exception as e:
                client.logger.error(f"Error in image_variation_api: {e}")
                return jsonify({"success": False, "error": str(e)}), 400

        @app.route('/v1/api/image/structure', methods=['POST'])
        def image_structure_api():
            """
            Handle structural guidance requests via form data and files.
            
            Form Parameters:
            - prompt (str, required): User's positive prompt
            - negative_prompt (str, optional): User's negative prompt
            - model_name (str, optional): Name of the model to use (default: "svi-realistic")
            - image_size (str, optional): Desired image size ratio (default: "1:1")
            - strength (str|float, optional): Strength presets ('low' | 'medium' | 'high') or custom float (default: "medium")
            - lora_svi (str, optional): Name of the LoRA SVI preset (default: "none")
            - image_seed (int, optional): Seed for image generation (default: 0)
            - style_name (str, optional): Name of the style preset (default: "none")
            
            Files:
            - image (file, required): Source image file
            """
            try:
                if 'image' not in request.files:
                    raise Exception("No image provided")

                data = {
                    'image': request.files['image'],
                    'prompt': request.form.get('prompt'),
                    'negative_prompt': request.form.get('negative_prompt', ''),
                    'model_name': request.form.get('model_name', 'svi-realistic'),
                    'image_size': request.form.get('image_size', '1:1'),
                    'strength': request.form.get('strength', 'medium'),
                    'lora_svi': request.form.get('lora_svi', 'none'),
                    'image_seed': request.form.get('image_seed', 0),
                    'style_name': request.form.get('style_name', 'none')
                }

                if not data['prompt']:
                    raise Exception("Missing prompt")

                result = client.image_structure(**data)
                if not result:
                    raise Exception("Structure guidance failed")

                data_url = __data_url_processor(result)
                if not data_url:
                    raise Exception("Failed to process image")

                return jsonify({"success": True, "result": data_url})

            except Exception as e:
                client.logger.error(f"Error in image_structure_api: {e}")
                return jsonify({"success": False, "error": str(e)}), 400

        @app.route('/v1/api/image/facial', methods=['POST'])
        def image_facial_api():
            """
            Handle facial guidance requests via form data and files.
            
            Form Parameters:
            - prompt (str, required): User's positive prompt
            - negative_prompt (str, optional): User's negative prompt 
            - model_name (str, optional): Name of the model to use (default: "svi-realistic")
            - image_size (str, optional): Desired image size ratio (default: "1:1")
            - strength (str|float, optional): Strength presets ('low' | 'medium' | 'high') or custom float (default: "medium")
            - lora_svi (str, optional): Name of the LoRA SVI preset (default: "none")
            - image_seed (int, optional): Seed for image generation (default: 0)
            - style_name (str, optional): Name of the style preset (default: "none")
            
            Files:
            - image (file, required): Source image file
            """
            try:
                if 'image' not in request.files:
                    raise Exception("No image provided")

                data = {
                    'image': request.files['image'],
                    'prompt': request.form.get('prompt'),
                    'negative_prompt': request.form.get('negative_prompt', ''),
                    'model_name': request.form.get('model_name', 'svi-realistic'),
                    'image_size': request.form.get('image_size', '1:1'),
                    'strength': request.form.get('strength', 'medium'),
                    'lora_svi': request.form.get('lora_svi', 'none'),
                    'image_seed': request.form.get('image_seed', 0),
                    'style_name': request.form.get('style_name', 'none')
                }

                if not data['prompt']:
                    raise Exception("Missing prompt")

                result = client.image_facial(**data)
                if not result:
                    raise Exception("Facial guidance failed")

                data_url = __data_url_processor(result)
                if not data_url:
                    raise Exception("Failed to process image")

                return jsonify({"success": True, "result": data_url})

            except Exception as e:
                client.logger.error(f"Error in image_facial_api: {e}")
                return jsonify({"success": False, "error": str(e)}), 400

        @app.route('/v1/api/image/style', methods=['POST'])
        def image_style_api():
            """
            Handle style guidance requests via form data and files.
            
            Form Parameters:
            - prompt (str, required): User's positive prompt
            - negative_prompt (str, optional): User's negative prompt
            - model_name (str, optional): Name of the model to use (default: "svi-realistic")
            - image_size (str, optional): Desired image size ratio (default: "1:1")
            - strength (str|float, optional): Strength presets ('low' | 'medium' | 'high') or custom float (default: "medium")
            - lora_svi (str, optional): Name of the LoRA SVI preset (default: "none")
            - image_seed (int, optional): Seed for image generation (default: 0)
            - style_name (str, optional): Name of the style preset (default: "none")
            
            Files:
            - image (file, required): Source image file
            """
            try:
                if 'image' not in request.files:
                    raise Exception("No image provided")

                data = {
                    'image': request.files['image'],
                    'prompt': request.form.get('prompt'),
                    'negative_prompt': request.form.get('negative_prompt', ''),
                    'model_name': request.form.get('model_name', 'svi-realistic'),
                    'image_size': request.form.get('image_size', '1:1'),
                    'strength': request.form.get('strength', 'medium'),
                    'lora_svi': request.form.get('lora_svi', 'none'),
                    'image_seed': request.form.get('image_seed', 0),
                    'style_name': request.form.get('style_name', 'none')
                }

                if not data['prompt']:
                    raise Exception("Missing prompt")

                result = client.image_style(**data)
                if not result:
                    raise Exception("Style guidance failed")

                data_url = __data_url_processor(result)
                if not data_url:
                    raise Exception("Failed to process image")

                return jsonify({"success": True, "result": data_url})

            except Exception as e:
                client.logger.error(f"Error in image_style_api: {e}")
                return jsonify({"success": False, "error": str(e)}), 400

        @app.route('/v1/api/image/outpaint', methods=['POST'])
        def image_outpaint_api():
            """
            Handle outpainting requests via form data and files.
            
            Form Parameters:
            - image_size (str, optional): Desired image size ratio
            
            Files:
            - image (file, required): Source image file
            """
            try:
                if 'image' not in request.files:
                    raise Exception("No image provided")

                data = {
                    'image': request.files['image'],
                    'image_size': request.form.get('image_size', '16:9')
                }

                result = client.image_outpaint(**data)
                if not result:
                    raise Exception("Outpainting failed")

                data_url = __data_url_processor(result)
                if not data_url:
                    raise Exception("Failed to process image")

                return jsonify({"success": True, "result": data_url})

            except Exception as e:
                client.logger.error(f"Error in image_outpaint_api: {e}")
                return jsonify({"success": False, "error": str(e)}), 400

        @app.route('/v1/api/realtime/canvas', methods=['POST'])
        def realtime_canvas_api():
            """
            Handle realtime canvas requests via form data and files.
            
            Form Parameters:
            - prompt (str, required): User's positive prompt
            - negative_prompt (str, optional): User's negative prompt
            - lora_rt (str, optional): Name of the LoRA RT preset (default: "none")
            - strength (float, optional): Strength of creativity application (default: 0.9)
            - image_seed (int, optional): Seed for image generation (default: 0)
            - style_name (str, optional): Name of the style preset (default: "none")
            
            Files:
            - image (file, required): Source image file
            """
            try:
                if 'image' not in request.files:
                    raise Exception("No image provided")

                data = {
                    'image': request.files['image'],
                    'prompt': request.form.get('prompt'),
                    'negative_prompt': request.form.get('negative_prompt', ''),
                    'lora_rt': request.form.get('lora_rt', 'none'),
                    'strength': float(request.form.get('strength', 0.9)),
                    'image_seed': request.form.get('image_seed', 0),
                    'style_name': request.form.get('style_name', 'none')
                }

                if not data['prompt']:
                    raise Exception("Missing prompt")

                result = client.realtime_canvas(**data)
                if not result:
                    raise Exception("Realtime canvas processing failed")

                data_url = __data_url_processor(result)
                if not data_url:
                    raise Exception("Failed to process image")

                return jsonify({"success": True, "result": data_url})

            except Exception as e:
                client.logger.error(f"Error in realtime_canvas_api: {e}")
                return jsonify({"success": False, "error": str(e)}), 400
                       
        @app.route('/v1/api/realtime/generate', methods=['POST'])
        def realtime_generate_api():
            """
            Handle realtime image generation requests via form data.
            
            Form Parameters:
            - prompt (str, required): User's positive prompt
            - negative_prompt (str, optional): User's negative prompt
            - image_size (str, optional): Desired image size ratio (default: "1:1")
            - lora_rt (str, optional): Name of the LoRA RT preset (default: "none")
            - image_seed (int, optional): Seed for image generation (default: 0)
            - style_name (str, optional): Name of the style preset (default: "none")
            """
            try:
                data = {
                    'prompt': request.form.get('prompt'),
                    'negative_prompt': request.form.get('negative_prompt', ''),
                    'image_size': request.form.get('image_size', '1:1'),
                    'lora_rt': request.form.get('lora_rt', 'none'),
                    'image_seed': request.form.get('image_seed', 0),
                    'style_name': request.form.get('style_name', 'none')
                }

                if not data['prompt']:
                    raise Exception("Missing prompt")

                result = client.realtime_generate(**data)
                if not result:
                    raise Exception("Realtime generation failed")

                data_url = __data_url_processor(result)
                if not data_url:
                    raise Exception("Failed to process image")

                return jsonify({"success": True, "result": data_url})

            except Exception as e:
                client.logger.error(f"Error in realtime_generate_api: {e}")
                return jsonify({"success": False, "error": str(e)}), 400
         
        @app.route('/v1/api/image/inpaint', methods=['POST'])
        def image_inpaint_api():
            """
            Handle inpainting requests via form data and files.
            
            Form Parameters:
            - prompt (str, required): User's positive prompt
            - negative_prompt (str, optional): User's negative prompt
            - strength (float, optional): Strength of inpainting (default: 0.5)
            - cfg (float, optional): Scale of the prompt (default: 9.0)
            - style_name (str, optional): Name of the style preset (default: "none")
            
            Files:
            - image (file, required): Source image file
            - mask (file, required): Mask image file
            """
            try:
                if 'image' not in request.files:
                    raise Exception("No image provided")
                
                if 'mask' not in request.files:
                    raise Exception("No mask image provided")

                data = {
                    'image': request.files['image'],
                    'prompt': request.form.get('prompt'),
                    'mask': request.files['mask'],
                    'negative_prompt': request.form.get('negative_prompt', ''),
                    'strength': request.form.get('strength', 0.5),
                    'cfg': request.form.get('cfg', 9.0),
                    'style_name': request.form.get('style_name', 'none')
                }

                if not data['prompt']:
                    raise Exception("Missing prompt")

                result = client.image_inpaint(**data)
                if not result:
                    raise Exception("Inpainting failed")

                data_url = __data_url_processor(result)
                if not data_url:
                    raise Exception("Failed to process image")

                return jsonify({"success": True, "result": data_url})

            except Exception as e:
                client.logger.error(f"Error in image_inpaint_api: {e}")
                return jsonify({"success": False, "error": str(e)}), 400

        @app.route('/v1/api/image/erase', methods=['POST'])
        def image_erase_api():
            """
            Handle image erasing requests via form data and files.
            
            Form Parameters:
            - cfg (float, optional): Scale of the prompt (default: 9.0)
            
            Files:
            - image (file, required): Source image file
            - mask (file, required): Mask image file
            """
            try:
                if 'image' not in request.files:
                    raise Exception("No image provided")
                
                if 'mask' not in request.files:
                    raise Exception("No mask image provided")

                data = {
                    'image': request.files['image'],
                    'mask': request.files['mask'],
                    'cfg': request.form.get('cfg', 9.0)
                }

                result = client.image_erase(**data)
                if not result:
                    raise Exception("Erasing failed")

                data_url = __data_url_processor(result)
                if not data_url:
                    raise Exception("Failed to process image")

                return jsonify({"success": True, "result": data_url})

            except Exception as e:
                client.logger.error(f"Error in image_erase_api: {e}")
                return jsonify({"success": False, "error": str(e)}), 400

        @app.route('/v1/api/image/enhance', methods=['POST'])
        def image_enhance_api():
            """
            Handle image enhancement requests via form data and files.
            
            Form Parameters:
            - prompt (str, required): User's positive prompt
            - negative_prompt (str, optional): User's negative prompt
            - creativity (float, optional): Strength of creativity application (default: 0.5)
            - resemblance (float, optional): Strength of resemblance application (default: 0.8)
            - hdr (float, optional): Strength of HDR application (default: 0.5)
            - style_name (str, optional): Name of the style preset (default: "none")
            
            Files:
            - image (file, required): Source image file
            """
            try:
                if 'image' not in request.files:
                    raise Exception("No image provided")

                data = {
                    'image': request.files['image'],
                    'prompt': request.form.get('prompt', ''),
                    'negative_prompt': request.form.get('negative_prompt', ''),
                    'creativity': request.form.get('creativity', 0.3),
                    'resemblance': request.form.get('resemblance', 1),
                    'hdr': request.form.get('hdr', 0),
                    'style_name': request.form.get('style_name', 'none')
                }

                result = client.image_enhance(**data)
                if not result:
                    raise Exception("Enhancement failed")

                data_url = __data_url_processor(result)
                if not data_url:
                    raise Exception("Failed to process image")

                return jsonify({"success": True, "result": data_url})

            except Exception as e:
                client.logger.error(f"Error in image_enhance_api: {e}")
                return jsonify({"success": False, "error": str(e)}), 400

        @app.route('/v1/api/image/controlnet', methods=['POST'])
        def image_controlnet_api():
            """
            Handle controlnet requests via form data and files.
            
            Form Parameters:
            - prompt (str, required): User's positive prompt
            - negative_prompt (str, optional): User's negative prompt
            - model_name (str, optional): Name of the model to use (default: "sd-toon")
            - controlnet (str, optional): Type of controlnet ( 'scribble' | 'pose' | 'line-art' | 'depth' | 'canny' ) (default: "scribble")
            - strength (int, optional): Strength of controlnet application (default: 70)
            - cfg (float, optional): Scale of the prompt (default: 9.0)
            - image_seed (int, optional): Seed for image generation (default: 0)
            - style_name (str, optional): Name of the style preset (default: "none")
            
            Files:
            - image (file, required): Source image file
            """
            try:
                if 'image' not in request.files:
                    raise Exception("No image provided")

                data = {
                    'image': request.files['image'],
                    'prompt': request.form.get('prompt'),
                    'negative_prompt': request.form.get('negative_prompt', ''),
                    'model_name': request.form.get('model_name', 'sd-toon'),
                    'controlnet': request.form.get('controlnet', 'scribble'),
                    'strength': request.form.get('strength', 70),
                    'cfg': request.form.get('cfg', 9.0),
                    'image_seed': request.form.get('image_seed', 0),
                    'style_name': request.form.get('style_name', 'none')
                }

                if not data['prompt']:
                    raise Exception("Missing prompt")

                result = client.image_controlnet(**data)
                if not result:
                    raise Exception("Controlnet processing failed")

                data_url = __data_url_processor(result)
                if not data_url:
                    raise Exception("Failed to process image")

                return jsonify({"success": True, "result": data_url})

            except Exception as e:
                client.logger.error(f"Error in image_controlnet_api: {e}")
                return jsonify({"success": False, "error": str(e)}), 400

        @app.route('/v1/api/face/gfpgan', methods=['POST'])
        def face_gfpgan_api():
            """
            Handle GFPGAN face restoration requests via form data and files.
            
            Form Parameters:
            - model_version (str, optional): Model version ( '1.3' | '1.2' ) (default: "1.3")
            
            Files:
            - image (file, required): Source image file
            """
            try:
                if 'image' not in request.files:
                    raise Exception("No image provided")

                data = {
                    'image': request.files['image'],
                    'model_version': request.form.get('model_version', '1.3')
                }

                result = client.face_gfpgan(**data)
                if not result:
                    raise Exception("Face restoration failed")

                data_url = __data_url_processor(result)
                if not data_url:
                    raise Exception("Failed to process image")

                return jsonify({"success": True, "result": data_url})

            except Exception as e:
                client.logger.error(f"Error in face_gfpgan_api: {e}")
                return jsonify({"success": False, "error": str(e)}), 400
            
        @app.route('/v1/api/face/codeformer', methods=['POST'])
        def face_codeformer_api():
            """
            Handle face restoration requests via form data and files.
            
            Files:
            - image (file, required): Source image file
            """
            try:
                if 'image' not in request.files:
                    raise Exception("No image provided")

                data = {
                    'image': request.files['image']
                }

                result = client.face_codeformer(**data)
                if not result:
                    raise Exception("Face restoration failed")

                data_url = __data_url_processor(result)
                if not data_url:
                    raise Exception("Failed to process image")

                return jsonify({"success": True, "result": data_url})

            except Exception as e:
                client.logger.error(f"Error in face_codeformer_api: {e}")
                return jsonify({"success": False, "error": str(e)}), 400
            
        @app.route('/v1/api/image/upscale', methods=['POST'])
        def image_upscale_api():
            """
            Handle image upscaling requests via form data and files.
            
            Files:
            - image (file, required): Source image file
            """
            try:
                if 'image' not in request.files:
                    raise Exception("No image provided")

                data = {
                    'image': request.files['image']
                }

                result = client.image_upscaler(**data)
                if not result:
                    raise Exception("Upscaling failed")

                data_url = __data_url_processor(result)
                if not data_url:
                    raise Exception("Failed to process image")

                return jsonify({"success": True, "result": data_url})

            except Exception as e:
                client.logger.error(f"Error in image_upscale_api: {e}")
                return jsonify({"success": False, "error": str(e)}), 400

        @app.route('/v1/api/image/bgremove', methods=['POST'])
        def image_bgremove_api():
            """
            Handle background removal requests via form data and files.
            
            Files:
            - image (file, required): Source image file
            """
            try:
                if 'image' not in request.files:
                    raise Exception("No image provided")

                data = {
                    'image': request.files['image']
                }

                result = client.image_bgremove(**data)
                if not result:
                    raise Exception("Background removal failed")

                data_url = __data_url_processor(result)
                if not data_url:
                    raise Exception("Failed to process image")

                return jsonify({"success": True, "result": data_url})

            except Exception as e:
                client.logger.error(f"Error in image_bgremove_api: {e}")
                return jsonify({"success": False, "error": str(e)}), 400

        @app.route('/v1/api/image/caption', methods=['POST'])
        def image_caption_api():
            """
            Handle image captioning requests via form data and files.
            
            Files:
            - image (file, required): Source image file
            """
            try:
                if 'image' not in request.files:
                    raise Exception("No image provided")
                
                data = {
                    'image': request.files['image']
                }

                result = client.image_caption(**data)
                if not result:
                    raise Exception("Captioning failed")

                return jsonify({"success": True, "result": result})

            except Exception as e:
                client.logger.error(f"Error in image_caption_api: {e}")
                return jsonify({"success": False, "error": str(e)}), 400

        @app.route('/v1/api/image/prompt', methods=['POST'])
        def image_prompt_api():
            """
            Handle image to prompt requests via form data and files.
            
            Files:
            - image (file, required): Source image file
            """
            try:
                if 'image' not in request.files:
                    raise Exception("No image provided")
                
                data = {
                    'image': request.files['image']
                }

                result = client.image_prompt(**data)
                if not result:
                    raise Exception("Prompt generation failed")

                return jsonify({"success": True, "result": result})

            except Exception as e:
                client.logger.error(f"Error in image_prompt_api: {e}")
                return jsonify({"success": False, "error": str(e)}), 400

        app.run(host=host, port=port, debug=debug)
    
    except Exception as e:
        client.logger.error(f"{str(e)}")
        raise