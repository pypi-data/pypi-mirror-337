from setuptools import setup, find_packages

setup(
    name='NumSense',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,  # Включает файлы, указанные в MANIFEST.in
    package_data={
        'NumSense': ['data/NS_data.npz'],  # Укажите путь к вашему .npz файлу
    },
)
