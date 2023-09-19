import openai

openai.api_key = "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"

if __name__ == "__main__":

    response = openai.ChatCompletion.create(
              model="gpt-3.5-turbo",
              messages=[{"role": "system", "content": 'SPECIFY HOW THE AI ASSISTANT SHOULD BEHAVE'},
                        {"role": "user", "content": 'SPECIFY WANT YOU WANT THE AI ASSISTANT TO SAY'}
              ])

