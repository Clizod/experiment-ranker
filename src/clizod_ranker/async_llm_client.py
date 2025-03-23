
import os
import time
import asyncio
import random
import openai
import tiktoken
import pandas as pd

class AsyncLLMClient:
    MAX_RETRIES = 5       # Maximum number of retries for a single request
    BASE_DELAY = 2        # Base delay for exponential backoff (in seconds)
    API_DELAY = 8.64      # API recommended delay
    JITTER = 2            # Jitter to prevent synchronized retries
    
    def __init__(self, info, output_format):
        self.info = info
        self.output_format = output_format
        self.target_model = self.info['target_model']
        self.source = self.info['source']
        self.encoder = tiktoken.encoding_for_model(self.info['target_model'])
        self.tokens_per_minute = self.info['tokens_per_minute']
        self.requests_per_minute = self.info['requests_per_minute']
        self.max_tokens = self.info['max_tokens']
        self.request_limit = self.info['request_limit']
        
        self.async_client = None
        self.limit_request = None
        self.cumulative_token_count = 0
        self.tpm_start = None        
        
        
    def get_async_client(self):
        if self.source == 'openAI':
            return openai.AsyncOpenAI(api_key=os.environ.get('OPEN_AI_API_KEY'), max_retries=0)
        else:
            raise ValueError(f'Unknown source "{self.source}"')
        
    async def throttle(self):
        await asyncio.sleep(60 / self.requests_per_minute)  # Sleep to ensure we are within rate limit

    def get_token_count(self, system_prompt:str, user_prompt:str):
        return len(self.encoder.encode(system_prompt)) + len(self.encoder.encode(user_prompt)) + self.max_tokens

    def initialize(self):
        self.async_client = self.get_async_client()
        self.limit_request = asyncio.Semaphore(self.request_limit)
        self.cumulative_token_count = 0
        self.tpm_start = time.perf_counter()
    
    async def make_request(self, request_id:str, system_prompt:str, user_prompt:str) -> (bool ,str):
        retries = 0
        delay = self.BASE_DELAY
        while retries < self.MAX_RETRIES:
            try:
                completion = await self.async_client.chat.completions.create(
                    model = self.target_model,
                    temperature = 0,                   # We want consistency not creativity so setting temperature to 0
                    max_tokens = self.max_tokens,      # Restrict the length of the output
                    top_p = 1,                         # Controls the randomness in the model output by the top tokens whose cumulative probability exceeds a defined threshold
                    frequency_penalty = 0,             # Used to reduce the likelihood of sampling repetitive sequences 
                    presence_penalty = 0,              # Same as above (see docs)
                    messages=[
                        { "role": "system", "content": system_prompt },
                        { "role": "user", "content": user_prompt}
                    ],
                    response_format = self.output_format            
                )
        
                if completion.choices[0].message.refusal:
                    return (False, f"Error: Request {request_id} was refused. {completion.choices[0].message.refusal}</ERROR>")
                else:
                    return (True, completion.choices[0].message.content)
    
            except openai.APIError as e:
                    # Handle rate limiting and retryable API errors
                    # https://github.com/openai/openai-python/blob/534d6c58f6c07d219ca74dd336eaca59d48d0ada/src/openai/_exceptions.py#L34 
                    print("---------------------------------------------------------------------------------")
                    print(f"APIError error message for request {request_id}: Attempt {retries}/{self.MAX_RETRIES}")
                    print(f"   HTTP Status Code: {e.code}")
                    print(f"   Body: {e.body}")
            
                    if retries < self.MAX_RETRIES:
                        wait_time = self.API_DELAY + delay + random.uniform(0, self.JITTER)  # Add jitter to delay                   
                        print(f"   Retrying in {wait_time:.2f}s...")                  
                        await asyncio.sleep(wait_time)
                        retries += 1
                        delay *= 2  # Exponential backoff
                    else:
                        return (False, f"Error: OpenAI API failed after {self.MAX_RETRIES} retries for request {request_id}: {e}.")
    
            except Exception as e:
                return (False, f"Error: An unexpected error occurred for request {request_id}: {e}")
    
        return (False, f"Error: Unknown error for request {request_id}.")


    async def execute(self, request_id:str, sys_prompt:str, user_prompt:str, result_file_path:str = None):
           
        token_count = self.get_token_count(sys_prompt, user_prompt)
        async with self.limit_request:

            if self.cumulative_token_count + token_count > self.tokens_per_minute:
                time_to_wait = time.perf_counter() - self.tpm_start + random.uniform(0, self.JITTER)   # we wait till tpm resets + jitter so that they don't start at once
                await asyncio.sleep(time_to_wait)
            
            if time.perf_counter() - self.tpm_start >= 60:
                # reset token count
                self.tpm_start = time.perf_counter()    
                self.cumulative_token_count = 0            
    
            self.cumulative_token_count += token_count
            (success, response) = await self.make_request(request_id, sys_prompt, user_prompt)
            
            if not success:
                print(response)

            if result_file_path is not None:
                df = pd.DataFrame([[request_id, response]], columns=["request_id", "response"])
                df.to_csv(result_file_path, mode="a", index=False, header=False, doublequote=True)            
            else:
                print(response)
        return
