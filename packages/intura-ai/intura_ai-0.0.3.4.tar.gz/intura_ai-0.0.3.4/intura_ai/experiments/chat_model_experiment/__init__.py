from uuid import uuid4
from intura_ai.libs.wrappers.langchain_chat_model import (
    InturaChatOpenAI,
    InturaChatAnthropic,
    InturaChatDeepSeek,
    InturaChatGoogleGenerativeAI
)
from intura_ai.callbacks import UsageTrackCallback
from intura_ai.client import get_intura_client

class ChatModelExperiment:
    def __init__(self, experiment_id=None):
        self._initialized = False
        self._intura_api = get_intura_client()
        if self._intura_api:
            if self._intura_api.check_experiment_id(experiment_id=experiment_id):
                self._experiment_id = experiment_id
                self._initialized = True
                self._usage_callback = UsageTrackCallback(experiment_id=experiment_id)
                self._choiced_model = None
                
    @property
    def choiced_model(self):
        return self._choiced_model

    def build(self, session_id=None, features={}, n_pred=1):
        if self._initialized:
            resp = self._intura_api.get_experiment_detail(self._experiment_id, features=features)
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
                    "callbacks": [self._usage_callback],
                    "metadata": {
                        "experiment_id": self._experiment_id,
                        "treatment_id": row["treatment_id"],
                        "treatment_name": row["treatment_name"],
                        "session_id": session_id or str(uuid4())
                    }
                }, chat_templates
                if n_pred == 1:
                    self._choiced_model = row["model_configuration"]["model"]
                    return result
                else:
                    results.append(result)
            return results
        else:
            raise ValueError("Need to initialized first")
