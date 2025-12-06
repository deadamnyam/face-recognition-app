# сюда пишет Полина
import cv2
import numpy as np
import os
import pickle
from datetime import datetime

class SimpleFaceRecognition:
    def __init__(self, data_dir='face_data'):
        self.data_dir = data_dir
        self.known_faces = []
        self.known_names = []
        self.load_saved_faces()
        
        # Инициализация детектора лиц OpenCV
        try:
            self.face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
        except:
            print("Ошибка загрузки классификатора лиц")
            self.face_cascade = None
        
        # Создаем директории для сохранения данных
        os.makedirs(data_dir, exist_ok=True)
        os.makedirs(os.path.join(data_dir, 'saved_faces'), exist_ok=True)
    
    def load_saved_faces(self):
        """Загружаем сохраненные лица"""
        data_file = os.path.join(self.data_dir, 'faces_data.pkl')
        
        if os.path.exists(data_file):
            try:
                with open(data_file, 'rb') as f:
                    data = pickle.load(f)
                    self.known_faces = data.get('faces', [])
                    self.known_names = data.get('names', [])
                print(f"Загружено {len(self.known_names)} сохраненных лиц")
            except:
                print("Ошибка загрузки данных лиц")
    
    def save_face_data(self):
        """Сохраняем данные о лицах"""
        data = {
            'faces': self.known_faces,
            'names': self.known_names
        }
        
        data_file = os.path.join(self.data_dir, 'faces_data.pkl')
        try:
            with open(data_file, 'wb') as f:
                pickle.dump(data, f)
        except:
            print("Ошибка сохранения данных лиц")
    
    def detect_faces(self, frame):
        """Обнаружение лиц с помощью Haar Cascade"""
        if self.face_cascade is None:
            return []
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        return faces
    
    def recognize_face(self, face_image):
        """Простая распознавание лица по сравнению с сохраненными"""
        if not self.known_faces:
            return "Неизвестно", -1
        
        try:
            # Конвертируем в grayscale и изменяем размер для сравнения
            gray_face = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
            gray_face = cv2.resize(gray_face, (100, 100))
            
            best_match_score = float('inf')
            best_match_index = -1
            
            for i, known_face in enumerate(self.known_faces):
                # Простое сравнение через MSE (Mean Squared Error)
                if known_face.shape == gray_face.shape:
                    mse = np.mean((known_face.astype("float") - gray_face.astype("float")) ** 2)
                    if mse < best_match_score:
                        best_match_score = mse
                        best_match_index = i
            
            # Порог для распознавания
            if best_match_score < 5000 and best_match_index != -1:
                return self.known_names[best_match_index], best_match_index
        except:
            pass
        
        return "Неизвестно", -1
    
    def save_new_face(self, frame, face_coords, name):
        """Сохраняем новое лицо"""
        if not name or name.strip() == "":
            print("Имя не может быть пустым")
            return False
        
        x, y, w, h = face_coords
        
        # Увеличиваем область лица
        y = max(0, y - 20)
        x = max(0, x - 20)
        h = min(frame.shape[0] - y, h + 40)
        w = min(frame.shape[1] - x, w + 40)
        
        face_image = frame[y:y+h, x:x+w]
        
        if face_image.size == 0:
            print("Не удалось вырезать лицо")
            return False
        
        # Сохраняем изображение лица
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        face_filename = os.path.join(self.data_dir, 'saved_faces', f"{name}_{timestamp}.jpg")
        try:
            cv2.imwrite(face_filename, face_image)
        except:
            print("Ошибка сохранения изображения")
            return False
        
        # Сохраняем для распознавания
        try:
            gray_face = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
            gray_face = cv2.resize(gray_face, (100, 100))
            
            self.known_faces.append(gray_face)
            self.known_names.append(name)
            self.save_face_data()
            
            print(f"✓ Лицо '{name}' успешно сохранено!")
            return True
        except:
            print("Ошибка обработки лица")
            return False
    
    def draw_face_info(self, frame, faces, names):
        """Рисуем квадраты и имена на кадре"""
        for (x, y, w, h), name in zip(faces, names):
            # Цвет квадрата
            color = (0, 255, 0) if name != "Неизвестно" else (0, 0, 255)
            
            # Рисуем квадрат
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            
            # Рисуем фон для текста
            cv2.rectangle(frame, (x, y-35), (x+w, y), color, -1)
            
            # Добавляем текст
            cv2.putText(frame, name, (x+6, y-6), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        return frame

def main():
    """Основная функция"""
    # Инициализация
    print("="*50)
    print("Инициализация системы распознавания лиц...")
    print("="*50)
    
    face_rec = SimpleFaceRecognition()
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Ошибка: не удалось открыть камеру")
        print("Убедитесь, что камера подключена и не используется другим приложением")
        input("Нажмите Enter для выхода...")
        return
    
    print("\n✓ Камера успешно подключена!")
    print("\n" + "="*50)
    print("ИНСТРУКЦИИ:")
    print("="*50)
    print("1. Для СОХРАНЕНИЯ НОВОГО лица:")
    print("   - Убедитесь, что лицо хорошо видно в кадре")
    print("   - Нажмите клавишу 's' на клавиатуре")
    print("   - Введите имя человека в консоли")
    print("   - Нажмите Enter")
    print("\n2. Для ВЫХОДА:")
    print("   - Нажмите клавишу 'q' или ESC")
    print("="*50 + "\n")
    
    print("Нажмите любую клавишу, чтобы начать...")
    cv2.waitKey(1000)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Ошибка: не удалось получить кадр с камеры")
            break
        
        # Обнаруживаем лица
        faces = face_rec.detect_faces(frame)
        
        # Распознаем каждое лицо
        face_names = []
        for (x, y, w, h) in faces:
            try:
                face_image = frame[y:y+h, x:x+w]
                name, _ = face_rec.recognize_face(face_image)
                face_names.append(name)
            except:
                face_names.append("Неизвестно")
        
        # Рисуем информацию
        frame = face_rec.draw_face_info(frame, faces, face_names)
        
        # Отображаем статистику
        info_text = f"Лиц в кадре: {len(faces)} | Известных: {len([n for n in face_names if n != 'Неизвестно'])}"
        cv2.putText(frame, info_text, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        # Инструкция на экране
        help_text = "s: сохранить новое лицо | q: выйти"
        cv2.putText(frame, help_text, (10, frame.shape[0] - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        cv2.imshow('Распознавание лиц', frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q') or key == 27:  # q или ESC
            print("\nВыход из программы...")
            break
        elif key == ord('s'):
            # Сохраняем первое неизвестное лицо
            unknown_found = False
            for i, (face_coords, name) in enumerate(zip(faces, face_names)):
                if name == "Неизвестно":
                    print("\n" + "-"*50)
                    print("Обнаружено неизвестное лицо!")
                    print("-"*50)
                    user_name = input("Введите имя нового человека: ").strip()
                    
                    if user_name:
                        success = face_rec.save_new_face(frame.copy(), face_coords, user_name)
                        if success:
                            print(f"✓ Лицо '{user_name}' добавлено в базу данных!")
                        else:
                            print("✗ Не удалось сохранить лицо")
                    else:
                        print("✗ Сохранение отменено: имя не введено")
                    
                    unknown_found = True
                    break
            
            if not unknown_found:
                print("\nℹ Неизвестных лиц не обнаружено")
                print("Убедитесь, что лицо видно в кадре и система его обнаружила")
    
    # Очистка
    cap.release()
    cv2.destroyAllWindows()
    print("\nПрограмма завершена. Данные сохранены в папке 'face_data'")

if __name__ == "__main__":
    main()
