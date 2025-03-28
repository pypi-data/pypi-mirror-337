from setuptools import setup, find_packages

setup(
    name="poppo213",
    version="1.7",  # تأكد من تغيير الإصدار عند الحاجة
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    include_package_data=True,  # لتضمين الملفات المحددة في MANIFEST.in
    entry_points={
        "console_scripts": [
            "poppo213 = poppo213.poppo213:main",
        ]
    },
)
