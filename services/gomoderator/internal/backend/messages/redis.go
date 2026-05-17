package messages

import "github.com/redis/go-redis/v9"

type MessagesRedis struct {
	redisClient *redis.Client
}
