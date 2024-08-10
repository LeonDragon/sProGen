#%% First test
from pydantic import BaseModel

from openai import OpenAI


class Step(BaseModel):
    explanation: str
    output: str


class MathResponse(BaseModel):
    steps: list[Step]
    final_answer: str


client = OpenAI()

completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": "You are a helpful math tutor."},
        {"role": "user", "content": "solve 8x + 31 = 2"},
    ],
    response_format=MathResponse,
)

message = completion.choices[0].message
if message.parsed:
    print(message.parsed.steps)
    print(message.parsed.final_answer)
else:
    print(message.refusal)
# %%
#Second test
from enum import Enum
from typing import List
from pydantic import BaseModel
from openai import OpenAI

client = OpenAI()

class UIType(str, Enum):
    div = "div"
    button = "button"
    header = "header"
    section = "section"
    field = "field"
    form = "form"

class Attribute(BaseModel):
    name: str
    value: str

class UI(BaseModel):
    type: UIType
    label: str
    children: List["UI"] 
    attributes: List[Attribute]

UI.model_rebuild() # This is required to enable recursive types

class Response(BaseModel):
    ui: UI

completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": "You are a UI generator AI. Convert the user input into a UI."},
        {"role": "user", "content": "Make a User Profile Form"}
    ],
    response_format=Response,
)

ui = completion.choices[0].message.parsed
print(ui)
# %%
from flask import Flask, render_template
from collections import namedtuple

app = Flask(__name__)

# Define the UIType Enum
class UIType:
    form = 'form'
    field = 'field'
    button = 'button'

# Define the Attribute and UI dataclasses
Attribute = namedtuple('Attribute', ['name', 'value'])
UI = namedtuple('UI', ['type', 'label', 'children', 'attributes'])

# Deserialize the given JSON-like structure
ui=UI(type=<UIType.form: 'form'>, label='User Profile Form', children=[UI(type=<UIType.field: 'field'>, label='First Name', children=[], attributes=[Attribute(name='type', value='text'), Attribute(name='placeholder', value='Enter your first name')]), UI(type=<UIType.field: 'field'>, label='Last Name', children=[], attributes=[Attribute(name='type', value='text'), Attribute(name='placeholder', value='Enter your last name')]), UI(type=<UIType.field: 'field'>, label='Email', children=[], attributes=[Attribute(name='type', value='email'), Attribute(name='placeholder', value='Enter your email')]), UI(type=<UIType.field: 'field'>, label='Phone Number', children=[], attributes=[Attribute(name='type', value='tel'), Attribute(name='placeholder', value='Enter your phone number')]), UI(type=<UIType.field: 'field'>, label='Bio', children=[], attributes=[Attribute(name='type', value='textarea'), Attribute(name='placeholder', value='Tell us about yourself')]), UI(type=<UIType.button: 'button'>, label='Submit', children=[], attributes=[Attribute(name='type', value='submit')])], attributes=[])


@app.route('/')
def index():
    # Pass the UI data to the template
    return render_template('index.html', ui=ui)

if __name__ == '__main__':
    app.run(debug=True)
