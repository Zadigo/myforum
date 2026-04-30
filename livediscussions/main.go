package main

import (
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

	log.Println("🚀 Live Discussions Server is running on :8080")
	http.ListenAndServe(":8080", router)
}
