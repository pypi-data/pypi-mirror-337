# NLP Date Parser

A Python package to parse natural language date expressions like:

✅ `next Tuesday`  
✅ `in 3 days`  
✅ `tomorrow at noon`  

## Installation & Usage

```sh
pip install nlp_date_parser
 
**Usage**

from nlp_date_parser import NLPDateParser

parser = NLPDateParser()
print(parser.parse("next Friday"))
