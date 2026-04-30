package main

import (
	"net/http"

	"github.com/Zadigo/livediscussions/internal/backend"
	"github.com/Zadigo/livediscussions/internal/handlers"
	"github.com/go-chi/chi/v5"
)

func main() {
	redisClient := backend.CreateRedisClient("redis://localhost:6379")
	serverRegistry := backend.NewServerRegistry(redisClient)

	router := chi.NewRouter()
	router.Get("/ws/general-discussion", func(w http.ResponseWriter, r *http.Request) {
		handlers.LiveDiscussionsHandler(w, r, serverRegistry)
	})
}
