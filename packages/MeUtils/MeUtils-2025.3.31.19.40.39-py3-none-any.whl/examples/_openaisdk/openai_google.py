#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : openai_siliconflow
# @Time         : 2024/6/26 10:42
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import os

from meutils.pipe import *
from openai import OpenAI
from openai import OpenAI, APIStatusError
from meutils.schemas.openai_types import ChatCompletionRequest
from meutils.llm.openai_utils import to_openai_completion_params


client = OpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url=os.getenv("GOOGLE_BASE_URL"),
)

print(client.models.list().model_dump_json(indent=4))

# {
#     "gemini-2.0-pro-exp": "models/gemini-2.0-pro-exp",
#     "gemini-2.0-pro-exp-02-05": "models/gemini-2.0-pro-exp-02-05",
#     "gemini-2.5-pro-exp-03-25": "models/gemini-2.5-pro-exp-03-25",
#     "gemini-2.0-flash-thinking-exp": "models/gemini-2.0-flash-thinking-exp",
#     "gemini-2.0-flash": "models/gemini-2.0-flash"
#
# }


if __name__ == '__main__':


    data = {
        "model": "models/gemini-2.0-flash",
        "messages": [
            {
                "role": "user",
                "content": "hi"
            }
        ],
        "stream": False,
        "stream_options": None,
        "top_p": 0.7,
        "temperature": 0.7,
        "n": 1,
        "max_tokens": 10,
        "stop": None,
        "presence_penalty": 0.0,
        "frequency_penalty": None,
        "user": None,
        "response_format": None,
        "function_call": None,
        "functions": None,
        "tools": None,
        "tool_choice": None,
        "parallel_tool_calls": None,
        "system_messages": [],
        "last_content": "hi",
        "urls": [],
        "system_fingerprint": "🔥"
    }

    request = ChatCompletionRequest(**data)

    data = to_openai_completion_params(request)
    if 'gemini' in request.model:
        data.pop("extra_body", None)

    print(bjson(data))

    try:
        completion = client.chat.completions.create(**data)
    #     completion = client.chat.completions.create(
    #         # model="models/gemini-2.5-pro-exp-03-25",
    #         model="models/gemini-2.0-flash-thinking-exp",
    #         # model="models/gemini-2.0-flash-exp-image-generation",
    #         messages=[
    #             {"role": "user", "content": "hi"}
    #
    #             # {
    #             #     "role": "user", "content": [
    #             #     {
    #             #         "type": "text",
    #             #         "text": "9.8 9.11哪个大"
    #             #     }
    #             # ]
    #             # }
    #
    #         ],
    #         # top_p=0.7,
    #         top_p=None,
    #         temperature=None,
    #         # stream=True,
    #         stream=False,
    #
    #         max_tokens=None,
    #     )
    except APIStatusError as e:
        print(e.status_code)

        print(e.response)
        print(e.message)
        print(e.code)
    print(completion)
    for chunk in completion:  # 剔除extra body
        print(chunk)
        if chunk.choices:
            print(chunk.choices[0].delta.content)