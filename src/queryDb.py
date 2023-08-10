from dotenv import load_dotenv
from langchain.sql_database import SQLDatabase
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.llms.openai import OpenAI
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI

load_dotenv()

db = SQLDatabase.from_uri("mssql+pyodbc://@localhost:1433/oodledev?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes",
                          )
toolkit = SQLDatabaseToolkit(db=db, llm=OpenAI(temperature=0))

agent_executor = create_sql_agent(
    llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo"),
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    prefix=
    """Given an input question, first create a syntactically correct MSSQL query to run, then look at the results of the query and return the answer.
    Alias the tables in the query to avoid ambiguity. The Model Number is stored in the Number column of the Models table. Purchase order line
    productmodelid references the modelid of models.If you get an error while executing a query, rewrite the query and try again.
    DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database. If the question does not seem related to the database, just return "I don\'t know" as the answer."""
)

agent_executor.run('How many purchase orders are there for model number RJ38-V3-DC35?')