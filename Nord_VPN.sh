#!/bin/bash

# NordVPN Control Script

function show_help() {
    echo "Usage: $0 {connect|disconnect|status|set|get|list|current|reconnect|logout|set_all_on|help}"
    echo "  connect [country|type] Connect to VPN. Optionally specify country or type (p2p, onion)."
    echo "  disconnect            Disconnect from VPN."
    echo "  status                Show VPN connection status."
    echo "  set <setting> <value> Set a NordVPN configuration (e.g., autoconnect, killswitch)."
    echo "  get <setting>         Get the current value of a NordVPN configuration."
    echo "  list                  List available NordVPN servers."
    echo "  current               Show the current connected server information."
    echo "  reconnect             Reconnect to the last connected server."
    echo "  logout                Log out from NordVPN."
    echo "  set_all_on            Set all available options to 'on'."
    echo "  help                  Show this help message."
}

function connect_vpn() {
    if [ -n "$1" ]; then
        if [ "$1" == "p2p" ]; then
            nordvpn connect p2p
        elif [ "$1" == "onion" ]; then
            nordvpn connect onion_over_vpn
        else
            nordvpn connect "$1"
        fi
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

function get_option()() {
    if [ -n "$1" ]; then
        nordvpn settings | grep "$1"
    else
        echo "Error: Missing setting."
        show_help
    fi
}

function list_servers() {
    nordvpn countries
}

function current_server()() {
    nordvpn status | grep 'Current server'
}

function reconnect_vpn()() {
    nordvpn reconnect
}

function logout_vpn()() {
    nordvpn logout
}

function set_all_options_on()() {
    # Enabling all available options to 'on'
    nordvpn set autoconnect on
    nordvpn set killswitch on
    nordvpn set cybersec on
    nordvpn set obfuscate on
    nordvpn set notify on
    nordvpn set ipv6 on
    nordvpn set dns 103.86.96.100 103.86.99.100
    echo "All options have been set to 'on'."
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
    get)
        get_option "$2"
        ;;
    list)
        list_servers
        ;;
    current)
        current_server
        ;;
    reconnect)
        reconnect_vpn
        ;;
    logout)
        logout_vpn
        ;;
    set_all_on)
        set_all_options_on
        ;;
    help)
        show_help
        ;;
    *)
        echo "Error: Invalid command."
        show_help
        ;;
esac

# Example usage for connecting to VPN:
# To connect to the best available server: ./scriptname connect
# To connect to a specific country: ./scriptname connect USA
# To connect to a P2P server: ./scriptname connect p2p
# To connect to an Onion Over VPN server: ./scriptname connect onion

# To set all options to 'on': ./scriptname set_all_on
