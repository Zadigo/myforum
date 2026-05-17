package server

import (
	"context"
	"fmt"
	"net/http"
	"time"

	"github.com/redis/go-redis/v9"
)

// Base structure for the application
type App struct {
	router      http.Handler
	redisClient *redis.Client
}

// Start runs the new server and its dependencies
func (a *App) Start(ctx context.Context) error {
	server := http.Server{
		Addr:    ":3000",
		Handler: a.router,
	}

	err := a.redisClient.Ping(ctx).Err()
	if err != nil {
		return fmt.Errorf("Unable to connect to Redis %w", err)
	}

	defer func() {
		err := a.redisClient.Close()
		if err != nil {
			fmt.Printf("Failed to close Redis %s", err)
		}
	}()

	ch := make(chan error, 1)

	// Start the server in new goroutine
	// on a new thread
	go func() {
		err = server.ListenAndServe()
		if err != nil {
			ch <- fmt.Errorf("Failed to start error %w", err)
		}
		// When the server is stopped, close the channel
		close(ch)
	}()

	select {
	case err := <-ch:
		return err
	case <-ctx.Done():
		timeoutCtx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
		defer cancel()
		return server.Shutdown(timeoutCtx)
	}
}

func NewApp() *App {
	app := &App{
		router: loadroutes(),
		redisClient: redis.NewClient(&redis.Options{
			Addr: "localhost:6379",
			DB:   0,
		}),
	}
	return app
}
