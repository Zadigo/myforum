package server

import (
	"context"
	"fmt"
	"net/http"

	"github.com/redis/go-redis/v9"
)

type App struct {
	router      http.Handler
	redisClient *redis.Client
}

func (a *App) Start(ctx context.Context) error {
	server := http.Server{
		Addr:    ":3000",
		Handler: a.router,
	}

	err := a.redisClient.Ping(ctx).Err()
	if err != nil {
		return fmt.Errorf("Unable to connect to Redis %w", err)
	}

	err = server.ListenAndServe()
	if err != nil {
		return fmt.Errorf("Failed to start error %w", err)
	}
	return nil
}

func NewApp() *App {
	redisClient := redis.NewClient(&redis.Options{
		Addr: "localhost:6379",
		DB:   0,
	})

	app := &App{
		router:      loadroutes(),
		redisClient: redisClient,
	}
	return app
}
