package server

import (
	"github.com/Zadigo/gomoderator/internal/handlers"
	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
)

// Creates and loads the router for chi
func loadroutes() *chi.Mux {
	router := chi.NewRouter()

	router.Use(middleware.Logger)
	router.Route("/messages", loadMessageRoutes)

	return router
}

// Loads the routes for message
func loadMessageRoutes(router chi.Router) {
	message := handlers.Message{}
	router.Post("/", message.Moderate)
}
