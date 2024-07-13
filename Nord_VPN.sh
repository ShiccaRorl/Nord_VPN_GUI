#!/bin/bash

# NordVPN Control Script

function show_help() {
    echo "Usage: $0 {connect|disconnect|status|set|help}"
    echo "  connect [country]   Connect to VPN. Optionally specify country."
    echo "  disconnect          Disconnect from VPN."
    echo "  status              Show VPN connection status."
    echo "  set <setting> <value> Set a NordVPN configuration (e.g., autoconnect, killswitch)."
    echo "  help                Show this help message."
}

function connect_vpn() {
    if [ -n "$1" ]; then
        nordvpn connect "$1"
    else
        nordvpn connect
    fi
}

function disconnect_vpn() {
    nordvpn disconnect
}

function show_status() {
    nordvpn status
}

function set_option() {
    if [ -n "$1" ] && [ -n "$2" ]; then
        nordvpn set "$1" "$2"
    else
        echo "Error: Missing setting or value."
        show_help
    fi
}

case "$1" in
    connect)
        connect_vpn "$2"
        ;;
    disconnect)
        disconnect_vpn
        ;;
    status)
        show_status
        ;;
    set)
        set_option "$2" "$3"
        ;;
    help)
        show_help
        ;;
    *)
        echo "Error: Invalid command."
        show_help
        ;;
esac
