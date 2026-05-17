package tests

import (
	"testing"

	"github.com/Zadigo/livediscussions/internal/backend"
	"github.com/joho/godotenv"
)

func TestServerRegistry(t *testing.T) {
	godotenv.Load("../.env")

	client := backend.CreateRedisClient()
	r := backend.NewServerRegistry(client)

	t.Run("Add and Get Discussion Space", func(t *testing.T) {
		go r.CreateRedisBroadcastChannel(t.Context())
		r.BroadcastMessage(backend.WebsocketMessage{
			Action:  "message",
			Message: "Simple message",
		})
	})
}
