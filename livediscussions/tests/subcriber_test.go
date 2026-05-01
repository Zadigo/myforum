package tests

import (
	"context"
	"testing"
	"time"

	"github.com/Zadigo/livediscussions/internal/backend"
	"github.com/stretchr/testify/assert"
)

func TestRedisSubscriber(t *testing.T) {
	conn1, server1, registry, redisClient := GetNewConnection()
	defer conn1.Close()
	defer server1.Close()

	conn2, server2, _, _ := GetNewConnection()
	defer conn2.Close()
	defer server2.Close()

	// Use the same registry for both connections to ensure
	// they are subscribed to the same channels
	registry.AddClient(backend.NewWebsocketClient("pauline", conn2))

	space := backend.DiscussionSpace{
		ID:   "test-space",
		Name: "General Discussions",
	}

	context := context.WithoutCancel(context.Background())

	serverRegistry := backend.NewServerRegistry(redisClient)
	space.StartBroadcaster2(context, redisClient, serverRegistry)

	t.Run("Should be able to broadcast to clients", func(t *testing.T) {
		message1 := backend.WebsocketMessage{}

		err := conn1.ReadJSON(&message1)
		assert.NoError(t, err)

		message2 := backend.WebsocketMessage{}
		err = conn2.ReadJSON(&message2)
		assert.NoError(t, err)

		time.Sleep(5 * time.Second)

		err = space.BroadcastMessage2(redisClient, backend.RedisWebsocketMessage{
			From: "test",
			Payload: backend.WebsocketMessage{
				Action: "test_message",
			},
		})

		assert.NoError(t, err)

		err = conn1.ReadJSON(&message1)
		assert.NoError(t, err)

		err = conn2.ReadJSON(&message2)
		assert.NoError(t, err)
	})

	<-context.Done()
}
