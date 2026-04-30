package backend

import (
	"sync"

	"github.com/redis/go-redis/v9"
)

type ServerRegistry struct {
	Clients     map[string]*WebsocketClient
	Discussions map[string][]*WebsocketClient
	RedisClient *redis.Client
	broadcast   chan WebsocketMessage
	mu          sync.Mutex
}

type ServerRegistryInterface interface {
	AddClient(client WebsocketClientInterface) error
	RemoveClient(client WebsocketClientInterface) error
	BroadcastMessage(message WebsocketMessage)
}

func (r *ServerRegistry) AddClient(client WebsocketClientInterface) error {
	r.mu.Lock()
	defer r.mu.Unlock()

	r.Clients[client.(*WebsocketClient).ID] = client.(*WebsocketClient)
	return nil
}

func (r *ServerRegistry) RemoveClient(client WebsocketClientInterface) error {
	r.mu.Lock()
	defer r.mu.Unlock()

	delete(r.Clients, client.(*WebsocketClient).ID)
	return nil
}

func (r *ServerRegistry) BroadcastMessage(message WebsocketMessage) {
	r.broadcast <- message
}

func NewServerRegistry(redisClient *redis.Client) ServerRegistryInterface {
	return &ServerRegistry{
		Clients:     make(map[string]*WebsocketClient),
		Discussions: make(map[string][]*WebsocketClient),
		broadcast:   make(chan WebsocketMessage, 100),
		RedisClient: redisClient,
	}
}
