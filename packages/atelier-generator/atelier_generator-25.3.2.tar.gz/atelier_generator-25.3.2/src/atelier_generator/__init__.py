import os
import uuid
import time
import json
import base64
import random
import inspect
import tempfile
import requests
from PIL import Image
from io import BytesIO
from datetime import datetime
from importlib import resources
from colorpaws import ColorPaws

class AtelierGenerator:
    """Copyright (C) 2025 Ikmal Said. All rights reserved."""
    def __init__(self, mode: str = "default", gradio: bool = False, timeout: int = 180, log_on: bool = True,
                 log_to: str = None, save_to: str = "outputs", save_as: str = "webp"):
        """
        Initialize Atelier Client module.

        Parameters:
        - mode    (str): Startup mode ('default', 'webui', 'api').
        - gradio (bool): Enable Gradio support.
        - timeout (int): Timeout for requests in seconds.
        - log_on (bool): Enable logging.
        - log_to  (str): Directory to save logs.
        - save_to (str): Directory to save outputs.
        - save_as (str): Output format ('png', 'webp', 'jpg', 'pil').
        """        
        self.logger = ColorPaws(
            name=self.__class__.__name__,
            log_on=log_on,
            log_to=log_to
        )
        
        self.gradio  = gradio
        self.timeout = timeout

        self.__online_check()  
        self.__load_preset()
        self.__load_locale()
        self.__load_lists()

        self.__init_checks(save_to, save_as)
        self.logger.info(f"{self.__class__.__name__} is now ready!")
        
        if mode != "default":
            self.__startup_mode(mode)

    def __init_checks(self, save_to: str, save_as: str):
        """
        Initialize essential checks.
        """
        try:
            self.save_to = save_to if save_to else tempfile.gettempdir()
            self.save_to = os.path.join(self.save_to, "atelier")
            
            if save_as.lower() in ['png', 'webp', 'jpg', 'pil']:
                self.save_as = save_as.lower()
            else:
                self.logger.warning(f"Invalid save format '{save_as}', defaulting to WEBP")
                self.save_as = 'webp'
        
        except Exception as e:
            error = f"Error in init_checks: {e}"
            self.logger.error(error)
            raise
   
    def __startup_mode(self, mode: str):
        """
        Startup mode for api or webui with default values.
        """
        try:
            if mode == "webui":
                self.start_webui()
            
            elif mode == "api":
                self.start_api()
            
            else:
                raise ValueError(f"Invalid startup mode: {mode}")
        
        except Exception as e:
            error = f"Error in startup_mode: {e}"
            self.logger.error(error)
            raise
   
    def __online_check(self, url: str = 'https://www.google.com', timeout: int = 10):
        """
        Check if there is an active internet connection.
        """
        try:
            requests.get(url, timeout=timeout)
        
        except Exception as e:
            error = f"No internet connection available! Please check your network connection."
            self.logger.error(error)
            raise

    def __load_preset(self, preset_path: str = "data.py"):
        """
        Loads the required preset.

        Parameters:
        - preset_path (str): Path to the preset file.
        """
        try:
            with open(resources.path(__name__, preset_path), 'r', encoding="utf-8") as f:
                __atr_preset = json.load(f)

            self.__atr_generate     = __atr_preset["adr"]["generate"]
            self.__atr_prompt       = __atr_preset["adr"]["prompt"]
            self.__atr_bgremove     = __atr_preset["adr"]["bgremove"]
            self.__atr_upscale      = __atr_preset["adr"]["upscale"]
            self.__atr_remix        = __atr_preset["adr"]["remix"]
            self.__atr_enhance      = __atr_preset["adr"]["enhance"]
            self.__atr_eraser       = __atr_preset["adr"]["eraser"]
            self.__atr_inpaint      = __atr_preset["adr"]["inpaint"]
            self.__atr_realtime     = __atr_preset["adr"]["realtime"]
            self.__atr_canvas       = __atr_preset["adr"]["canvas"]
            self.__atr_outpaint     = __atr_preset["adr"]["outpaint"]
            self.__atr_caption      = __atr_preset["adr"]["caption"]
            self.__atr_codeformer   = __atr_preset["adr"]["codeformer"]
            self.__atr_g_variation  = __atr_preset["guide_range"]["variation"]
            self.__atr_g_structure  = __atr_preset["guide_range"]["structure"]
            self.__atr_g_facial     = __atr_preset["guide_range"]["facial"]
            self.__atr_g_style      = __atr_preset["guide_range"]["style"]
            self.__atr_controlnets  = __atr_preset["controlnets"]
            self.__atr_models_sdxl  = __atr_preset["models_sdxl"]
            self.__atr_models_flux  = __atr_preset["models_flux"]
            self.__atr_models_svi   = __atr_preset["models_svi"]
            self.__atr_lora_flux    = __atr_preset["lora_flux"]
            self.__atr_loc          = __atr_preset["locale"][0]
            self.__atr_ime          = __atr_preset["locale"][1]
            self.__atr_inf          = __atr_preset["locale"][2]
            self.__atr_arc          = __atr_preset["locale"][3]
            self.__atr_error        = __atr_preset["error"][0]
            self.__atr_lora_svi     = __atr_preset["lora_svi"]
            self.__atr_lora_rt      = __atr_preset["lora_rt"]
            self.__atr_test         = __atr_preset["test"][0]
            self.__atr_styles       = __atr_preset["styles"]
            self.__atr_gfpgan       = __atr_preset["gfpgan"]
            self.__atr_remix_model  = __atr_preset["remix"]
            self.__atr_size         = __atr_preset["size"]
            self.__atr_models       = {**self.__atr_models_flux, **self.__atr_models_svi, **self.__atr_models_sdxl}
            self.__atr_models_guide = {**self.__atr_models_flux, **self.__atr_models_svi}
        
        except Exception as e:
            error = f"Error in load_atr_preset: {e}"
            self.logger.error(error)
            raise
    
    def __load_locale(self):
        """
        Loads locale settings.
        """
        try:
            self.__loc = base64.b64decode(self.__atr_loc).decode('utf-8')
            self.__ime = base64.b64decode(self.__atr_ime).decode('utf-8')
            self.__inf = base64.b64decode(self.__atr_inf).decode('utf-8')
            self.__arc = base64.b64decode(self.__atr_arc).decode('utf-8')
            self.__err = BytesIO(base64.b64decode(self.__atr_error)).read()
            self.__xea = {"bearer": self.__loc}

        except Exception as e:
            error = f"Error in load_locale: {e}"
            self.logger.error(error)
            raise

    def __load_lists(self):
        """
        Loads preset lists for models, loras, features and styles.
        """
        try:
            self.list_atr_models_sdxl  = list(self.__atr_models_sdxl.keys())
            self.list_atr_models_flux  = list(self.__atr_models_flux.keys())
            self.list_atr_models_svi   = list(self.__atr_models_svi.keys())
            self.list_atr_g_variation  = list(self.__atr_g_variation.keys())
            self.list_atr_g_structure  = list(self.__atr_g_structure.keys())
            self.list_atr_g_facial     = list(self.__atr_g_facial.keys())
            self.list_atr_g_style      = list(self.__atr_g_style.keys())
            self.list_atr_lora_svi     = list(self.__atr_lora_svi.keys())
            self.list_atr_lora_flux    = list(self.__atr_lora_flux.keys())
            self.list_atr_size         = list(self.__atr_size.keys())
            self.list_atr_remix_model  = list(self.__atr_remix_model.keys())
            self.list_atr_controlnets  = list(self.__atr_controlnets.keys())
            self.list_atr_lora_rt      = list(self.__atr_lora_rt.keys())
            self.list_atr_gfpgan       = list(self.__atr_gfpgan.keys())
            self.list_atr_styles       = list(self.__atr_styles.keys())
            self.list_atr_models       = list(self.__atr_models.keys())
            self.list_atr_models_guide = list(self.__atr_models_guide.keys())
            
        except Exception as e:
            error = f"Error in load_lists: {e}"
            self.logger.error(error)
            raise

    def __random_seed_generator(self, seed: int = 0, task_id: str = None):
        """
        Generate a random seed.

        Parameters:
        - seed (int): Initial seed value. If 0, a random seed is generated.
        - task_id (str): Unique identifier for the task.
        """
        try:
            if isinstance(seed, str):
                seed = int(seed)
            
            if seed == -1:
                return str(random.randint(0, 2**31 - 1))
            
            elif seed == 0:
                return None    
            
            else:
                return str(seed)
        
        except Exception as e:
            self.logger.error(f"[{task_id}] Error in random_seed_generator: {e}")
            raise

    def __lora_checker(self, model_name: str, lora_svi: str = "none", lora_flux: str = "none", task_id: str = None):
        """
        Validates LoRA compatibility with different models.

        Parameters:
        - model_name (str): Name of the model to use.
        - lora_svi (str): Name of the LoRA SVI preset.
        - lora_flux (str): Name of the LoRA Flux preset.
        - task_id (str): Unique identifier for the task.
        """
        try:
            validated_svi = lora_svi if lora_svi else "none"
            validated_flux = lora_flux if lora_flux else "none"

            if model_name in self.list_atr_models_flux:
                if lora_svi not in ["none", None]:
                    self.logger.warning(f"[{task_id}] {model_name} only supports flux lora. Ignoring svi lora!")
                    validated_svi = "none"
            
            elif model_name in self.list_atr_models_svi:
                if lora_flux not in ["none", None]:
                    self.logger.warning(f"[{task_id}] {model_name} only supports svi lora. Ignoring flux lora!")
                    validated_flux = "none"
            
            else:
                if lora_svi not in ["none", None] or lora_flux not in ["none", None]:
                    self.logger.warning(f"[{task_id}] {model_name} doesn't support any lora for now!")
                    validated_svi = "none"
                    validated_flux = "none"

            return validated_svi, validated_flux

        except Exception as e:
            self.logger.error(f"[{task_id}] Error in lora_checker: {e}")
            raise

    def __prompt_processor(self, prompt: str = "", negative_prompt: str = "", style_name: str = "none",
                           lora_svi: str = "none", task_id: str = None):
        """
        Setup user prompt with their chosen style preset.

        Parameters:
        - prompt (str): User's positive prompt.
        - negative_prompt (str): User's negative prompt.
        - style_name (str): Name of the style preset.
        - lora_svi (str): Name of the LoRA SVI preset.
        - task_id (str): Unique identifier for the task.
        """
        try:
            pos = prompt
            neg = negative_prompt
            
            try:
                if style_name is not None and style_name != "none":
                    pos_sty = self.__atr_styles[style_name]["prompt"]
                    neg_sty = self.__atr_styles[style_name]["negative_prompt"]
                    
                    pos = pos_sty.replace("{prompt}", pos)
                    neg = neg_sty.replace("{negative_prompt}", neg)
            
            except Exception as e:
                error = f"[{task_id}] {e} not valid style preset!"
                self.logger.warning(error)
                raise ValueError(error)
            
            try:
                if lora_svi is not None and lora_svi != "none":
                    pos_lora = self.__atr_lora_svi[lora_svi]["prompt"]
                    neg_lora = self.__atr_lora_svi[lora_svi]["negative_prompt"]

                    pos = pos_lora.replace("{prompt}", pos)
                    neg = neg_lora.replace("{negative_prompt}", neg)
            
            except Exception as e:
                error = f"[{task_id}] {e} not valid lora_svi preset!"
                self.logger.warning(error)
                raise ValueError(error)
            
            return pos, neg
        
        except Exception as e:
            self.logger.error(f"[{task_id}] Error in prompt_processor: {e}")
            raise

    def __image_processor(self, image, gr_editor_type: str = None, gr_mask_layer: int = 0, resize: bool = False,
                          max_width: int = 1700, max_height: int = 1000, task_id: str = None):
        """
        Helper method to process images and masks for Gradio/normal usage.

        Parameters:
        - image: Can be PIL Image, FileStorage object, or file path
        - gr_editor_type (str): Type of Gradio editor ('mask', 'background', 'composite')
        - gr_mask_layer (int): Layer index for mask processing
        - resize (bool): Whether to resize the image
        - max_width (int): Maximum width for resizing
        - max_height (int): Maximum height for resizing
        - task_id (str): Unique identifier for the task.
        """
        try:
            # Handle Gradio editor types only if both gradio mode and gr_editor_type are set
            if gr_editor_type and self.gradio:
                if not isinstance(image, dict):
                    raise ValueError(f"Expected dict from gradio editor!")
                
                if gr_editor_type == 'mask':
                    img = image["layers"][gr_mask_layer]
                    self.logger.info(f"[{task_id}] Created mask from gradio editor layer {gr_mask_layer}!")
                
                elif gr_editor_type == 'background':
                    img = image["background"]
                    self.logger.info(f"[{task_id}] Created image from gradio editor background!")
                
                elif gr_editor_type == 'composite':
                    img = image["composite"]
                    self.logger.info(f"[{task_id}] Created image from gradio editor composite!")

                else:
                    raise ValueError(f"Invalid gr_editor_type: {gr_editor_type}!")
            
            # Handle regular image types
            elif isinstance(image, Image.Image):
                img = image
                self.logger.info(f"[{task_id}] Created image from pil object!")
                
            elif hasattr(image, 'read'):
                img = Image.open(image)
                self.logger.info(f"[{task_id}] Created image from file-like object!")
                
            elif isinstance(image, str):
                img = Image.open(image)
                self.logger.info(f"[{task_id}] Created image from file path!")
            
            else:
                raise ValueError(f"Unsupported image type: {type(image)}")

            if resize:
                width, height = img.size
                if width > max_width or height > max_height:
                    aspect_ratio = width / height
                    
                    if aspect_ratio > max_width / max_height:
                        new_width = max_width
                        new_height = int(new_width / aspect_ratio)
                    else:
                        new_height = max_height
                        new_width = int(new_height * aspect_ratio)

                    img = img.resize((new_width, new_height), Image.LANCZOS)
                    self.logger.info(f"[{task_id}] Resized image from {width}x{height} to {new_width}x{new_height}")

            byte_array = BytesIO()
            img.save(byte_array, format="PNG")
            byte_array.seek(0)
            
            return byte_array
        
        except Exception as e:
            self.logger.error(f"[{task_id}] Error in image_processor: {e}")
            raise

    def __get_task_id(self):
        """
        Generate a unique task ID for request tracking.
        Returns a truncated UUID (8 characters).
        """
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            uuid_part = str(uuid.uuid4())[:8]
            task_id = f"{timestamp}_{uuid_part}"
            caller_name = self.__get_caller_name(task_id)
            
            self.logger.info(f"[{task_id}] Created task id from {caller_name} request!")
            return task_id
        
        except Exception as e:
            self.logger.error(f"Error in get_task_id: {e}")
            raise

    def __get_caller_name(self, task_id: str):
        """
        Get the name of the caller function.
        """
        try:
            caller_name = inspect.currentframe().f_back.f_back.f_code.co_name
            return caller_name
        
        except Exception as e:
            self.logger.error(f"[{task_id}] Error in get_caller_name: {e}")
            raise

    def __file_handler(self, content: bytes, file_path: str, task_id: str):
        """
        Helper method to save content to a temporary file or return PIL object.
        """
        try:
            with open(file_path, 'wb') as output:
                output.write(content)
                
            self.logger.info(f"[{task_id}] Saved output: {file_path}")
            return file_path
        
        except Exception as e:
            self.logger.error(f"[{task_id}] Error in file_handler: {e}")
            raise

    def __save_output(self, content: bytes, extension: str, caller_name: str, task_id: str):
        """
        Helper method to save content to a file organized by date and task ID.
        """
        try:
            # Extract date from task_id and format it
            date_part = task_id.split('_')[0]
            formatted_date = f"{date_part[:4]}-{date_part[4:6]}-{date_part[6:8]}"
        
            output_dir = os.path.join(self.save_to, formatted_date)
            os.makedirs(output_dir, exist_ok=True)
        
            # Handle non-image files
            if extension.lower() not in ['.png', '.jpg', '.webp']:
                file_path = os.path.join(self.save_to, formatted_date, f"{task_id}_{caller_name}{extension}")
                return self.__file_handler(content, file_path, task_id)

            # Process image files
            img = Image.open(BytesIO(content))
            
            if self.save_as == 'pil':
                self.logger.info(f"[{task_id}] Saved output as PIL object!")
                return img

            # Set format-specific parameters
            save_params = {}
            
            if self.save_as == 'webp':
                format_name = 'WebP'
                extension = '.webp'
                save_params['quality'] = 90
                
            elif self.save_as == 'jpg':
                format_name = 'JPEG'
                extension = '.jpg'
                save_params['quality'] = 95
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                    
            else:
                format_name = 'PNG'
                extension = '.png'

            # Save image with selected format
            output_buffer = BytesIO()
            img.save(output_buffer, format=format_name, **save_params)
            content = output_buffer.getvalue()

            # Save to file
            file_path = os.path.join(self.save_to, formatted_date, f"{task_id}_{caller_name}{extension}")
            return self.__file_handler(content, file_path, task_id)

        except Exception as e:
            self.logger.error(f"[{task_id}] Error in save_output: {e}")
            raise

    def __service_request(self, url: str, header: dict, files: dict, data: dict = None,
                          delay: float = 0.5, custom: str = None, task_id: str = None):
        """
        Process inputs for each server connection concurrently and return results.

        Parameters:
        - url (str): URL for the service request.
        - header (dict): Headers for the request.
        - files (dict): Files to send with the request.
        - data (dict): Additional data for the request.
        - delay (float): Delay between requests.
        - custom (str): Custom request type.
        """
        
        try:
            tx_timeout = rx_timeout = self.timeout
            caller_name = self.__get_caller_name(task_id)

            self.logger.info(f"[{task_id}] Processing {caller_name} request in {tx_timeout} seconds")
            
            def handle_custom_response(response, custom_type):
                try:
                    if custom_type == "gfpgan":
                        result = response["data"][0]["image_base64"].split(",")[1]
                        content = base64.b64decode(result)
                        return self.__save_output(content, ".png", caller_name, task_id)
                    
                    elif custom_type == "caption":
                        result = response["caption"]
                        self.__save_output(result.encode('utf-8'), ".txt", caller_name, task_id)
                        return result
                    
                    self.logger.warning(f"[{task_id}] Invalid custom request: {custom_type}")            
                
                except Exception as e:
                    self.logger.error(f"[{task_id}] Error handling {custom_type} response!")
                    return None           

            def handle_streaming_response(response):
                try:
                    content_type = response.headers.get("Content-Type", "").lower()
                    
                    if "text/plain" in content_type:
                        text_response = response.text.strip()
                        
                        if text_response == "NSFW content detected":
                            self.logger.error(f"[{task_id}] Request rejected! (likely NSFW content)")
                            return None                   

                    if "json" in content_type:
                        return response.json()

                    if "text" in content_type:
                        return response.text

                    content = BytesIO()
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            content.write(chunk)
                    
                    content_bytes = content.getvalue()

                    if len(content_bytes) <= 4096:
                        self.logger.error(f"[{task_id}] Response is too small! (4096 bytes or less)")
                        return None                

                    if content_bytes == self.__err:
                        self.logger.error(f"[{task_id}] Request rejected! (likely NSFW content)")
                        return None                
                    
                    return self.__save_output(content_bytes, ".png", caller_name, task_id)

                except Exception as e:
                    self.logger.error(f"[{task_id}] Error handling streaming response: {e}")
                    return None           

            def request_handler(custom=None):
                try:
                    time.sleep(delay)
                    start_time = time.time()
                    
                    if custom:
                        custom = custom.lower()
                        response = requests.post(
                            url, 
                            headers=header,
                            data=data if custom == "gfpgan" else None,
                            files=files,
                            timeout=(tx_timeout, rx_timeout)
                        )
                        return handle_custom_response(response.json(), custom)
                    
                    response = requests.post(
                        url,
                        headers=header,
                        files=files,
                        timeout=(tx_timeout, rx_timeout),
                        stream=True
                    )
                    
                    if response.status_code != 200:
                        self.logger.error(f"[{task_id}] Request failed! Status: {response.status_code} ({response.text})")
                        return None
                    
                    return handle_streaming_response(response)
                
                except requests.exceptions.RequestException as e:
                    self.logger.error(f"[{task_id}] Request error or timeout!")
                    return None        
                
                finally:
                    self.logger.info(f"[{task_id}] Request took {time.time() - start_time:.2f} seconds.")

            return request_handler(custom)

        except Exception as e:
            self.logger.error(f"[{task_id}] Error in service_request: {e}")
            raise

    def image_generate(self, prompt: str, negative_prompt: str = "", model_name: str = "flux-turbo",
                       image_size: str = "1:1", lora_svi: str = "none", lora_flux: str = "none",
                       image_seed: int = 0, style_name: str = "none"):
        """
        High quality image generation.

        Parameters:
        - prompt (str): User's positive prompt.
        - negative_prompt (str): User's negative prompt.
        - model_name (str): Name of the model to use.
        - image_size (str): Desired image size ratio.
        - lora_svi (str): Name of the LoRA SVI preset.
        - lora_flux (str): Name of the LoRA Flux preset.
        - image_seed (int): Seed for image generation.
        - style_name (str): Name of the style preset.
        """
        try:
            task_id = self.__get_task_id()
            
            lora_svi, lora_flux = self.__lora_checker(model_name, lora_svi, lora_flux, task_id)
            
            prompt, negative_prompt = self.__prompt_processor(prompt, negative_prompt, style_name, lora_svi, task_id)
            
            seed = self.__random_seed_generator(image_seed, task_id)
            
            model_name = self.__atr_models.get(model_name)
            if not model_name:
                raise ValueError(f"Invalid model name!")

            image_size = self.__atr_size.get(image_size)
            if not image_size:
                raise ValueError(f"Invalid image size!")

            url = self.__ime + self.__atr_generate
            header = self.__xea
            
            body = {
                "negative_prompt": (None, negative_prompt),
                "aspect_ratio": (None, image_size),
                "style_id": (None, model_name),
                "variation": (None, "txt2img"),
                "enable_hr": (None, "true"),
                "prompt": (None, prompt),
                "seed": (None, seed)
            }
            
            if lora_flux is not None and lora_flux != "none":
                lora_flux = self.__atr_lora_flux.get(lora_flux)
                if not lora_flux:
                    raise ValueError(f"Invalid lora flux: {lora_flux}")
                
                body["style_id"] = (None, "310")
                body["effect"] = (None, lora_flux)
            
            return self.__service_request(url, header, body, task_id = task_id)
        
        except Exception as e:
            self.logger.error(f"[{task_id}] Error in image_generate: {e}")
            raise

    def image_variation(self, image: str, prompt: str, negative_prompt: str = "", model_name: str = "flux-turbo",
                        image_size: str = "1:1", strength: str = "high", lora_svi: str = "none", 
                        lora_flux: str = "none", image_seed: int = 0, style_name: str = "none"):
        """
        Generate variations of an input image.
        
        Parameters:
        - image (file): Source image file.
        - prompt (str): User's positive prompt.
        - negative_prompt (str): User's negative prompt.
        - model_name (str): Name of the model to use.
        - image_size (str): Desired image size ratio.
        - strength (str|float): Strength presets ('low', 'medium', 'high') or custom float
        - lora_svi (str): Name of the LoRA SVI preset.
        - lora_flux (str): Name of the LoRA Flux preset.
        - image_seed (int): Seed for image generation.
        - style_name (str): Name of the style preset.
        """
        try:
            task_id = self.__get_task_id()
            
            guide_array = self.__image_processor(image, task_id = task_id)
            if not guide_array:
                raise ValueError(f"Invalid image!")
            
            if isinstance(strength, str):
                strength = self.__atr_g_variation.get(strength)
                if not strength:
                    raise ValueError(f"Invalid strength!")
            
            strength = str(float(strength))
            
            lora_svi, lora_flux = self.__lora_checker(model_name, lora_svi, lora_flux, task_id)
            
            prompt, negative_prompt = self.__prompt_processor(prompt, negative_prompt, style_name, lora_svi, task_id)
            
            seed = self.__random_seed_generator(image_seed, task_id)
            
            if model_name in self.list_atr_models_flux:
                model_name = self.__atr_models_flux.get(model_name)
            
            elif model_name in self.list_atr_models_svi:
                model_name = self.__atr_models_svi.get(model_name)
            
            else:
                raise ValueError(f"Invalid model name!")

            image_size = self.__atr_size.get(image_size)
            if not image_size:
                raise ValueError(f"Invalid image size!")
            
            url = self.__ime + self.__atr_generate
            header = self.__xea
            
            body = {
                "image": ("guide.png", guide_array, "image/png"),
                "enable_layer_diffusion": (None, "false"),
                "enable_adetailer": (None, "false"),
                "negative_prompt": (None, negative_prompt),
                "aspect_ratio": (None, image_size),
                "style_id": (None, model_name),
                "variation": (None, "img2img"),
                "strength": (None, strength),
                "enable_hr": (None, "true"),
                "is_enhance": (None, "0"),
                "prompt": (None, prompt),
                "seed": (None, seed)
            }
            
            if lora_flux is not None and lora_flux != "none":
                lora_flux = self.__atr_lora_flux.get(lora_flux)
                if not lora_flux:
                    raise ValueError(f"Invalid lora flux: {lora_flux}")
                
                body["style_id"] = (None, "310")
                body["effect"] = (None, lora_flux)
            
            return self.__service_request(url, header, body, task_id = task_id)
        
        except Exception as e:
            self.logger.error(f"[{task_id}] Error in image_variation: {e}")
            raise

    def image_structure(self, image: str, prompt: str, negative_prompt: str = "", model_name: str = "svi-realistic",
                        image_size: str = "1:1", strength: str = "high", lora_svi: str = "none",
                        image_seed: int = 0, style_name: str = "none"):
        """
        Generate images using structural guidance.
        
        Parameters:
        - image (file): Source image file.
        - prompt (str): User's positive prompt.
        - negative_prompt (str): User's negative prompt.
        - model_name (str): Name of the model to use.
        - image_size (str): Desired image size ratio.
        - strength (str|float): Strength presets ('low', 'medium', 'high') or custom float
        - lora_svi (str): Name of the LoRA SVI preset.
        - image_seed (int): Seed for image generation.
        - style_name (str): Name of the style preset.
        """
        try:
            task_id = self.__get_task_id()
            
            guide_array = self.__image_processor(image, task_id = task_id)
            if not guide_array:
                raise ValueError(f"Invalid image!")
            
            if isinstance(strength, str):
                strength = self.__atr_g_structure.get(strength)
                if not strength:
                    raise ValueError(f"Invalid strength!")
            
            strength = str(float(strength))
            
            prompt, negative_prompt = self.__prompt_processor(prompt, negative_prompt, style_name, lora_svi, task_id)
            
            seed = self.__random_seed_generator(image_seed, task_id)
            
            model_name = self.__atr_models_svi.get(model_name)
            if not model_name:
                raise ValueError(f"Invalid model name!")

            image_size = self.__atr_size.get(image_size)
            if not image_size:
                raise ValueError(f"Invalid image size!")
            
            url = self.__ime + self.__atr_generate
            header = self.__xea
            
            body = {
                "image": ("guide.png", guide_array, "image/png"),
                "negative_prompt": (None, negative_prompt),
                "enable_layer_diffusion": (None, "false"),
                "enable_adetailer": (None, "false"),
                "control_weight": (None, strength),
                "aspect_ratio": (None, image_size),
                "variation": (None, "restructure"),
                "style_id": (None, model_name),
                "enable_hr": (None, "true"),
                "is_enhance": (None, "0"),
                "prompt": (None, prompt),
                "seed": (None, seed)
            }
            
            return self.__service_request(url, header, body, task_id = task_id)
        
        except Exception as e:
            self.logger.error(f"[{task_id}] Error in image_structure: {e}")
            raise

    def image_facial(self, image: str, prompt: str, negative_prompt: str = "", model_name: str = "svi-realistic",
                    image_size: str = "1:1", strength: str = "high", lora_svi: str = "none",
                    image_seed: int = 0, style_name: str = "none"):
        """
        Generate images using facial guidance.
        
        Parameters:
        - image (file): Source image file.
        - prompt (str): User's positive prompt.
        - negative_prompt (str): User's negative prompt.
        - model_name (str): Name of the model to use.
        - image_size (str): Desired image size ratio.
        - strength (str|float): Strength presets ('low', 'medium', 'high') or custom float
        - lora_svi (str): Name of the LoRA SVI preset.
        - image_seed (int): Seed for image generation.
        - style_name (str): Name of the style preset.
        """
        try:
            task_id = self.__get_task_id()
            
            guide_array = self.__image_processor(image, task_id = task_id)
            if not guide_array:
                raise ValueError(f"Invalid image!")
            
            if isinstance(strength, str):
                strength = self.__atr_g_facial.get(strength)
                if not strength:
                    raise ValueError(f"Invalid strength!")
            
            strength = str(float(strength))
            
            prompt, negative_prompt = self.__prompt_processor(prompt, negative_prompt, style_name, lora_svi, task_id)
            
            seed = self.__random_seed_generator(image_seed, task_id)
            
            model_name = self.__atr_models_svi.get(model_name)
            if not model_name:
                raise ValueError(f"Invalid model name!")

            image_size = self.__atr_size.get(image_size)
            if not image_size:
                raise ValueError(f"Invalid image size!")
            
            url = self.__ime + self.__atr_generate
            header = self.__xea
            
            body = {
                "image": ("guide.png", guide_array, "image/png"),
                "negative_prompt": (None, negative_prompt),
                "enable_layer_diffusion": (None, "false"),
                "enable_adetailer": (None, "false"),
                "control_weight": (None, strength),
                "aspect_ratio": (None, image_size),
                "variation": (None, "face-portrait"),
                "style_id": (None, model_name),
                "enable_hr": (None, "true"),
                "is_enhance": (None, "0"),
                "prompt": (None, prompt),
                "seed": (None, seed)
            }
            
            return self.__service_request(url, header, body, task_id = task_id)
        
        except Exception as e:
            self.logger.error(f"[{task_id}] Error in image_facial: {e}")
            raise

    def image_style(self, image: str, prompt: str, negative_prompt: str = "", model_name: str = "svi-realistic",
                    image_size: str = "1:1", strength: str = "high", lora_svi: str = "none",
                    image_seed: int = 0, style_name: str = "none"):
        """
        Generate images using style guidance.
        
        Parameters:
        - image (file): Source image file.
        - prompt (str): User's positive prompt.
        - negative_prompt (str): User's negative prompt.
        - model_name (str): Name of the model to use.
        - image_size (str): Desired image size ratio.
        - strength (str|float): Strength presets ('low', 'medium', 'high') or custom float
        - lora_svi (str): Name of the LoRA SVI preset.
        - image_seed (int): Seed for image generation.
        - style_name (str): Name of the style preset.
        """
        try:
            task_id = self.__get_task_id()
            
            guide_array = self.__image_processor(image, task_id = task_id)
            if not guide_array:
                raise ValueError(f"Invalid image!")
            
            if isinstance(strength, str):
                strength = self.__atr_g_style.get(strength)
                if not strength:
                    raise ValueError(f"Invalid strength!")
            
            strength = str(float(strength))
            
            prompt, negative_prompt = self.__prompt_processor(prompt, negative_prompt, style_name, lora_svi, task_id)
            
            seed = self.__random_seed_generator(image_seed, task_id)
            
            model_name = self.__atr_models_svi.get(model_name)
            if not model_name:
                raise ValueError(f"Invalid model name!")

            image_size = self.__atr_size.get(image_size)
            if not image_size:
                raise ValueError(f"Invalid image size!")
            
            url = self.__ime + self.__atr_generate
            header = self.__xea
            
            body = {
                "image": ("guide.png", guide_array, "image/png"),
                "negative_prompt": (None, negative_prompt),
                "enable_layer_diffusion": (None, "false"),
                "enable_adetailer": (None, "false"),
                "control_weight": (None, strength),
                "aspect_ratio": (None, image_size),
                "variation": (None, "restyle"),
                "style_id": (None, model_name),
                "enable_hr": (None, "true"),
                "is_enhance": (None, "0"),
                "prompt": (None, prompt),
                "seed": (None, seed)
            }
            
            return self.__service_request(url, header, body, task_id = task_id)
        
        except Exception as e:
            self.logger.error(f"[{task_id}] Error in image_style: {e}")
            raise

    def image_outpaint(self, image: str, image_size: str = "16:9"):
        """
        Outpainting images with a mask.

        Parameters:
        - image (file): Source image file.
        - image_size (str): Desired image size ratio.
        """
        try:
            task_id = self.__get_task_id()
            
            byte_array = self.__image_processor(image, task_id = task_id)
            if not byte_array:
                raise ValueError(f"Invalid image!")
            
            image_size = self.__atr_size.get(image_size)
            if not image_size or image_size in ["12:5", "5:12"]:
                raise ValueError(f"Invalid image size!")
            
            url = self.__ime + self.__atr_outpaint
            header = self.__xea
            
            body = {
                "image": ("image.png", byte_array, "image/png"),
                "aspect_ratio": (None, image_size)
            }
            
            return self.__service_request(url, header, body, task_id = task_id)
            
        except Exception as e:
            self.logger.error(f"[{task_id}] Error in image_outpaint: {e}")
            raise

    def realtime_canvas(self, image: str, prompt: str, negative_prompt: str = "", lora_rt: str = "none",
                        strength: float = 0.9, image_seed: int = 0, style_name: str = "none"):
        """
        Instant drawing canvas.

        Parameters:
        - image (file): Source image file.
        - prompt (str): User's positive prompt.
        - negative_prompt (str): User's negative prompt.
        - lora_rt (str): Name of the LoRA RT preset.
        - strength (float): Strength of creativity application.
        - image_seed (int): Seed for image generation.
        - style_name (str): Name of the style preset.
        """
        try:
            task_id = self.__get_task_id()
            
            byte_array = self.__image_processor(image, task_id = task_id)
            if not byte_array:
                raise ValueError(f"Invalid image!")
            
            prompt, _ = self.__prompt_processor(prompt, "", style_name, task_id = task_id)
            
            seed = self.__random_seed_generator(image_seed, task_id)
            
            strength = str(float(strength))
            
            lora_rt = self.__atr_lora_rt.get(lora_rt)
            if not lora_rt:
                raise ValueError(f"Invalid lora style!")
            
            url = self.__ime + self.__atr_canvas
            header = self.__xea
            
            body = {
                "image": ("input.png", byte_array, "image/png"),
                "negative_prompt": (None, negative_prompt),
                "lora_style": (None, lora_rt),
                "strength": (None, strength),
                "prompt": (None, prompt),
                "style_id": (None, "1"),
                "seed": (None, seed)
            }

            return self.__service_request(url, header, body, task_id = task_id)

        except Exception as e:
            self.logger.error(f"[{task_id}] Error in realtime_canvas: {e}")
            raise

    def realtime_generate(self, prompt: str, negative_prompt: str = "", image_size: str = "1:1",
                          lora_rt: str = "none", image_seed: int = 0, style_name: str = "none"):
        """
        Instant image generation.

        Parameters:
        - prompt (str): User's positive prompt.
        - negative_prompt (str): User's negative prompt.
        - image_size (str): Desired image size ratio.
        - lora_rt (str): Name of the LoRA style preset.
        - image_seed (int): Seed for image generation.
        - style_name (str): Name of the style preset.
        """
        try:
            task_id = self.__get_task_id()
            
            prompt, _ = self.__prompt_processor(prompt, "", style_name, task_id = task_id)
            
            seed = self.__random_seed_generator(image_seed, task_id)
            
            image_size = self.__atr_size.get(image_size)
            if not image_size:
                raise ValueError(f"Invalid image size!")
            
            lora_rt = self.__atr_lora_rt.get(lora_rt)
            if not lora_rt:
                raise ValueError(f"Invalid lora style!")
            
            url = self.__ime + self.__atr_realtime
            header = self.__xea
            
            body = {
                "negative_prompt": (None, negative_prompt),
                "aspect_ratio": (None, image_size),
                "lora_style": (None, lora_rt),
                "prompt": (None, prompt),
                "style_id": (None, "1"),
                "seed": (None, seed)
            }
            
            return self.__service_request(url, header, body, task_id = task_id)

        except Exception as e:
            self.logger.error(f"[{task_id}] Error in realtime_generate: {str(e)}")
            raise

    def image_inpaint(self, image: str, prompt: str, mask: str = None, style_name: str = "none"):
        """
        Inpaint elements into an image.

        Parameters:
        - image (file): Source image file.
        - prompt (str): User's positive prompt.
        - mask (file): Mask image file.
        - style_name (str): Name of the style preset.
        """
        try:
            task_id = self.__get_task_id()
            
            source_image = self.__image_processor(
                image,
                gr_editor_type='background' if self.gradio else None,
                task_id = task_id
            )
            if not source_image:
                raise ValueError(f"Invalid image!")
            
            mask_image = self.__image_processor(
                image if self.gradio else mask,
                gr_editor_type='mask' if self.gradio else None,
                task_id = task_id
            )
            if not mask_image:
                raise ValueError(f"Invalid mask image!")
            
            prompt, _ = self.__prompt_processor(prompt, "", style_name, task_id = task_id)

            url = self.__ime + self.__atr_inpaint
            header = self.__xea
            
            body = {
                "image": ("image.png", source_image, "image/png"),
                "mask": ("mask.png", mask_image, "image/png"),
                "variation": (None, "inpaint"),
                "model_version": (None, "1"),
                "prompt": (None, prompt),
                "priority": (None, "1"),
                "cfg": (None, "10.0")
            }

            return self.__service_request(url, header, body, task_id = task_id)

        except Exception as e:
            self.logger.error(f"[{task_id}] Error in image_inpaint: {str(e)}")
            raise

    def image_erase(self, image: str, mask: str = None):
        """
        Erase specific elements from an image.

        Parameters:
        - image (file): Source image file.
        - mask (file): Mask image file.
        """
        try:
            task_id = self.__get_task_id()
            
            source_image = self.__image_processor(
                image,
                gr_editor_type='background' if self.gradio else None,
                task_id = task_id
            )
            if not source_image:
                raise ValueError(f"Invalid image!")
            
            mask_image = self.__image_processor(
                image if self.gradio else mask,
                gr_editor_type='mask' if self.gradio else None,
                task_id = task_id
            )
            if not mask_image:
                raise ValueError(f"Invalid mask image!")
            
            url = self.__ime + self.__atr_eraser
            header = self.__xea
            
            body = {
                "image": ("image.png", source_image, "image/png"),
                "mask": ("mask.png", mask_image, "image/png"),
                "model_version": (None, "1"),
                "priority": (None, "1"),
                "cfg": (None, "9.0")
            }

            return self.__service_request(url, header, body, task_id = task_id)

        except Exception as e:
            self.logger.error(f"[{task_id}] Error in image_erase: {str(e)}")
            raise

    def image_enhance(self, image: str, prompt: str = "", negative_prompt: str = "", creativity: float = 0.3,
                      resemblance: float = 0.9, hdr: float = 0, style_name: str = "none"):
        """
        Generative image upscaler.

        Parameters:
        - image (file): Source image file.
        - prompt (str): User's positive prompt.
        - negative_prompt (str): User's negative prompt.
        - creativity (float): Strength of creativity application.
        - resemblance (float): Strength of resemblance application.
        - hdr (float): Strength of HDR application.
        - style_name (str): Name of the style preset.
        """
        try:
            task_id = self.__get_task_id()
            
            byte_array = self.__image_processor(image, task_id = task_id)
            if not byte_array:
                raise ValueError(f"Invalid image!")
                
            prompt, negative_prompt = self.__prompt_processor(prompt, negative_prompt, style_name, task_id = task_id)
            
            resemblance = str(float(resemblance))
            creativity = str(float(creativity))
            hdr = str(float(hdr))
            
            url = self.__ime + self.__atr_enhance
            header = self.__xea
            
            body = {
                "image": ("input.png", byte_array, "image/png"),
                "negative_prompt": (None, negative_prompt),
                "negativePrompt": (None, negative_prompt),
                "resemblance": (None, resemblance),
                "creativity": (None, creativity),
                "model_version": (None, "1"),
                "prompt": (None, prompt),
                "style_id": (None, "6"),
                "hdr": (None, hdr)
            }

            return self.__service_request(url, header, body, task_id = task_id)

        except Exception as e:
            self.logger.error(f"[{task_id}] Error in image_enhance: {str(e)}")
            raise

    def image_controlnet(self, image: str, prompt: str, negative_prompt: str = "", model_name: str = "sd-toon", 
                         controlnet: str = "scribble", strength: int = 70, cfg: float = 9.0, 
                         image_seed: int = 0, style_name: str = "none"):
        """
        Controls an image into a different subject.

        Parameters:
        - image (file): Source image file.
        - prompt (str): User's positive prompt.
        - negative_prompt (str): User's negative prompt.
        - model_name (str): Name of the model to use.
        - controlnet (str): Type of controlnet ('scribble', 'pose', 'line-art', 'depth', 'canny').
        - strength (int): Strength of controlnet application.
        - cfg (float): Scale of the prompt.
        - image_seed (int): Seed for image generation.
        - style_name (str): Name of the style preset.
        """
        try:
            task_id = self.__get_task_id()
            
            byte_array = self.__image_processor(image, task_id = task_id)
            if not byte_array:
                raise ValueError(f"Invalid image!")
                
            prompt, negative_prompt = self.__prompt_processor(prompt, negative_prompt, style_name, task_id = task_id)

            seed = self.__random_seed_generator(image_seed, task_id)
            
            strength = str(int(strength))
            cfg = str(float(cfg))
            
            model_name = self.__atr_remix_model.get(model_name)
            if not model_name:
                raise ValueError(f"Invalid model name!")

            controlnet = self.__atr_controlnets.get(controlnet)
            if not controlnet:
                raise ValueError(f"Invalid controlnet type!")
            
            url = self.__ime + self.__atr_remix
            header = self.__xea
            
            body = {
                "image": ("input.png", byte_array, "image/png"),
                "negative_prompt": (None, negative_prompt),
                "high_res_results": (None, "1"),
                "style_id": (None, model_name),
                "control": (None, controlnet),
                "model_version": (None, "1"),
                "strength": (None, strength),
                "prompt": (None, prompt),
                "priority": (None, "1"),
                "seed": (None, seed),
                "cfg": (None, cfg)
            }

            return self.__service_request(url, header, body, task_id = task_id)

        except Exception as e:
            self.logger.error(f"[{task_id}] Error in image_controlnet: {str(e)}")
            raise

    def face_gfpgan(self, image: str, model_version: str = "1.3"):
        """
        Uses gfpgan to restore faces.

        Parameters:
        - image (file): Source image file.
        - model_version (str): Model version ('1.3', '1.2').
        """
        try:
            task_id = self.__get_task_id()
            
            input_array = self.__image_processor(image, resize=True, task_id = task_id)
            if not input_array:
                raise ValueError(f"Invalid image!")
            
            arc_array = BytesIO(base64.b64decode(self.__atr_test))
        
            version = self.__atr_gfpgan.get(model_version)
            if not version:
                raise ValueError(f"Invalid model version!")
        
            url = self.__arc
            header = None
            
            data = {
                "model_seltct": version
            }
            
            files = {
                "file": ("file.png", input_array, "image/png"),
                "file2": ("file2.jpg", arc_array, "image/jpeg")
            }
            
            return self.__service_request(url, header, files, data, custom = "gfpgan", task_id = task_id)

        except Exception as e:
            self.logger.error(f"[{task_id}] Error in face_gfpgan: {str(e)}")
            raise

    def face_codeformer(self, image: str):
        """
        Uses codeformer to restore faces.

        Parameters:
        - image (file): Source image file.
        """
        try:
            task_id = self.__get_task_id()
            
            byte_array = self.__image_processor(image, task_id = task_id)
            if not byte_array:
                raise ValueError(f"Invalid image!")
                
            url = self.__inf + self.__atr_codeformer
            header = self.__xea
            
            body = {
                "image": ("input.png", byte_array, "image/png"),
                "model_version": (None, "1")
            }

            return self.__service_request(url, header, body, task_id = task_id)

        except Exception as e:
            self.logger.error(f"[{task_id}] Error in face_codeformer: {str(e)}")
            raise

    def image_upscale(self, image: str):
        """
        Upscales an image.

        Parameters:
        - image (file): Source image file.
        """
        try:
            task_id = self.__get_task_id()
            
            byte_array = self.__image_processor(image, task_id = task_id)
            if not byte_array:
                raise ValueError(f"Invalid image!")
                
            url = self.__ime + self.__atr_upscale
            header = self.__xea
            
            body = {
                "image": ("input.png", byte_array, "image/png"),
                "model_version": (None, "1")
            }

            return self.__service_request(url, header, body, task_id = task_id)

        except Exception as e:
            self.logger.error(f"[{task_id}] Error in image_upscale: {str(e)}")
            raise

    def image_bgremove(self, image: str):
        """
        Removes background from an image.

        Parameters:
        - image (file): Source image file.
        """
        try:
            task_id = self.__get_task_id()
            
            byte_array = self.__image_processor(image, task_id = task_id)
            if not byte_array:
                raise ValueError(f"Invalid image!")
                
            url = self.__ime + self.__atr_bgremove
            header = self.__xea
            
            body = {
                "image": ("input.png", byte_array, "image/png"),
                "model_version": (None, "1")
            }

            return self.__service_request(url, header, body, task_id = task_id)

        except Exception as e:
            self.logger.error(f"[{task_id}] Error in image_bgremove: {str(e)}")
            raise

    def image_caption(self, image: str):
        """
        Turns input image into a descriptive caption.

        Parameters:
        - image (file): Source image file.
        """
        try:
            task_id = self.__get_task_id()
            
            byte_array = self.__image_processor(image, task_id = task_id)
            if not byte_array:
                raise ValueError(f"Invalid image!")
                
            url = self.__ime + self.__atr_caption
            header = self.__xea
            
            body = {
                "image": ("input.png", byte_array, "image/png")
            }

            return self.__service_request(url, header, body, custom="caption", task_id = task_id)

        except Exception as e:
            self.logger.error(f"[{task_id}] Error in image_caption: {str(e)}")
            raise

    def image_prompt(self, image: str):
        """
        Turns input image into a prompt.

        Parameters:
        - image (file): Source image file.
        """
        try:
            task_id = self.__get_task_id()
            
            byte_array = self.__image_processor(image, task_id = task_id)
            if not byte_array:
                raise ValueError(f"Invalid image!")
                
            url = self.__ime + self.__atr_prompt
            header = self.__xea
            
            body = {
                "image": ("input.png", byte_array, "image/png"),
                "model_version": (None, "1")
            }

            return self.__service_request(url, header, body, task_id = task_id)

        except Exception as e:
            self.logger.error(f"[{task_id}] Error in image_prompt: {str(e)}")
            raise

    def start_api(self, host: str = '0.0.0.0', port: int = None, debug: bool = False):
        """
        Start the API server with all endpoints.

        Parameters:
        - host (str): Host to run the server on (default: '0.0.0.0')
        - port (int): Port to run the server on (default: None)
        - debug (bool): Enable Flask debug mode (default: False)
        """
        try:
            from .api import AtelierWebAPI
            self.save_as = 'pil'
            AtelierWebAPI(self, host=host, port=port, debug=debug)
        
        except Exception as e:
            self.logger.error(f"WebAPI error: {str(e)}")
            raise
        
    def start_webui(self, host: str = None, port: int = None, browser: bool = False, upload_size: str = "4MB",
                    public: bool = False, limit: int = 10, quiet: bool = False):
        """
        Start Atelier WebUI with all features.
        
        Parameters:
        - host (str): Server host (default: None)
        - port (int): Server port (default: None) 
        - browser (bool): Launch browser automatically (default: False)
        - upload_size (str): Maximum file size for uploads (default: "4MB")
        - public (bool): Enable public URL mode (default: False)
        - limit (int): Maximum number of concurrent requests (default: 10)
        - quiet (bool): Enable quiet mode (default: False)
        """
        try:
            from .webui import AtelierWebUI
            self.gradio = True
            AtelierWebUI(self, host=host, port=port, browser=browser, upload_size=upload_size,
                         public=public, limit=limit, quiet=quiet)
        
        except Exception as e:
            self.logger.error(f"WebUI error: {str(e)}")
            raise