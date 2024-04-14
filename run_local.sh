export CORS_ORIGINS="http://localhost,http://localhost:8000"
export MONGO_HOST=mongodb://mongo
export MONGO_PORT=27017
export MONGO_USERNAME=root
export mongo_password=example
export DB_NAME=task_app
export HASH_ALGORITHM=HS256
export HASH_KEY=put_your_HS256_random_hash_key

cd local
docker-compose up
