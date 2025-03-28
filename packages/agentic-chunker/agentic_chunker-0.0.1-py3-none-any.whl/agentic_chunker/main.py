from openai import OpenAI
import json

from . import prompts

class AgenticChunker:
    def __init__(self, api_key: str, model: str, base_url = None):
        if base_url:
            self.client = OpenAI(base_url=base_url, api_key=api_key)
        else:
            self.client = OpenAI(api_key=api_key)
        self.model = model

    def validate_response(self, response: str) -> dict:
        try:
            data = json.loads(response)
            assert "output" in data, "Missing 'output' field"
            return data
        except (json.JSONDecodeError, AssertionError) as e:
            raise ValueError(f"Invalid JSON format: {str(e)}")

    def agentic_chunking(self, text: str, seperator: str) -> list:
        chunks = []
        original_chunks = text.split(seperator)
        current_chunk = None
        previous_chunk = None
        for chunk in original_chunks:
            current_chunk = chunk
            if not previous_chunk:
                previous_chunk = current_chunk
                chunks.append(current_chunk)
            else:
                prompt = prompts.AGENTIC_CHUNKER_PROMPT.format(
                    previous_chunk=previous_chunk,
                    current_chunk=current_chunk
                )
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"}
                )
                print(response.choices[0].message.content)
                processed_response = self.validate_response(response.choices[0].message.content)
                if processed_response:
                    processed_chunk = processed_response['output']
                    chunks.append(processed_chunk)
                    previous_chunk = processed_chunk
                else:
                    print("current chunk: ", current_chunk)
                    break
        return chunks



# file_path = "test_files/pronoun_dep.md"
# # file_path = "test_files/multi_sentense_context.md"
# api_key = "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"
# with open(file_path, 'r', encoding='utf-8') as f:
#     md_content = f.read()
# text = markdown.markdown(md_content)
# chunker = AgenticChunker(api_key=api_key, model="gpt-4o-mini")
# chunks = chunker.agentic_chunking(text, '.')
# for chunk in chunks:
#     print("*******")
#     print(chunk)
# pdb.set_trace()
