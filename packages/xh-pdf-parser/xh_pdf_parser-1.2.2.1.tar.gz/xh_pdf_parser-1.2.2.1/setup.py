from pathlib import Path
from setuptools import setup, find_packages
from magic_pdf.libs.version import __version__


def parse_requirements(filename):
    with open(filename) as f:
        lines = f.read().splitlines()

    requires = []

    for line in lines:
        if "http" in line:
            pkg_name_without_url = line.split('@')[0].strip()
            requires.append(pkg_name_without_url)
        else:
            requires.append(line)

    return requires


if __name__ == '__main__':
    with Path(Path(__file__).parent,
              'README.md').open(encoding='utf-8') as file:
        long_description = file.read()
    setup(
        name="xh_pdf_parser",  # 项目名
        version=__version__+".1",  # 自动从tag中获取版本号
        packages=find_packages() + ["magic_pdf.resources"],  # 包含所有的包
        package_data={
            "magic_pdf.resources": ["**"],  # 包含magic_pdf.resources目录下的所有文件
        },
        install_requires=[
        "boto3>=1.28.43",
        "Brotli>=1.1.0",
        "click>=8.1.7",
        "fast-langdetect>=0.2.3,<0.3.0",
        "loguru>=0.6.0",
        "numpy>=1.21.6,<2.0.0",
        "pydantic>=2.7.2",
        "PyMuPDF>=1.24.9,<=1.24.14",
        "scikit-learn>=1.0.2",
        "transformers",
        "pdfminer.six==20231228",
        "omegaconf>=2.3.0",
        "matplotlib>=3.8.4",
        "iopath>=0.1.9",
        "timm==0.9.16",
        "opencv-python>=4.6.0",
        "fairscale>=0.4.13",
        "ftfy>=6.2.0",
        "albumentations>=1.4.4",
        "wand>=0.6.13",
        "webdataset>=0.2.86",
        "rapidfuzz>=3.8.1",
        "termcolor>=2.4.0",
        "pandas>=2.2.2",
        "evaluate>=0.4.1",
        "rich>=13.7.1",
        "jupyterlab>=4.1.6",
        "tabulate>=0.9.0",
        "nltk>=3.8.1",
        "streamlit>=1.33.0",
        "pypdfium2>=4.29.0",
        "pdf2image>=1.17.0",
        "streamlit_drawable_canvas>=0.9.3",
        "torch>=2.2.2,<=2.3.1",
        "torchvision>=0.17.2,<=0.18.1",
        "ultralytics>=8.3.48",
        "paddleocr==2.7.3",
        "struct-eqtable==0.3.2",
        "einops",
        "accelerate",
        "doclayout_yolo==0.0.2b1",
        "rapidocr-paddle>=1.4.5,<2.0.0",
        "rapidocr_onnxruntime>=1.4.4,<2.0.0",
        "rapid_table>=1.0.3,<2.0.0",
        "PyYAML",
        "openai",
        "detectron2",
        "paddlepaddle==3.0.0",
        "paddlepaddle-gpu==2.6.0",
    ],  # 项目依赖的第三方库
        extras_require={},
        description="A practical tool for converting PDF to Markdown",  # 简短描述
        long_description=long_description,  # 详细描述
        long_description_content_type="text/markdown",  # 如果README是Markdown格式
        url="https://github.com/opendatalab/MinerU",
        python_requires=">=3.9",  # 项目依赖的 Python 版本
        find_links=[
        "https://www.paddlepaddle.org.cn/packages/stable/cu118/",
    ],
        entry_points={
            "console_scripts": [
                "magic-pdf = magic_pdf.tools.cli:cli",
                "magic-pdf-dev = magic_pdf.tools.cli_dev:cli" 
            ],
        },  # 项目提供的可执行命令
        include_package_data=True,  # 是否包含非代码文件，如数据文件、配置文件等
        zip_safe=False,  # 是否使用 zip 文件格式打包，一般设为 False
    )
