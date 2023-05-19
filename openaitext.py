import os
import openai
from config import apikey
openai.api_key = apikey

response = openai.Completion.create(
  model="text-davinci-003",
  prompt="write an email to my boss for resignation\n",
  temperature=1,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

print(response)


'''
{
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null,
      "text": "\nSubject: Resignation \u2013 [Your Name]\n\nDear [Employer],\n\nI am writing to inform you that I am officially resigning from my role as [Position] at [Company]. My last day of employment will be [date], and I plan to make sure all my tasks and projects are completed by then. \n\nI have appreciated all the opportunities and experiences I have had working here, and I am thankful for the support I have received from you and my colleagues. \n\nIf there is anything I can do to help during this transition, please don't hesitate to let me know. \n\nOnce again, thank you for your support and guidance over the years. \n\nSincerely,\n[Your Name]"
    }
  ],
  "created": 1684495570,
  "id": "cmpl-7HsXKGcjHfdaVVzLWDZWsoG4BuW76",
  "model": "text-davinci-003",
  "object": "text_completion",
  "usage": {
    "completion_tokens": 155,
    "prompt_tokens": 9,
    "total_tokens": 164
  }
}
'''

