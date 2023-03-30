import openai
import json
import pandas as pd
import subprocess

openai.organization = "org-d0E1PdrhxHIKNPdGeMqwWkpx"
# 设置OpenAI API凭证
openai.api_key = ""
with open("api_key.txt",'r',encoding='utf-8') as f:
  openai.api_key = f.read()
model = "test-model"


def read_data():
    prompt = "help me discover vulnerabilities in this smart contract"
    # 读取合约内容
    smart_contract = ""
    with open("code.txt", 'r', encoding='utf-8') as f:
        smart_contract = f.read()

    # 读取bug内容
    bug = ""
    with open("bug.txt", 'r', encoding='utf-8') as f:
        bug = f.read()

    training_data = {"prompt": prompt+"\n"+smart_contract, "completion": bug}
        # TODO add more prompts

    f = open("training_data.json","w")
    f.write(training_data)

    return

def FineTune_create():
    # 使用OpenAI API微调模型
    # 定义微调所需的参数
    training_data = "training_data.json"
    model = "ada"

    ## Start fine-tuning
    subprocess.run(
        'openai api ' + " --api-key "+ openai.api_key + "  --organization  " + openai.organization +' fine_tunes.create --training_file '+training_data + ' --model '+model
    )


# 提问
def chat_gpt(prompt):

    # 调用 微调 接口
    global model
    completion = openai.Completion.create(
        model=model,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    response = completion.choices[0].text
    print(response)


if __name__ == "__main__":
    FineTune_create()

