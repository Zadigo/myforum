package server

import (
	"os"
	"strconv"

	"github.com/joho/godotenv"
)

type Config struct {
	Port uint
}

func LoadConfig() *Config {
	godotenv.Load(".env")

	config := &Config{
		Port: 3000,
	}

	if port, exists := os.LookupEnv("PORT"); exists {
		if port, err := strconv.ParseUint(port, 10, 16); err == nil {
			config.Port = uint(port)
		}
	}

	return config
}
