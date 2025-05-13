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

if __name__ == '__main__':
    prompts = [row for row in csv.reader(open("neurips25-simeng-open-deep-research.csv", "r", encoding = "ISO-8859-1")) if "ID" not in row[0]]

    results = []
    for p in prompts:
        base_prompt = p[2]
        remove_first = f"""{p[3]}

    Do not use the fact: {p[-5]}
    """
        remove_second = f"""{p[4]}

    Do not use the fact: {p[-4]}
    """
        p[-3] = run_one(base_prompt)['compile_final_report']['final_report']
        p[-2] = run_one(remove_first)['compile_final_report']['final_report']
        p[-1] = run_one(remove_second)['compile_final_report']['final_report']
        results += [p]
        with open('eval.csv', 'w', newline='') as wfp:
            writer = csv.writer(wfp)
            writer.writerows(results)
