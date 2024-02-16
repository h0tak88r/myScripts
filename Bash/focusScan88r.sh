#!/bin/bash

# Constants
RESULTS_DIR="results"
WORDLIST_DIR="Wordlists"
FUZZ_WORDLIST="$WORDLIST_DIR/h0tak88r_fuzz.txt"

# Initialize variables
TARGET_DOMAIN=""
SUBDOMAIN_LIST=""
DISCORD_WEBHOOK="https://discord.com/api/webhooks/1195162083768152234/Jg3wB9-w9lNEoqxmpi4Gzv7neUaWWCDf0QFAjGahT10lPz8oa7r7834oHywgP6WisoF8"

check_required_tools() {
    echo "[+] Checking if the tools and required files are available"

    # Check if the nuclei_templates directory exists
    if [ ! -d "nuclei_templates" ]; then
        echo "Error: The 'nuclei_templates' directory does not exist. Please ensure it is present before running the script."
        exit 1
    fi

    # Check if the fuzz wordlist file exists
    if [ ! -f "$FUZZ_WORDLIST" ]; then
        echo "Error: The 'h0tak88r_fuzz.txt' wordlist file does not exist in the specified directory. Please provide the correct path or ensure the file is present."
        exit 1
    fi

    # Check if the required tools are installed
    local required_tools=("notify" "naabu" "httpx" "gau" "kxss" "nuclei" "curl" "ffuf")
    
    for tool in "${required_tools[@]}"; do
        if ! command -v "$tool" &> /dev/null; then
            echo "Error: $tool is not installed. Please install it before running the script."
            exit 1
        fi
    done

    echo "[+] All required tools and files are available."
}

banner() {
    cat << "EOF"
    ____                _____                  ____  ____      
   / __/______  _______/ ___/_________ _____  ( __ )( __ )_____
  / /_/ ___/ / / / ___/\__ \/ ___/ __ `/ __ \/ __  / __  / ___/
 / __/ /__/ /_/ (__  )___/ / /__/ /_/ / / / / /_/ / /_/ / /    
/_/  \___/\__,_/____//____/\___/\__,_/_/ /_/\____/\____/_/     
                                                                                                                               
EOF
}

cleanup_results_directory() {
    echo "[+] Cleaning up the results directory"
    rm -rf "$RESULTS_DIR"
    mkdir "$RESULTS_DIR"
}

get_discord_webhook() {
    read -p "Enter the Discord webhook URL: " DISCORD_WEBHOOK
}

send_file_to_discord() {
    local webhook_url="$1"
    local file_path="$2"

    if [ -f "$file_path" ]; then
        curl -X POST -F "file=@$file_path" "$webhook_url"
        echo "File '$file_path' successfully sent to Discord."
    else
        echo "Error: File '$file_path' not found."
    fi
}

perform_port_scanning() {
    echo "[+] Performing port scanning"
    if [ -n "$SUBDOMAIN_LIST" ]; then
        naabu -list "$SUBDOMAIN_LIST" -top-ports 1000 | notify -bulk
    elif [ -n "$TARGET_DOMAIN" ]; then
        naabu -list "$TARGET_DOMAIN" -top-ports 1000 | notify -bulk
    else
        echo "Error: No target domain or subdomain list provided."
    fi
}

perform_exposed_panels_scan() {
    echo "[+] Performing exposed panels scan"
    if [ -n "$SUBDOMAIN_LIST" ]; then
        cat "$SUBDOMAIN_LIST" | nuclei -t nuclei_templates/panels | notify -bulk
    elif [ -n "$TARGET_DOMAIN" ]; then
        echo "$TARGET_DOMAIN" | nuclei -t nuclei_templates/panels | notify -bulk
    else
        echo "Error: No target domain or subdomain list provided."
    fi
}

perform_js_exposure_scan() {
    echo "[+] Performing JS exposure scan"
    if [ -n "$SUBDOMAIN_LIST" ]; then
        cat "$SUBDOMAIN_LIST" | gau | grep "\\.js$" | sort -u | tee JS.txt
        nuclei -l JS.txt -t nuclei_templates/js/information-disclosure-in-js-files.yaml | notify -bulk
    elif [ -n "$TARGET_DOMAIN" ]; then
        echo "$TARGET_DOMAIN" | gau | grep "\\.js$" | sort -u | tee JS.txt
        nuclei -l JS.txt -t nuclei_templates/js/information-disclosure-in-js-files.yaml | notify -bulk
    else
        echo "Error: No target domain or subdomain list provided."
    fi
}

scan_with_new_nuclei_templates() {
    echo "[+] Scan with newly added templates to the nuclei templates repo"
    if [ -n "$TARGET_DOMAIN" ]; then
        echo "$TARGET_DOMAIN" | nuclei -t nuclei-templates/ -nt -es info | notify -bulk
    elif [ -n "$SUBDOMAIN_LIST" ]; then
        cat "$SUBDOMAIN_LIST" | nuclei -t nuclei-templates/ -nt -es info | notify -bulk
    else
        echo "Error: No target domain or subdomain list provided."
        exit 1
    fi
}

perform_full_nuclei_scan() {
    echo "[+] Performing a full nuclei scan"
    if [ -n "$TARGET_DOMAIN" ]; then
        echo "$TARGET_DOMAIN" | nuclei -t nuclei_templates/Others -es info | notify -bulk
    elif [ -n "$SUBDOMAIN_LIST" ]; then
        cat "$SUBDOMAIN_LIST" | nuclei -t nuclei_templates/Others -es info | notify -bulk
    else
        echo "Error: No target domain or subdomain list provided."
        exit 1
    fi
}

xss_scan() {
    echo "[+] Scanning for XSS"
    cat "$SUBDOMAIN_LIST" | gau | kxss | notify --bulk
}

fuzzing() {
    echo "[+] Fuzzing using h0tak88r_fuzz.txt wordlist"
    if [ -n "$SUBDOMAIN_LIST" ]; then
        ffuf "https://FUZZDOMAIN/FUZZDIR" -w "$FUZZ_WORDLIST:FUZZDIR,$SUBDOMAIN_LIST:FUZZDOMAIN" -mc 200 -o "$RESULTS_DIR/ffufGET.txt"
        ffuf "https://FUZZDOMAIN/FUZZDIR" -w "$FUZZ_WORDLIST:FUZZDIR,$SUBDOMAIN_LIST:FUZZDOMAIN" -mc 200 -X POST -o "$RESULTS_DIR/ffufPOST.txt"
        send_file_to_discord "$DISCORD_WEBHOOK" "$RESULTS_DIR/ffufGET.txt"
        send_file_to_discord "$DISCORD_WEBHOOK" "$RESULTS_DIR/ffufPOST.txt"
    elif [ -n "$TARGET_DOMAIN" ]; then
        ffuf "https://TARGET_DOMAIN/FUZZ" -w "$FUZZ_WORDLIST" -mc 200 -o "$RESULTS_DIR/ffufGET.txt"
        ffuf "https://TARGET_DOMAIN/FUZZ" -w "$FUZZ_WORDLIST" -mc 200 -o "$RESULTS_DIR/ffufGET.txt" -X POST
        send_file_to_discord "$DISCORD_WEBHOOK" "$RESULTS_DIR/ffufGET.txt"
        send_file_to_discord "$DISCORD_WEBHOOK" "$RESULTS_DIR/ffufPOST.txt"
    else 
        echo "Error: No target domain or subdomain list provided"
        exit 1
    fi
}

focusScan() {
    banner
    check_required_tools
    cleanup_results_directory

    while getopts ":d:l:w:" opt; do
        case $opt in
            d)
                TARGET_DOMAIN="$OPTARG"
                ;;
            l)
                SUBDOMAIN_LIST="$OPTARG"
                ;;
            w)
                DISCORD_WEBHOOK="$OPTARG"
                ;;
            \?)
                echo "Invalid option: -$OPTARG" >&2
                exit 1
                ;;
            :)
                echo "Option -$OPTARG requires an argument." >&2
                exit 1
                ;;
        esac
    done

    if [ -z "$TARGET_DOMAIN" ] && [ -z "$SUBDOMAIN_LIST" ]; then
        echo "Error: Specify either a target domain (-d) or a list of subdomains (-l)."
        exit 1
    fi

    if [ -z "$DISCORD_WEBHOOK" ]; then
        get_discord_webhook
    fi

    xss_scan
    perform_port_scanning
    perform_exposed_panels_scan
    perform_js_exposure_scan
    scan_with_new_nuclei_templates
    perform_full_nuclei_scan
    fuzzing
}

# Main execution
focusScan "$@"