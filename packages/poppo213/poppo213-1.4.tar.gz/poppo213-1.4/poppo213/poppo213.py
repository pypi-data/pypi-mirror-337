import subprocess
import threading
import os

# تحديد مسار ملف الروابط بجانب السكربت
script_dir = os.path.dirname(os.path.abspath(__file__))  # مسار ملف السكربت
file_name = os.path.join(script_dir, "links.txt")  # ملف links.txt بجانب السكربت

# قراءة الروابط من الملف
def read_links(file_name):
    with open(file_name, "r") as file:
        return [line.strip() for line in file if line.strip()]

# تنفيذ أمر ab لرابط معين
def execute_ab(link):
    command = [
        "ab",
        "-n", "1000",
        "-c", "50",
        "-k",
        "-H", "Content-Type: application/json; charset=utf-8",
        "-H", "User-Agent: Dalvik/2.1.0 (Linux; U; Android 10; Redmi 8A MIUI/V12.5.2.0.QCPMIXM)",
        "-H", "Accept-Encoding: gzip, deflate, br",
        "-H", "Host: api.liaoke520.com",
        link
    ]
    try:
        print(f"Starting ab on: {link}")
        result = subprocess.run(command, capture_output=True, text=True)
        print(f"Finished ab on: {link}")
        print(result.stdout)
    except Exception as e:
        print(f"Error occurred while running ab on {link}: {e}")

# تشغيل الأوامر لجميع الروابط بالتوازي
def execute_all_links(links):
    threads = []
    for link in links:
        thread = threading.Thread(target=execute_ab, args=(link,))
        threads.append(thread)
        thread.start()

    # انتظار انتهاء جميع المهام
    for thread in threads:
        thread.join()

# الدالة الرئيسية
def main():
    links = read_links(file_name)
    if links:
        execute_all_links(links)
    else:
        print(f"No links found in the file: {file_name}")

# بدء البرنامج
if __name__ == "__main__":
    main()
