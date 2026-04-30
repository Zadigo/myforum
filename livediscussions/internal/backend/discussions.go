package backend

import (
	"sync"

	"github.com/google/uuid"
)

type DiscussionSpace struct {
	ID           string                        `json:"id"`
	Name         string                        `json:"name"`
	Participants []WebsocketClientInterface    `json:"participants"`
	broadcast    chan WebsocketMessage         `json:"-"`
	register     chan WebsocketClientInterface `json:"-"`
	unregister   chan WebsocketClientInterface `json:"-"`
	mu           sync.Mutex                    `json:"-"`
}

type DiscussionSpaceInterface interface {
	AddClient(client WebsocketClientInterface) error
	RemoveClient(client WebsocketClientInterface) error
	BroadcastMessage(message WebsocketMessage)
	StartBroadcaster()
	GetID() string
}

func (d *DiscussionSpace) GetID() string {
	return d.ID
}

func (d *DiscussionSpace) AddClient(client WebsocketClientInterface) error {
	d.mu.Lock()
	defer d.mu.Unlock()

	d.Participants = append(d.Participants, client)
	return nil
}

// RemoveClient removes a client from the discussion space. It is important to call
// this when a client disconnects to prevent memory leaks and ensure that the client
// is no longer part of the discussion.
func (d *DiscussionSpace) RemoveClient(client WebsocketClientInterface) error {
	d.mu.Lock()
	defer d.mu.Unlock()

	for i, c := range d.Participants {
		if c.GetClient().ID == client.GetClient().ID {
			d.Participants = append(d.Participants[:i], d.Participants[i+1:]...)
			break
		}
	}
	return nil
}

// StartBroadcaster starts a goroutine that listens for messages
// to broadcast to all clients in the discussion, as well as client registration
// and unregistration. This should be called when a new discussion space is created.
func (d *DiscussionSpace) StartBroadcaster() {
	go func() {
		for {
			select {
			case message := <-d.broadcast:
				d.BroadcastMessage(message)
			case client := <-d.register:
				d.AddClient(client)
			case client := <-d.unregister:
				d.RemoveClient(client)
			}
		}
	}()
}

func (d *DiscussionSpace) BroadcastMessage(message WebsocketMessage) {
	d.mu.Lock()
	defer d.mu.Unlock()

	for _, client := range d.Participants {
		client.SendJsonMessage(message)
	}
}

func NewDiscussionSpace(name string) DiscussionSpaceInterface {
	ds := &DiscussionSpace{
		ID:           uuid.NewString(),
		Name:         name,
		Participants: []WebsocketClientInterface{},
		broadcast:    make(chan WebsocketMessage, 100),
		register:     make(chan WebsocketClientInterface, 100),
		unregister:   make(chan WebsocketClientInterface, 100),
	}
	ds.StartBroadcaster()
	return ds
}
