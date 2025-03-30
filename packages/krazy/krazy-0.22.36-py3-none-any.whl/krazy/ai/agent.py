import chromadb
from chromadb.utils.embedding_functions import EmbeddingFunction
import openai
import os
from crewai import Agent, Task, LLM, Crew, Process
from pathlib import Path
from typing import Dict, List, Optional, Any
from krazy.ai.tools import (
    PDFReaderTool, CSVCustomReaderTool, WebSearchTool, 
    ExcelImportTool, CSVorExcelExportTool,
    WordFileReaderTool, PowerPointFileReaderTool, FolderListFilesTool
)
from pydantic import BaseModel
from typing import Optional, Union
from krazy.ai.tools import Config
import json

# ✅ Custom Azure OpenAI Embedding Function for ChromaDB
class AzureOpenAIEmbeddingFunction(EmbeddingFunction):
    """
    A custom embedding function that uses Azure OpenAI to generate vector embeddings for input texts.

    Attributes:
        api_key (str): Azure OpenAI API key.
        api_base (str): Azure endpoint base URL.
        api_version (str): Azure OpenAI API version.
        model (str): The model used to generate embeddings (e.g., 'text-embedding-ada-002').

    Methods:
        __call__(input_texts: List[str]) -> List[List[float]]:
            Generates embeddings for a list of input strings.
    """

    def __init__(self, api_key: str, api_base: str, api_version: str, model: str = 'text-embedding-ada-002'):
        if not api_key:
            raise ValueError("Azure OpenAI API key is required.")
        if not api_base:
            raise ValueError("Azure API base endpoint is required.")
        if not api_version:
            raise ValueError("Azure API version is required.")

        self.api_key = api_key
        self.api_base = api_base
        self.api_version = api_version
        self.model = model

    def __call__(self, input_texts: list) -> list:
        """
        Generates embeddings using Azure OpenAI for the given input texts.

        Args:
            input_texts (list): A list of strings for which embeddings are to be generated.

        Returns:
            list: A list of embedding vectors corresponding to the input texts.

        Raises:
            ValueError: If input_texts is not a valid list of strings.
            RuntimeError: If Azure OpenAI fails to return valid embeddings.
        """
        if not isinstance(input_texts, list) or not all(isinstance(t, str) for t in input_texts):
            raise ValueError("input_texts must be a list of strings.")

        try:
            client = openai.AzureOpenAI(
                api_key=self.api_key,
                azure_endpoint=self.api_base,
                api_version=self.api_version
            )

            response = client.embeddings.create(
                input=input_texts,
                model=self.model
            )

            return [r.embedding for r in response.data]

        except Exception as e:
            raise RuntimeError(f"Failed to generate embeddings via Azure OpenAI: {str(e)}")



# ✅ AI Assistant Class with ChromaDB-Based Memory
class AIAssistant:
    def __init__(self,
                 config: Config,
                 db_path="DBs/chroma_memory",
                 embedding_model: str = 'text-embedding-ada-002',
                 output_schema: Optional[BaseModel] = None,
                 llm_choice:str = 'azure',
                 verbose=True):

        # ✅ Ensure ChromaDB path exists and init memory client
        project_dir = Path(__file__).parent
        absolute_db_path = project_dir.joinpath(db_path)
        os.makedirs(absolute_db_path, exist_ok=True)

        self.config = config

        self.memory_client = chromadb.PersistentClient(path=str(absolute_db_path))
        self.memory_collection = self.memory_client.get_or_create_collection(
            name="assistant_memory",
            embedding_function=AzureOpenAIEmbeddingFunction(
                api_key=config.open_ai_api_key,
                api_base=self.config.azure_endpoint,
                api_version=self.config.azure_version,
                model=embedding_model
            )
        )

        # output schema
        self.output_schema = output_schema

        # output variables
        self.response_full = None
        self.response = None
        self.response_json = None
        self.response_dict = None
        self.response_pydantic = None
        self.verbose = verbose

        # ✅ Tools
        self.tools_list = []
        self.pdf_reader_tool = PDFReaderTool()
        self.csv_reader_tool = CSVCustomReaderTool()
        self.web_search_tool = WebSearchTool()
        self.excel_import_tool = ExcelImportTool()
        self.csv_export_tool = CSVorExcelExportTool()
        self.word_reader_tool = WordFileReaderTool()
        self.powerpoint_reader_tool = PowerPointFileReaderTool()
        self.folder_list_files_tool = FolderListFilesTool()
        self.postgres_query_tool = None
        self.web_search_tavliy_tool = None

        self.tools_list.extend([
                self.pdf_reader_tool, self.csv_reader_tool, self.web_search_tool,
                self.excel_import_tool, self.csv_export_tool,
                self.word_reader_tool, self.powerpoint_reader_tool, self.folder_list_files_tool
            ])

        self.llm_options = {'azure': LLM(
            model=f"azure/{config.model}",
            api_key=self.config.open_ai_api_key,
            api_base=self.config.azure_endpoint,
            api_version=self.config.azure_version,
            temperature=0
        ), 'ollama': LLM(
            model='ollama/deepseek-r1:7b',
            base_url='http://localhost:11434',
            temperature=0
        )}

        # ✅ LLM Setup
        self.llm_choice = llm_choice
        self.llm = self.llm_options[self.llm_choice]

        # initialize crew
        self.reinitialize()

    def reinitialize(self):
            # ✅ LLM
            self.llm = self.llm_options[self.llm_choice]

            # ✅ Agent
            self.agent = None
            self.agent_generator()

            # ✅ Task
            self.task = None
            self.task_generator()

            # ✅ Crew
            self.crew = None
            self.crew_generator()

    def agent_generator(self):
        self.agent = Agent(
            role="AI Assistant",
            goal="Answer user queries using data and long-term memory if provided.",
            backstory="You are a knowledgeable assistant with memory capabilities.",
            llm=self.llm,
            verbose=self.verbose,
            tools = self.tools_list
        )

    def task_generator(self):
        self.task = Task(
            description= "{query}",
            expected_output = "A response to question based on given information.",
            agent = self.agent,
            output_json=self.output_schema
        )
    
    def crew_generator(self):
        self.crew = Crew(
            name="AI_Memory_Crew",
            agents=[self.agent],
            tasks=[self.task],
            process=Process.sequential
        )

    def prompt_generator(self, query, data, memory):
        if query:
            prompt = str(query)
        else:
            prompt = f'Answer this question:\n Question:{query}.'
        
        if data:
            prompt += f"\nUse this data to answer the question:\nData: {str(data)}."

        if memory != None:
            prompt += f"\\Use this context:\nContext: {str(memory)}."

        return prompt

    def store_memory(self, user_input, agent_response):
        self.memory_collection.add(
            ids=[str(len(self.memory_collection.get()["ids"]))],
            documents=[f"User: {user_input}\nAssistant: {agent_response}"]
        )

    def retrieve_memory(self, query, top_k=5):
        results = self.memory_collection.query(query_texts=[query], n_results=top_k)
        return "\n".join(results["documents"][0]) if results["documents"] else "No relevant memories found."

    def extract_json_from_text(text: str) -> Union[dict, list, None]:
        """
        Attempts to extract the first valid JSON object or array from a string.

        Args:
            text (str): A string that may contain JSON.

        Returns:
            dict | list | None: Parsed JSON object or array if found, otherwise None.
        """
        decoder = json.JSONDecoder()
        idx = 0
        while idx < len(text):
            if text[idx] in ('{', '['):  # JSON must start with object or array
                try:
                    result, end_idx = decoder.raw_decode(text[idx:])
                    return result
                except json.JSONDecodeError:
                    pass
            idx += 1
        return None

    def invoke(self, prompt, data=None, use_memory=True, save_chat_history=True, response_format="text"):
        if use_memory:
            retrieved_memories = self.retrieve_memory(prompt)
        else:
            retrieved_memories = None

        generated_prompt = self.prompt_generator(query=prompt, data=None, memory=retrieved_memories)

        self.response_full = self.crew.kickoff(inputs={"query": generated_prompt})

        if "content_filter" in str(self.response_full):
            return "⚠️ Your request was blocked due to content policy violations. Please rephrase and try again."

        try:
            self.response = self.response_full.raw
        except Exception as e:
            self.response = f"Error: {e}"

        if save_chat_history:
            self.store_memory(prompt, self.response)

        try:
            if self.output_schema:
                self.response_pydantic = self.output_schema.model_validate_json(self.response)
                self.response_dict = self.response_pydantic.model_dump()
                self.response_json = self.response_pydantic.model_dump_json()
            else:
                try:
                    self.response_json = self.extract_json_from_text(self.response)
                    self.response_dict = json.loads(self.response_json)
                except:
                    self.response_json = None
                    self.response_dict = None

        except Exception as e:
            try:
                # fallback to json exractor
                extracted_val = self.extract_json_from_text(self.response)
                if isinstance(extracted_val, dict):
                    self.response_dict = extracted_val
                    self.response_json = json.dumps(extracted_val)
            except Exception as e:
                self.response_dict = None
                self.response_json = None
                print(f"Error in output schema validation: {e}")
            

        try:
            if response_format == "json" and self.response_json is not None:
                return self.response_json
            elif response_format == "dict":
                return self.response_dict
            elif response_format == "pydantic":
                return self.response_pydantic
            elif response_format == 'text':
                return self.response
            else:
                return self.response
        except Exception as e:
            return f"Error: {e}"

