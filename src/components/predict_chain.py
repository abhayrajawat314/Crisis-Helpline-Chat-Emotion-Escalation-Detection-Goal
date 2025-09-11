from langchain.prompts import PromptTemplate
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from src.entity.config_entity import PredictionOutput
from typing import Optional
from dotenv import load_dotenv
import os, json, traceback, re

load_dotenv()

class CrisisHelplinePredictor:
    def __init__(self, model_repo_id="HuggingFaceTB/SmolLM3-3B", temperature=0):
        
        self.llm = HuggingFaceEndpoint(
            repo_id=model_repo_id,
            task="text-generation",
            temperature=temperature,
            model_kwargs={"hf_token": os.environ.get("HF_TOKEN")}
        )

        
        self.model = ChatHuggingFace(llm=self.llm)

       
        base_prompt = """
You are an expert crisis helpline assistant.
Output **ONLY valid JSON** in the exact format below, nothing else:

{{"risk_level": "Low/Medium/High", "events": ["..."], "rationale": "..."}}

Conversation:
{conversation}
"""
        
        self.template = PromptTemplate(
            input_variables=["conversation"],
            template=base_prompt
        )

       
        self.predict_chain = self.template | self.model

    def predict(self, conversation_text: str) -> Optional[PredictionOutput]:
        """
        Predicts escalation risk based on conversation text.
        Returns a PredictionOutput instance or None if error occurs.
        """
        try:
            
            raw_output_obj = self.predict_chain.invoke({"conversation": conversation_text})

            if hasattr(raw_output_obj, "content"):
                raw_output = raw_output_obj.content
            else:
                
                raw_output = str(raw_output_obj)

            match = re.search(r'\{.*\}', raw_output, re.DOTALL)
            if not match:
                print("[Warning] No JSON found in LLM output")
                print("LLM output was:", raw_output)
                return None

            json_str = match.group()

            data = json.loads(json_str)

            result = PredictionOutput(**data)
            return result

        except Exception as e:
            import traceback
            print(f"[Error] In prediction: {str(e)}")
            print(traceback.format_exc())
            return None
