import PySimpleGUI as sg
import subprocess
import threading
import time
import queue
import os

class GUI:
    def __init__(self):
        self.window = sg.Window("Nord_VPN_GUI", self.get_layout(), resizable=True, finalize=True)
        self.running = True
        self.status_message = "Ready"
        self.status_queue = queue.Queue()

        # Correct PATH setting
        os.environ["PATH"] += os.pathsep + "/usr/bin"
        os.environ["PATH"] += os.pathsep + "/usr/local/bin"

        self.initial_setup()
        self.update_status_thread = threading.Thread(target=self.update_status_loop)
        self.update_status_thread.start()

    def get_layout(self):
        接続タブ = [
            [sg.Text("Nord_VPN_GUI", size=(15, 1))],
            [sg.Text("コネクト", size=(10, 1)), sg.Button("最寄りのスタンダードサーバー", key="-最寄りのスタンダードサーバー-")],
            [sg.Text("        ", size=(10, 1)), sg.Button("P2Pサーバー", key="-P2Pサーバー-")],
            [sg.Text("        ", size=(10, 1)), sg.Button("ダブルVPNサーバー", key="-ダブルVPNサーバー-")],
            [sg.Text("        ", size=(10, 1)), sg.Button("Onion Over VPNサーバー", key="-Onion_Over_VPNサーバー-")],
            [sg.Text("        ", size=(10, 1)), sg.Button("Dedicated IPサーバー", key="-Dedicated_IPサーバー-")],
            [sg.Text("        ", size=(10, 1)), sg.Button("Obfuscatedサーバー", key="-Obfuscatedサーバー-")],
            [sg.Text("", size=(10, 1)), sg.Button("ログイン", key="-ログイン-"), sg.Button("切断", key="-切断-"), sg.Button("ログアウト", key="-ログアウト-")]
        ]

        オプションタブ = [
            [sg.Text("オプション")],
            [sg.Checkbox("脅威防御ライト", True, key="-脅威防御ライト-")],
            [sg.Checkbox("キルスイッチ", True, key="-キルスイッチ-")],
            [sg.Checkbox("自動接続", True, key="-自動接続-")],
            [sg.Checkbox("通知", True, key="-通知-")],
            [sg.Checkbox("混乱化", True, key="-混乱化-")],
            [sg.Checkbox("メッシュネット", True, key="-メッシュネット-")]
        ]

        ステータスタブ = [
            [sg.Text("ステータス")],
            [sg.Text("", key="-ステータス-", size=(50, 1))]
        ]

        設定タブ = [
            [sg.Text("設定")],
            [sg.Button("インストール"), sg.Input("sh <(curl -sSf https://downloads.nordcdn.com/apps/linux/install.sh)", key='-インストール-', size=(50, 1))],
            [sg.Button("systemctl enable nordvpnd", key="systemctl_enable"),],
            [sg.Button("systemctl start nordvpnd", key="systemctl_start")],
            [sg.Button("systemctl stop nordvpnd", key="systemctl_stop")],
            [sg.Button("systemctl disable nordvpnd", key="systemctl_disable")],
            [sg.Button("systemctl status nordvpnd", key="systemctl_status")],
            [sg.Button("systemctl restart nordvpnd", key="systemctl_restart")],
            [sg.Input("", key="port_add"), sg.Button("ポートの開放")],
            [sg.Input("", key="port_remove"), sg.Button("ポートを閉じる")]
        ]

        tab_group = sg.TabGroup([
            [sg.Tab('接続', 接続タブ), sg.Tab('オプション', オプションタブ), sg.Tab('設定', 設定タブ)]
        ])

        layout = [
            [tab_group],
            [ステータスタブ]
        ]

        return layout

    def update_status(self, message):
        self.status_message = message
        self.status_queue.put(message)

    def run_command(self, command):
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else result.stderr

    def initial_setup(self):
        options = [
            ("-脅威防御ライト-", "nordvpn set threatprotectionlite on"),
            ("-キルスイッチ-", "nordvpn set killswitch on"),
            ("-自動接続-", "nordvpn set autoconnect on"),
            ("-通知-", "nordvpn set notify on"),
            ("-混乱化-", "nordvpn set obfuscate on"),
            ("-メッシュネット-", "nordvpn set meshnet on"),
        ]
        for key, command in options:
            self.window[key].update(True)
            result = self.run_command(command)
            print(f"{key} を設定: {result}")
            self.update_status(result)
            time.sleep(1)

    def update_status_loop(self):
        while self.running:
            if not self.status_queue.empty():
                status = self.status_queue.get()
                self.window.write_event_value('-UPDATE_STATUS-', status)
            time.sleep(1)

    def get_events(self):
        while self.running:
            event, values = self.window.read(timeout=1000)
            if event == sg.WINDOW_CLOSED or event == '終了':
                self.running = False
                break

            if event == '-UPDATE_STATUS-':
                self.window['-ステータス-'].update(values['-UPDATE_STATUS-'])
            elif event:
                print(f"Event: {event}")
                print(f"Values: {values}")

            if event == "-最寄りのスタンダードサーバー-":
                self.update_status("最寄りのスタンダードサーバーに接続中...")
                result = self.run_command("nordvpn connect")
                self.update_status(result)
            elif event == "-P2Pサーバー-":
                self.update_status("P2Pサーバーに接続中...")
                result = self.run_command("nordvpn connect P2P")
                self.update_status(result)
            elif event == "-ダブルVPNサーバー-":
                self.update_status("ダブルVPNサーバーに接続中...")
                result = self.run_command("nordvpn connect Double_VPN")
                self.update_status(result)
            elif event == "-Onion_Over_VPNサーバー-":
                self.update_status("Onion Over VPNサーバーに接続中...")
                result = self.run_command("nordvpn connect Onion_Over_VPN")
                self.update_status(result)
            elif event == "-Dedicated_IPサーバー-":
                self.update_status("Dedicated IPサーバーに接続中...")
                result = self.run_command("nordvpn connect Dedicated_IP")
                self.update_status(result)
            elif event == "-Obfuscatedサーバー-":
                self.update_status("Obfuscatedサーバーに接続中...")
                result = self.run_command("nordvpn connect Obfuscated")
                self.update_status(result)
            elif event == "-ログイン-":
                self.update_status("ログイン中...")
                result = self.run_command("nordvpn login")
                self.update_status(result)
            elif event == "-切断-":
                self.update_status("切断中...")
                result = self.run_command("nordvpn disconnect")
                self.update_status(result)
            elif event == "-ログアウト-":
                self.update_status("ログアウト中...")
                result = self.run_command("nordvpn logout")
                self.update_status(result)
            elif event in ["-脅威防御ライト-", "-キルスイッチ-", "-自動接続-", "-通知-", "-混乱化-", "-メッシュネット-"]:
                self.update_status(f"{event} を設定中...")
                result = self.run_command(f"nordvpn set {event[1:-1]} {'on' if values[event] else 'off'}")
                self.update_status(result)
            elif event == "systemctl_enable":
                self.update_status("systemctl enable nordvpnd 実行中...")
                result = self.run_command("sudo systemctl enable nordvpnd")
                self.update_status(result)
            elif event == "systemctl_start":
                self.update_status("systemctl start nordvpnd 実行中...")
                result = self.run_command("sudo systemctl start nordvpnd")
                self.update_status(result)
            elif event == "systemctl_stop":
                self.update_status("systemctl stop nordvpnd 実行中...")
                result = self.run_command("sudo systemctl stop nordvpnd")
                self.update_status(result)
            elif event == "systemctl_disable":
                self.update_status("systemctl disable nordvpnd 実行中...")
                result = self.run_command("sudo systemctl disable nordvpnd")
                self.update_status(result)
            elif event == "systemctl_status":
                self.update_status("systemctl status nordvpnd 実行中...")
                result = self.run_command("sudo systemctl status nordvpnd")
                self.update_status(result)
            elif event == "systemctl_restart":
                self.update_status("systemctl restart nordvpnd 実行中...")
                result = self.run_command("sudo systemctl restart nordvpnd")
                self.update_status(result)
            elif event == "ポートの開放":
                self.update_status("ポートの開放中...")
                result = self.run_command(f"sudo ufw allow {values['port_add']}")
                self.update_status(result)
            elif event == "ポートを閉じる":
                self.update_status("ポートを閉じる中...")
                result = self.run_command(f"sudo ufw deny {values['port_remove']}")

    def run(self):
        event_thread = threading.Thread(target=self.get_events)
        event_thread.start()
        while self.running:
            time.sleep(1)
        event_thread.join()
        self.update_status_thread.join()

gui = GUI()
gui.run()
