

Входной файл – FP_SNPs.txt из архива программы GRAF версии 2.4 с официального сайта:
https://www.ncbi.nlm.nih.gov/projects/gap/cgi-bin/Software.cgi.

Референсный геном человека версии GRCh38.d1.vd1
(https://gdc.cancer.gov/about-data/data-harmonization-and-generation/gdc-reference-files). Был разбит на 25 файлов основных хромосом {chr1-22,M,Y,X}, хранятся на хост-машине в /mnt/data/ref/GRCh38.d1.vd1_mainChr/sepChrs/ и пробрасываются в папку /ref/GRCh38.d1.vd1_mainChr/sepChrs/ при запуске docker-контейнера.

# SNP Converter

## Описание скрипта

Скрипт `snp_converter.py` предназначен для конвертации файлов с SNP данными. Он принимает на вход файл с исходными данными, директорию с файлами FASTA для референсного генома, и выводит файл с конвертированными данными. Также скрипт ведет логирование процесса работы.

### Аргументы

- `-i, --input`: Путь к входному файлу с исходными данными SNP.
- `-o, --output`: Путь к выходному файлу для сохранения конвертированных данных.
- `-f, --fasta`: Директория с файлами FASTA для референсного генома.
- `-l, --log`: Путь к файлу логов.
- `-h, --help`: Показать описание аргументов скрипта и выйти.

### Пример использования

```sh
python snp_converter.py -i /app/data/FP_SNPs_10k_GB38_twoAllelsFormat.tsv -o /app/data/FP_SNPs_10k_output.txt -f /app/data/GRCh38.d1.vd1_mainChr/sepChrs -l /app/data/snp_converter.log

```
# Принцип работы
1. Инициализация логирования: Скрипт начинает с настройки логирования для отслеживания выполнения и возможных ошибок. 

2. Чтение входного файла: Считывает входной файл, содержащий данные SNP.

3. Обработка данных: Для каждого SNP из входного файла: 

   - Определяет хромосому и позицию SNP.
   
   - Использует соответствующий файл FASTA для поиска референсного нуклеотида.
   
   - Формирует выходной VCF-like формат строки.
   
4. Запись выходного файла: Все обработанные SNP записываются в выходной файл.

5. Логирование завершения: Логирование завершения работы скрипта или ошибок, если они возникли.

# Установка и запуск в Docker
Для удобства использования и установки всех зависимостей, скрипт упакован в Docker контейнер.

## Шаги для подготовки
Клонируйте репозиторий:
```sh
git clone https://github.com/Porolo-V/SNP_converter.git
cd SNP_converter

```
Переместите необходимые файлы проекта в клонированный репозиторий:
```sh

mv /yur_path/SNP_converter_docker/* .
```
Соберите Docker образ:
```sh
docker build -t snp_converter .
```
# Запуск Docker контейнера
Убедитесь, что файлы референсного генома расположены на хостовой машине в папке /mnt/data/ref/GRCh38.d1.vd1_mainChr/sepChrs/. Пример команды для запуска Docker контейнера с пробросом необходимых директорий:

```sh
docker run -it \
  -v /your_path/FP_SNPs_10k_GB38_twoAllelsFormat:/app/data \
  -v /mnt/data/ref/GRCh38.d1.vd1_mainChr/sepChrs:/app/data/GRCh38.d1.vd1_mainChr/sepChrs \
  snp_converter
```
## Команда для запуска скрипта в Docker контейнере
```sh
docker run --rm \
  -v /your_path/FP_SNPs_10k_GB38_twoAllelsFormat:/app/data \
  -v /mnt/data/ref/GRCh38.d1.vd1_mainChr/sepChrs:/app/data/GRCh38.d1.vd1_mainChr/sepChrs \
  snp_converter python snp_converter.py \
  -i /app/data/FP_SNPs_10k_GB38_twoAllelsFormat.tsv \
  -o /app/data/FP_SNPs_10k_output.txt \
  -f /app/data/GRCh38.d1.vd1_mainChr/sepChrs \
  -l /app/data/snp_converter.log
```
## Описание работы скрипта применительно к FP_SNPs.txt
Скрипт считывает входной файл 'FP_SNPs_10k_GB38_twoAllelsFormat.tsv', обрабатывает каждую запись SNP, используя файлы FASTA для референсного генома, и выводит результаты в файл 'FP_SNPs_10k_output.txt'. Логирование процесса происходит в файл 'snp_converter.log'.
```sh
docker run --rm \
  -v /your_path/FP_SNPs_10k_GB38_twoAllelsFormat:/app/data \
  -v /mnt/data/ref/GRCh38.d1.vd1_mainChr/sepChrs:/app/data/GRCh38.d1.vd1_mainChr/sepChrs \
  snp_converter python snp_converter.py \
  -i /app/data/FP_SNPs_10k_GB38_twoAllelsFormat.tsv \
  -o /app/data/FP_SNPs_10k_output.txt \
  -f /app/data/GRCh38.d1.vd1_mainChr/sepChrs \
  -l /app/data/snp_converter.log
