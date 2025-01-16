# CHRONOS: News Timeline Summarization DEMO
## Environment
```bash
 pip install -r requirements.txt 
```

```bash
 export MODEL_NAME=qwen-plus-latest

 export DASHSCOPE_API_KEY=
 export DASHSCOPE_BASE_HTTP=https://poc-dashscope.aliyuncs.com/api/v1
 export DASHSCOPE_BASE_WEBSOCKET=wss://poc-dashscope.aliyuncs.com/api-ws/v1/inference

 export REWRITER_API_KEY=
 export REWRITER_HTTP=https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation
 export REWRITER_MODEL_NAME=qwen-rag-tool-use-turbo
```

## Execution
```bash
 streamlit run app.py
```