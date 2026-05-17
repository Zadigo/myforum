package backend

import (
	"context"
	"os"

	"github.com/redis/go-redis/v9"
)

func CreateRedisClient() *redis.Client {
	url := os.Getenv("REDIS_URL")
	if url == "" {
		panic("REDIS_URL environment variable is not set")
	}

	options, err := redis.ParseURL(url)

	if err != nil {
		panic(err)
	}

	client := redis.NewClient(options)
	_, err = client.Ping(context.Background()).Result()

	if err != nil {
		panic(err)
	}

	return client
}
