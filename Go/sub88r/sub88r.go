package sub88r

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"strings"

	"github.com/gocolly/colly"
)

type Crtsh struct {
	NameValue string `json:"name_value"`
}

type Urlscan struct {
	Results []struct {
		Task struct {
			Domain string
		} `json:"task"`
	} `json:"results"`
}

type Otx struct {
	PassiveDNS []struct {
		Hostname string `json:"hostname"`
	} `json:"passive_dns"`
}

// Scrap subdomains from rapiddns.io
func rapiddnsSubdomains(domain string) (subdomains []string, err error) {

	c := colly.NewCollector()
	c.OnHTML("tbody tr", func(h *colly.HTMLElement) {
		tdText := h.DOM.Find("td").First().Text()
		subdomains = append(subdomains, tdText)
	})

	url := fmt.Sprintf("https://rapiddns.io/subdomain/%s?full=1#result", domain)
	c.Visit(url)

	return subdomains, nil
}

// Scrap subdomains from hacker target on api.hackertarget.com
func hackertargetSubdoamins(domain string) (subdomains []string, err error) {

	// Send request
	url := fmt.Sprintf("https://api.hackertarget.com/hostsearch/?q=%s", domain)

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

// Scrap subdomains from Anubis via jldc.me
func anubisSubdomains(domain string) (subdomains []string, err error) {
	// Send Reques
	url := fmt.Sprintf("https://jldc.me/anubis/subdomains/%s", domain)
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

// Scrap subdomains from urlscan.io
func urlscanSubdomains(domain string) (subdomains []string, err error) {
	// Send Request
	url := fmt.Sprintf("https://urlscan.io/api/v1/search/?q=%s", domain)
	resp, err := http.Get(url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	// Decode the JSON response
	var result Urlscan
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, err
	}

	// Extract subdomains
	for _, res := range result.Results {
		subdomains = append(subdomains, res.Task.Domain)
	}

	return subdomains, nil
}

// Scrap subdomaisn from Alien Vault via otx.alienvault.com
func otxSubdoamins(domain string) (subdomains []string, err error) {

	// Send Request
	url := fmt.Sprintf("https://otx.alienvault.com/api/v1/indicators/domain/%s/passive_dns", domain)
	resp, err := http.Get(url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	// Decode Json
	var res Otx
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

// Scrap subdomains from crt.sh
func crtshSubdomains(domain string) (subdomains []string, wildcards []string, err error) {

	// Declare Response Structure
	var Responses []Crtsh

	// Send Request
	url := fmt.Sprintf("https://crt.sh/?q=%s&output=json", domain)
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
