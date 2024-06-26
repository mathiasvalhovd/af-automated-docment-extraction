import bs4
from langchain import hub
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts import ChatPromptTemplate
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
import textwrap
import getpass
import os

class Rag:
    def __init__(self):
        os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")
        os.environ["LANGCHAIN_API_KEY"] = getpass.getpass("Enter your Langchain API key: ")

        os.environ["LANGCHAIN_TRACING_V2"]= "true"
        os.environ["LANGCHAIN_ENDPOINT"]="https://api.smith.langchain.com"
        os.environ["LANGCHAIN_PROJECT"]="RAG-test"

        from langchain_openai import ChatOpenAI, OpenAI

        self.llm = ChatOpenAI(model="gpt-3.5-turbo-0125", api_key=os.environ.get("OPENAI_API_KEY"), temperature=0)

        # Specify the absolute path to the target directory
        target_directory_path = r"\Users\mava08\OneDrive - AF Gruppen ASA\Datamateriale-endringer\CCB"

        # Get the current working directory
        current_directory = os.getcwd()

        # List all files in the target directory
        files = os.listdir(target_directory_path)

        vectorstore = Chroma()
        for file_name in files:
            # Construct the absolute path to the file
            file_path = os.path.join(target_directory_path, file_name)
            
            # Check if it's a file and not a directory
            if os.path.isfile(file_path):
                # Find the relative path from the current directory to the file
                relative_path = os.path.relpath(file_path, start=current_directory)
                loader = PyPDFLoader(relative_path)
                pages = loader.load_and_split()

                
                # Split the text of the document
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
                splits = text_splitter.split_documents(pages)
                
                # Add the splits to the vectorstore
                vectorstore = vectorstore.from_documents(documents=splits, embedding=OpenAIEmbeddings())
        self.retriever = vectorstore.as_retriever()
    


    def method1(self, endring):
        # Prompt
        template = """Du er en juridisk assistent som skal granske dokumenter for å sjekke om den innkommende endringsmeldingen
        fra et selskap med krav om betaling er gyldig i henhold til relevante kontraktsdokumenter. De mener at de har utført arbeid som ikke er inkludert i kontrakten for byggeprosjektet. 
        Dette betyr i all hovedsak at du skal sjekke at dette faktisk er en endring fra det som står beskrevet i kontrakten, og at dette medfører en ekstra kostnad. 
        Har de rett på ekstra betaling, eller er arbeidet de ber om allerede inkludert i kontrakten, Begrunn svaret ditt og henvis til punkter i kontrakten og gi sitater.
        hold svaret kort og konsist, og vær så presis som mulig.
        {context}

        Question: {question}
        """

        prompt = ChatPromptTemplate.from_template(template)



        rag_chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )


        response = rag_chain.invoke(endring)
        return response
    
