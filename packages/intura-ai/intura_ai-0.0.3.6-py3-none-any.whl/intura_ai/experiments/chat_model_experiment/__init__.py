from uuid import uuid4
from intura_ai.libs.wrappers.langchain_chat_model import (
    InturaChatOpenAI,
    InturaChatAnthropic,
    InturaChatDeepSeek,
    InturaChatGoogleGenerativeAI
)
from intura_ai.shared.external.intura_api import InturaFetch

class ChatModelExperiment:
    def __init__(self, intura_api_key=None, experiment_id=None):
        self._experiment_id = experiment_id
        self._choiced_model = None
        self._intura_api = InturaFetch(intura_api_key)
        
    @property
    def choiced_model(self):
        return self._choiced_model

    def build(self, session_id=None, features={}, max_pred=1):
        resp = self._intura_api.get_experiment_detail(self._experiment_id, features=features)
        if not resp:
            return None, {}, []
        self._data = resp["data"]
        results = []
        result = {}
        for row in self._data:
            if row["model_provider"] == "Google":
                model = InturaChatGoogleGenerativeAI
            elif row["model_provider"] == "Anthropic":
                model = InturaChatAnthropic
            elif row["model_provider"] == "Deepseek":
                model = InturaChatDeepSeek
            elif row["model_provider"] == "OpenAI":
                model = InturaChatOpenAI
            else:
                raise NotImplementedError("Model not implemented")
            
            chat_templates = [("system", f"{prompt['name']} {prompt['value']}") for prompt in row["prompts"]]
            result = model, {
                **row["model_configuration"],
                "metadata": {
                    "experiment_id": self._experiment_id,
                    "treatment_id": row["treatment_id"],
                    "treatment_name": row["treatment_name"],
                    "session_id": session_id or str(uuid4())
                }
            }, chat_templates
            results.append(result)
            if len(result) == 1:
                self._choiced_model = row["model_configuration"]["model"]
                return results[0]
            elif len(result) == max_pred:
                break
        return results
