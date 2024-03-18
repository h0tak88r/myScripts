package sub88r

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"strings"

	"github.com/gocolly/colly"
)

// Subber provides methods to scrape subdomains from various sources.
type Subber struct {
	Domain string // Domain is the target domain for which subdomains will be scraped.
}

// crtshResponse represents the response structure from crt.sh API.
type crtshResponse struct {
	NameValue string `json:"name_value"`
}

// urlscanResponse represents the response structure from urlscan.io API.
type urlscanResponse struct {
	Results []struct {
		Task struct {
			Domain string
		} `json:"task"`
	} `json:"results"`
}

// otxResults represents the response structure from Alien Vault (OTX) API.
type otxResults struct {
	PassiveDNS []struct {
		Hostname string `json:"hostname"`
	} `json:"passive_dns"`
}

// RapidDNS scrapes subdomains from rapiddns.io.
func (s *Subber) RapidDNS() (subdomains []string, err error) {

	c := colly.NewCollector()
	c.OnHTML("tbody tr", func(h *colly.HTMLElement) {
		tdText := h.DOM.Find("td").First().Text()
		subdomains = append(subdomains, tdText)
	})

	url := fmt.Sprintf("https://rapiddns.io/subdomain/%s?full=1#result", s.Domain)
	c.Visit(url)

	return subdomains, nil
}

// HackerTarget scrapes subdomains from hackertarget.com.
func (s *Subber) HackerTarget() (subdomains []string, err error) {

	// Send request
	url := fmt.Sprintf("https://api.hackertarget.com/hostsearch/?q=%s", s.Domain)

	resp, err := http.Get(url)
	if err != nil {
		return nil, err
	}

	// Read Response
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	// Scrap subdomains
	lines := strings.Split(string(body), "\n")

	for _, line := range lines {
		parts := strings.Split(line, ",")
		if len(parts) > 1 {
			subdomains = append(subdomains, parts[0])
		}
	}

	return subdomains, nil
}

// Anubis scrapes subdomains from Anubis via jldc.me.
func (s *Subber) Anubis() (subdomains []string, err error) {
	// Send Reques
	url := fmt.Sprintf("https://jldc.me/anubis/subdomains/%s", s.Domain)
	resp, err := http.Get(url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	// Decode json and scrap subdomains
	if err := json.NewDecoder(resp.Body).Decode(&subdomains); err != nil {
		return nil, err
	}

	return subdomains, err
}

// UrlScan scrapes subdomains from urlscan.io.
func (s *Subber) UrlScan() (subdomains []string, err error) {
	// Send Request
	url := fmt.Sprintf("https://urlscan.io/api/v1/search/?q=%s", s.Domain)
	resp, err := http.Get(url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	// Decode the JSON response
	var result urlscanResponse
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, err
	}

	// Extract subdomains
	for _, res := range result.Results {
		subdomains = append(subdomains, res.Task.Domain)
	}

	return subdomains, nil
}

// Otx scrapes subdomains from Alien Vault (OTX) via otx.alienvault.com.
func (s *Subber) Otx() (subdomains []string, err error) {

	// Send Request
	url := fmt.Sprintf("https://otx.alienvault.com/api/v1/indicators/domain/%s/passive_dns", s.Domain)
	resp, err := http.Get(url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	// Decode Json
	var res otxResults
	if err := json.NewDecoder(resp.Body).Decode(&res); err != nil {
		return nil, err
	}

	// Scrap Subdomains
	hostnames := make([]string, len(res.PassiveDNS))
	for i, entry := range res.PassiveDNS {
		hostnames[i] = entry.Hostname
	}
	return hostnames, nil
}

// CrtSh scrapes subdomains from crt.sh.
func (s *Subber) CrtSh() (subdomains []string, wildcards []string, err error) {

	// Declare Response Structure
	var Responses []crtshResponse

	// Send Request
	url := fmt.Sprintf("https://crt.sh/?q=%s&output=json", s.Domain)
	resp, err := http.Get(url)
	if err != nil {
		return nil, nil, err
	}
	defer resp.Body.Close()

	// Parse JSON response
	if err := json.NewDecoder(resp.Body).Decode(&Responses); err != nil {
		return nil, nil, err
	}

	// Scrap subdomains and wildcards save them in a slices
	for _, response := range Responses {
		nameValue := response.NameValue
		if strings.Contains(nameValue, "\n") {
			subnameValues := strings.Split(nameValue, "\n")
			for _, subname := range subnameValues {
				subname = strings.TrimSpace(subname)
				if subname != "" {
					if strings.Contains(subname, "*") {
						wildcards = append(wildcards, subname)
					} else {
						subdomains = append(subdomains, subname)
					}
				}
			}
		} else {
			if strings.Contains(nameValue, "*") {
				wildcards = append(wildcards, nameValue)
			} else {
				subdomains = append(subdomains, nameValue)
			}
		}
	}

	return subdomains, wildcards, nil
}
