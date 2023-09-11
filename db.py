from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text

app = Flask(__name__)

# Replace with your AWS RDS endpoint, username, and password
aws_rds_endpoint = 'fintech-dev.cbnt8xhvtzh0.ap-southeast-1.rds.amazonaws.com'
username = 'admin'
password = 'CknvMh74qeFv'

# Construct the AWS RDS URI without specifying the database name
aws_rds_uri = f'mysql+pymysql://{username}:{password}@{aws_rds_endpoint}:3306/'
app.config['SQLALCHEMY_DATABASE_URI'] = aws_rds_uri

db = SQLAlchemy(app)

def get_database_names():
    try:
        engine = create_engine(aws_rds_uri)
        connection = engine.connect()
        result = connection.execute(text('SHOW DATABASES'))
        databases = [row[0] for row in result]
        connection.close()
        return databases
    except Exception as e:
        return f'Error fetching database names: {str(e)}'

@app.route('/')
def test_db_connection():
    try:
        db.session.execute(text('SELECT 1'))
        return 'Database connection successful!'
    except Exception as e:
        return f'Database connection error: {str(e)}'

@app.route('/databases')
def list_databases():
    database_names = get_database_names()
    return '\n'.join(database_names)

if __name__ == '__main__':
    app.run()
