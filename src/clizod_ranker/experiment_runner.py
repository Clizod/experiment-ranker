import time
from .create_directory import create_directory
import asyncio
import datetime
import os

class ExperimentRunner:
    
    def __init__(self, promptGenerator, llmClient, results_root_dir):
        self.promptGenerator = promptGenerator
        self.llmClient = llmClient
        self.results_root_dir = results_root_dir


    async def async_run(self, df_sample, model_alias, exp):
        self.llmClient.initialize()

        exp_start_time = time.time()
        df_combs = df_sample[['disease','variable']].drop_duplicates().reset_index(drop=True)

        for index, crow in df_combs.iterrows():
                
                disease = crow['disease']
                variable = crow['variable']
                keywords = f"{disease}-{variable}"

                print(f'Processing prompts for {disease} - {variable}')
                
                #Create a results directory
                result_dir = create_directory(self.results_root_dir, [model_alias, exp, keywords])
            
                #Grab just the rows for the given disease and variable
                df_sub = df_sample.query(f"disease == '{disease}' & variable == '{variable}'")[["id","target"]]

                result_file_path = os.path.join(result_dir, f"{model_alias}_{exp}.csv")
                with open(result_file_path,"w") as f_out:
                    f_out.write(f'"id","response"\n')

                print(f'Attempting to processing {df_sub.shape[0]} records for {disease} - {variable}')
                tasks = []
                batch_start_time = time.time()
                for (idx, id, text) in df_sub.itertuples():            
                                                    
                    [sys_prompt, user_prompt] = self.promptGenerator.generate(keywords, text)

                    task = asyncio.create_task(self.llmClient.execute(id, sys_prompt, user_prompt, result_file_path))
                    tasks.append(task)

                await asyncio.gather(*tasks)
                        
                elapsed_time = time.time() - batch_start_time
                print(f"Batch completed in {str(datetime.timedelta(seconds=elapsed_time))}.")

        elapsed_time = time.time() - exp_start_time
        print(f"All batches completed in {str(datetime.timedelta(seconds=elapsed_time))}.")