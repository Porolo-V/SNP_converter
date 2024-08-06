FROM python:3.8-slim 

WORKDIR /app

COPY snp_converter.py /app/

RUN pip install --no-cache-dir pysam

CMD ["python", "snp_converter.py", "-i", "/app/data/FP_SNPs_10k_GB38_twoAllelsFormat.tsv", "-o", "/app/data/FP_SNPs_10k_output.txt", "-f", "/app/data/GRCh38.d1.vd1_mainChr/sepChrs", "-l", "/app/data/snp_converter.log"]


