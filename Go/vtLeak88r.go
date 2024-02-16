package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"regexp"
	"strings"
)

func main() {
	fmt.Print("Enter the target domain: ")
	var domain string
	fmt.Scan(&domain)

	apiKey := "0cb2e59de3c5cece2ba98d8e24874b965dc87820a5b7fbc19030672bfd7db3dc" // Replace with your actual API key

	url := fmt.Sprintf("https://www.virustotal.com/vtapi/v2/domain/report?apikey=%s&domain=%s", apiKey, domain)

	resp, err := http.Get(url)
	if err != nil {
		fmt.Println("Error making the request:", err)
		return
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("Error reading the response body:", err)
		return
	}

	var result map[string]interface{}
	err = json.Unmarshal(body, &result)
	if err != nil {
		fmt.Println("Error parsing JSON:", err)
		return
	}

	// Create the "results" directory if it doesn't exist
	err = os.MkdirAll("results", os.ModePerm)
	if err != nil {
		fmt.Println("Error creating 'results' directory:", err)
		return
	}

	// Extracting all URLs
	urlFilePath := fmt.Sprintf("results/%s_filtered_urls.txt", domain)
	urlFile, err := os.Create(urlFilePath)
	if err != nil {
		fmt.Println("Error creating filtered URLs file:", err)
		return
	}
	defer urlFile.Close()

	emailRegex := regexp.MustCompile(`\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b|\b[a-zA-Z0-9._%+-]+%40[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b`)

	if detectedURLs, ok := result["detected_urls"].([]interface{}); ok {
		fmt.Println("Detected URLs:")
		for _, urlInfo := range detectedURLs {
			urlData := urlInfo.(map[string]interface{})
			url := urlData["url"].(string)

			// Check if the URL contains an email address
			if containsEmail(url, emailRegex) {
				fmt.Println(url)
				fmt.Fprintln(urlFile, url)
			}
		}
	}

	if undetectedURLs, ok := result["undetected_urls"].([]interface{}); ok {
		fmt.Println("Undetected URLs:")
		for _, urlInfo := range undetectedURLs {
			urlData := urlInfo.([]interface{})
			url := urlData[0].(string)

			// Check if the URL contains an email address
			if containsEmail(url, emailRegex) {
				fmt.Println(url)
				fmt.Fprintln(urlFile, url)
			}
		}
	}

	fmt.Printf("Filtered URLs (containing emails) saved to: %s\n", urlFilePath)
}

// Helper function to check if a string contains an email address
func containsEmail(s string, regex *regexp.Regexp) bool {
	return strings.Contains(s, "@") && regex.MatchString(s)
}