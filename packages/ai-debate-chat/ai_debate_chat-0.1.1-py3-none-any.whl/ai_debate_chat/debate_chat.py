import sys
import os
from ml_pipeline_langchain import prepare_debate_facts
from langchain_community.chat_models import ChatOpenAI, ChatAnthropic
from langchain_huggingface import HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import ConversationalRetrievalChain
from langchain.llms.base import LLM
from langchain.memory import ConversationBufferMemory
from g4f.client import Client
from langchain.chains import LLMChain

# Set up minimal logging for critical errors only
import logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

class AIDebateBot:
    def __init__(self, topic="Artificial intelligence", model_choice="openai", api_key=None, 
                 local_model_path=None, g4f_provider=None, memory=None, max_memory_items=10,
                 custom_prompt=None, custom_input_variables=None):
        self.topic = topic
        self.model_choice = model_choice.lower()
        self.api_key = api_key
        self.local_model_path = local_model_path
        self.max_memory_items = max_memory_items
        self.llm_chain = None
        
        # Initialize conversation memory
        if memory:
            self.memory = memory
        else:
            self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        
        # Set API keys
        if self.model_choice == "openai" and self.api_key:
            os.environ["OPENAI_API_KEY"] = self.api_key
        elif self.model_choice == "claude" and self.api_key:
            os.environ["ANTHROPIC_API_KEY"] = self.api_key
        
        # Initialize debate knowledge base
        print(f"Initializing AI Debate Bot on topic: {self.topic}")
        print("Gathering and processing information...")
        self.debate_facts = prepare_debate_facts(self.topic)
        
        if not self.debate_facts["vector_store"]:
            print("ERROR: Failed to build knowledge base. Exiting.")
            sys.exit(1)
        
        # Initialize LLM and QA chain
        self.llm = self._initialize_llm()
        if self.llm:
            self._setup_qa_chain()
        else:
            self.qa_chain = None
            print("Limited mode: Will retrieve relevant information but cannot generate debate responses.")

    def _initialize_llm(self):
        try:
            if self.model_choice == "openai":
                if not self.api_key and not os.environ.get("OPENAI_API_KEY"):
                    return None
                return ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
                
            elif self.model_choice == "claude":
                if not self.api_key and not os.environ.get("ANTHROPIC_API_KEY"):
                    return None
                return ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0.7)
                
            elif self.model_choice == "deepseek":
                if not self.api_key and not os.environ.get("HUGGINGFACEHUB_API_TOKEN"):
                    return None
                os.environ["HUGGINGFACEHUB_API_TOKEN"] = self.api_key
                
                from langchain.llms import HuggingFaceHub
                return HuggingFaceHub(
                    repo_id="deepseek-ai/deepseek-coder-33b-instruct",
                    model_kwargs={"temperature": 0.7, "max_length": 1024}
                )
                
            elif self.model_choice == "local":
                if not self.local_model_path:
                    return None
                return self._setup_local_model(self.local_model_path)
            
            elif self.model_choice == "g4f":
                return self._setup_g4f_model()
                
            return None
                
        except Exception as e:
            logger.error(f"Error initializing model {self.model_choice}: {e}")
            return None

    def _setup_local_model(self, model_path):
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
            import torch
            
            device = "cuda" if torch.cuda.is_available() else "cpu"
            print(f"Using device: {device}")
            
            tokenizer = AutoTokenizer.from_pretrained(model_path)
            model = AutoModelForCausalLM.from_pretrained(
                model_path, 
                torch_dtype=torch.float16 if device == "cuda" else torch.float32,
                device_map="auto" if device == "cuda" else None
            )
            
            pipe = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                max_length=1024,
                temperature=0.7,
                top_p=0.95,
                repetition_penalty=1.15
            )
            
            return HuggingFacePipeline(pipeline=pipe)
            
        except Exception as e:
            logger.error(f"Error setting up local model: {e}")
            return None

    def _setup_g4f_model(self, provider=None):
        try:
            class G4FLangChain(LLM):
                model: str = "gpt-3.5-turbo"
                temperature: float = 0.7
                max_tokens: int = 1024
                
                @property
                def _llm_type(self) -> str:
                    return "g4f"
                
                def _call(self, prompt: str, stop=None) -> str:
                    try:
                        client = Client()
                        response = client.chat.completions.create(
                            model=self.model,
                            messages=[{"role": "user", "content": prompt}],
                            temperature=self.temperature,
                            max_tokens=self.max_tokens
                        )
                        
                        # Extract the text content from the response
                        if hasattr(response, 'choices') and response.choices:
                            return response.choices[0].message.content
                        elif isinstance(response, str):
                            return response
                        else:
                            logger.error(f"Unexpected response format: {type(response)}")
                            return "I couldn't generate a proper response at this time."
                            
                    except Exception as e:
                        logger.error(f"Error in G4F call: {e}")
                        return f"Error generating response: {str(e)}"
            
            return G4FLangChain()
            
        except ImportError:
            print("Error: g4f package not installed. Please install it with 'pip install g4f'")
            return None
        except Exception as e:
            logger.error(f"Error setting up g4f model: {e}")
            return None

    def _setup_qa_chain(self):
        try:
            template = f"""
            You are an AI debate assistant discussing the topic of {self.topic}.
            
            The user has asked: {{question}}
            
            Previous conversation history:
            {{chat_history}}
            
            Your response should:
            1. Directly address the query
            2. Present multiple perspectives when appropriate
            3. Cite sources when possible
            4. Be conversational and engaging
            5. End with a thought-provoking question if appropriate
            """
            
            PROMPT = PromptTemplate(
                template=template,
                input_variables=["context", "question", "chat_history"]
            )
            
            # Create an LLMChain with the memory directly
            self.llm_chain = LLMChain(
                llm=self.llm,
                prompt=PROMPT,
                memory=self.memory,
                verbose=False
            )
            
            # Still keep retriever for finding relevant info
            retriever = self.debate_facts["vector_store"].as_retriever()
            self.qa_chain = {"retriever": retriever}
            
        except Exception as e:
            logger.error(f"Error setting up QA chain: {e}")
            self.qa_chain = None
            self.llm_chain = None

    def generate_response(self, query):
        if not query.strip():
            return "Please provide a question or statement to discuss."
        
        try:
            if self.qa_chain and self.llm_chain:
                # Get relevant documents
                docs = self.qa_chain["retriever"].get_relevant_documents(query)
                
                if not docs:
                    return f"I couldn't find specific information about that in my knowledge base about {self.topic}."
                
                # Format context from retrieved documents
                context = "\n\n".join([doc.page_content for doc in docs])
                
                # Add context to the query
                enhanced_query = f"Based on this information: {context}\n\nRespond to: {query}"
                
                # Use LLMChain directly with memory
                result = self.llm_chain.predict(question=enhanced_query)
                
                # Add sources if available
                sources = {doc.metadata["source"] for doc in docs if "source" in doc.metadata}
                if sources:
                    result += f"\n\nSources: {', '.join(sources)}"
                
                # Trim memory if it's getting too long
                self._trim_memory()
                
                return result
            else:
                # Limited mode - just retrieve relevant passages
                docs = self.debate_facts["vector_store"].as_retriever().invoke(query)
                
                if not docs:
                    return f"I couldn't find specific information about that in my knowledge base about {self.topic}."
                
                response = f"Here's what I know about '{query}':\n\n"
                for i, doc in enumerate(docs[:3], 1):
                    response += f"{i}. {doc.page_content}\n\n"
                
                response += "(Note: Running in limited mode without response generation.)"
                
                # Save to memory manually since we're not using LLMChain here
                self.memory.save_context({"input": query}, {"output": response})
                
                # Trim memory if it's getting too long
                self._trim_memory()
                
                return response
                
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"Sorry, I encountered an error while responding to your query: {str(e)}"

    def run_interactive(self):
        print(f"\n===== AI Debate Bot: {self.topic} =====")
        print(f"Model: {self.model_choice.upper()}")
        print("Ask me anything about this topic or type 'exit' to quit.\n")
        
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("\nThank you for the debate! Goodbye.")
                break
            
            response = self.generate_response(user_input)
            print(f"\nDebate Bot: {response}")

    def _trim_memory(self):
        """
        Trim the conversation history when it gets too long.
        Keep the most recent conversations up to max_memory_items.
        """
        # Handle buffer type memory (backward compatibility)
        if hasattr(self.memory, 'buffer') and len(self.memory.buffer) > self.max_memory_items * 2:
            self.memory.buffer = self.memory.buffer[-(self.max_memory_items * 2):]
        
        # Handle chat_memory type (used by LLMChain)
        if hasattr(self.memory, 'chat_memory') and hasattr(self.memory.chat_memory, 'messages'):
            messages = self.memory.chat_memory.messages
            if len(messages) > self.max_memory_items * 2:  # Each exchange has human + ai message
                # Keep only the most recent messages
                self.memory.chat_memory.messages = messages[-(self.max_memory_items * 2):]

    def clear_memory(self):
        """
        Clear all conversation memory.
        Useful when starting a new conversation or when memory context needs to be reset.
        """
        # Clear the buffer if it exists
        if hasattr(self.memory, 'buffer'):
            self.memory.buffer = []

        # Clear chat_memory if it exists (for ConversationBufferMemory)
        if hasattr(self.memory, 'chat_memory'):
            self.memory.chat_memory.messages = []

        # Use the memory's own clear method if available
        if hasattr(self.memory, 'clear'):
            self.memory.clear()

        return True


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Debate Chatbot")
    parser.add_argument("--topic", type=str, default="Artificial intelligence", 
                        help="Topic for the debate")
    parser.add_argument("--model", type=str, default="openai", 
                        choices=["openai", "claude", "deepseek", "local", "g4f"],
                        help="Which LLM to use")
    parser.add_argument("--api-key", type=str, help="API key for the chosen service")
    parser.add_argument("--local-model-path", type=str, help="Path to local model")
    
    args = parser.parse_args()
    
    # Check for topic in positional arguments
    if len(sys.argv) > 1 and not sys.argv[1].startswith('-'):
        topic = " ".join(sys.argv[1:])
        for arg in sys.argv[1:]:
            if arg.startswith('-'):
                topic = " ".join(sys.argv[1:sys.argv.index(arg)])
                break
        args.topic = topic
    
    debate_bot = AIDebateBot(
        topic=args.topic,
        model_choice=args.model,
        api_key=args.api_key,
        local_model_path=args.local_model_path,
    )
    debate_bot.run_interactive()


if __name__ == "__main__":
    main()