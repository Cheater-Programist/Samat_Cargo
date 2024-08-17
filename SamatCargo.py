from aiogram import Bot, Dispatcher, types, executor
import logging, sqlite3

bot = Bot(token='7431398748:AAH8EeYiftjRXlP5POIZAzYRadijPiOyNzg')
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
connect = sqlite3.connect('users.db')
cursor = connect.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS user(
    id VARCHAR(255),
    username VARCHAR(255),
    first_name VARCHAR(255),
    personal_number INTEGER DEFAULT 0
);
""")
connect.commit()

start_buttons = [
    types.KeyboardButton('Жеке код алуу'),
    types.KeyboardButton('Биз жөнүндө маалымат'),
    types.KeyboardButton('Адрес📍'),
    types.KeyboardButton('Кандай кылып жеке кодту регистрация кылуу керек?')
]
start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_buttons)

@dp.message_handler(commands='start')
async def start(message:types.Message):
        user_id = message.from_user.id
    
        cursor.execute("SELECT personal_number FROM user WHERE id = ?", (user_id,))
        result = cursor.fetchone()

        if result is None:
            # Получаем максимальный текущий personal_number или 1159, если таблица пустая
            cursor.execute("SELECT MAX(personal_number) FROM user")
            max_personal_number = cursor.fetchone()[0]
            if max_personal_number is None:
                max_personal_number = 1199
            
            # Генерируем новый personal_number
            new_personal_number = max_personal_number + 1
            
            cursor.execute(
                'INSERT INTO user (id, username, first_name, personal_number) VALUES (?, ?, ?, ?)', 
                (user_id, message.from_user.username, message.from_user.first_name, new_personal_number)
            )
            connect.commit()
            await message.answer(f"Саламатсызбы {message.from_user.first_name}\nБиздин samatcargoго кош келипсиз🤩", reply_markup=start_keyboard) 
        
        else:
            await message.answer(f"Саламатсызбы {message.from_user.first_name}\nБиздин samatcargoго кош келипсиз🤩", reply_markup=start_keyboard) 

@dp.message_handler(text='Жеке код алуу')
async def personal_number(message:types.Message):
        cursor.execute(f"SELECT personal_number FROM user WHERE id = {message.from_user.id};")   
        connect.commit()
        result = cursor.fetchall()
                
        await message.answer(f"收货人：坦二四({result[0][0]})\n电话：17324524246\n\n佛山市南海区里水镇得村横五路5号\n（院内103俄仓）唛\n头:QYUXO({result[0][0]})+996")

@dp.message_handler(text='Биз жөнүндө маалымат')
async def adress(message:types.Message):
    await message.answer('КАРГО | КИТАЙ - ОШ | КАРА -СУУ |\nТез убакта: 12-18 күндө\n💵 1кг-3.2$\n🚚 Кыргызстандын бардык аймактарына жеткирип берүү бар\nЭң негизгиси бизде арзан жана сапаттуу.🤝🫂')

@dp.message_handler(text='Адрес📍')
async def adress(message:types.Message):
    await message.answer('11д/1 улица Алишера Навои, Ош')
    await message.answer_location(40.53754426029724, 72.80227876729016)
    with open('img/photo_2024-08-16_11-12-35.jpg', 'rb') as image1:
        await message.answer_photo(image1)
    with open('img/photo_2024-08-16_11-12-36.jpg', 'rb') as image2:
        await message.answer_photo(image2)

@dp.message_handler(text='Кандай кылып жеке кодту регистрация кылуу керек?')
async def info(message:types.Message):
    await message.answer("Кичине куто турунуз 😇…")
    # input1_video = 'img/1.MOV'
    # input2_video = 'img/2.MOV'
    # input3_video = 'img/3.MOV'
    output_video_1 = 'img/1_compressed.MOV'
    output_video_2 = 'img/2_compressed.MOV'
    output_video_3 = 'img/3_compressed.MOV'

    # subprocess.run(['ffmpeg', '-i', input1_video, '-vcodec', 'libx265', '-crf', '28', output_video_1])
    # subprocess.run(['ffmpeg', '-i', input2_video, '-vcodec', 'libx265', '-crf', '28', output_video_2])
    # subprocess.run(['ffmpeg', '-i', input3_video, '-vf', 'scale=1280:-2', '-vcodec', 'libx265', '-crf', '40', output_video_3])

    # Отправляем сжатое видео
    with open(output_video_1, 'rb') as video:
        await message.answer_video(video, width=720, height=1280)
    with open(output_video_2, 'rb') as video:
        await message.answer_video(video, width=720, height=1280)
    with open(output_video_3, 'rb') as video:
        await message.answer_video(video, width=720, height=1280)
    
executor.start_polling(dp)