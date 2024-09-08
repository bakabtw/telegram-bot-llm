import google.generativeai as genai


class GeminiModel:
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash", prompt: str = "") -> None:
        self.generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }
        self.model_params = {
            "model": model,
            "prompt": prompt
        }

        genai.configure(api_key=api_key)

        self.model = genai.GenerativeModel(
            model_name=self.model_params['model'],
            generation_config=self.generation_config,
            system_instruction=self.model_params['prompt']
        )

    async def generate_content(self, message: str) -> str:
        response = self.model.generate_content(message)

        return response.text

    async def change_system_prompt(self, prompt):
        # self.model = None
        self.model = genai.GenerativeModel("gemini-1.5-pro-001", system_instruction=[prompt])

        return True
