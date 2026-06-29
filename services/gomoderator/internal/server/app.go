package server

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/redis/go-redis/v9"
)

// Base app struct that holds the
// router and any dependencies such as the
// redis client and config
type App struct {
	router      http.Handler
	redisClient *redis.Client
	config      *Config
}

// Start runs the new server and its dependencies
func (a *App) Start(ctx context.Context) error {
	server := http.Server{
		Addr:    "localhost:5379",
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

	// Create a channel to listen for any
	// errors from the server
	ch := make(chan error, 1)

	// Start the server in new goroutine
	// on a new thread
	go func() {
		log.Print("🟢 Server ready to receive requests...")
		err = server.ListenAndServe()
		if err != nil {
			ch <- fmt.Errorf("Failed to start error %w", err)
		}
		close(ch)
	}()

	select {
	case err := <-ch:
		return err
	case <-ctx.Done():
		// Create a new context with a timeout to allow the server to shutdown gracefully
		// If the server does not shutdown within the timeout, it will be forcefully closed
		// This is to ensure that the server does not hang indefinitely if it is unable to shutdown
		timeoutCtx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
		defer cancel()
		return server.Shutdown(timeoutCtx)
	}
}

func NewApp(config *Config) *App {
	app := &App{
		config: config,
		redisClient: redis.NewClient(&redis.Options{
			Addr: "localhost:6379",
			DB:   0,
		}),
	}
	app.loadroutes()
	return app
}
