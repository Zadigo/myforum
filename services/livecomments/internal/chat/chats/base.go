package chats

import (
	"github.com/Zadigo/livecomments/internal/models"
	"github.com/google/uuid"
)

const (
	STANDARD  = "standard"
	EXTENSION = "extension"
)

// CreateChat is a factory function that creates a new chat instance based on the specified chat type.
// It returns an instance of ChatInterface, which can be either a StandardChat or an ExtensionChat,
// depending on the provided chatType. If the chatType is not recognized, it returns nil.
func CreateChat(options models.ChatAppOptions) ChatInterface {
	var chat ChatInterface

	switch options.ChatType {
	case STANDARD:
		chat = &StandardChat{
			BaseChat: BaseChat{
				Uuid: uuid.NewString(),
			},
		}
	default:
		return nil
	}

	chat.SetOptions(options)
	return chat
}
