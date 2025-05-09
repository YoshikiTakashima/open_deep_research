from langgraph_sdk import get_sync_client
import csv

client = get_sync_client(url="http://localhost:2024")

def run_one(PROMPT):
    thread = client.threads.create()
    thread_id = thread["thread_id"]
    last = {}
    for chunk in client.runs.stream(
         thread_id,
         "open_deep_research", # Name of assistant. Defined in langgraph.json.
         input={
         "topic": PROMPT,
         },
         stream_mode="updates",
    ):
         last = chunk.data
    return last

prompts = []

results = [[p, run_one(p)['compile_final_report']['final_report']] for p in prompts]


with open('eval.csv', 'w', newline='') as wfp:
    writer = csv.writer(wfp)
    writer.writerows(results)
