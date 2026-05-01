package main

import (
	"context"
	"log"
	"net/http"
	"time"

	"github.com/Zadigo/livediscussions/internal/backend"
	"github.com/Zadigo/livediscussions/internal/handlers"
	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"github.com/go-co-op/gocron"
)

func main() {
	log.Println("🚀 Starting Live Discussions Server...")

	// Create Redis client and server registry
	redisClient := backend.CreateRedisClient("redis://localhost:6379")
	log.Println("✅ Connected to Redis")

	serverRegistry := backend.NewServerRegistry(redisClient)

	// Create the main general discussion space
	discussionSpace := backend.NewDiscussionSpace("General Discussion")
	err := serverRegistry.AddDiscussionSpace(discussionSpace)

	if err != nil {
		panic(err)
	}

	// Context with shutdown signal for broadcasters
	// This will allow us to gracefully shut down the broadcasters when the server is stopped
	// and prevent any potential memory leaks or dangling goroutines.
	shutdownContext, cancel := context.WithCancel(context.Background())
	defer cancel()

	// Start the global broadcaster for the general discussion space
	discussionSpace.StartBroadcaster2(shutdownContext, redisClient, serverRegistry)
	log.Print("⚡️ Started broadcaster for General Discussion")

	// Global scheduler
	scheduler := gocron.NewScheduler(time.UTC)
	go backend.StartCleanupRouting(scheduler)
	serverRegistry.GetRegistry().SetScheduler(scheduler)
	log.Print("⚡️ Started cleanup scheduler")

	router := chi.NewRouter()

	router.Use(middleware.RequestID)
	router.Use(middleware.RealIP)
	router.Use(middleware.Logger)
	router.Use(middleware.Recoverer)
	router.Use(middleware.Timeout(60 * time.Second))

	router.Get("/ws/general-discussion", func(w http.ResponseWriter, r *http.Request) {
		handlers.LiveDiscussionsHandler(w, r, serverRegistry)
	})

	log.Println("🚀 Live Discussions Server is running on :9000")
	http.ListenAndServe(":9000", router)
}
