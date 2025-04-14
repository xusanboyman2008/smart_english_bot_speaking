from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",  # Replace with your real key
)

def get_scores(speech_text):
    prompt = f"""
    🧑‍🏫 You are an expert IELTS Speaking examiner.

    You must strictly follow this format for an Aiogram Telegram bot with `parse_mode=HTML`. If you break HTML formatting or use unsupported tags, the bot will crash and never forget to put end tag properly at the end. Be extremely careful.

    ---

    <b>🎯 STEP 1: CORRECT GRAMMAR MISTAKES</b>  
(    Show the student's original speech. If there are grammar mistakes, strike through <s>only the incorrect word</s> (not the whole sentence) and follow it with the corrected word in <i>italics</i>.)
    ✅ Allowed HTML tags: <b>, <i>, <s>, <code>  
    ❌ Never use: <u>, <strike>, <br>, <div>, <p>, etc.  
    ⚠️ Every tag must be properly closed. If any tag is left open, the response is invalid.

    Then summarize key grammar or sentence structure issues briefly under:

    <b>🔑 KEY GRAMMAR/SENTENCE STRUCTURE ERRORS:</b>  
    (use bullet points and <b> tags if needed)

    ---

    <b>📚 STEP 2: ADVANCED VOCABULARY CHECK</b>  

    <b>☀️ USED ADVANCED WORDS (IF ADVANCED WORDS ARE USED):</b>  
    ✅ [advanced word 1]  
    ✅ [advanced word 2]  
    ✅ [advanced word 3]  

    <b>💎 IF NO ADVANCED WORDS ARE USED:</b> Suggest 2–3 better synonyms inside a <pre> block.  
    Use this format exactly:

    <pre>advanced_words
    📝 nice 👇  
            ✨ pleasant (B2), 🌸 delightful (C1), 🌟 impressive (B2)  
    📝 good 👇  
            💯 remarkable (C1), 🎯 exceptional (C1), 🏅 beneficial (B2)
    </pre>

    Do not change this format or add emojis/tags outside <pre>.

    ---

    <b>🎯 STEP 3: SCORE THE RESPONSE USING IELTS SPEAKING CRITERIA</b>  

    <b>🗣️ FLUENCY AND COHERENCE: score (e.g., 5, 6, 7)</b>  
    <i>Short explanation here</i>  

    <b>🧠 LEXICAL RESOURCE: score</b>  
    <i>Use of vocabulary, errors or feedback</i>  

    <b>🛠️ GRAMMATICAL RANGE AND ACCURACY: score+0.5</b>  
    <i>Errors and feedback here</i>  

    <b>🔊 PRONUNCIATION: score</b>  
    <i>Clarity and fluency feedback</i>  

    <b>💫 OVERALL BAND SCORE:</b>  
    (sum the 4 above scores, divide by 4, round to nearest half if needed. Show only the number like 5.5 or 6)

    ---

        (Do NOT repeat it again, just analyze it in steps above.)🎧 <b>STUDENT'S TRANSCRIPTION:</b>  

    Input:
    {speech_text}
    """

    try:
        completion = client.chat.completions.create(
            model="openrouter/optimus-alpha",
            messages=[
                {
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}]
                }
            ],
            max_tokens=2000
        )

        result = completion.choices[0].message.content
        print("\nAI Feedback:\n", result)
        return result

    except Exception as e:
        print("❌ Error occurred:", e)
        if hasattr(e, 'response') and e.response:
            print("Error response:", e.response.text)

def fix_error(speech_text,error):
    prompt=f"""You role is programmer of aiogram and you should fix the text 

the error is {error} and fix this text for aiogram parse_mode='HTML' just give me ready made text
the text is {speech_text}"""
    try:
        completion = client.chat.completions.create(
            model="openrouter/optimus-alpha",
            messages=[
                {
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}]
                }
            ],
            max_tokens=2000
        )

        result = completion.choices[0].message.content
        print("\nAI Feedback:\n", result)
        return result

    except Exception as e:
        print("❌ Error occurred:", e)
        if hasattr(e, 'response') and e.response:
            print("Error response:", e.response.text)