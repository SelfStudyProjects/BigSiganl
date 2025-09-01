"""
Django 기본 설정 파일

FUNCTION configure_database():
    IF environment == 'production':
        USE AWS RDS PostgreSQL connection
    ELSE:
        USE local PostgreSQL connection
    
    CONFIGURE connection pooling
    SET timezone to 'Asia/Seoul'

FUNCTION configure_cors():
    ALLOW Firebase Hosting domain
    ALLOW localhost for development
    
FUNCTION configure_rest_framework():
    SET pagination to 50 items
    CONFIGURE authentication (optional)
    SET permission classes

"""
