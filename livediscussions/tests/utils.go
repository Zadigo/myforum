package tests

import (
	"net/http"
	"net/http/httptest"

	"github.com/Zadigo/livediscussions/internal/backend"
	"github.com/Zadigo/livediscussions/internal/handlers"
	"github.com/gorilla/websocket"
	"github.com/redis/go-redis/v9"
)

func GetNewConnection() (*websocket.Conn, *httptest.Server, backend.ServerRegistryInterface, *redis.Client) {
	redisClient := backend.CreateRedisClient("redis://@localhost:6379/0")
	serverRegistry := backend.NewServerRegistry(redisClient)

	handler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		r.Header.Set("Origin", "http://localhost:3000")
		handlers.LiveDiscussionsHandler(w, r, serverRegistry)
	})

	server := httptest.NewServer(handler)

	wsUrl := "ws" + server.URL[len("http"):] + "/ws/general-discussion"
	conn, _, err := websocket.DefaultDialer.Dial(wsUrl, nil)
	if err != nil {
		panic(err)
	}
	serverRegistry.AddClient(backend.NewWebsocketClient("alice", conn))
	return conn, server, serverRegistry, redisClient
}
