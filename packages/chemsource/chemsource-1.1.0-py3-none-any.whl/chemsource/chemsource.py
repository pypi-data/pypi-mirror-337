from .config import Config
from .config import BASE_PROMPT

from .classifier import classify as cls
from .retriever import retrieve as ret

class ChemSource(Config):
    def __init__(self, 
                 model_api_key=None, 
                 model="gpt-4-0125-preview", 
                 ncbi_key=None, 
                 prompt=BASE_PROMPT,
                 temperature=0,
                 logprobs=None,
                 max_tokens=250000
                 ):
        super().__init__(model_api_key=model_api_key, 
                         model=model, 
                         ncbi_key=ncbi_key,
                         prompt=prompt, 
                         temperature=temperature,
                         logprobs=logprobs,
                         max_tokens=max_tokens
                         )
    
    def chemsource(self, name, priority="WIKIPEDIA", single_source=False):
        if self.model_api_key is None:
            raise ValueError("Model API key must be provided")

        information = ret(name, 
                         priority,
                         single_source, 
                         ncbikey=self.ncbi_key
                         )
        
        if information[1] == "":
            return (None, None), None
        
        return information, cls(name, 
                                information, 
                                self.model_api_key,
                                self.prompt,
                                self.model,
                                self.temperature,
                                self.top_p,
                                self.logprobs,
                                self.max_tokens)

    def classify(self, name, information):
        if self.model_api_key is None:
            raise ValueError("Model API key must be provided")
        
        if information == "":
            return None
        
        return cls(name, 
                   information,
                   self.model_api_key,
                   self.prompt,
                   self.model,
                   self.temperature,
                   self.top_p,
                   self.logprobs,
                   self.max_tokens)
    
    def retrieve(self, name, priority="WIKIPEDIA", single_source=False):
        return ret(name, 
                   priority, 
                   single_source,
                   ncbikey=self.ncbi_key
                   )