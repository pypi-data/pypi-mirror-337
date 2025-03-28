# ai_api_utils
just a wrapper for multiple apis like deepseek or google


## Usage

- install the package
```bash
pip install ai_api_utils
```

- export your keys
> we did this so you can use environment variables and secrets
```bash
export GEMINI_API_KEY="..."
export DEEPSEEK_API_KEY="..."
```
- import and use
```python
from  ai_api_utils import generate_gemini_text
prompt="how is the weather in paris?"
instructions="you are the weather reporter"
max_tokens=256
response=generate_gemini_text(prompt, instructions,max_tokens)
```
