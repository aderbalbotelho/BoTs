# CONTEXTS DATA
1 = """

"""

2 = """

"""

3 = """

"""

4 = """

"""

5 = """

"""

6 = """

"""

# API Settings
# Configurações da API
openai.api_key = "XxXxXxXxXxX"
openai.api_base = 'https://xxx.etx.tec.br'
media_key = "XxXxXxXxXxX"
media_base = 'https://xxx.etx.tec.br'

# Function to transcribe audio
# Função para transcrever áudio
def transcrever_audio(media_url):
    login_url = "https://acesso.webzap.tec.br/login"
    login_data = {
        "username": "XxXxXxXxXxX",
        "password": "XxXxXxXxXxX",
    }
    with requests.Session() as session:
        # Login
        # Fazer login
        login_response = session.post(login_url, data=login_data)
        if login_response.status_code == 200:
          
          # Download the audio/video file
            # Baixar o arquivo de áudio/vídeo
            media_response = session.get(media_url)
            print(f"Status do download: {media_response.status_code}")
            print(f"Tipo de conteúdo: {media_response.headers.get('Content-Type')}")

            if media_response.status_code == 200
          
                # Check if it is audio or video
                # Verificar se é áudio ou vídeo
                content_type = media_response.headers.get('Content-Type', '')
                if 'audio' in content_type or 'video' in content_type:
                  
                    # Send content directly to transcription
                    # Enviar o conteúdo diretamente para a transcrição
                    files = {
                        'file': (media_url.split('/')[-1], media_response.content, content_type)
                    }
                    data = {
                        'model': 'whisper-1',
                        'language': 'pt'
                    }
                    response = requests.post(f"{openai.api_base}/audio/api/v1/transcriptions", headers={
                        "Authorization": f"Bearer {openai.api_key}"
                    }, files=files, data=data)

                    if response.status_code == 200:
                        return response.json()["text"]
                    else:
                        raise Exception(f"Erro ao converter áudio para texto: Status {response.status_code}")
                else:
                    raise Exception(f"Tipo de conteúdo inesperado: {content_type}")
            else:
                raise Exception(f"Erro ao baixar a mídia: Status {media_response.status_code}")
        else:
            raise Exception(f"Falha no login: Status {login_response.status_code}")
            
# Function to generate text using the ChatCompletion API
# Função para gerar texto usando a API ChatCompletion
def gerar_texto(prompt, static_prompts):
    url = f"{openai.api_base}/api/chat/completions"
    headers = {
        "Authorization": f"Bearer {openai.api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "etx",
        "language": "portuguese",
        "num_predict": 1,
        "top_k": 0,
        "top_p": 0.0,
        "min_p": 0.0,
        "tfs_z": 1.000,
        "typical_p": 0.8,
        "repeat_last_n": 1,
        "temperature": 0.0,
        "repeat_penalty": 1.000,
        "presence_penalty": 1.0,
        "frequency_penalty": 1.0,
        "mirostat": 0,
        "mirostat_tau": 0.0,
        "mirostat_eta": 0.0,
        "num_ctx": 8192,
        "num_batch": 1,
        "num_gpu": 1,
        "main_gpu": 1,
        "num_thread": 8,
        "stop": None,
        "messages": [{"role": "user", "content": f"{static_prompts}\n\n{prompt}"}]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response_data = response.json()
        if "choices" in response_data and len(response_data["choices"]) > 0:
            texto_gerado = response_data["choices"][0]["message"]["content"]
            return texto_gerado
        else:
            print("Resposta inesperada da API de texto:", response_data)
            return None
    except requests.RequestException as e:
        print(f"Erro ao gerar texto: {e}")
        return None
      
# Function to generate image using external API
# Função para gerar imagem usando a API externa
def generate_image(user_prompt, positive_prompt=None, negative_prompt=None, system_prompt=None):
    url = f"{openai.api_base}/images/api/v1/generations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"
    }

    prompt = user_prompt
    if system_prompt:
        prompt = f"{system_prompt}\n\n{prompt}"
    if positive_prompt:
        prompt = f"{positive_prompt}\n\n{prompt}"
    if negative_prompt:
        prompt = f"{prompt}\n\n{negative_prompt}"

    data = {
        "prompt": prompt,
        "size": "360x640",
        "n": 1,
        "negative_prompt": ""
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response_data = response.json()

        if response_data and len(response_data) > 0:
            image_url = f"https://chat.etx.tec.br{response_data[0]['url']}"
            return image_url
        else:
            print("URL da imagem não encontrada na resposta.")
            return None
    except requests.RequestException as e:
        print(f"Erro ao gerar imagem: {e}")
        return None  # Certifique-se de retornar None em caso de erro

# Function to generate audio
# Função para gerar áudio
def generate_audio(text):
    url = 'https://xxx.etx.tec.br/audio/api/v1/speech'
    headers = {
        'accept': 'application/json',
        "Authorization": f"Bearer {openai.api_key}"
    }
    data = {
        'input': text,
        'voice': 'shimmer',
        'response_format': 'wav',
        'speed': 1.0
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Levanta um erro se a resposta não for 2xx
        return response.content  # Retorna o conteúdo do áudio
    except Exception as e:
        print(f"Erro ao gerar áudio: {e}")
        return None
      
# Function to download files
# Função para baixar arquivos
def download_file(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        print(f"Erro ao baixar o arquivo: {e}")
        return None

# Function to send text message to customer
# Função para enviar mensagem de texto ao cliente
def send_message_to_customer(message):
    try:
        if customer:
            customer.sendTextMessage(message)
            customer.save()
        else:
            print("Cliente não está inicializado.")
    except Exception as e:
        print(f"Erro ao enviar a mensagem ao cliente: {str(e)}")

# Function to send document to client
# Função para enviar documento ao cliente
def send_document_to_customer(title, filename, content=None, url=None):
    try:
        if url:
            customer.sendDocumentMessage(title, filename, None, url=url, hide_user_name=False)
        elif content:
            customer.sendDocumentMessage(title, filename, content)
        else:
            print(f"Erro: Nenhum conteúdo ou URL fornecido para {title}.")
            return

        customer.save_document(filename)
    except Exception as e:
        print(f"Erro ao enviar o documento ao cliente: {str(e)}")
      
# Function to send audio and image for conversion to video
# Função para enviar áudio e imagem para conversão em vídeo
def send_audio_and_image_for_conversion(audio_content, image_url, audio_file_name, image_file_name):
    url = 'https://xxx.etx.tec.br/generate-video/'
    headers = {
        "Authorization": f"Bearer {media_key}"
    }

    try:
        files = {
            "audio": (audio_file_name, audio_content, "audio/x-wav"),
            "images": (image_file_name, requests.get(image_url).content, "image/png")
        }

        # Sending the request for conversion
        # Enviando a solicitação para conversão
        convert_response = requests.post(url, headers=headers, files=files)
        convert_response.raise_for_status()

        # Check the response type to make sure it is the converted video        
        # Verifique o tipo de resposta para garantir que é o vídeo convertido
        content_type = convert_response.headers.get('Content-Type')
        if content_type == 'video/mp4':
            return convert_response.content
        else:
            print(f"Tipo de conteúdo inesperado na resposta de conversão: {content_type}")
            return None
    except requests.RequestException as e:
        print(f"Erro ao converter áudio e imagem: {e}")
        return None
      
# Function to split text into paragraphs
# Função para dividir texto em parágrafos
def split_text_by_paragraphs(text):
    return text.split('\n\n')
  
# Function to check supported formats
# Função para verificar formatos suportados
def is_audio_or_video(mime_type):
    audio_video_formats = [
        'audio/mpeg', 'audio/ogg', 'audio/wav', 'audio/mp3', 'audio/mp4', 
        'audio/m4a', 'audio/opus', 'audio/3gp', 'video/mp4', 'video/m4v', 
        'video/avi', 'video/ogg', 'video/mpeg', 'video/x-msvideo'
    ]
    return any(fmt in mime_type for fmt in audio_video_formats)
  
# Main code for generating text, image and audio
# Código principal para geração de texto, imagem e áudio
try:
    if hasattr(customer.message, 'attachment') and customer.message.attachment:
        attachment = customer.message.attachment
        if is_audio_or_video(attachment.mime):
            # Generate the file URL
            # Gera a URL do arquivo
            base_url = "https://xxx.webzap.tec.br/media/chatapp/"
            file_url = base_url + str(attachment.file.path).split('/chatapp/')[-1]
            user_question = transcrever_audio(file_url)
            send_message_to_customer(f"Você disse: {user_question}")
        else:
            user_question = customer.message.content
    else:
        user_question = customer.message.content

    static_prompts = 1 + 2 + 3 + 4 + 5 + 6
    resposta_texto = gerar_texto(user_question, static_prompts)
    
    if resposta_texto:
        print(f"Resposta do modelo: {resposta_texto}")
        send_message_to_customer(f"BoT: {resposta_texto}\n\nhttps://etx.tec.br/#contato.")

        partes_texto = split_text_by_paragraphs(resposta_texto)
        for i, parte in enumerate(partes_texto):

            system_prompt = f'TEACHING"{partes_texto}".'
            positive_prompt = "BRAND LOGO WITH THE LETTERS: ETX"
            negative_prompt = "NO ANINALS OR HUMANS"
            # Image generation
            # Geração da imagem
            image_url = generate_image(parte)
            if image_url:
                print(f"Imagem gerada com sucesso: {image_url}")
                # Audio generation
                # Geração do áudio
                audio_content = generate_audio(parte)
                if audio_content:
                    file_name_audio = f'audio_gerado_{i}.wav'
                    file_name_image = f'imagem_gerada_{i}.png'
                  
                    # Upload audio and image for conversion to video
                    # Enviar áudio e imagem para conversão em vídeo
                    video_content = send_audio_and_image_for_conversion(audio_content, image_url, file_name_audio, file_name_image)
                    if video_content:
                        send_document_to_customer(f'Vídeo gerado por IA - Parte {i + 1}', f'video_gerado_{i}.mp4', content=video_content)
                    else:
                        send_message_to_customer(f"Desculpe, não foi possível converter o áudio e a imagem para vídeo na parte {i + 1}.")
                else:
                    send_message_to_customer(f"Desculpe, não foi possível gerar o áudio na parte {i + 1}.")
            else:
                send_message_to_customer(f"Erro ao gerar a imagem para a parte {i + 1}.")
    else:
        send_message_to_customer("Desculpe, houve um erro ao gerar o texto.")

except Exception as e:
    print(f"Erro ao processar a solicitação: {str(e)}")
    send_message_to_customer(f"Desculpe, houve um erro ao processar sua solicitação: {str(e)}")
