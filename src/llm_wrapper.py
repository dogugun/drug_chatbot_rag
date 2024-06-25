import os

from langchain.llms import LlamaCpp
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

BASEDIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

n_gpu_layers = 1  # Metal set to 1 is enough.
n_batch = 512  # Should be between 1 and n_ctx, consider the amount of RAM of your Apple Silicon Chip.
# Make sure the model path is correct for your system!
"""llm = LlamaCpp(
    #model_path="/Users/rlm/Desktop/Code/llama.cpp/models/openorca-platypus2-13b.gguf.q4_0.bin",
    model_path="../models/openorca-platypus2-13b.gguf.q4_0.bin",
    n_gpu_layers=n_gpu_layers,
    n_batch=n_batch,
    f16_kv=True,  # MUST set to True, otherwise you will run into problem after a couple of calls
    #callback_manager=callback_manager,
    verbose=True, # Verbose is required to pass to the callback manager
)"""

def get_gpt_llm():
    llm = LlamaCpp(
        model_path=os.path.join(BASEDIR, "models", "openorca-platypus2-13b.gguf.q4_0.bin"),
        n_gpu_layers=n_gpu_layers,
        n_batch=n_batch,
        f16_kv=True,
        verbose=True,
        n_ctx=2048
    )
    return llm

