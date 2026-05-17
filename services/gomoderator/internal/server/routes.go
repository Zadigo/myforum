package server

import (
	"github.com/Zadigo/gomoderator/internal/handlers"
	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
)

// Creates and loads the router for chi
func (a *App) loadroutes() {
	router := chi.NewRouter()

	router.Use(middleware.Logger)
	router.Route("/messages", a.loadMessageRoutes)

	a.router = router
}

// Loads the routes for message
func (a *App) loadMessageRoutes(router chi.Router) {
	message := handlers.MessageApi{}
	router.Post("/", message.Moderate)
}
