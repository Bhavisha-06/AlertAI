from setuptools import setup, find_packages

setup(
    name="alertai",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "ultralytics>=8.0.0",
        "gtts>=2.3.1",
        "opencv-python>=4.7.0",
        "numpy>=1.22.0",
        "playsound>=1.3.0",
    ],
    entry_points={
        "console_scripts": [
            "alertai=alert_ai:main",
        ],
    },
    author="AlertAI Team",
    author_email="bhavisha2705@gmail.com",
    description="Drowsiness and distraction detection system with audio alerts",
    keywords="yolo, drowsiness, detection, safety, alert",
    url="https://github.com/Bhavisha-06/AlertAI",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries",
    ],
)
