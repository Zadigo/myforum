package chats

import "github.com/redis/go-redis/v9"

type RedisChat struct {
	redisClient *redis.Client
}

func (r *RedisChat) SaveChat() {}

func (r *RedisChat) GetChat() {}

func (r *RedisChat) StartChannel() {}

func NewRedisChat(redisClient *redis.Client) *RedisChat {
	return &RedisChat{
		redisClient: redisClient,
	}
}
