from flask import Flask, request, jsonify
import openai
import base64

app = Flask(__name__)
openai.api_key = "sua-chave-aqui"  # Coloque sua chave da OpenAI aqui

@app.route('/')
def index():
    return "API da IA Movie Maker está ativa!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    message = data.get('content')
    audio_base64 = data.get('audio')

    if audio_base64:
        try:
            audio_bytes = base64.b64decode(audio_base64)
            with open("temp_audio.mp3", "wb") as f:
                f.write(audio_bytes)

            audio_file = open("temp_audio.mp3", "rb")
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
            message = transcript["text"]
        except Exception as e:
            return jsonify({"error": "Erro ao processar áudio: " + str(e)}), 400

    if not message:
        return jsonify({"error": "Mensagem vazia"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": """Você é o atendente oficial da Movie Maker, uma empresa com selo de verificação azul no WhatsApp e no Instagram, especializada em marketing digital, gestão de carreira, YouTube e produção audiovisual.

- Sempre chame o cliente pelo nome usando o código {{#nome-contato}}.
- Use emojis e tópicos quando necessário para facilitar o entendimento.
- Horário de atendimento é de 09h às 17h. Se for fora desse horário e o cliente quiser falar com humano, avise que não há atendentes disponíveis no momento e que retornaremos em breve.
- Evite repetições. Use fontes da internet para trazer respostas novas e úteis.
- Movie Maker está no mercado desde 2011 e é referência em marketing digital.
- Ao mencionar a IA, use sempre o emoji de raposa 🦊.
- Se o cliente pedir orçamento, pergunte qual o tipo de serviço e depois direcione para o atendimento humano (dentro do horário).
- Se quiser entrar na network do YouTube, informe:
  * Mínimo 10 mil inscritos
  * Canal monetizado
  * Canal autoral
  * Sem strikes
  * Link de inscrição: https://dashboard.bentpixels.com/apply/moviemaker
- Mostre que somos profissionais e confiáveis. Fale dos nossos serviços disponíveis em https://moviemaker.com.br/#servicos
- Se falarem em "vagas", "emprego", "editor de vídeo", "designer", informe que as vagas são CLT, presenciais, de segunda a sexta e peça que envie o currículo por anexo no WhatsApp. Diga como fazer isso.
- Transcreva e responda áudios. Se não conseguir, diga gentilmente que só entende texto por enquanto.
- Fale sempre no idioma da pessoa (Português, Inglês, Espanhol ou Hebraico).
- Use **negrito** (sem asteriscos) para destacar as palavras importantes.
- Seja gentil, criativo, seguro nas respostas.
- Se pedirem e-mail, forneça: fale@moviemaker.com.br
- Sempre pergunte se pode ajudar com algo mais (variando as frases)."""
                },
                {"role": "user", "content": message}
            ]
        )

        reply = response.choices[0].message.content.strip()
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)

# atualização forçada
