import cv2
import numpy as np

def extract_profile_photo_with_transparency(input_filename, output_filename, output_size=(100, 100)):
    # Carregar a imagem e converter para escala de cinza
    image = cv2.imread(input_filename)
    if image is None:
        print("Erro ao carregar a imagem. Verifique o caminho do arquivo.")
        return None
    
    # Redimensionar a imagem se for muito grande (opcional, pode ser ajustado ou removido)
    max_dimension = 1000
    height, width = image.shape[:2]
    if max(height, width) > max_dimension:
        scaling_factor = max_dimension / float(max(height, width))
        image = cv2.resize(image, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Definir a região de interesse (ROI) na área superior esquerda onde o perfil geralmente está
    roi = gray[0:int(height * 0.3), 0:int(width * 0.3)]

    # Detectar círculos na ROI para localizar a foto de perfil
    circles = cv2.HoughCircles(
        roi, 
        cv2.HOUGH_GRADIENT, 
        dp=1.2, 
        minDist=20, 
        param1=50, 
        param2=30, 
        minRadius=15, 
        maxRadius=60
    )

    # Verificar se algum círculo foi detectado
    if circles is not None and len(circles[0]) > 0:
        # Extrair as coordenadas do primeiro círculo detectado e ajustar para a área completa da imagem
        x, y, r = map(int, circles[0][0])
        
        # Ajuste das coordenadas para a posição relativa na imagem original
        x_full, y_full = x, y  # Como a ROI é a parte superior esquerda, usamos diretamente x e y

        # Criar uma imagem transparente (4 canais) do mesmo tamanho da região recortada
        user_photo = image[y_full - r:y_full + r, x_full - r:x_full + r]
        
        # Redimensionar a foto de perfil para o tamanho desejado (100x100) com interpolação bicúbica
        resized_photo = cv2.resize(user_photo, output_size, interpolation=cv2.INTER_CUBIC)
        
        # Criar uma nova imagem com transparência
        h, w = resized_photo.shape[:2]
        transparent_photo = np.zeros((h, w, 4), dtype=np.uint8)

        # Copiar o conteúdo RGB da foto redimensionada
        transparent_photo[:, :, :3] = resized_photo

        # Criar uma máscara circular
        mask = np.zeros((h, w), dtype=np.uint8)
        cv2.circle(mask, (w // 2, h // 2), min(w, h) // 2, 255, -1)

        # Aplicar a máscara ao canal alfa para deixar o fundo transparente
        transparent_photo[:, :, 3] = mask

        # Salvar o resultado com transparência
        cv2.imwrite(output_filename, transparent_photo)
        return output_filename
    else:
        print("Nenhuma foto de perfil detectada.")
        return None

# Caminho dos arquivos
input_filename = 'teste.png'  # Nome da imagem de entrada
output_filename = 'profile_photo_transparent_100x100.png'  # Nome da imagem de saída

# Executar a função de extração
result = extract_profile_photo_with_transparency(input_filename, output_filename)

if result:
    print(f"Foto de perfil com transparência salva em: {result}")
else:
    print("A extração falhou.")
