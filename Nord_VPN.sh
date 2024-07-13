#!/bin/bash

# NordVPN Control Script

function show_help() {
    echo "Usage: $0 {connect|disconnect|status|set|get|list|current|reconnect|logout|help}"
    echo "  connect [country]     Connect to VPN. Optionally specify country."
    echo "  disconnect            Disconnect from VPN."
    echo "  status                Show VPN connection status."
    echo "  set <setting> <value> Set a NordVPN configuration (e.g., autoconnect, killswitch)."
    echo "  get <setting>         Get the current value of a NordVPN configuration."
    echo "  list                  List available NordVPN servers."
    echo "  current               Show the current connected server information."
    echo "  reconnect             Reconnect to the last connected server."
    echo "  logout                Log out from NordVPN."
    echo "  help                  Show this help message."
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

function get_option() {
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

function current_server() {
    nordvpn status | grep 'Current server'
}

function reconnect_vpn() {
    nordvpn reconnect
}

function logout_vpn() {
    nordvpn logout
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
    help)
        show_help
        ;;
    *)
        echo "Error: Invalid command."
        show_help
        ;;
esac
