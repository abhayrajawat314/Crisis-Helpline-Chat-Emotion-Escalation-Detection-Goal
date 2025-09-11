from src.components.predict_chain import CrisisHelplinePredictor

conversation_text = """
User: I feel anxious and scared.
Consultant: Can you tell me what triggered this feeling?
User: It's my exams coming up and I can't sleep.
"""

predictor = CrisisHelplinePredictor()
result = predictor.predict(conversation_text)

if result:
    print(result)
else:
    print("Prediction failed.")
