from fastapi import FastAPI
from pydantic import BaseModel, Field, create_model
from typing import Optional, List, Dict, Any
from krazy.ai.agent import AIAssistant
from krazy.ai.general import QueryRequest, build_dynamic_schema_recursive
from krazy.ai.tools import Config


def create_api(config: Config) -> FastAPI:
    app = FastAPI()
    assistant = AIAssistant(verbose=True, config=config)

    @app.post("/invoke")
    def ask_query(payload: QueryRequest):
        try:
            if payload.schema:
                dynamic_model = build_dynamic_schema_recursive("DynamicModel", dict(payload.output_schema))
                assistant.output_schema = dynamic_model
                assistant.agent_generator()
                assistant.task_generator()
                assistant.crew_generator()

            result = assistant.invoke(
                prompt=payload.query,
                use_memory=payload.use_memory,
                save_chat_history=payload.save_chat_history,
                response_format=payload.response_format,
            )
            return result
        except Exception as e:
            return {"error": str(e)}

    @app.get("/memory")
    def get_memory(query: str):
        try:
            memory = assistant.retrieve_memory(query)
            return {"query": query, "memory": memory}
        except Exception as e:
            return {"error": str(e)}
        
    @app.get("/sample_payload")
    def get_sample_payload():
        sample_payload = {
            "query": "What is the capital of France?",
            "use_memory": True,
            "save_chat_history": True,
            "response_format": "text",
            "schema": {
                'hint': 'use function extract_dynamic_schema from module general'
            }
        }
        return sample_payload

    return app
