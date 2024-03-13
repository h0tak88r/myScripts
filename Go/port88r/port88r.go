package main

import (
	"flag"
	"fmt"
	"net"
	"regexp"
	"sync"
)

func worker(target string, ports []int, wg *sync.WaitGroup) {
	defer wg.Done()

	for _, port := range ports {
		address := fmt.Sprintf("%s:%d", target, port)
		conn, err := net.Dial("tcp", address)
		if err != nil {
			continue
		}
		conn.Close()
		fmt.Printf("port %d is open !! \n", port)
	}
}

func main() {

	var (
		target             string
		startPort, endPort int
		wg                 sync.WaitGroup
	)

	// Define flags
	flag.StringVar(&target, "t", "", "target domain or IP address")
	flag.IntVar(&startPort, "s", 0, "start port")
	flag.IntVar(&endPort, "e", 1024, "end port")
	flag.Parse()

	// Validate user input
	if !validateInput(target) {
		fmt.Println("Wrong input please input either domain or ip Example: port88r -t example.com OR port88r -t 45.33.32.156")
		flag.Usage()
		return
	}

	// Define the number of ports each worker will scan concurrently
	portsPerWorker := 100

	// Iterate over the port range, launching a worker for each range of ports
	for i := startPort; i <= endPort; i += portsPerWorker {
		// Define the range of ports for this worker
		end := i + portsPerWorker - 1
		if end > endPort {
			end = endPort
		}

		// Increment the WaitGroup counter for this worker
		wg.Add(1)

		// Launch a worker goroutine
		go func(start, end int) {
			// Decrement the WaitGroup counter when the worker finishes
			defer wg.Done()

			// Create a slice of ports for this worker
			var ports []int
			for j := start; j <= end; j++ {
				ports = append(ports, j)
			}

			// Perform port scanning
			worker(target, ports, &wg)
		}(i, end)
	}

	// Wait for all workers to finish
	wg.Wait()
}

// Function that validates user input as either a domain or IP address
func validateInput(input string) bool {
	// Define regex for domain and IP address
	domainRegex := regexp.MustCompile(`^([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$`)
	ipRegex := regexp.MustCompile(`^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$`)

	return domainRegex.MatchString(input) || ipRegex.MatchString(input)
}
