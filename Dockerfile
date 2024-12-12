FROM postgres
ENV POSTGRES_USER sepp
ENV POSTGRES_PASSWORD P3p3823rCvEq6HpELsxCdn4RwBlaE5
ENV POSTGRES_DB marking
ADD marking.sql /docker-entrypoint-initdb.d/