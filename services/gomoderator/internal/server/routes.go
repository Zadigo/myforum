package server

import (
	"github.com/Zadigo/gomoderator/internal/handlers"
	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
)

func loadroutes() *chi.Mux {
	router := chi.NewRouter()

	router.Use(middleware.Logger)
	router.Route("/messages", loadMessageRoutes)

	return router
}

func loadMessageRoutes(router chi.Router) {
	message := handlers.Message{}
	router.Post("/", message.Moderate)
}
