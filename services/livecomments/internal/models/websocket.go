package models

import (
	"github.com/gorilla/websocket"
)

const (
	// A player wants to join the chat
	JOIN = "join"
	// A user want to send a message to the chat
	SEND_MESSAGE = "send_message"

	MUST_IDENTIFY = "must_identify"
)

// WebsocketMessage represents a message sent
// over the websocket connection.
type BaseWebsocketMessage struct {
	Action string `json:"action"`
}

type WebsocketMessage struct {
	BaseWebsocketMessage
}

type WebscoketClientInterface interface {
	GetUuid() string
	SetConn(conn *websocket.Conn)
	SendJsonMessage(message WebsocketMessage) error
	ReceiveJsonMessage() (WebsocketMessage, error)
}
