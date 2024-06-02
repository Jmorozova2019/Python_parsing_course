import time
import aiofiles
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import os
import itertools

domain = '...'
img_url_list = []

def get_folder_size(filepath, size=0):
    for root, dirs, files in os.walk(filepath):
        for f in files:
            size += os.path.getsize(os.path.join(root, f))
    return size

async def write_file(session, img_url, semaphore):
    img_name = img_url.split('/')[-1]

    async with semaphore:
        #открыть на запись файл
        async with aiofiles.open(f'images/{img_name}', mode='wb') as f:
            async with session.get(img_url) as response:
                # собрать файл чанками
                async for x in response.content.iter_chunked(2048):  
                    await f.write(x)  # записать каждый чанк

async def main():
    conn = aiohttp.TCPConnector(limit=5)
    async with aiohttp.ClientSession(connector=conn) as session:
        #с главной странцы собрать ссылки на страницы с файлами картинок
        async with session.get('https://parsinger.ru/asyncio/aiofile/3/index.html') as response:    
            soup = BeautifulSoup(await response.text(), 'lxml')
            #получить ссылки на страницу со ссылками следующего уровня
            imgs_urls_1 = [domain + x["href"] for x in soup.findAll(class_= "lnk_img")]
            tasks = []

            for img_url_1 in imgs_urls_1:
                subdomain = img_url_1.split('/')[-2]
                async with session.get(img_url_1) as response:
                    soup = BeautifulSoup(await response.text(), 'lxml')
                    
                    # получить ссылки на след. уровень
                    imgs_urls_2 = [domain + subdomain + '/' + x["href"] for x in soup.findAll(class_= "lnk_img")]  

                    for img_url_2 in imgs_urls_2:
                        async with session.get(img_url_2) as response:
                            soup = BeautifulSoup(await response.text(), 'lxml')
                            
                            # получить ссылки на картинки
                            imgs_urls_3 = soup.find_all('img')  

                            for img in imgs_urls_3:
                                img_url = img['src']
                                if img_url not in img_url_list:
                                    img_url_list.append(img_url)

            for img_url in img_url_list:
                semaphore = asyncio.Semaphore(50)
                
                #создать таски
                task = asyncio.create_task(write_file(session, img_url, semaphore)) 
                tasks.append(task)
            await asyncio.gather(*tasks)

start = time.perf_counter()
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())# запуск

print(get_folder_size(f'images', size=0))
print(time.perf_counter() - start)
