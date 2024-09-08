import vertexai
from vertexai.generative_models import GenerativeModel


class VertexModel:
    def __init__(self, project_id: int, location: str = "us-central1", prompt: str = "") -> None:
        vertexai.init(project=project_id, location=location)
        self.model = GenerativeModel("gemini-1.5-pro-001", system_instruction=[prompt])

    async def generate_content(self, message: str) -> str:
        response = self.model.generate_content(message)

        return response.text

    async def change_system_prompt(self, prompt):
        # self.model = None
        self.model = GenerativeModel("gemini-1.5-pro-001", system_instruction=[prompt])

        return True
