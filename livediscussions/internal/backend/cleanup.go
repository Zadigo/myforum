package backend

import (
	"log"

	"github.com/go-co-op/gocron"
)

// StartCleanupRouting starts a scheduled task that runs
// every hour to clean up old discussions and clients.
func StartCleanupRouting(scheduler *gocron.Scheduler) {
	// Schedule the cleanup task to run every hour
	scheduler.Every(1).Hour().Do(func() {
		log.Println("🧹 Running cleanup task...")
		// Add your cleanup logic here
	})

	// Start the scheduler
	scheduler.StartAsync()
}
