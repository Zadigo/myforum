package main

import (
	"context"
	"fmt"

	"github.com/Zadigo/gomoderator/internal/server"
	"github.com/joho/godotenv"
)

func main() {
	godotenv.Load(".env")

	app := server.NewApp()
	
	ctx := context.Background()
	err := app.Start(ctx)
	
	if err != nil {
		fmt.Printf("Could not start server %s", err)
	}
}
