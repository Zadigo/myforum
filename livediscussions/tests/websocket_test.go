package tests

import (
	"fmt"
	"testing"

	"github.com/Zadigo/livediscussions/internal/backend"
	"github.com/stretchr/testify/assert"
)

func TestLiveDiscussionsHandler(t *testing.T) {
	conn, server, serverRegistry := GetNewConnection()
	defer server.Close()
	defer conn.Close()

	message := backend.WebsocketMessage{}
	clientId := ""

	// Create a test discussion space and add it to the registry
	discussionSpace := backend.NewDiscussionSpace("Test General Discussion")
	err := serverRegistry.AddDiscussionSpace(discussionSpace)

	if err != nil {
		panic(err)
	}

	t.Run("Should open new connection", func(t *testing.T) {
		err := conn.ReadJSON(&message)
		assert.NoError(t, err)
		assert.Equal(t, "must_identify", message.Action)

		clientId = message.ClientId
		assert.NotEmpty(t, clientId)

		t.Run("Should identify correctly", func(t *testing.T) {
			err := conn.WriteJSON(backend.WebsocketMessage{
				Action:   "identify",
				ClientId: clientId,
				Username: "alice",
			})
			assert.NoError(t, err)

			err = conn.ReadJSON(&message)
			assert.NoError(t, err)
			assert.Equal(t, "identified", message.Action)
			assert.Contains(t, message.Message, "Identification successful as alice")
		})

		t.Run("Should get available discussions", func(t *testing.T) {
			err = conn.WriteJSON(backend.WebsocketMessage{
				Action:   "get_discussions",
				ClientId: clientId,
			})
			assert.NoError(t, err)

			err = conn.ReadJSON(&message)
			assert.NoError(t, err)

			assert.Equal(t, "available_discussions", message.Action)
			fmt.Print(message)
		})
	})
}
