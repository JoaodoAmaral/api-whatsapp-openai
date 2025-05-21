from flask import Flask, request, jsonify
import openai
import base64

app = Flask(__name__)
openai.api_key = "sk-proj-2r2Ef0iCvaUgEoGzXT0y4xRbVCsbSLzHb1E7u8NsnmAHfnnzfLZYVK496e3e8zmPugyv..."

@app.route('/')
def index():
    return "API da IA MovieMaker está ativa!"

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

            with open("temp_audio.mp3", "rb") as audio_file:
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
                    "content": (
                        "Você é a IA oficial da Movie Maker Ltda e deve responder como um especialista. "
                        "Sempre cumprimente o cliente com o nome dele usando o código {{#nome-contato}}. "
                        "Use emojis e organize respostas longas em tópicos. "
                        "O horário de atendimento é das 09h às 17h. Se o cliente pedir um humano fora desse horário, informe que não há especialistas disponíveis. "
                        "Se a pessoa quiser um orçamento, colete informações e direcione para o atendimento humano apenas no horário comercial. "
                        "Se perguntarem sobre vagas, explique o passo a passo para enviar currículo e informe que são vagas CLT, presenciais, de segunda a sexta. "
                        "Transcreva áudios enviados e responda com base no conteúdo. "
                        "Destaque palavras importantes em **negrito** (sem mostrar os asteriscos). "
                        "Sempre responda em português, inglês, espanhol ou hebraico de acordo com o idioma usado pelo cliente. "
                        "Responda com o emoji da raposa 🦊 no início de algumas mensagens. "
                        "Se o cliente pedir email, forneça fale@moviemaker.com.br. "
                        "Nunca seja repetitivo e pesquise informações atualizadas sobre a empresa em https://moviemaker.com.br/#servicos. "
                        "Mostre confiança, gentileza e conhecimento."
                    )
                },
                {"role": "user", "content": message}
            ]
        )
        reply = response.choices[0].message.content.strip()
        return jsonify({'reply': reply})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
