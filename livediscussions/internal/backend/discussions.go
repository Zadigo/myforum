package backend

import "sync"

type DiscussionSpace struct {
	ID      string             `json:"id"`
	Clients []*WebsocketClient `json:"clients"`
	mu      sync.Mutex         `json:"-"`
}

type DiscussionSpaceInterface interface {
	AddClient(client *WebsocketClient) error
	RemoveClient(client *WebsocketClient) error
	BroadcastMessage(message WebsocketMessage)
}

func (d *DiscussionSpace) AddClient(client *WebsocketClient) error {
	d.mu.Lock()
	defer d.mu.Unlock()

	d.Clients = append(d.Clients, client)
	return nil
}

func (d *DiscussionSpace) RemoveClient(client *WebsocketClient) error {
	d.mu.Lock()
	defer d.mu.Unlock()

	for i, c := range d.Clients {
		if c.ID == client.ID {
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

func NewDiscussionSpace(id string) DiscussionSpaceInterface {
	return &DiscussionSpace{
		ID:      id,
		Clients: []*WebsocketClient{},
	}
}
