package main

import (
	"fmt"
	"time"
)

func main() {

	// Loop that runs 5 Sleepy gophers go routines
	c := make(chan int)
	for i := 0; i < 5; i++ {
		go sleepyGopher(i, c)
	}

	// Loop Receives Gopher id
	for i := 0; i < 5; i++ {
		gopherId := <-c
		fmt.Println("gopher ", gopherId, " has Finished Sleeping")
	}
}

// sleepy Gopher Sends id when finish sleeping
func sleepyGopher(id int, c chan int) {
	time.Sleep(5 * time.Second)
	fmt.Println("......", id, " snore.....")
	c <- id
}
