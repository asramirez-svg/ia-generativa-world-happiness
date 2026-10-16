"""
Agente de datos en lenguaje natural: LangChain + IBM watsonx.ai (Llama 4 Maverick)
conectado a un DataFrame de pandas con create_pandas_dataframe_agent.

Requiere credenciales de IBM watsonx.ai (API key + project_id) para ejecutarse
en vivo -- no están incluidas en este repo. El código y las notas de depuración
de abajo documentan un problema real que se encontró y resolvió al construirlo
(ver "Notas de depuración").

Dataset: student-mat.csv (UCI, Student Alcohol Consumption, 395 alumnos).
"""
import os
import pandas as pd
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_ibm import WatsonxLLM

DATA_PATH = "data/student-mat.csv"


def construir_agente():
    df = pd.read_csv(DATA_PATH)

    llm = WatsonxLLM(
        model_id="meta-llama/llama-4-maverick-17b-128e-instruct-fp8",
        url=os.environ["WATSONX_URL"],
        apikey=os.environ["WATSONX_APIKEY"],
        project_id=os.environ["WATSONX_PROJECT_ID"],
        params={"temperature": 0, "max_new_tokens": 1024},
    )

    # agent_executor_kwargs con handle_parsing_errors: ver "Notas de depuración"
    # mas abajo -- pasarlo solo en create_pandas_dataframe_agent(...) no basta.
    agent = create_pandas_dataframe_agent(
        llm,
        df,
        verbose=True,
        return_intermediate_steps=True,
        agent_executor_kwargs={"handle_parsing_errors": True},
        prefix=(
            "You are a pandas agent working with a student dataset. "
            "Never output raw data directly; summarize or plot it instead."
        ),
    )
    return agent, df


PROMPTS_DEMOSTRADOS = [
    "how many rows of data are in this file?",
    "Generate a bar chart to plot the gender count.",
    "Generate a pie chart to display average value of Walc for each Gender.",
    "Create box plots to analyze the relationship between 'freetime' and 'G3' across different levels of free time.",
    "Generate scatter plots to examine the correlation between 'Dalc' and 'G3', and between 'Walc' and 'G3'.",
]


def main():
    agent, df = construir_agente()
    for prompt in PROMPTS_DEMOSTRADOS:
        print(f"\n> {prompt}")
        response = agent.invoke(prompt)
        print(response["output"])
        print("Código usado:")
        print(response["intermediate_steps"][-1][0].tool_input.replace("; ", "\n"))


if __name__ == "__main__":
    main()

"""
## Notas de depuración (hallazgo real durante la construcción del agente)

Al ejecutar la primera consulta ("how many rows of data are in this file?")
el agente lanzaba `OutputParserException`: el LLM respondía en un formato que
LangChain no podía interpretar (no seguía el patrón ReAct
Thought/Action/Action Input/Final Answer).

`handle_parsing_errors=True` pasado directamente a
`create_pandas_dataframe_agent(...)` NO llega al `AgentExecutor` (que es
quien maneja ese error) en `langchain-experimental==0.0.57` -- hay que
pasarlo explícitamente via `agent_executor_kwargs={"handle_parsing_errors": True}`,
como está arriba.

Causa raíz observada con `verbose=True`: el modelo escribía una frase antes
de "Thought:" (ej. "To determine the number of rows...") -- texto fuera del
formato que el parser esperaba. Subir `max_new_tokens` de 256 a 1024 también
ayudó a evitar respuestas cortadas a mitad del formato.
"""
