import dash_bootstrap_components as dbc
from dash import Dash, html, Input, Output, State, callback
from langchain import OpenAI, ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.agents import create_pandas_dataframe_agent
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from config.keys import OPENAI_API_KEY
from langchain.llms import OpenAI
import pandas as pd


path_data = "./database/data/amostras_resistracker.csv"

df = pd.read_csv(path_data, sep=",", encoding="utf-8")

prompt_text = "qual microrganismo apresenta maior sensibilidade ao antibiótico Amicacina?"

agent = create_pandas_dataframe_agent(
    ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613", openai_api_key=OPENAI_API_KEY),
    df,
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
)

app = Dash(__name__,
           external_stylesheets=[dbc.themes.FLATLY])

app.layout = html.Div(
    className="main-body-page",
    children=[
        dbc.Container(
            class_name="main-body-header",
            fluid=True,
            children=[
                dbc.Button([
                    "Solude ",
                    html.Span("Responde", className="logo-title-span"),
                    ], id="open2", className="btn-goto-solude", n_clicks=0),
                dbc.Button("Acessar Resistracker", id="open", className="btn-goto-resistracker", n_clicks=0),
            ],
        ),
        dbc.Container(
                    className="main-body-container",
                    fluid=True,
                    children=[
                        html.Img(src="/assets/main-image.svg", className="main-title-image"),
                        html.Br(),
                        dbc.Row(
                            children=[
                                html.H1([
                                    html.Span("ChatBot", className="main-title-star-span"),
                                    " Solude Responde"
                                    ], className="main-title"),
                                html.H4([
                                    "Tire aqui suas dúvidas sobre a ", 
                                    html.Span("resistência dos microrganismos aos antibióticos", className="main-title-star-span"),
                                    " no Hospital Universitário da UFPI"], className="sub-title")
                            ],
                        ),
                        html.Br(),
                        dbc.Row(
                            [
                                dbc.Col(
                                    width=1,
                                ),
                                dbc.Col(
                                    width=10,
                                    children=dbc.Card(
                                        [
                                            dbc.CardBody([
                                                html.Br(),
                                                dbc.InputGroup([
                                                    dbc.Input(id='prompt', value="", placeholder='Digite aqui sua pergunta', type='text'),
                                                    dbc.Button(id='sendPrompt', children=">", n_clicks=0),
                                                    ],
                                                ),
                                                html.Br(),
                                                html.P(id='outputHuman', children=""),
                                                html.P(id='outputChatBot', children=""),
                                            ])
                                        ],
                                    )
                                ),
                                dbc.Col(
                                    width=1,
                                ),
                            ]
                        )
                    ]
                ),
    ]
)

@callback(
    Output(component_id='outputHuman', component_property='children'),
    Output(component_id='outputChatBot', component_property='children'),
    Output(component_id='prompt', component_property='value'),
    Input(component_id='sendPrompt', component_property='n_clicks'),
    State(component_id='prompt', component_property='value')
)
def call_openai_api(n, human_prompt):
    if n==0:
        return "", "", ""
    else:
        result_ai = agent.run(human_prompt)
        human_output = f"Pergunta: {human_prompt}"
        chatbot_output = f"Solude AI: {result_ai}"

        return human_output, chatbot_output, ""

if __name__ == '__main__':
    app.run_server(debug=True,
                   host='0.0.0.0',
                   port=8052,
                   )