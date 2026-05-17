package server

import (
	"context"
	"fmt"
	"net/http"
)

type App struct {
	router http.Handler
}

func (a *App) Start(ctxt context.Context) error {
	server := http.Server{
		Addr:    ":3000",
		Handler: a.router,
	}
	err := server.ListenAndServe()
	if err != nil {
		return fmt.Errorf("Failed to start error %W", err)
	}
	return nil
}

func NewApp() *App {
	app := &App{
		router: loadroutes(),
	}
	return app
}
