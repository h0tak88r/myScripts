package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"regexp"
)

type sub88r struct{}

func (s *sub88r) fetchSubdomainsFromRapiddns(domain string) []string {
	url := fmt.Sprintf("https://rapiddns.io/subdomain/%s?full=1#result", domain)

	resp, err := http.Get(url)
	if err != nil {
		fmt.Println("[X] Error fetching subdomains:", err)
		return nil
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("[X] Error reading response body:", err)
		return nil
	}

	// Find subdomains using regular expression
	re := regexp.MustCompile(`<td>([^<]+)</td>`)
	matches := re.FindAllStringSubmatch(string(body), -1)

	subdomains := make([]string, 0, len(matches))
	for _, match := range matches {
		subdomains = append(subdomains, match[1])
	}

	return subdomains
}

func main() {
	s := sub88r{}
	domain := "example.com"
	subdomains := s.fetchSubdomainsFromRapiddns(domain)
	fmt.Println("Subdomains for", domain+":", subdomains)
}
