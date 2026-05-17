package main

import (
	"context"
	"fmt"
	"os"
	"os/signal"

	"github.com/Zadigo/gomoderator/internal/server"
	"github.com/joho/godotenv"
)

func main() {
	godotenv.Load(".env")

	app := server.NewApp()

	// Listen to any app interruptions (control + c) and send it to the context
	ctx, cancel := signal.NotifyContext(context.Background(), os.Interrupt)
	defer cancel()

	err := app.Start(ctx)

	if err != nil {
		fmt.Printf("Could not start server %s", err)
	}
}
