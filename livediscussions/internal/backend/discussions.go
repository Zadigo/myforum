package backend

import (
	"sync"

	"github.com/google/uuid"
)

type DiscussionSpace struct {
	ID      string                     `json:"id"`
	Clients []WebsocketClientInterface `json:"clients"`
	mu      sync.Mutex                 `json:"-"`
}

type DiscussionSpaceInterface interface {
	AddClient(client WebsocketClientInterface) error
	RemoveClient(client WebsocketClientInterface) error
	BroadcastMessage(message WebsocketMessage)
}

func (d *DiscussionSpace) AddClient(client WebsocketClientInterface) error {
	d.mu.Lock()
	defer d.mu.Unlock()

	d.Clients = append(d.Clients, client)
	return nil
}

func (d *DiscussionSpace) RemoveClient(client WebsocketClientInterface) error {
	d.mu.Lock()
	defer d.mu.Unlock()

	for i, c := range d.Clients {
		if c.GetClient().ID == client.GetClient().ID {
			d.Clients = append(d.Clients[:i], d.Clients[i+1:]...)
			break
		}
	}
	return nil
}

func (d *DiscussionSpace) BroadcastMessage(message WebsocketMessage) {
	d.mu.Lock()
	defer d.mu.Unlock()

	for _, client := range d.Clients {
		client.SendJsonMessage(message)
	}
}

func NewDiscussionSpace() DiscussionSpaceInterface {
	return &DiscussionSpace{
		ID:      uuid.NewString(),
		Clients: []WebsocketClientInterface{},
	}
}
