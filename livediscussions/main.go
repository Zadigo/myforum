package main

import (
	"net/http"
	"time"

	"github.com/Zadigo/livediscussions/internal/backend"
	"github.com/Zadigo/livediscussions/internal/handlers"
	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
)

func preStartup(r *backend.ServerRegistry) {}

func main() {
	// Create Redis client and server registry
	redisClient := backend.CreateRedisClient("redis://localhost:6379")
	serverRegistry := backend.NewServerRegistry(redisClient)

	// Create the main general discussion space
	discussionSpace := backend.NewDiscussionSpace()
	err := serverRegistry.AddDiscussionSpace(discussionSpace)

	if err != nil {
		panic(err)
	}

	router := chi.NewRouter()

	router.Use(middleware.RequestID)
	router.Use(middleware.RealIP)
	router.Use(middleware.Logger)
	router.Use(middleware.Recoverer)
	router.Use(middleware.Timeout(60 * time.Second))

	router.Get("/ws/general-discussion", func(w http.ResponseWriter, r *http.Request) {
		handlers.LiveDiscussionsHandler(w, r, serverRegistry)
	})

	http.ListenAndServe(":8080", router)
}
